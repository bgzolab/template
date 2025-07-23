#include <iostream>

struct Message{
    int oprand1;
    int oprand2;
    int op;
    int res;
    char status;
};

std::istream& operator >>(std::istream& in, Message& m);
std::ostream& operator <<(std::ostream& out, const Message& m);

