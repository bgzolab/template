GCC=gcc
CFLAG=-c
OFLAG=-o
EXE=db
OBJ=db.o

# InputBuffer.o

all:${EXE} 
${EXE}:${OBJ}
	${GCC} ${OFLAG} $@ $^

%.o:%.cpp
	${GCC} ${CFLAG} $^

clean:
	rm *.o
	rm ${EXE}
