GCC=g++
CFLAG=-c
OFLAG=-o
EXE=anmiMain
OBJ=anmiMain.o threadguard.o amic.o
${EXE}:${OBJ}
	${GCC} ${OFLAG} $@ $^ -pthread
%.o:%.cpp
	${GCC} ${CFLAG} $^
clean:
	rm *.o
	rm ${EXE}
