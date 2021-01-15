from compiler import *
from asm import *
import ast, astpretty, sys

sys.tracebacklimit = 0


title = "input"
lexer = CalcLexer()
parser = CalcParser()
with open(f"{title}.txt", encoding="utf-8") as f:
    data = f.read()
tokens = list(lexer.tokenize(data))


def add_brackets(i, before, after):
    check = False
    if i == 0:
        while True:
            i += 1
            if tokens[i].type == "TAB":
                while True:
                    if tokens[i].type == "TAB":
                        after += 1
                    else:
                        nl = i - 1
                        check = True
                        break
                    i += 1
            if check:
                break

    else:
        while True:
            i += 1
            if i >= len(tokens):
                return 0
            if tokens[i].type == "NL" and tokens[i + 1].type == "TAB":
                nl = i
                i += 1
                while True:
                    if tokens[i].type == "TAB":
                        after += 1
                    else:
                        check = True
                        break
                    i += 1
            elif tokens[i].type == "NL" and tokens[i + 1].type != "TAB":
                nl = i
                after = 0
                check = True
            if check:
                break
    if (before - after) == -1:
        tokens[nl].type = "{"
        tokens[nl].value = "{"
    elif (before - after) == 1:
        tokens[nl].type = "}"
        tokens[nl].value = "}"
    add_brackets(i, after, 0)


try:
    add_brackets(0, 0, 0)
except:
    pass


def del_element(type):
    list_index = []
    for i in range(0, len(tokens)):
        if tokens[i].type == type:
            list_index.append(i)
    count = 0
    for i in list_index:
        del tokens[i - count]
        count += 1


del_element('TAB')
del_element('NL')

tree = parser.parse(iter(tokens))
print(dir(parser))
asm = AssemblerGenerator(tree)
asm.generate()
f = open(f"{title}.cpp", 'w')
f.write(asm.generate_cpp())
for i in ast.parse(data).body: print(astpretty.pprint(i, show_offsets=False))
print("--------------")

for i in iter(tokens):
    print(i)
print("--------------")
print(data)
print("--------------")
input("press Enter to exit")
