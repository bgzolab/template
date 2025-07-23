#include "message.h"
#include <stdio.h>

std::istream& operator >>(std::istream& in, Message& m){
    in>>m.oprand1;
    getchar();
    in>>m.op;
    getchar();
    in>>m.oprand2;
    return in;
}

std::ostream& operator <<(std::ostream& out, const Message& m){
    if(m.op == '/' && m.oprand2 == 0)
        out<<"rand2 cannot be zone";
    else 
        out<<m.oprand1<<" "<<m.op<<" "<<m.oprand2<<"="<<m.res;
    return out;
}
