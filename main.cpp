#include <iostream>
#include "line.h"
#include <stdlib.h>

int main(int argc, char *argv[]){
	dot x1(atof(argv[1]), atof(argv[2]));
	dot x2(atof(argv[3]), atof(argv[4]));
	dot x3(atof(argv[5]), atof(argv[6]));
	dot x4(atof(argv[7]), atof(argv[8]));
	line l1(x1, x2);
	line l2(x3, x4);

	if(l1.is_dot_existed(l2)){
		dot tmp=l1.get_dot_with_line(l2);
		printf("%f\n", tmp.get_x());
		printf("%f", tmp.get_y());
	}else{
		printf("404 Not Found.");
	}
	return 0;
}
