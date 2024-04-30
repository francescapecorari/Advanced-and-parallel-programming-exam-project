
/*    Francesca  Pecorari  SM3201259    */

#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <stdint.h>
#include <omp.h>

#ifndef _MANDELBROT_H
#define _MANDELBROT_H

/*

    ComplexGrid: 
        Questa struttura rappresenta una griglia di numeri complessi 
        utilizzata, in questo caso, per rappresentare il dominio nello spazio complesso 
        su cui viene calcolato il set di Mandelbrot. 
        Contiene il numero di righe (nrows) e colonne (ncols) della griglia, 
        insieme ai valori minimi e massimi della parte reale (realMin, realMax) 
        e della parte immaginaria (imagMin, imagMax) del dominio. 
        La griglia stessa è rappresentata come un puntatore a un array bidimensionale di numeri complessi.

*/

struct ComplexGrid {
    int nrows, ncols;   // Dimensions of the grid
    double realMin, realMax;  // Real part range
    double imagMin, imagMax;  // Imaginary part range
    double complex** grid;  // Pointer to the 2D array of complex numbers
};

// Funzione che crea e salva una griglia complessa.
void createAndSaveComplexGrid(struct ComplexGrid* cgrid);

// Funzione che stampa una griglia complessa
void printComplexGrid(struct ComplexGrid cgrid);

// Funzione che libera la memoria allocata per una griglia complessa
void freeComplexGrid(struct ComplexGrid* cgrid);

// Funzione che calcola il set di Mandelbrot
void mandelbrotSet(int r, int M, struct ComplexGrid *cgrid);

// Funzione che calcola il numero di iterazioni necessarie per determinare l'appartenenza di un punto al set di Mandelbrot
int calculateMandelbrotIterations(double complex c, int M, int r);

// Funzione che stampa il set di Mandelbrot
void printMandelbrot(struct ComplexGrid cgrid);

// Funzione che calcola la griglia dei colori basata sulle iterazioni di Mandelbrot
void calculateColourGrid(struct ComplexGrid *cgrid, int M);

#endif

