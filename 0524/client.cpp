#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <string.h>
#include <error.h>
#include "client.h"

using SAI = struct sockaddr_in;
using SA = struct sockaddr;

const int LEN = 4096;

void process(const int confd){
    while(true){
        char buf[LEN];
        memset(buf, '\0', sizeof(buf));
        std::cout << " plz enter:";
        std::cin>>buf;
        if(strcmp(buf, "quit") == 0){
            break;
        }
        if(std::cin.eof()){
            break;
        }
        write(confd, buf, strlen(buf));

        memset(buf, '\0', sizeof(buf));
        ssize_t s = read(confd, buf, sizeof(buf));
        if(s == 0){
            std::cout << "server quit" << std::endl;
            break;
        } else if(s < 0){
            std::cout << "read error" << std::endl;
            break;
        } else{
            std::cout << "read " << s << " bytes: " << buf << std::endl;
        }

    }
}

void client(const char* ip, const int port){
    int confd;
    do{
        confd = socket(PF_INET, SOCK_STREAM, 0);
        if (confd < 0) { // -1
            std::cerr<<"ERROR opening socket" << std::endl;
            break;
        }
        SAI saddr;
        saddr.sin_family = AF_INET;
        inet_pton(AF_INET, ip, &saddr.sin_addr );
        saddr.sin_port = htons(port); 
        if(connect(confd, (SA*)&saddr, sizeof(saddr)) < 0){ //-1
            std::cerr << "ERROR on binding" << std::endl;
            break;
        }
        process(confd);
    }while(0); //via: https://www.cnblogs.com/lizhenghn/p/3674430.html & https://www.zhihu.com/question/24386599
    close(confd);
    
}