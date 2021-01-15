class AssemblerGenerator:
    literals = ["IntegerLiteral", "StringLiteral"]

    def __init__(self, tree):
        self.txt = ""
        self.table_symbol = dict()
        self.table_register = dict()
        self.tree = tree

    def assign_values(self, name, func_name, value):
        if name not in self.table_register[func_name].keys():
            if self.table_register[func_name].values():
                self.table_register[func_name][name] = list(self.table_register[func_name].values())[-1] + 4
            else:
                self.table_register[func_name][name] = 0
            self.txt += "mov {0}, {1}\n".format(self.get_register(func_name, name), value)

    def get_register(self, func_name, name):
        if name != "return":
            try:
                return f"dword ptr[esp+{self.table_register[func_name][name]}]"
            except:
                raise NameError(f'{name} is not defined')
        else:
            return "b"

    def generate(self):
        for branch in self.tree:
            if self.__get_class_name(branch) == "FuncDeclaration":
                func_name = branch.name
                self.table_symbol[func_name] = dict()
                self.table_register[func_name] = dict()
                self.generate_body(branch.body, func_name)

    def generate_body(self, body, func_name):
        for row in body:
            row_class = self.__get_class_name(row)
            if row_class == "VarDeclaration":
                row_class_value = self.__get_class_name(row.value)
                if row_class_value == "BinOp":
                    self.generate_bin_op(row.name, row.value.left, row.value.right, row.value.op, func_name)
                elif row_class_value in self.literals:
                    self.assign_values(row.name, func_name, row.value.value)
                elif row_class_value == "UnaryOp":
                    self.generate_unary_op(row.name, row.value.right, row.value.op, func_name)
            elif row_class == "ReturnStatement":
                self.generate_return(func_name, row.value)

    def generate_bin_op(self, name, left, right, op, func_name):
        self.assign_values(name, func_name, 0)
        if op == "/":
            self.txt += f"mov eax, {self.get_value_or_reg(left, func_name)}\n"
            self.txt += f"mov ebx, {self.get_value_or_reg(right, func_name)}\n"
            self.txt += f"xor edx,edx\n"
            self.txt += f"div ebx\n"
        elif op == "*":
            self.txt += f"mov eax, {self.get_value_or_reg(left, func_name)}\n"
            self.txt += f"mov ecx, {self.get_value_or_reg(right, func_name)}\n"
            self.txt += f"mul ecx\n"
        elif op == "or":
            self.txt += f"mov eax,{self.get_value_or_reg(left, func_name)}\n"
            self.txt += f"test eax, eax\n"
            self.txt += f"jnz _or\n"
            self.txt += f"mov eax, {self.get_value_or_reg(right, func_name)}\n"
            self.txt += f"_or:\n"
        if name != "return":
            self.txt += f"mov {self.get_register(func_name, name)}, eax\n"
        else:
            self.txt += f"mov ebx, eax\n"
            self.txt += f"mov b, ebx\n"

    def generate_unary_op(self, name, right, op, func_name):
        if op == "-":
            if self.__get_class_name(right) in self.literals:
                self.assign_values(name, func_name, 0 - int(right.value))
            else:
                self.txt += f"neg {self.get_value_or_reg(right, func_name)}\n"
                if name == "return":
                    self.txt += f"mov ebx, {self.get_value_or_reg(right, func_name)}\n"
                    self.txt += f"mov b, ebx\n"

    def generate_return(self, func_name, arg):
        arg_class = self.__get_class_name(arg)

        if arg_class == "ReadLocation":
            self.txt += f"mov ebx, {self.get_register(func_name, arg.location.name)}\n"
            self.txt += f"mov b, ebx\n"
        elif arg_class in self.literals:
            self.txt += f"mov ebx, {arg.value}\n"
            self.txt += f"mov b, ebx\n"
        elif arg_class == "BinOp":
            self.generate_bin_op("return", arg.left, arg.right, arg.op, func_name)
        elif arg_class == "UnaryOp":
            self.generate_unary_op("return", arg.right, arg.op, func_name)

    def get_value_or_reg(self, object, func_name):
        if self.__get_class_name(object) in self.literals:
            return object.value
        elif self.__get_class_name(object) == "ReadLocation":
            return f"{self.get_register(func_name, object.location.name)}"

    def generate_cpp(self):
        cpp_code = f"""
#include <iostream>
#include <string>
#include <stdint.h>
using namespace std;
string r = "";

string toBinary(int n)
{{   
    r = (n % 2 == 0 ? "0" : "1") + r;
    if (n / 2 != 0) {{
        toBinary(n / 2);
    }}
    return r;
}}
int main()
{{
int b;
__asm {{
    {self.txt}
}}
cout << "DEC: " << b << endl;
cout << "BIN: " << toBinary(b) << endl;
}}
"""
        return cpp_code

    def __get_class_name(self, object):
        return object.__class__.__name__