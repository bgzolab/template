#include<unistd.h>
#include<stdlib.h>
#include<signal.h>
#include<cstring>
#include<iostream>
#include"client.h"
#include"server.h"
#include"mysig.h"

int main(int argc,char* argv[]){
	signal(SIGCHLD,handle_child);
	int fd[2];
	int fd2[2];
	pipe(fd);
	pipe(fd2);
	int i;
	for(i=0; i<3; i++){
		pid_t child=fork();
		if(child==0) break;
	}
	if(i==0){
		close(fd[0]);
		client(fd[1], argv[1],argv[2]);
		exit(0);
	}else if(i==1){
		// close(fd[1]);
		// server(fd[0], argv[3]);

		// // 怎么把 fd[0] 的内容, 搬到 fd2[1] ???
		// // 答案是老师定义的这个函数逻辑是无法实现的 ...
		// close(fd2[0]);
		// client(fd2[1], "" , ""); // fd[0]

		// char msg[4096];
		// read(fd[0], msg, 4096);
		// std::cout<<msg<<std::endl;
		// write(fd[0], msg, strlen(msg)+ 1);
		// client(fd2[1], msg, "");

		close(fd[1]);
		close(fd2[0]);

		dup2(fd[0], 0); // 0
	    dup2(fd2[1], 1);  //***

		execlp(argv[3], argv[3], NULL); //***

		exit(0);
	}else if(i==2){
		close(fd[0]);
        close(fd[1]);
		
		close(fd2[1]);
		server(fd2[0], argv[4]);
		exit(0);
	}else{
		close(fd[0]);
		close(fd[1]);
		close(fd2[0]);
		close(fd2[1]);
		while(true){
		}
	}
	return 0;
}
