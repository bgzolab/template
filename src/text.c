#include <stdio.h>
#include "mylib.h"
int main(){
    double r;
    printf("Please enter the radius of the circle：\n");
    scanf("%lf",&r);
    printf("Circumferenceof the circle is：\n");
    printf("%lf\n",get_circumference(r));
    printf("Area of the circleis：\n");
    printf("%lf\n",get_area(r));
    return 0;
}