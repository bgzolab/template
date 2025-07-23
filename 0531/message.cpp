#include <arpa/inet.h>
#include <string.h>
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

void decode(const char* buf, Message& m){
    size_t len =0;

    memcpy(&m.oprand1, buf+len, sizeof(m.oprand1));
    m.oprand1 = ntohl(m.oprand1);
    len += sizeof(m.oprand1);

    memcpy(&m.op, buf+len, sizeof(m.op));
    m.op = ntohl(m.op);
    len += sizeof(m.op);

    memcpy(&m.oprand2, buf+len, sizeof(m.oprand2));
    m.oprand2 = ntohl(m.oprand2);
    len += sizeof(m.oprand2);

    memcpy(&m.res, buf+len, sizeof(m.res));
    m.res = ntohl(m.res);
    len += sizeof(m.res);

    memcpy(&m.status, buf+len, sizeof(m.status));
    // m.status = ntohl(m.status);
    len+=sizeof(m.status);
}

void encode(char* buf, const Message& m){
    size_t len = 0;
    *(int*)(buf+len) = htonl(m.oprand1);
    len += sizeof(int);
    *(int*)(buf+len) = htonl(m.op);
    len += sizeof(int);
    *(int*)(buf+len) = htonl(m.oprand2);
    len += sizeof(int);
    *(int*)(buf+len) = htonl(m.res);
    len += sizeof(int);
    memcpy(buf+len, &m.status, sizeof(m.status));
    len += sizeof(m.status);
    // message to buf
}
