class AST(object):
    _nodes = {}

    @classmethod
    def __init_subclass__(cls):
        AST._nodes[cls.__name__] = cls

        if not hasattr(cls, '__annotations__'):
            return

        fields = list(cls.__annotations__.items())

        def __init__(self, *args, **kwargs):
            if len(args) != len(fields):
                raise TypeError(f'Expected {len(fields)} arguments')
            for (name, ty), arg in zip(fields, args):
                if isinstance(ty, list):
                    if not isinstance(arg, list):
                        raise TypeError(f'{name} must be list')
                    if not all(isinstance(item, ty[0]) for item in arg):
                        raise TypeError(f'All items of {name} must be {ty[0]}')
                elif not isinstance(arg, ty):
                    raise TypeError(f'{name} must be {ty}')
                setattr(self, name, arg)

            for name, val in kwargs.items():
                setattr(self, name, val)

        cls.__init__ = __init__
        cls._fields = [name for name, _ in fields]

    def __repr__(self):
        vals = [getattr(self, name) for name in self._fields]
        argstr = ', '.join(f'{name}={type(val).__name__ if isinstance(val, AST) else repr(val)}'
                           for name, val in zip(self._fields, vals))
        return f'{type(self).__name__}({argstr})'


class Statement(AST):
    pass


class Expression(AST):
    pass


class Literal(Expression):
    pass


class DataType(AST):
    pass


class Location(AST):
    pass


# Concrete AST nodes
class PrintStatement(Statement):
    value: Expression


class IntegerLiteral(Literal):
    value: int


class StringLiteral(Literal):
    value: str


class BoolLiteral(Literal):
    value: str


class IfStatement(Statement):
    condition: Expression
    true_block: [Statement]
    false_block: [Statement]


class WhileStatement(Statement):
    condition: Expression
    body: [Statement]


class BinOp(Expression):
    op: str
    left: Expression
    right: Expression


class UnaryOp(Expression):
    op: str
    right: Expression


class FuncCall(Expression):
    name: str
    arguments: [Expression]


class ConstDeclaration(Statement):
    name: str
    value: Expression


class FuncParameter(AST):
    name: str


class FuncDeclaration(Statement):
    name: str
    params: [FuncParameter]
    body: [Statement]


class ReturnStatement(Statement):
    value: Expression


class SimpleType(DataType):
    name: str


class VarDeclaration(Statement):
    name: str
    value: (Expression, type(None))


class SimpleLocation(Location):
    name: str


class ReadLocation(Expression):
    location: Location


class WriteLocation(Statement):
    location: Location
    value: Expression
