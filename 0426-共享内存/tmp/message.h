#include <iostream>

struct Message{
    char name[20];
    char passwd[20];
    char status;
};

std::istream& operator >>(std::istream& in, Message& m);
std::ostream& operator <<(std::ostream& out, const Message& m);

