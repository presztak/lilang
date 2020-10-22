import os
import subprocess

import llvmlite.binding as llvm_binding
from llvmlite import ir

from .codegen import CodeGenerator
from .parser import LilangParser
from .types import IntArrayType, IntType, VoidType


class LLVMVariable(object):

    def __init__(self, identifier, type, address):
        self.identifier = identifier
        self.type = type
        self.address = address


class LLVMCodeGenerator(CodeGenerator):

    def __init__(self):
        super().__init__()

        self.builder = None
        self.main_module = None
        self.block = None
        self.variables = {}
        self.functions = {}

        llvm_binding.initialize()
        llvm_binding.initialize_native_target()
        llvm_binding.initialize_native_asmprinter()

        self.create_main_module()

    def create_target_machine(self):
        target = llvm_binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        return target_machine

    def create_main_module(self):
        self.main_module = ir.Module(name='main')
        main_f_type = ir.FunctionType(VoidType.llvm_type, ())
        main_func = ir.Function(self.main_module, main_f_type, name='main')
        self.block = main_func.append_basic_block(name='entry')
        self.builder = ir.IRBuilder(self.block)

    def compile(self, str_code, exec_name):

        object_file_name = f'{exec_name}.o'

        with open(os.path.join(self.lib_path, 'io.li')) as lib_script:
            lib = lib_script.read()

        parser = LilangParser()
        self.generate_code(parser.run(lib + str_code))
        self.builder.ret_void()

        mod = llvm_binding.parse_assembly(str(self.main_module))
        mod.verify()

        target_machine = self.create_target_machine()
        with open(os.path.join(self.bin_path, object_file_name), "wb") as o:
            o.write(target_machine.emit_object(mod))

        subprocess.check_call([
            'gcc',
            '-o',
            os.path.join(self.bin_path, exec_name),
            os.path.join(self.bin_path, object_file_name),
            os.path.join(self.lib_path, "libio.so")
        ])
        os.remove(os.path.join(self.bin_path, object_file_name))

    def _generate_AstProgram(self, node):
        self.generate_code(node.program)

    def _generate_AstStatLst(self, node):
        for stat in node.stat_lst:
            self.generate_code(stat)

    def _generate_AstBinExpr(self, node):
        expr0 = self.generate_code(node.expr0)
        expr1 = self.generate_code(node.expr1)

        if node.operator == '+':
            return self.builder.add(expr0, expr1)
        elif node.operator == '-':
            return self.builder.sub(expr0, expr1)
        elif node.operator == '*':
            return self.builder.mul(expr0, expr1)
        elif node.operator == '/':
            return self.builder.sdiv(expr0, expr1)
        elif node.operator == '&&':
            return self.builder.and_(expr0, expr1)
        elif node.operator == '||':
            return self.builder.or_(expr0, expr1)
        else:
            return self.builder.icmp_signed(node.operator, expr0, expr1)

    def _generate_AstAssignStat(self, node):
        result = self.generate_code(node.expr)

        var_addr = self.variables[node.identifier].address
        if node.index_expr:
            idx = self.generate_code(node.index_expr)
            var_addr = self.builder.gep(var_addr, [idx])
        self.builder.store(result, var_addr)
        return result

    def _generate_AstDeclStat(self, node):
        result = self.generate_code(node.expr)
        if node.type == IntType.str_code:
            var_addr = self.builder.alloca(
                IntType.llvm_type, size=None, name=node.identifier
            )
            self.builder.store(result, var_addr)
            self.variables[node.identifier] = LLVMVariable(
                node.identifier,
                node.type,
                var_addr
            )
        elif node.type == IntArrayType.str_code:
            self.variables[node.identifier] = LLVMVariable(
                node.identifier,
                node.type,
                result
            )
        return result

    def _generate_AstIfStat(self, node):
        condition = self.generate_code(node.condition)

        # 'If' without else clause
        if not node.else_stat_lst:
            with self.builder.if_then(condition):
                return self.generate_code(node.stat_lst)
        # 'If'/'Else' case
        else:
            with self.builder.if_else(condition) as (then, otherwise):
                with then:
                    self.generate_code(node.stat_lst)
                with otherwise:
                    self.generate_code(node.else_stat_lst)

    def _generate_AstWhileStat(self, node):
        loop_cond = self.builder.function.append_basic_block(name='loop_cond')
        self.builder.branch(loop_cond)
        self.builder.position_at_end(loop_cond)
        condition = self.generate_code(node.condition)

        loop_body = self.builder.function.append_basic_block(name='loop_body')
        self.builder.position_at_start(loop_body)
        self.generate_code(node.stat_lst)

        loop_end = self.builder.function.append_basic_block(name='loop_end')
        self.builder.branch(loop_cond)

        self.builder.position_at_end(loop_cond)
        self.builder.cbranch(condition, loop_body, loop_end)

        self.builder.position_at_start(loop_end)

    def _generate_AstReturnStat(self, node):
        expr = self.generate_code(node.expr)
        self.builder.ret(expr)

    def _generate_AstNumber(self, node):
        return ir.Constant(IntType.llvm_type, int(node.value))

    def _generate_AstLstExpr(self, node):
        result = []
        for arg in node.args_lst.args_lst:
            result.append(self.generate_code(arg))

        var_addr = self.builder.alloca(
                IntType.llvm_type, size=len(result)
            )

        for idx, num in enumerate(result):
            el_addr = self.builder.gep(
                var_addr, [ir.Constant(IntType.llvm_type, idx)]
            )
            self.builder.store(num, el_addr)
        return var_addr

    def _generate_AstVariable(self, node):

        var = self.variables[node.identifier]
        var_addr = var.address
        if var.type == IntType.str_code:
            return self.builder.load(var_addr)
        elif var.type == IntArrayType.str_code:
            index = ir.Constant(IntType.llvm_type, 0)
            if node.index_expr:
                index = self.generate_code(node.index_expr)

            var_addr = self.builder.gep(
                var_addr, [index]
            )
            if node.index_expr:
                return self.builder.load(var_addr)
            return var_addr

    def _generate_AstFnDef(self, node):
        args = node.params_lst.params_lst

        fn_args = []
        for arg in args:
            if arg[1] == IntArrayType.str_code:
                fn_args.append(IntArrayType.llvm_type)
            elif arg[1] == IntType.str_code:
                fn_args.append(IntType.llvm_type)

        return_type = VoidType.llvm_type
        if node.type == IntType.str_code:
            return_type = IntType.llvm_type
        elif node.type == IntArrayType.str_code:
            return_type = IntArrayType.llvm_type

        fn_type = ir.FunctionType(return_type, fn_args)
        fn = ir.Function(self.main_module, fn_type, name=node.name)
        self.functions[node.name] = fn

        if not node.declaration:
            last_block = self.block
            last_builder = self.builder
            self.block = fn.append_basic_block(name='entry')
            self.builder = ir.IRBuilder(self.block)

            for index, arg in enumerate(args):
                if arg[1] == IntType.str_code:
                    alloca = self.builder.alloca(
                        IntType.llvm_type, name=arg[0]
                    )
                    self.variables[arg[0]] = LLVMVariable(
                        arg[0],
                        arg[1],
                        alloca
                    )
                    self.builder.store(fn.args[index], alloca)
                elif arg[1] == IntArrayType.str_code:
                    self.variables[arg[0]] = LLVMVariable(
                        arg[0],
                        arg[1],
                        fn.args[index]
                    )

            if node.stat_lst:
                self.generate_code(node.stat_lst)
            if node.type == VoidType.str_code:
                self.builder.ret_void()
            self.block = last_block
            self.builder = last_builder

    def _generate_AstFnCall(self, node):
        args = []
        for arg_expr in node.args_lst.args_lst:
            arg = self.generate_code(arg_expr)
            args.append(arg)
        return self.builder.call(self.functions[node.name], args)
