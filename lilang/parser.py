from sly import Parser

from .ast import (
    AstArgsLst,
    AstAssignStat,
    AstBinExpr,
    AstDeclStat,
    AstFnCall,
    AstFnDef,
    AstIfStat,
    AstLstExpr,
    AstNumber,
    AstParamsLst,
    AstProgram,
    AstReturnStat,
    AstStatLst,
    AstVariable,
    AstWhileStat
)
from .lexer import LilangLexer


class LilangParser(Parser):
    tokens = LilangLexer.tokens

    precedence = (
        ('left', OR),
        ('left', AND),
        ('nonassoc', LT, LE, GT, GE, EQ),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
    )

    @_('stat_lst')
    def program(self, p):
        return AstProgram(p.stat_lst)

    @_('stat')
    def stat_lst(self, p):
        return AstStatLst(p.stat)

    @_('stat_lst stat')
    def stat_lst(self, p):
        return AstStatLst(p.stat, p.stat_lst)

    @_('empty')
    def args_lst(self, p):
        return AstArgsLst(None)

    @_('expr')
    def args_lst(self, p):
        return AstArgsLst(p.expr)

    @_('args_lst "," expr')
    def args_lst(self, p):
        return AstArgsLst(p.expr, p.args_lst)

    @_('empty')
    def params_lst(self, p):
        return AstParamsLst(None, None)

    @_('TYPE ID')
    def params_lst(self, p):
        return AstParamsLst(p.ID, p.TYPE)

    @_('params_lst "," TYPE ID')
    def params_lst(self, p):
        return AstParamsLst(p.ID, p.TYPE, p.params_lst)

    @_('expr ";"')
    def stat(self, p):
        return AstStatLst(p.expr)

    @_('TYPE ID "(" params_lst ")" "{" stat_lst "}"')
    def stat(self, p):
        return AstFnDef(p.TYPE, p.ID, p.stat_lst, p.params_lst)

    @_('TYPE ID "(" params_lst ")" "{" "}"')
    def stat(self, p):
        return AstFnDef(p.TYPE, p.ID, None, p.params_lst)

    @_('TYPE ID "(" params_lst ")" ";"')
    def stat(self, p):
        return AstFnDef(p.TYPE, p.ID, None, p.params_lst, declaration=True)

    @_('ID "(" args_lst ")"')
    def expr(self, p):
        return AstFnCall(p.ID, p.args_lst)

    @_('TYPE ID ASSIGN expr ";"')
    def stat(self, p):
        return AstDeclStat(p.TYPE, p.ID, p.expr)

    @_('ID ASSIGN expr ";"')
    def stat(self, p):
        return AstAssignStat(p.ID, p.expr)

    @_('ID "[" expr "]" ASSIGN expr ";"')
    def stat(self, p):
        return AstAssignStat(p.ID, p.expr1, p.expr0)

    @_('IF "(" expr ")" "{" stat_lst "}" ')
    def stat(self, p):
        return AstIfStat(p.expr, p.stat_lst)

    @_('WHILE "(" expr ")" "{" stat_lst "}" ')
    def stat(self, p):
        return AstWhileStat(p.expr, p.stat_lst)

    @_('RETURN expr ";"')
    def stat(self, p):
        return AstReturnStat(p.expr)

    @_(
        'expr PLUS expr',
        'expr MINUS expr',
        'expr TIMES expr',
        'expr DIVIDE expr',
        'expr AND expr',
        'expr OR expr',
        'expr LT expr',
        'expr LE expr',
        'expr GT expr',
        'expr GE expr',
        'expr EQ expr',
    )
    def expr(self, p):
        return AstBinExpr(p.expr0, p.expr1, p[1])

    @_('"[" args_lst "]"')
    def expr(self, p):
        return AstLstExpr(p.args_lst)

    @_('ID "[" expr "]"')
    def expr(self, p):
        return AstVariable(p.ID, p.expr)

    @_('ID')
    def expr(self, p):
        return AstVariable(p.ID)

    @_('NUMBER')
    def expr(self, p):
        return AstNumber(p.NUMBER)

    @_('')
    def empty(self, p):
        pass

    def run(self, data):
        lexer = LilangLexer()
        return self.parse(lexer.tokenize(data))
