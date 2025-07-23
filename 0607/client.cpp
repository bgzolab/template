#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <string.h>
#include <error.h>
#include "client.h"
// #include "message.h"

using SAI = struct sockaddr_in;
using SA = struct sockaddr;

const int LEN = 4096;

void process (const int confd, SAI& saddr){
    char buf[LEN];

    while(true){
        memset(buf, 0, LEN);
        // std::cin.clear();
        std::cin>>buf;

        sendto(confd, buf, strlen(buf), 0, (SA*)&saddr, sizeof(saddr));

        recvfrom(confd, buf, LEN, 0, NULL, NULL); // LEN-1
        std::cout<<buf<<std::endl;
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