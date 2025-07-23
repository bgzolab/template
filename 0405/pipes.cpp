#include<unistd.h>
#include<stdlib.h>
#include<signal.h>
#include<unistd.h>
#include<unistd.h>

#include<iostream>
#include<sys/types.h>
#include<sys/wait.h>

void handle_child(int signo){
	pid_t child;
	while((child=waitpid(-1,NULL,WNOHANG)) > 0){
		std::cerr<<child<<" finish\n";
	}
}

int main(int argc,char* argv[]){
	signal(SIGCHLD,handle_child);
	int fd[2];
	int fd2[2];

    pipe(fd);
	pipe(fd2);

	int i=0;
	for(;i<3;i++){
		pid_t child=fork();
		if(child==0) break;
	}
	if(i==0){
		close(fd2[0]);
		close(fd2[1]);

		close(fd[0]);
        dup2(fd[1],1);
	    execlp(argv[1], argv[1], argv[2], NULL);

		exit(0);
	}else if(i==1){
        close(fd2[0]);
		close(fd[1]);

	    dup2(fd[0], 0); // 0
	    dup2(fd2[1], 1);  //***

	    execlp(argv[3], argv[3], NULL); //***
		exit(0);
	}else if(i==2){
        close(fd[0]);
        close(fd[1]);

		close(fd2[1]);
	    dup2(fd2[0], 0);

        // printf("test");

    	execlp(argv[4], argv[4], NULL);

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
