#include"line.h"

line::line():k(0), b(0){}

line::line(dot a, dot b){
	this->k = ( b.get_y()-a.get_y() ) / ( b.get_x()-a.get_x() );
	this->b = a.get_y() - k* a.get_x();
}

bool line::is_dot_existed(line a) const{
   return this->k != a.get_k();
}

dot line::get_dot_with_line(line a) const{
	double x = ( this->b - a.get_b() ) / ( a.get_k() - this->k);
	double y = ( a.get_k()* this->b - this->k*a.get_b() ) / ( a.get_k() - this->k);
    return {x, y};
}

double line::get_k() const{ return k; }
double line::get_b() const{ return b; }

