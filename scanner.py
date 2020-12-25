from sly import Lexer


class CalcLexer(Lexer):
    # Set of token names.   This is always required

    literals = {
        '(', ')', '{', '}', ';'
    }

    tokens = {
        'PRINT', 'ELSE', 'DEF', 'IF', 'RETURN', 'WHILE',
        'ID',
        'INTEGER', 'FLOAT', 'BOOLEAN', 'STRING', 'COMA',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'COLON',
        'LE', 'LT', 'GE', 'GT', 'EQ', 'NE', 'AND', 'OR', 'NOT',
        'TAB', "NL"
    }

    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    EQ = r'=='
    NE = r'!='
    AND = r'&&'
    OR = r'\|\||or'
    NOT = r'!'
    TAB = '    '
    NL = '\n'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    COLON = r':'
    COMA = r','

    FLOAT = r'(((\d+\.\d*)|(\.\d+))([eE][+-]?\d+)?)|(\d+[eE][+-]?\d+)'
    INTEGER = r'(0x[0-9ABCDEF]+)|(0b[01]+)|(0o[0-5]+)|\d+'

    BOOLEAN = r'(true)|(false)'
    STRING = r'(\".*\")|(\'.*\')'

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        keywords = {
            'else',
            'def',
            'if',
            'print',
            'return',
            'while'
        }
        if t.value in keywords:
            t.type = t.value.upper()
        return t

    ignore_comment = r'\#.*'

    def error(self, t):
        self.index += 1
