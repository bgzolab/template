#include<iostream>
#include "message.h"

std::istream& operator >>(std::istream& in, Message& m){
    std::cout<<"plz enter name:";
    in >> m.name;
    std::cout<<"plz enter password:";
    in >> m.passwd;
    return in;
}

std::ostream& operator <<(std::ostream& out, const Message& m){
    switch(m.status){
        case 'N':
            out << "Name ERROR";
            break;
        case 'P':
            out << "Password ERROR";
            break;
        case 'O':
            out << "Login uccessfully";
            break;
        default:
            break;
    }
    return out;
}
