#include "message.h"


std::istream& operator >>(std::istream&in, Message& m){
    in>>m.oprand1>>m.op>>m.oprand2;
    return in;
}

std::ostream& operator <<(std::ostream&out, const Message& m){
    char ops[]={'+', '-', '*', '/'};
    out<<m.oprand1<<ops[m.op]<<m.oprand2;
    if(m.status != 'E' ) out << '=' <<m.res;
    else out << '=' << "error";
    return out;
}
