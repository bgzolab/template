GCC=g++
CFLAG=-c
OFLAG=-o
EXE=sibpipe
OBJ=sibpipe.o server.o client.o mysig.o
${EXE}:${OBJ}
	${GCC} ${OFLAG} $@ $^
%.o:%.cpp
	${GCC} ${CFLAG} -fPIE $^
clean:
	rm *.o
	rm ${EXE}
