#include<iostream>

struct Message{
    long mtype;
    long rtype;
    int oprand1;
    int op;
    int oprand2;
    int res;
    char status;
};

std::istream& operator >>(std::istream& in, Message& m);
std::ostream& operator <<(std::ostream& out, const Message& m);
