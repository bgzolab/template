#include <stdio.h>

int input(char *s,int length);

int main()
{
    //char buffer[32];
    
    char *b;
    size_t bufsize = 0;
    size_t characters;

    printf("Type something: ");
    characters = getline(&b, &bufsize, stdin);
    printf("%ld\n", bufsize);
    //characters = getline(&b, &bufsize, stdin);
    printf("%zu characters were read.\n", characters);
    printf("You typed: '%s'\n", b);

    return(0);
}
