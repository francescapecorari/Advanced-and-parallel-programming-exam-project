CC = gcc
CFLAGS = -O3 
OMPPATH = -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp

all: main

main: main.o mandelbrot.o pgm.o
	${CC} -Xpreprocessor -fopenmp ${CFLAGS} -o $@ $^ ${OMPPATH}

main.o: main.c mandelbrot.h pgm.h
	${CC} -Xpreprocessor -fopenmp ${CFLAGS} -c $< ${OMPPATH}

mandelbrot.o: mandelbrot.c mandelbrot.h
	${CC} -Xpreprocessor -fopenmp ${CFLAGS} -c $< ${OMPPATH}

pgm.o: pgm.c pgm.h
	${CC} -Xpreprocessor -fopenmp ${CFLAGS} -c $< ${OMPPATH}


.PHONY: clean

clean:
	rm -f *.o
