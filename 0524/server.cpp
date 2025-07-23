#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <error.h>
#include <string.h>
#include <ctype.h>

#include "server.h"

using SAI = struct sockaddr_in;
using SA = struct sockaddr;

const int LEN = 4096;

void handle_msg(const int confd){
    while(true){
        char buf[LEN];
        bool flag = true;
        memset(buf, '\0', sizeof(buf));
        ssize_t s = read(confd, buf, sizeof(buf));
        if(s == 0){
            std::cout << "client quit" << std::endl;
            break;
        } else if(s < 0){
            std::cout << "read error" << std::endl;
            break;
        } else{
            std::cout << "read " << s << " bytes: " << buf << std::endl;
            for(int i=0;i<strlen(buf);i++){
                if (!isdigit(buf[i])) {  // for(auto i: buf) ????
                    flag = false; 
                    std::cout<<"error"<< i <<std::endl;
                    break; 
                }
            }
        }
        int tmp;
        if(flag) tmp = atoi(buf);

        std::cout<<"flag:"<<flag <<"; tmp:"<<tmp<<std::endl;

        memset(buf, '\0', sizeof(buf));

        // std::cout << " plz enter:";
        // do{
            // std::cin>>buf;
        // }while(std::cin.eof()==true);
        if (flag) {
            if( tmp%2 == 0) strcpy(buf, "Yes");
            else strcpy(buf, "No");
        } else {
            strcpy(buf, "No");
        }
        write(confd, buf , strlen(buf));

    }
}

void process(const int listenfd){
    while(true){
        int confd = accept(listenfd, nullptr, nullptr);
        if(confd == -1){
            std::cerr << "accept error" << std::endl;
            exit(EXIT_FAILURE);
        }
        handle_msg(confd);
    }
}

void server(int port){
    int listenfd;
    do{
        listenfd = socket(PF_INET, SOCK_STREAM, 0);
        // tcp transform to stream
        if (listenfd < 0) { // -1
            std::cerr << "ERROR opening socket" << std::endl;
            break;
        }
        SAI saddr;
        saddr.sin_family = AF_INET; // IP, PF_INET == AF_INET
        saddr.sin_addr.s_addr = htonl(INADDR_ANY); // all IP address okey; network byte order; INADDR_ANY == 0
        saddr.sin_port = htons(port); // port
        if(bind(listenfd, (SA*)&saddr, sizeof(saddr)) < 0){ //-1
            std::cerr << "ERROR on binding" << std::endl;
            break;
        }
        if(listen(listenfd, 5) < 0){ //-1, queue length==5
            std::cerr << "ERROR on listen" << std::endl;
            break;
        }
        process(listenfd);
    }while(0); //via: https://www.cnblogs.com/lizhenghn/p/3674430.html & https://www.zhihu.com/question/24386599
    close(listenfd);
}

    // int sockfd, newsockfd, portno;
    // socklen_t clilen;
    // char buffer[256];
    // struct sockaddr_in serv_addr, cli_addr;
    // int n;
    // if (argc < 2) {
    //     fprintf(stderr,"ERROR, no port provided\n");
    //     exit(1);
    // }
    // sockfd = socket(AF_INET, SOCK_STREAM, 0);
    // if (sockfd < 0) 
    //     error("ERROR opening socket");
    // bzero((char *) &serv_addr, sizeof(serv_addr));
    // portno = port;
    // serv_addr.sin_family = AF_INET;
    // serv_addr.sin_addr.s_addr = INADDR_ANY;
    // serv_addr.sin_port = htons(portno);
    // if (bind(sockfd, (struct sockaddr *) &serv_addr,
    //          sizeof(serv_addr)) < 0) 
    //     error("ERROR on binding");
    // listen(sockfd,5);
    // clilen = sizeof(cli_addr);
    // while (1) {
    //     newsockfd = accept(sockfd, 
    //             (struct sockaddr *) &cli_addr, 
    //             &clilen);
    //     if (newsockfd < 0) 
    //         error("ERROR on accept");
    //     bzero(buffer,256);
    //     n = read(newsockfd,buffer,255);
    //     if (n < 0) error("ERROR reading from socket");
    //     printf("Here is the message: %s\n",buffer);
    //     n = write(newsockfd,"I got your message",18);
    //     if (n < 0) error("ERROR writing to socket");
    // }
    // close(newsockfd);
    // close(sockfd);
    // return 0; 
// }