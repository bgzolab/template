#include "amic.h"
#include <iostream>

int Amicable::factorAmi(int n){
    int i = 1, t = 0;
    while (i < n) {
    if (n % i == 0 ) {
        t += i;
    }
        i++;
    }
    return t;
}

void Amicable::operator()(){
    if(factorAmi(n) == m && factorAmi(m) == n){
        std:: cout<< "yes\n";
    }else{
        std:: cout<< "no\n";
    }
}