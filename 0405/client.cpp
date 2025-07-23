#include<unistd.h>
#include"client.h"

void client(const int wfd,const char* cmd,const char* param){
	dup2(wfd,1);
	execlp(cmd,cmd,param,NULL);
}
