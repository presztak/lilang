class AstNode(object):
    pass


class AstProgram(AstNode):

    def __init__(self, program):
        self.program = program


class AstStatLst(AstNode):

    def __init__(self, stat, stat_lst=None):
        if stat_lst:
            self.stat_lst = stat_lst.stat_lst + [stat]
        else:
            self.stat_lst = [stat]


class AstParamsLst(AstNode):
    def __init__(self, param, type, params_lst=None):
        if not param:
            self.params_lst = []
        elif params_lst:
            self.params_lst = params_lst.params_lst + [(param, type)]
        else:
            self.params_lst = [(param, type)]


class AstArgsLst(AstNode):
    def __init__(self, arg, args_lst=None):
        if not arg:
            self.args_lst = []
        elif args_lst:
            self.args_lst = args_lst.args_lst + [arg]
        else:
            self.args_lst = [arg]


class AstNumber(AstNode):

    def __init__(self, value):
        self.value = value


class AstVariable(AstNode):

    def __init__(self, identifier, index_expr=None):
        self.identifier = identifier
        self.index_expr = index_expr


class AstBinExpr(AstNode):

    def __init__(self, expr0, expr1, operator):
        self.expr0 = expr0
        self.expr1 = expr1
        self.operator = operator


class AstLstExpr(AstNode):
    def __init__(self, args_lst):
        self.args_lst = args_lst


class AstAssignStat(AstNode):

    def __init__(self, identifier, expr, index_expr=None):
        self.identifier = identifier
        self.expr = expr
        self.index_expr = index_expr


class AstDeclStat(AstNode):

    def __init__(self, type, identifier, expr):
        self.type = type
        self.identifier = identifier
        self.expr = expr


class AstIfStat(AstNode):

    def __init__(self, condition, stat_lst):
        self.condition = condition
        self.stat_lst = stat_lst


class AstWhileStat(AstNode):

    def __init__(self, condition, stat_lst):
        self.condition = condition
        self.stat_lst = stat_lst


class AstReturnStat(AstNode):

    def __init__(self, expr):
        self.expr = expr


class AstFnDef(AstNode):

    def __init__(
        self, type, name, stat_lst=None, params_lst=None, declaration=False
    ):
        self.type = type
        self.name = name
        self.stat_lst = stat_lst
        self.params_lst = params_lst
        self.declaration = declaration


class AstFnCall(AstNode):

    def __init__(self, name, args_lst=None):
        self.name = name
        self.args_lst = args_lst