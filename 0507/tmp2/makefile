# GCC=g++
# CFLAG=-c
# OFLAG=-o

# EXE=anmiMain

# ${EXE}:${OBJ}
# 	${GCC} ${OFLAG} $@ $^
# %.o:%.cpp
# 	${GCC} ${CFLAG} $^
# clean:
# 	rm *.o

GCC=g++
CFLAG=-c
OFLAG=-o
EXE=narcMain
OBJ=narcMain.o threadguard.o narc.o
${EXE}:${OBJ}
	${GCC} ${OFLAG} $@ $^ -pthread
%.o:%.cpp
	${GCC} ${CFLAG} $^
clean:
	rm *.o
	rm ${EXE}
