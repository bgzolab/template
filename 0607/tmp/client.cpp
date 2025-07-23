#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <string.h>
#include <error.h>

#include "client.h"
#include "message.h"

using SAI = struct sockaddr_in;
using SA = struct sockaddr;

// const int LEN = sizeof(Message)+1;
const int LEN = 4096;

void process (const int confd, SAI& saddr){
    while(true){
        char buf[LEN];
        memset(buf, 0, LEN);

        Message m;
        memset(&m, '\0', sizeof(m));

        std::cout << "plz enter:";
        std::cin>>m;
        if(std::cin.eof()){
            break;
        }
        m.status='S';

        encode(buf, m);
        sendto(confd, buf, LEN-1, 0, (SA*)&saddr, sizeof(saddr));

        memset(buf, '\0', sizeof(buf));

        recvfrom(confd, buf, LEN - 1 , 0, NULL, NULL); // LEN-1
        decode(buf, m);
        std::cout << m << std::endl;

    }
}

void client(const char* ip, const int port){
    int confd;
    do{
        confd = socket(PF_INET, SOCK_DGRAM, 0);
        if (confd < 0) { // -1
            std::cerr<<"ERROR opening socket" << std::endl;
            break;
        }
        // udp don't bind , don't connect
        SAI saddr;
        saddr.sin_family = AF_INET;
        inet_pton(AF_INET, ip, &saddr.sin_addr );
        saddr.sin_port = htons(port);
        process(confd, saddr);
    }while(0);
    close(confd);
}