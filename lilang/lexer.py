from sly import Lexer


class LilangLexer(Lexer):

    tokens = [
        IF, WHILE, RETURN, TYPE, ID, ASSIGN, NUMBER,
        PLUS, MINUS, TIMES, DIVIDE, LT, LE, GT, GE, EQ,
        AND, OR
    ]

    literals = {';', '(', ')', '{', '}', '[', ']', ','}

    ignore = ' \t\n'

    IF = r'if'
    WHILE = r'while'
    RETURN = r'return'
    TYPE = r'void|int\[\]|int'
    ID = r'[a-zA-Z][a-zA-Z]*'
    EQ = r'=='
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
