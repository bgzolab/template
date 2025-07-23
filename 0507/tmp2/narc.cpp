#include "narc.h"
#include <iostream>

int Narcissistic::factorSum(int n){
    int sum = 0; // 记录最终求和结果

    int x1 = n / 100; // 原数除以100即为百位
    int x2 = n % 100 / 10; // 原数模100后，除以10就是十位数
    int x3 = n % 10; // 模10的结果就是个位数

    sum = x1 * x1 * x1 + x2 * x2 * x2 + x3 * x3 * x3;
    return sum;
}

void Narcissistic::operator()(){
    if(factorSum(n) == n){
        std:: cout<< "yes\n";
    }else{
        std:: cout<< "no\n";
    }
}