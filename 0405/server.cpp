#include<unistd.h>
#include"server.h"

void server(const int rfd,const char* cmd){
	dup2(rfd,0);
	execlp(cmd,cmd,NULL);
}
