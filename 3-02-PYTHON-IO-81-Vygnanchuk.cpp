
#include <iostream>
#include <string>
#include <stdint.h>
using namespace std;
string r = "";

string toBinary(int n)
{   
    r = (n % 2 == 0 ? "0" : "1") + r;
    if (n / 2 != 0) {
        toBinary(n / 2);
    }
    return r;
}
int main()
{
int b;
__asm {
    mov dword ptr[esp+0], 4
mov dword ptr[esp+4], 0
mov eax, dword ptr[esp+0]
mov ecx, 5
mul ecx
mov dword ptr[esp+4], eax
mov ebx, dword ptr[esp+4]
mov b, ebx

}
cout << "DEC: " << b << endl;
cout << "BIN: " << toBinary(b) << endl;
}
