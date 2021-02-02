from sly import Parser

from .ast import (
    AstArgsLst,
    AstAssignStat,
    AstBinExpr,
    AstBool,
    AstBreakStat,
    AstContinueStat,
    AstDeclStat,
    AstFnCall,
    AstFnDef,
    AstForStat,
    AstGetAttribute,
    AstIfStat,
    AstInitDecl,
    AstInitDeclList,
    AstLstExpr,
    AstNumber,
    AstParamsLst,
    AstProgram,
    AstReturnStat,
    AstStatLst,
    AstString,
    AstStructLiteral,
    AstStructStat,
    AstVariable,
    AstWhileStat
)
from .lexer import LilangLexer
from .lib import column_from_index


class LilangParser(Parser):
    tokens = LilangLexer.tokens

    precedence = (
        ('left', OR),
        ('left', AND),
        ('left', THEN),
        ('left', ELSE),
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

    @_('var_type ID')
    def params_lst(self, p):
        return AstParamsLst(p.ID, p.var_type)

    @_('var_type ELLIPSIS ID')
    def params_lst(self, p):
        return AstParamsLst(p.ID, p.var_type, var_args=True)

    @_('params_lst "," var_type ID')
    def params_lst(self, p):
        return AstParamsLst(p.ID, p.var_type, p.params_lst)

    @_('params_lst "," var_type ELLIPSIS ID')
    def params_lst(self, p):
        return AstParamsLst(p.ID, p.var_type, p.params_lst, var_args=True)

    @_('expr ";"')
    def stat(self, p):
        return AstStatLst(p.expr)

    @_('"{" stat_lst "}"')
    def stat(self, p):
        return p.stat_lst

    @_('var_type ID "(" params_lst ")" "{" stat_lst "}"')
    def stat(self, p):
        return AstFnDef(p.var_type, p.ID, p.stat_lst, p.params_lst)

    @_('var_type ID "(" params_lst ")" "{" "}"')
    def stat(self, p):
        return AstFnDef(p.var_type, p.ID, None, p.params_lst)

    @_('var_type ID "(" params_lst ")" ";"')
    def stat(self, p):
        return AstFnDef(p.var_type, p.ID, None, p.params_lst, declaration=True)

    @_('ID "(" args_lst ")"')
    def expr(self, p):
        return AstFnCall(p.ID, p.args_lst)

    @_('ID ASSIGN expr')
    def init_decl(self, p):
        return AstInitDecl(p.ID, p.expr)

    @_('init_decl')
    def init_decl_lst(self, p):
        return AstInitDeclList(p.init_decl)

    @_('init_decl "," init_decl_lst')
    def init_decl_lst(self, p):
        return AstInitDeclList(p.init_decl, p.init_decl_lst)

    @_('var_type init_decl_lst ";"')
    def stat(self, p):
        return AstDeclStat(p.var_type, p.init_decl_lst)

    @_(
        'ID ASSIGN expr ";"',
        'ID PLUS_ASSIGN expr ";"',
        'ID MINUS_ASSIGN expr ";"',
        'ID TIMES_ASSIGN expr ";"',
        'ID DIVIDE_ASSIGN expr ";"'
    )
    def stat(self, p):
        return AstAssignStat(p.ID, p.expr, p[1])

    @_(
        'ID "[" expr "]" ASSIGN expr ";"',
        'ID "[" expr "]" PLUS_ASSIGN expr ";"',
        'ID "[" expr "]" MINUS_ASSIGN expr ";"',
        'ID "[" expr "]" TIMES_ASSIGN expr ";"',
        'ID "[" expr "]" DIVIDE_ASSIGN expr ";"'
    )
    def stat(self, p):
        return AstAssignStat(p.ID, p.expr1, p[4], p.expr0)

    @_('IF "(" expr ")" stat ELSE stat')
    def stat(self, p):
        return AstIfStat(p.expr, p.stat0, p.stat1)

    @_('IF "(" expr ")" stat %prec THEN')
    def stat(self, p):
        return AstIfStat(p.expr, p.stat)

    @_('WHILE "(" expr ")" "{" stat_lst "}" ')
    def stat(self, p):
        return AstWhileStat(p.expr, p.stat_lst)

    @_('FOR "(" stat  expr ";" stat ")" "{" stat_lst "}" ')
    def stat(self, p):
        return AstForStat(p.stat0, p.expr, p.stat1, p.stat_lst)

    @_('RETURN expr ";"')
    def stat(self, p):
        return AstReturnStat(p.expr)

    @_('BREAK ";"')
    def stat(self, p):
        return AstBreakStat()

    @_('CONTINUE ";"')
    def stat(self, p):
        return AstContinueStat()

    @_('var_type ID ";"')
    def struct_fields(self, p):
        return AstParamsLst(p.ID, p.var_type)

    @_('struct_fields  var_type ID ";"')
    def struct_fields(self, p):
        return AstParamsLst(p.ID, p.var_type, p.struct_fields)

    @_('STRUCT ID "{" struct_fields "}"')
    def stat(self, p):
        return AstStructStat(p.ID, p.struct_fields)

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

    @_('"{" args_lst "}"')
    def expr(self, p):
        return AstStructLiteral(p.args_lst)

    @_('ID "[" expr "]"')
    def expr(self, p):
        return AstVariable(p.ID, p.expr)

    @_('expr "." ID')
    def expr(self, p):
        return AstGetAttribute(p.expr, p.ID)

    @_('ID')
    def expr(self, p):
        return AstVariable(p.ID)

    @_('NUMBER')
    def expr(self, p):
        return AstNumber(p.NUMBER)

    @_('TRUE', 'FALSE')
    def expr(self, p):
        return AstBool(p[0])

    @_('STRING')
    def expr(self, p):
        return AstString(p.STRING)

    @_(
        'BASE_TYPE',
        'ID'
    )
    def var_type(self, p):
        return p[0]

    @_('')
    def empty(self, p):
        pass

    def __init__(self, code):
        super().__init__()
        self.code = code

    def run(self, data):
        lexer = LilangLexer(self.code)
        return self.parse(lexer.tokenize(data))

    def error(self, p):
        if p:
            if p.type == 'error':
                self.errok()
                return
            print(
                f"Syntax error near '{p.value}' at line "
                f"{p.lineno} column {column_from_index(self.code, p)}"
            )
            self.errok()
        else:
            print("Syntax error at EOF")
