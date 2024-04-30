
/*    Francesca  Pecorari  SM3201259     */

#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <stdint.h>
#include <omp.h>
#include "mandelbrot.h"

/*
    mandelbrotSet: 
        Questa funzione è responsabile di calcolare il set di Mandelbrot. 
        Prende come argomenti il raggio r, il massimo numero di iterazioni M, e un puntatore a una struttura ComplexGrid. 
        Utilizza OpenMP per eseguire il calcolo in parallelo. 
        Viene utilizzata la direttiva #pragma omp parallel for collapse(2) per parallelizzare i due cicli annidati che attraversano la griglia complessa.

*/

void mandelbrotSet(int r, int M, struct ComplexGrid *cgrid){
    
     createAndSaveComplexGrid(cgrid);
    // Calculate Mandelbrot iterations for each complex number in the grid
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < cgrid->nrows; i++) {
        for (int j = 0; j < cgrid->ncols; j++) {

            cgrid->grid[i][j] = calculateMandelbrotIterations(cgrid->grid[i][j], M, r);
    
        }
    }
    
}

/*

   calculateMandelbrotIterations: 
        Questa funzione calcola il numero di iterazioni richieste per determinare se un punto appartiene o meno al set di Mandelbrot. 
        Prende come argomenti un numero complesso c, il massimo numero di iterazioni M, e il raggio r. 
        Restituisce il numero di iterazioni effettuate prima che il valore assoluto del numero complesso superi il raggio specificato. 
        Se il punto è nel set di Mandelbrot, restituisce il valore massimo di iterazioni M.

*/

int calculateMandelbrotIterations(double complex c, int M, int r){
    double complex z = 0;
    int iter;
    int result;
    
    
    for (iter = 0; iter < M; iter++) {
        z = cpow(z,2) + c;

        // Controllo se il numero supera la soglia del raggio
        if (cabs(z) >= r) {
            return iter;
            
        }
    }
    return M;
}


/* 

    printMandelbrot: 
        Questa funzione stampa il set di Mandelbrot. 
        Utilizza OpenMP per eseguire il calcolo in parallelo. 
        Stampa il valore intero della parte reale dei numeri complessi per semplicità.

*/

void printMandelbrot(struct ComplexGrid cgrid) {
    // stampa il set di Mandelbrot
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < cgrid.nrows; i++) {
        for (int j = 0; j < cgrid.ncols; j++) {
            printf("%d\t", (int)creal(cgrid.grid[i][j]));  // stampa la parte intera per semplicità
        }
        printf("\n");
    }
}

/*
    createAndSaveComplexGrid: 
        Questa funzione crea e salva una griglia complessa. 
        Prende un puntatore a una struttura ComplexGrid come argomento 
        e utilizza OpenMP per parallelizzare il processo di creazione della griglia.

*/
void createAndSaveComplexGrid(struct ComplexGrid* cgrid) {
    // Calcolo lo step size per entrambi gli assi
    double x_step = (cgrid->realMax - cgrid->realMin) / (cgrid->ncols);
    double y_step = (cgrid->imagMax - cgrid->imagMin) / (cgrid->nrows);

    // alloco la memoria per l'array 2D
    cgrid->grid = (double complex**)malloc(cgrid->nrows * sizeof(double complex*));
    #pragma omp parallel for
    for (int i = 0; i < cgrid->nrows; i++) {
        cgrid->grid[i] = (double complex*)malloc(cgrid->ncols * sizeof(double complex));
    }

    // creo la griglia equispaziata di numeri complessi
    #pragma omp for collapse(2)
    for (int i = 0; i < cgrid->nrows; i++) {
        for (int j = 0; j < cgrid->ncols; j++) {
            // calcolo le parti reali e immaginarie
            double real = cgrid->realMin + j * x_step;
            double imag = cgrid->imagMin + i * y_step;

            // creo un numero complesso e lo inserisco nella griglia
            cgrid->grid[i][j] = real + imag * I;
    }
}

}

/*
    printComplexGrid: 
        Questa funzione stampa la griglia complessa salvata. 
        Utilizza OpenMP per eseguire il calcolo in parallelo. 
        Stampa sia la parte reale che la parte immaginaria dei numeri complessi.

*/

void printComplexGrid(struct ComplexGrid cgrid) {
    
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < cgrid.nrows; i++) {
        for (int j = 0; j < cgrid.ncols; j++) {
            printf("%f + %fi\t", creal(cgrid.grid[i][j]), cimag(cgrid.grid[i][j]));
        }
        printf("\n");
    }
}

/*
    freeComplexGrid: 
        Questa funzione libera la memoria allocata per la griglia complessa.

*/
void freeComplexGrid(struct ComplexGrid* cgrid) {
    #pragma omp parallel for
    for (int i = 0; i < cgrid->nrows; i++) {
        free(cgrid->grid[i]);
    }
    free(cgrid->grid);
}

/*
    calculateColourGrid: 
        Questa funzione assegna un colore a ciascun punto della griglia 
        in base al numero di iterazioni richieste per determinare 
        se il punto appartiene al set di Mandelbrot. 
        Utilizza OpenMP per eseguire il calcolo in parallelo. 
        Se il punto è nel set di Mandelbrot, viene assegnato il colore bianco. 
        Altrimenti, il colore viene calcolato in base al numero di iterazioni.
        
*/
void calculateColourGrid(struct ComplexGrid *cgrid, int M) {
    // scelogo un colore per ogni posizione della griglia
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < cgrid->nrows; i++) {
        for (int j = 0; j < cgrid->ncols; j++) {
            if (cgrid->grid[i][j] == M) {
                // il punto è nell' insieme di Mandelbrot, assegno il colore bianco
                cgrid->grid[i][j] = 255.0;
            } 
            else {
                // il punto è fuori dall' insieme, calcolo il colore in base alle iterazioni
                 double colorValue = 255 * (log(cgrid->grid[i][j]) / log(M));
                
                cgrid->grid[i][j] = colorValue;

            }
        }
    }
}


