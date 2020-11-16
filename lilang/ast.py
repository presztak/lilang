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

    def __init__(self, identifier, expr, operator, index_expr=None):
        self.identifier = identifier
        self.expr = expr
        self.operator = operator
        self.index_expr = index_expr


class AstInitDecl(AstNode):

    def __init__(self, identifier, expr):
        self.identifier = identifier
        self.expr = expr


class AstInitDeclList(AstNode):

    def __init__(self, init_decl, init_decl_lst=None):
        if init_decl_lst:
            self.init_decl_lst = init_decl_lst.init_decl_lst + [init_decl]
        else:
            self.init_decl_lst = [init_decl]


class AstDeclStat(AstNode):

    def __init__(self, type, init_decl_lst):
        self.type = type
        self.init_decl_lst = init_decl_lst


class AstIfStat(AstNode):

    def __init__(self, condition, stat_lst, else_stat_lst=None):
        self.condition = condition
        self.stat_lst = stat_lst
        self.else_stat_lst = else_stat_lst


class AstForStat(AstNode):

    def __init__(self, init_stat, condition, step_stat, stat_lst):
        self.init_stat = init_stat
        self.condition = condition
        self.step_stat = step_stat
        self.stat_lst = stat_lst


class AstWhileStat(AstNode):

    def __init__(self, condition, stat_lst):
        self.condition = condition
        self.stat_lst = stat_lst


class AstReturnStat(AstNode):

    def __init__(self, expr):
        self.expr = expr


class AstBreakStat(AstNode):
    pass


class AstContinueStat(AstNode):
    pass


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
