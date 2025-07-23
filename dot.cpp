#include"dot.h"
dot::dot():x(0),y(0){}
dot::dot(double a, double b){ x=a; y=b; }
double dot::get_x() const{ return x; }
double dot::get_y() const{ return y; }

