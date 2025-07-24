#include<iostream>
/* Greatest common divisor(GCD)&least common multiple(LCM)
 * from: https://blog.csdn.net/qq_42504734/article/details/88369780
 * 辗转相除法(欧几里德算法)定理：两个正整数a和b（a>b），它们的最大公约数等于
 * a除以b的余数c和b之间的最大公约数. 但是当数字比较大的时候a%b的性能会变差.
 */
int cdivisor(int m, int n) {
    int a, b, r;
    a = (m > n) ? m : n;
    b = (m > n) ? n : m;
    r = b;
    while (r != 0) {
        r = a % b;
        a = b;
        b = r;
    }
    return a;
}

/* 出自九章算术, 两个正整数a和b(a>b), 它们的最大公约数等于a-b的差值c和
 * 较小数b的最大公约数。（可以用递归实现）
 */
int cdivisor(int a, int b) {
    while (a != b) {
        if (a > b)a -= b;
        else b -= a;
    }
    return a;
}