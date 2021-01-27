from sly import Lexer

from .lib import column_from_index


class LilangLexer(Lexer):

    tokens = [
        IF, ELSE, WHILE, RETURN, BASE_TYPE, ID, ASSIGN, NUMBER,
        PLUS, MINUS, TIMES, DIVIDE, LT, LE, GT, GE, EQ,
        AND, OR, PLUS_ASSIGN, MINUS_ASSIGN, TIMES_ASSIGN, DIVIDE_ASSIGN,
        FOR, BREAK, CONTINUE, TRUE, FALSE, STRING, STRUCT
    ]

    literals = {';', '(', ')', '{', '}', '[', ']', ',', '"', '.'}

    ignore = ' \t'

    IF = r'if'
    ELSE = r'else'
    WHILE = r'while'
    FOR = r'for'
    RETURN = r'return'
    BREAK = r'break'
    CONTINUE = r'continue'
    TRUE = r'true'
    FALSE = r'false'
    STRUCT = r'struct'
    BASE_TYPE = r'void|int\[\]|int|bool\[\]|bool|string'
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
    STRING = r'\".*\"'

    def __init__(self, code):
        super().__init__()
        self.code = code

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(
            f"Illegal character {t.value[0]} in line "
            f"{self.lineno} column {column_from_index(self.code, t)}")
        self.index += 1
