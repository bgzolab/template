#include <iostream>

class dot{
    double x;
    double y;
public:
    dot();
    dot(double, double);
    double get_x();
    double get_y();
};

dot::dot():x(0),y(0){}
dot::dot(double a, double b){ x=a; y=b; }
double dot::get_x(){ return x; }
double dot::get_y(){ return y; }

class line{
    double k;
    double b;
public:
    line();
    line(dot, dot);

    bool is_dot_existed(line);
    dot get_dot_with_line(line);

    double get_k();
    double get_b();

};

line::line():k(0), b(0){}

line::line(dot a, dot b){
    this->k = ( b.get_y()-a.get_y() ) / ( b.get_x()-a.get_x() );
    this->b = a.get_y() - k* a.get_x();
}

bool line::is_dot_existed(line a){
    return this->k != a.get_k() ? true : false;
}

dot line::get_dot_with_line(line a){
    double x = ( this->b - a.get_b() ) / ( a.get_k() - this->k);
    double y = ( a.get_k()* this->b - this->k*a.get_b() ) / ( a.get_k() - this->k);
    return dot(x, y);
}

double line::get_k(){ return k; }
double line::get_b(){ return b; }


int main(){
    dot x1(1, 1);
    dot x2(1, 2);
    dot x3(1, 1);
    dot x4(0, 1);
    line l1(x1, x2);
    line l2(x3, x4);

    if(l1.is_dot_existed(l2)){
        dot tmp=l1.get_dot_with_line(l2);
        std::cout<<tmp.get_x()<<'\n'<< tmp.get_y();
        printf("%f", tmp.get_x());
        printf("%f", tmp.get_y());
    }else{
        printf("404 Not Found.");
    }
    return 0;
}

