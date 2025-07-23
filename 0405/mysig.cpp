#include<iostream>
#include<sys/types.h>
#include<sys/wait.h>
#include"mysig.h"

void handle_child(int signo){
	pid_t child;
	while((child=waitpid(-1,NULL,WNOHANG)) > 0){
		std::cerr<<child<<" finish\n";
	}
}
