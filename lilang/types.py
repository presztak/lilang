from llvmlite import ir


class LilangType(object):

    subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls.str_code] = cls

    @classmethod
    def type_from_str(cls, str_type):
        return cls.subclasses[str_type]


class VoidType(LilangType):

    str_code = 'void'
    llvm_type = ir.VoidType()


class BoolType(LilangType):

    str_code = 'bool'
    llvm_type = ir.IntType(1)


class IntType(LilangType):

    str_code = 'int'
    llvm_type = ir.IntType(32)


class StringType(LilangType):

    str_code = 'string'
    llvm_type = ir.PointerType(ir.IntType(8))
