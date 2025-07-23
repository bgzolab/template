#ifndef XY_MESSAGE_H
#define XY_MESSAGE_H
//#pragma once

#include<iostream>

struct Message{
    int oprand1;
    int op;
    int oprand2;
    int res;
    char status;
};

std::istream& operator >>(std::istream& in, Message& m);
std::ostream& operator <<(std::ostream& out, const Message& m);

#endif