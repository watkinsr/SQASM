#include <cstdio>
#include <string>
#include <iostream>

extern "C"
void printi(long long val)
{
    printf("%lld\n", val);
}
extern "C"
void printd(double val)
{
    printf("%f\n", val);
}
extern "C"
void prints(std::string val)
{
    std::cout << val << std::endl;
}
