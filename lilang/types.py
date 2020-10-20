from llvmlite import ir


class VoidType(object):

    str_code = 'void'
    llvm_type = ir.VoidType()


class IntType(object):

    str_code = 'int'
    llvm_type = ir.IntType(32)


class IntArrayType(object):

    str_code = 'int[]'
    llvm_type = ir.PointerType(IntType.llvm_type)
