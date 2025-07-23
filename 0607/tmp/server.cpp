#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <string.h>

#include "server.h"
#include "message.h"

using SAI = struct sockaddr_in;
using SA = struct sockaddr;

// const int LEN = sizeof(Message)+1;
const int LEN = 4096;

void handle_msg(char *buf){
    Message m;
    memset(&m, '\0', sizeof(m));

    decode(buf, m);
    // std::cout << m << std::endl;
    
    // std::cout << buf << std::endl;
    switch(m.op){
        case 0:
            m.res = m.oprand1 + m.oprand2;
            break;
        case 1:
            m.res = m.oprand1 - m.oprand2;
            break;
        case 2:
            m.res = m.oprand1 * m.oprand2;
            break;
        case 3:
            if(m.oprand2 == 0 ){
                m.status = 'E';
                m.res = -1;
                break;
            }
            m.res = m.oprand1 / m.oprand2;
            break;
        default:
            break;
    }
    std::cout  << m << std::endl;
    encode(buf, m);
}

void process(const int confd) {
    while(true){
        char buf[LEN];
        memset(buf, '\0', LEN);

        SAI caddr;
        memset (&caddr, 0, sizeof(caddr));
        socklen_t calen = sizeof(caddr);

        recvfrom(confd, buf, LEN - 1, 0, (SA *)&caddr, &calen);

        handle_msg(buf);

        sendto(confd, buf, LEN - 1, 0, (SA *)&caddr, calen);
    }
}


void server(const int port){
    // udp just have a port
    int confd;

    do{
        confd = socket(PF_INET, SOCK_DGRAM, 0);
        if(confd == -1) {
            std::cerr<<"socket error"<<std::endl;
            break;
        }
        // bind address 
        SAI saddr;
        memset(&saddr, 0, sizeof(saddr));
        saddr.sin_family = AF_INET;
        saddr.sin_addr.s_addr = htonl(INADDR_ANY);
        saddr.sin_port = htons(port);
        if(bind(confd, (SA*)&saddr, sizeof(saddr)) == -1) {
            std::cerr<<"bind error"<<std::endl;
            break;
        }
        process(confd);
    }while(0);
    close(confd);
}