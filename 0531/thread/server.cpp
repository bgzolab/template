#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <error.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <signal.h>
#include <thread>
#include <sys/types.h>
#include <sys/wait.h>

#include "server.h"
#include "message.h"

using SAI = struct sockaddr_in;
using SA = struct sockaddr;

const int LEN = sizeof(Message)+1;

void handle_msg(const int confd){
    while(true){
        char buf[LEN];
        bool flag = true;
        memset(buf, '\0', sizeof(buf));
        ssize_t s = read(confd, buf, LEN-1);
        if(s == 0){
            std::cout << "client quit" << std::endl;
            break;
        } else if(s < 0){
            std::cout << "read error" << std::endl;
            break;
        } else{
            Message m;
            memset(&m, '\0', sizeof(m));
            decode(buf,m);
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
            std::cout << "read " << s << " bytes: " << m << std::endl;
            encode(buf, m);
            write(confd, buf, LEN-1);
            break;
        }
    }
}

void handle_child(int signo){
    pid_t child;
    std::cout<<"ready to catch"<<std::endl;

    while( (child = waitpid( -1, &child, WNOHANG)) > 0){
        std::cerr << child << " finish\n"; //cout
    }//NULL
}

// void SIG_IGN(int signo){
//     if(signo == SIGPIPE){
//         std::cout << "client quit" << std::endl;
//     }
// }

void process(const int listenfd){
    //注册信号处理函数
    signal(SIGCHLD, handle_child); //SIG_IGN

    while(true){

        int confd = accept(listenfd, nullptr, nullptr);
        if(confd == -1){
            std::cerr << "accept error" << std::endl;
            exit(EXIT_FAILURE);
        }else{
            std::cout << "get a new client" << std::endl;
            std::thread t(handle_msg, confd);
            t.detach();                             // 独立运行, 除非客户端断开, 否则不会停止(低并发可以用)
            handle_msg(confd);
            // exit(EXIT_SUCCESS);
            
        }
        close(confd);
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