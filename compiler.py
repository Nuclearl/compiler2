from node import *
from sly import Parser
from scanner import CalcLexer


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', 'AND', 'NOT'),
        ('nonassoc', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLICATION', 'DIVIDE'),
        ('right', 'UNARY')
    )

    @_("statements")
    def block(self, p):
        return p.statements

    @_("")
    def block(self, p):
        return []

    @_('statement')
    def statements(self, p):
        return [p.statement]

    @_('statements statement')
    def statements(self, p):
        p.statements.append(p.statement)
        return p.statements

    @_('var_declaration')
    def statement(self, p):
        return p.var_declaration

    @_('assign_statement')
    def statement(self, p):
        return p.assign_statement

    @_('func_declaration')
    def statement(self, p):
        return p.func_declaration

    @_('ret_statement')
    def statement(self, p):
        return p.ret_statement

    @_('DEF ID "(" func_params ")" COLON "{" block "}"')
    def func_declaration(self, p):
        return FuncDeclaration(p.ID, p.func_params, p.block, lineno=p.lineno)

    @_('func_params COMA func_param')
    def func_params(self, p):
        p.func_params.append(p.func_param)
        return p.func_params

    @_('func_param')
    def func_params(self, p):
        return [p.func_param]

    @_('')
    def func_params(self, p):
        return []

    @_('ID ')
    def func_param(self, p):
        return FuncParameter(p.ID, lineno=p.lineno)

    @_("RETURN expression")
    def ret_statement(self, p):
        return ReturnStatement(p.expression, lineno=p.lineno)

    @_('ID "(" arguments ")"')
    def func_call(self, p):
        return FuncCall(p.ID, p.arguments, lineno=p.lineno)

    @_('arguments COMA argument')
    def arguments(self, p):
        p.arguments.append(p.argument)
        return p.arguments

    @_('argument')
    def arguments(self, p):
        return [p.argument]

    @_('')
    def arguments(self, p):
        return []

    @_('expression')
    def argument(self, p):
        return p.expression

    @_('ID ASSIGN expression')
    def var_declaration(self, p):
        return VarDeclaration(p[0], p.expression, lineno=p.lineno)

    @_('location ASSIGN expression')
    def assign_statement(self, p):
        return WriteLocation(p.location, p.expression, lineno=p.lineno)

    @_('expression MINUS expression',
       'expression MULTIPLICATION expression',
       'expression DIVIDE expression',
       'expression OR expression')
    def expression(self, p):
        return BinOp(p[1], p.expression0, p.expression1, lineno=p.lineno)

    @_('expression PLUS expression',
       'expression LT expression',
       'expression LE expression',
       'expression GT expression',
       'expression GE expression',
       'expression EQ expression',
       'expression NE expression',
       'expression AND expression')
    def expression(self, p):
        raise SyntaxError(f'Unexpected symbol at {p.lineno+1} line')

    @_('PLUS expression',
       'MINUS expression',
       'NOT expression %prec UNARY')
    def expression(self, p):
        return UnaryOp(p[0], p.expression, lineno=p.lineno)

    @_('"(" expression ")"')
    def expression(self, p):
        return p.expression

    @_('location')
    def expression(self, p):
        return ReadLocation(p.location, lineno=p.location.lineno)

    @_('literal')
    def expression(self, p):
        return p.literal

    @_('func_call')
    def statement(self, p):
        return p.func_call

    @_('INTEGER')
    def literal(self, p):
        return IntegerLiteral(int(p.INTEGER), lineno=p.lineno)

    @_('STRING')
    def literal(self, p):
        return StringLiteral(p.STRING, lineno=p.lineno)

    @_('FLOAT', 'BOOLEAN', 'HEX', 'BIN', 'OCT')
    def literal(self, p):
        raise SyntaxError(f'Unexpected symbol at {p.lineno+1} line')

    @_('ID')
    def location(self, p):
        return SimpleLocation(p.ID, lineno=p.lineno)

    def error(self, p):
        if p:
            print(p.lineno, "Syntax error in input at token '%s'" % p.type)
        else:
            print('EOF', 'Syntax error. No more input.')
