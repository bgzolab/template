# run command
# gcc -o text mylib.c text.c
# or using following makefile.

hello : mylib.o  text.o
	gcc -o hello mylib.o text.o
mylib.o : mylib.c mylib.h
	gcc -c mylib.c
text.o: text.c
	gcc -c text.c
clean:
	rm hello mylib.o text.o
