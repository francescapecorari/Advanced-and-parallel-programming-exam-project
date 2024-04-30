CC = gcc
CFLAGS = -O3 

all: main

main: main.o mandelbrot.o pgm.o
	${CC} -Xpreprocessor -fopenmp ${CFLAGS} -o $@ $^ -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp

main.o: main.c mandelbrot.h pgm.h
	${CC} -Xpreprocessor -fopenmp ${CFLAGS} -c $< -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp

mandelbrot.o: mandelbrot.c mandelbrot.h
	${CC} -Xpreprocessor -fopenmp ${CFLAGS} -c $< -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp

pgm.o: pgm.c pgm.h
	${CC} -Xpreprocessor -fopenmp ${CFLAGS} -c $< -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp


.PHONY: clean

clean:
	rm -f *.o
