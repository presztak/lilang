from sly import Lexer


class LilangLexer(Lexer):

    tokens = [
        IF, ELSE, WHILE, RETURN, TYPE, ID, ASSIGN, NUMBER,
        PLUS, MINUS, TIMES, DIVIDE, LT, LE, GT, GE, EQ,
        AND, OR, PLUS_ASSIGN, MINUS_ASSIGN, TIMES_ASSIGN, DIVIDE_ASSIGN,
        FOR, BREAK, CONTINUE
    ]

    literals = {';', '(', ')', '{', '}', '[', ']', ','}

    ignore = ' \t\n'

    IF = r'if'
    ELSE = r'else'
    WHILE = r'while'
    FOR = r'for'
    RETURN = r'return'
    BREAK = r'break'
    CONTINUE = r'continue'
    TYPE = r'void|int\[\]|int'
    ID = r'[a-zA-Z][a-zA-Z]*'
    EQ = r'=='
    PLUS_ASSIGN = r'\+='
    MINUS_ASSIGN = r'-='
    TIMES_ASSIGN = r'\*='
    DIVIDE_ASSIGN = r'/='
    ASSIGN = r'='
    NUMBER = r'\d+'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    AND = r'&&'
    OR = r'\|\|'
