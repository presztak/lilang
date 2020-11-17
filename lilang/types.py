from llvmlite import ir


class VoidType(object):

    str_code = 'void'
    llvm_type = ir.VoidType()


class BoolType(object):

    str_code = 'bool'
    llvm_type = ir.IntType(1)


class BoolArrayType(object):

    str_code = 'bool[]'
    llvm_type = ir.PointerType(BoolType.llvm_type)


class IntType(object):

    str_code = 'int'
    llvm_type = ir.IntType(32)


class IntArrayType(object):

    str_code = 'int[]'
    llvm_type = ir.PointerType(IntType.llvm_type)
