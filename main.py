from scanner import CalcLexer
from compiler import *
from asm import *

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    with open("test.txt", encoding="utf-8") as f:
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

    for tok in tokens:
        print('type=%r, value=%r' % (tok.type, tok.value))

    result = parser.parse(iter(tokens))
    asm = AssemblerGenerator(result)
    asm.generate()
    print(asm.txt)
