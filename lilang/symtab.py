from .parser import ModuleParser


class SymTab(object):

    def __init__(self):
        self.functions = {}
        self.variables = {}

    def gen(self, code):
        parser = ModuleParser(code)
        ast = parser.run()
        if ast:
            self.walk(ast)
        return ast

    def walk(self, node, data=None):
        method_name = f'_walk_{node.__class__.__name__}'
        method = getattr(self, method_name)
        return method(node, data)

    def _walk_AstProgram(self, node, data):
        self.walk(node.program)

    def _walk_AstStatLst(self, node, data):
        for stat in node.stat_lst:
            self.walk(stat)

    def _walk_AstStructStat(self, node, data):
        pass

    def _walk_AstStructLiteral(self, node, data):
        for arg in node.args_lst.args_lst:
            self.walk(arg)

    def _walk_AstFnDef(self, node, data):
        self.functions[node.name] = node.type
        for param in node.params_lst.params_lst:
            self.variables[param[0]] = param[1]
        if node.stat_lst:
            self.walk(node.stat_lst)

    def _walk_AstFnCall(self, node, data):
        for arg_expr in node.args_lst.args_lst:
            self.walk(arg_expr)

    def _walk_AstReturnStat(self, node, data):
        self.walk(node.expr)

    def _walk_AstBinExpr(self, node, data):
        self.walk(node.expr0)
        self.walk(node.expr1)
        self.type = node.expr0.type

    def _walk_AstNumber(self, node, data):
        pass

    def _walk_AstString(self, node, data):
        pass

    def _walk_AstBool(self, node, data):
        pass

    def _walk_AstVariable(self, node, data):
        if not node.type:
            node.type = self.variables[node.identifier]
        if node.index_expr:
            self.walk(node.index_expr)

    def _walk_AstGetAttribute(self, node, data):
        self.walk(node.variable)

    def _walk_AstAssignStat(self, node, data):
        self.walk(node.expr)
        if node.index_expr:
            self.walk(node.index_expr)

    def _walk_AstDeclStat(self, node, data):
        for init_decl in node.init_decl_lst.init_decl_lst:
            self.walk(init_decl, {"type": node.type})

    def _walk_AstInitDecl(self, node, data):
        self.variables[node.identifier] = data["type"]
        self.walk(node.expr)

    def _walk_AstWhileStat(self, node, data):
        self.walk(node.condition)
        self.walk(node.stat_lst)

    def _walk_AstForStat(self, node, data):
        self.walk(node.init_stat)
        self.walk(node.condition)
        self.walk(node.stat_lst)
        self.walk(node.step_stat)

    def _walk_AstIfStat(self, node, data):
        self.walk(node.condition)
        self.walk(node.stat_lst)

        # 'If' with else clause
        if node.else_stat_lst:
            self.walk(node.else_stat_lst)

    def _walk_AstLstExpr(self, node, data):
        for arg in node.args_lst.args_lst:
            self.walk(arg)

    def _walk_AstBreakStat(self, node, data):
        pass

    def _walk_AstContinueStat(self, node, data):
        pass
