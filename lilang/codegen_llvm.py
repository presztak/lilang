import os
import subprocess

import llvmlite.binding as llvm_binding
from llvmlite import ir

from .codegen import CodeGenerator
from .symtab import SymTab
from .types import BoolType, IntType, LilangType, VoidType


class LLVMVariable(object):

    def __init__(
        self, identifier, type, array_depth, address, is_struct=False
    ):
        self.identifier = identifier
        self.type = type
        self.array_depth = array_depth
        self.address = address
        self.is_struct = is_struct


class LLVMFunction(object):

    def __init__(self, function, var_arg=False):
        self.function = function
        self.var_arg = var_arg


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

    libs = ["io.li", "str.li", "vaarg.li"]

    def __init__(self):
        super().__init__()

        self.builder = None
        self.main_module = None
        self.block = None
        self.variables = {}
        self.functions = {}
        self.loops = []
        self.break_stat_generation = False

        self.symtab = SymTab()

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
            VoidType.llvm_type,
            (IntType.llvm_type, ir.PointerType(ir.PointerType(ir.IntType(8))))
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
            0,
            var_addr
        )

        self.variables['argv'] = LLVMVariable(
            'argv',
            'string',
            1,
            main_func.args[1]
        )

    def compile_libs(self):
        for lib in self.libs:
            with open(os.path.join(self.lib_path, lib)) as lib_script:
                lib_code = lib_script.read()
                self.generate_code(self.symtab.gen(lib_code))

    def libs_paths(self):
        result = []
        for lib in self.libs:
            result.append(
                os.path.join(self.lib_path, f"lib{lib.split('.')[0]}.so")
            )
        return result

    def compile(self, str_code, exec_name):

        object_file_name = f'{exec_name}.o'
        self.va_start = self.main_module.declare_intrinsic(
            'llvm.va_start',
            fnty=ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer()])
        )
        self.va_end = self.main_module.declare_intrinsic(
            'llvm.va_end',
            fnty=ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer()])
        )

        self.compile_libs()
        ast = self.symtab.gen(str_code)
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
            *self.libs_paths()
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

        # TODO: Temporary workeround
        expr_type = node.expr0.type
        if hasattr(expr_type, "type"):
            expr_type = expr_type.type

        if expr_type == "string":
            op = node.operator
            const = ir.Constant(
                ir.ArrayType(ir.IntType(8), len(op)),
                bytearray(op, encoding='ascii')
            )
            alloca = self.builder.alloca(const.type)
            self.builder.store(const, alloca)
            return self.builder.call(
                self.main_module.get_global('llstrcmp'),
                [
                    expr0, expr1,
                    self.builder.bitcast(alloca, ir.IntType(8).as_pointer())
                ]
            )
        else:
            # int operations
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
        result = self.generate_code(node.expr)
        lilang_type = LilangType.type_from_str(node.type.type)

        if node.type.array_depth > 0 or node.type.is_struct:
            self.variables[node.identifier] = LLVMVariable(
                node.identifier,
                node.type.type,
                node.type.array_depth,
                result,
                is_struct=node.type.is_struct
            )
        else:
            var_addr = self.builder.alloca(
                lilang_type.llvm_type, size=None, name=node.identifier
            )
            self.builder.store(result, var_addr)
            self.variables[node.identifier] = LLVMVariable(
                node.identifier,
                node.type.type,
                node.type.array_depth,
                var_addr
            )

        return result

    def _generate_AstDeclStat(self, node):
        for init_decl in node.init_decl_lst.init_decl_lst:
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
        str_val = ir.Constant(
            ir.ArrayType(ir.IntType(8), len(node.value)),
            bytearray(node.value, encoding='ascii')
        )
        alloca = self.builder.alloca(str_val.type)
        self.builder.store(str_val, alloca)
        return self.builder.bitcast(alloca, ir.IntType(8).as_pointer())

    def _generate_AstLstExpr(self, node):
        result = []

        for arg in node.args_lst.args_lst:
            result.append(self.generate_code(arg))

        var_addr = self.builder.alloca(
            result[0].type, size=len(result)
        )

        for idx, num in enumerate(result):
            el_addr = self.builder.gep(
                var_addr, [ir.Constant(ir.IntType(32), idx)]
            )
            self.builder.store(num, el_addr)
        return var_addr

    def _generate_AstStructLiteral(self, node):
        result = []

        for arg in node.args_lst.args_lst:
            result.append(self.generate_code(arg))

        var_addr = self.builder.alloca(
            LilangType.type_from_str(node.type.type).llvm_type,
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
                        node.type.type
                    ).llvm_type.elements[idx],
                    el.constant
                ),
                el_addr
            )
        return var_addr

    def _generate_AstVariable(self, node):

        var = self.variables[node.identifier]
        var_addr = var.address

        if var.array_depth > 0:
            index = ir.Constant(IntType.llvm_type, 0)
            if node.index_exprs:
                for expr in node.index_exprs:
                    index = self.generate_code(expr)
                    var_addr = self.builder.gep(
                        var_addr, [index]
                    )
                    var_addr = self.builder.load(var_addr)
            return var_addr
        elif var.is_struct:
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
        var_arg = False
        for arg in args:
            if arg[2] is True:
                var_arg = True
                fn_args.append(ir.IntType(32))
                break
            arg_type = LilangType.type_from_str(arg[1].type).llvm_type
            if arg[1].array_depth > 0:
                arg_type = ir.PointerType(arg_type)
                for i in range(arg[1].array_depth - 1):
                    arg_type = ir.PointerType(arg_type)
            fn_args.append(arg_type)

        return_type = LilangType.type_from_str(node.type.type).llvm_type
        if node.type.array_depth > 0:
            return_type = ir.PointerType(return_type)
            for i in range(arg[1].array_depth - 1):
                return_type = ir.PointerType(return_type)

        fn_type = ir.FunctionType(return_type, fn_args, var_arg=var_arg)
        fn = ir.Function(self.main_module, fn_type, name=node.name)
        self.functions[node.name] = LLVMFunction(fn, var_arg=var_arg)

        if not node.declaration:
            last_block = self.block
            last_builder = self.builder
            self.block = fn.append_basic_block(name='entry')
            self.builder = ir.IRBuilder(self.block)

            for index, arg in enumerate(args):
                if arg[2] is True:
                    var_addr = self.builder.alloca(
                        LilangType.type_from_str('valist').llvm_type,
                        size=None,
                        name='elipsis'
                    )
                    var_addr_i8 = self.builder.bitcast(
                        var_addr,
                        ir.IntType(8).as_pointer()
                    )
                    self.builder.call(self.va_start, [var_addr_i8])
                    result = self.builder.call(
                        self.main_module.get_global(f'vaargs{arg[1].type}'),
                        [fn.args[index], var_addr_i8]
                    )
                    self.builder.call(self.va_end, [var_addr_i8])
                    self.variables[arg[0]] = LLVMVariable(
                        arg[0],
                        f'{arg[1].type}',
                        1,
                        result
                    )
                    break

                lilang_type = LilangType.type_from_str(arg[1].type)
                if arg[1].array_depth > 0:
                    address = fn.args[index]
                else:
                    address = self.builder.alloca(
                        lilang_type.llvm_type, name=arg[0]
                    )

                self.variables[arg[0]] = LLVMVariable(
                    arg[0],
                    arg[1].type,
                    arg[1].array_depth,
                    address,
                    is_struct=node.type.is_struct
                )

                if arg[1].array_depth == 0:
                    self.builder.store(fn.args[index], address)

            if node.stat_lst:
                self.generate_code(node.stat_lst)
            if node.type.type == VoidType.str_code:
                self.builder.ret_void()
            self.block = last_block
            self.builder = last_builder

    def _generate_AstFnCall(self, node):
        args = []
        fn = self.functions[node.name]

        for arg_expr in node.args_lst.args_lst:
            arg = self.generate_code(arg_expr)
            args.append(arg)
        if fn.var_arg:
            var_arg_len = len(args) - len(fn.function.args) + 1
            args.insert(
                len(fn.function.args) - 1,
                ir.Constant(ir.IntType(32), var_arg_len)
            )
        return self.builder.call(fn.function, args)

    def _generate_AstStructStat(self, node):
        fields = node.struct_fields.params_lst

        fields_types = []
        for field in fields:
            fields_types.append(
                LilangType.type_from_str(field[1].type).llvm_type
            )

        type(
            f"Struct{node.name}Type",
            (LilangType,),
            {
                "str_code": node.name,
                "llvm_type": ir.LiteralStructType(fields_types),
                "fields": fields
            }
        )
