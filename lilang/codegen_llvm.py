import os
import subprocess

import llvmlite.binding as llvm_binding
from llvmlite import ir

from .codegen import CodeGenerator
from .parser import LilangParser
from .types import BoolType, IntType, LilangType, StringArrayType, VoidType


class LLVMVariable(object):

    def __init__(self, identifier, type, address):
        self.identifier = identifier
        self.type = type
        self.address = address


class LLVMLoop(object):

    def __init__(self, loop_cond, loop_body, loop_end, loop_step=None):
        self.loop_cond = loop_cond
        self.loop_body = loop_body
        self.loop_end = loop_end
        self.loop_step = loop_step

    def continue_block(self):
        if self.loop_step:
            return self.loop_step
        return self.loop_cond


class LLVMCodeGenerator(CodeGenerator):

    def __init__(self):
        super().__init__()

        self.builder = None
        self.main_module = None
        self.block = None
        self.variables = {}
        self.functions = {}
        self.loops = []
        self.break_stat_generation = False

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
        main_f_type = ir.FunctionType(
            VoidType.llvm_type, (IntType.llvm_type, StringArrayType.llvm_type)
        )
        main_func = ir.Function(self.main_module, main_f_type, name='main')
        self.block = main_func.append_basic_block(name='entry')
        self.builder = ir.IRBuilder(self.block)

        var_addr = self.builder.alloca(
            IntType.llvm_type, size=None, name='argc'
        )
        self.builder.store(main_func.args[0], var_addr)
        self.variables['argc'] = LLVMVariable(
            'argc',
            'int',
            var_addr
        )

        self.variables['argv'] = LLVMVariable(
            'argv',
            'string[]',
            main_func.args[1]
        )

    def compile(self, str_code, exec_name):

        object_file_name = f'{exec_name}.o'

        with open(os.path.join(self.lib_path, 'io.li')) as lib_script:
            lib = lib_script.read()

        parser = LilangParser(lib)
        self.generate_code(parser.run(lib))

        parser = LilangParser(str_code)
        ast = parser.run(str_code)
        if not ast:
            return
        self.generate_code(ast)

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
            if self.break_stat_generation is True:
                break
            self.generate_code(stat)

        self.break_stat_generation = False

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

        if node.operator == '+=':
            result = self.builder.add(self.builder.load(var_addr), result)
        elif node.operator == '-=':
            result = self.builder.sub(self.builder.load(var_addr), result)
        elif node.operator == '*=':
            result = self.builder.mul(self.builder.load(var_addr), result)
        elif node.operator == '/=':
            result = self.builder.sdiv(self.builder.load(var_addr), result)

        self.builder.store(result, var_addr)
        return result

    def _generate_AstInitDecl(self, node):
        # Pass down type of variable
        node.expr.type = node.type

        result = self.generate_code(node.expr)
        lilang_type = LilangType.type_from_str(node.type)

        if lilang_type.is_array:
            self.variables[node.identifier] = LLVMVariable(
                node.identifier,
                node.type,
                result
            )
        else:
            var_addr = self.builder.alloca(
                lilang_type.llvm_type, size=None, name=node.identifier
            )
            self.builder.store(result, var_addr)
            self.variables[node.identifier] = LLVMVariable(
                node.identifier,
                node.type,
                var_addr
            )

        return result

    def _generate_AstDeclStat(self, node):
        for init_decl in node.init_decl_lst.init_decl_lst:
            # Pass info about type to child nodes
            init_decl.type = node.type
            self.generate_code(init_decl)

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

    def _generate_AstForStat(self, node):
        loop_cond = self.builder.function.append_basic_block(name='loop_cond')
        loop_body = self.builder.function.append_basic_block(name='loop_body')
        loop_step = self.builder.function.append_basic_block(name='loop_step')
        loop_end = self.builder.function.append_basic_block(name='loop_end')

        self.loops.append(LLVMLoop(loop_cond, loop_body, loop_end, loop_step))

        self.generate_code(node.init_stat)

        self.builder.branch(loop_cond)
        self.builder.position_at_start(loop_cond)
        condition = self.generate_code(node.condition)

        self.builder.position_at_start(loop_body)
        self.generate_code(node.stat_lst)

        if not self.builder.block.is_terminated:
            self.builder.branch(loop_step)

        self.builder.position_at_start(loop_step)
        self.generate_code(node.step_stat)
        self.builder.branch(loop_cond)

        self.builder.position_at_end(loop_cond)
        self.builder.cbranch(condition, loop_body, loop_end)

        self.builder.position_at_start(loop_end)

        self.loops.pop()

    def _generate_AstWhileStat(self, node):
        loop_cond = self.builder.function.append_basic_block(name='loop_cond')
        loop_body = self.builder.function.append_basic_block(name='loop_body')
        loop_end = self.builder.function.append_basic_block(name='loop_end')

        self.loops.append(LLVMLoop(loop_cond, loop_body, loop_end))

        self.builder.branch(loop_cond)
        self.builder.position_at_end(loop_cond)
        condition = self.generate_code(node.condition)

        self.builder.position_at_start(loop_body)
        self.generate_code(node.stat_lst)
        if not self.builder.block.is_terminated:
            self.builder.branch(loop_cond)

        self.builder.position_at_end(loop_cond)
        self.builder.cbranch(condition, loop_body, loop_end)

        self.builder.position_at_start(loop_end)

    def _generate_AstReturnStat(self, node):
        expr = self.generate_code(node.expr)
        self.builder.ret(expr)

    def _generate_AstBreakStat(self, node):
        self.builder.branch(self.loops[-1].loop_end)
        self.break_stat_generation = True

    def _generate_AstContinueStat(self, node):
        self.builder.branch(self.loops[-1].continue_block())
        self.break_stat_generation = True

    def _generate_AstNumber(self, node):
        return ir.Constant(IntType.llvm_type, int(node.value))

    def _generate_AstBool(self, node):
        if node.value == 'true':
            return ir.Constant(BoolType.llvm_type, 1)
        return ir.Constant(BoolType.llvm_type, 0)

    def _generate_AstString(self, node):
        alloca = self.builder.alloca(
            ir.IntType(8), size=len(node.value)
        )
        # TODO: Store string without iteration it
        for idx, num in enumerate(node.value):
            el_addr = self.builder.gep(
                alloca, [ir.Constant(IntType.llvm_type, idx)]
            )
            self.builder.store(ir.Constant(ir.IntType(8), ord(num)), el_addr)
        return alloca

    def _generate_AstLstExpr(self, node):
        result = []
        lst_type = LilangType.type_from_str(node.type).base_type.llvm_type

        for arg in node.args_lst.args_lst:
            result.append(self.generate_code(arg))

        var_addr = self.builder.alloca(
            lst_type, size=len(result)
        )

        for idx, num in enumerate(result):
            # TODO: Here should be int type explicity
            el_addr = self.builder.gep(
                var_addr, [ir.Constant(IntType.llvm_type, idx)]
            )
            self.builder.store(num, el_addr)
        return var_addr

    def _generate_AstStructLiteral(self, node):
        result = []

        for arg in node.args_lst.args_lst:
            result.append(self.generate_code(arg))

        var_addr = self.builder.alloca(
            LilangType.type_from_str(node.type).llvm_type,
            size=None
        )

        for idx, el in enumerate(result):
            el_addr = self.builder.gep(
                var_addr,
                [
                    ir.Constant(IntType.llvm_type, 0),
                    ir.Constant(IntType.llvm_type, idx)
                ]
            )
            self.builder.store(
                ir.Constant(
                    LilangType.type_from_str(
                        node.type
                    ).llvm_type.elements[idx],
                    el.constant
                ),
                el_addr
            )
        return var_addr

    def _generate_AstVariable(self, node):

        var = self.variables[node.identifier]
        var_addr = var.address
        lilang_type = LilangType.type_from_str(var.type)

        if lilang_type.is_array:
            index = ir.Constant(IntType.llvm_type, 0)
            if node.index_expr:
                index = self.generate_code(node.index_expr)

            var_addr = self.builder.gep(
                var_addr, [index]
            )
            if node.index_expr:
                return self.builder.load(var_addr)
            return var_addr
        else:
            return self.builder.load(var_addr)

    def _generate_AstGetAttribute(self, node):

        var_name = ''
        if hasattr(node.variable, "attribute"):
            var_name = node.variable.attribute
        else:
            var_name = node.variable.identifier
        var = self.variables[var_name]
        idx = 0
        for field in LilangType.type_from_str(var.type).fields:
            if field[0] == node.attribute:
                break
            idx += 1
        var_addr = self.generate_code(node.variable)
        var_addr = self.builder.gep(
            var_addr,
            [
                ir.Constant(IntType.llvm_type, 0),
                ir.Constant(IntType.llvm_type, idx)
            ]
        )
        return self.builder.load(var_addr)

    def _generate_AstFnDef(self, node):
        args = node.params_lst.params_lst

        fn_args = []
        for arg in args:
            fn_args.append(LilangType.type_from_str(arg[1]).llvm_type)

        return_type = LilangType.type_from_str(node.type).llvm_type

        fn_type = ir.FunctionType(return_type, fn_args)
        fn = ir.Function(self.main_module, fn_type, name=node.name)
        self.functions[node.name] = fn

        if not node.declaration:
            last_block = self.block
            last_builder = self.builder
            self.block = fn.append_basic_block(name='entry')
            self.builder = ir.IRBuilder(self.block)

            for index, arg in enumerate(args):
                lilang_type = LilangType.type_from_str(arg[1])
                if lilang_type.is_array:
                    address = fn.args[index]
                else:
                    address = self.builder.alloca(
                        lilang_type.llvm_type, name=arg[0]
                    )

                self.variables[arg[0]] = LLVMVariable(
                    arg[0],
                    arg[1],
                    address
                )

                if not lilang_type.is_array:
                    self.builder.store(fn.args[index], address)

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

    def _generate_AstStructStat(self, node):
        fields = node.struct_fields.params_lst

        fields_types = []
        for field in fields:
            fields_types.append(LilangType.type_from_str(field[1]).llvm_type)

        type(
            f"Struct{node.name}Type",
            (LilangType,),
            {
                "str_code": node.name,
                "llvm_type": ir.LiteralStructType(fields_types),
                "base_type": None,
                "is_array": True,
                "fields": fields
            }
        )
