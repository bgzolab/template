#include "message.h"

std::istream& operator >>(std::istream& in, Message& m){
    in >> m.name >> m.passwd;
    return in;
}

std::ostream& operator <<(std::ostream& out, const Message& m){
	switch(m.status){
		case 1: 
			out<<"login sucessfully";
			break;
 		case 2: 
			out<< "passwd error";
			break;
		case 3:
			out<< "name error";
		 	break;
		default:
			out<< "error";
			break;
		
	}
    	return out;
}
