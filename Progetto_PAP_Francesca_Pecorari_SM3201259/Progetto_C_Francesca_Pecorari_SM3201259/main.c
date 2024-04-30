
/*    Francesca  Pecorari  SM3201259    */

#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h> 
#include <omp.h>
#include "mandelbrot.h"
#include "pgm.h"

int main(int argc, char* argv[])
{
      /* Parsing degli argomenti da linea di comando */
      if (argc != 4) {
        printf("Usage:   %s <out.pbm> <M> <nrows>\n", argv[0]);
        printf("Example: %s image.pbm  1000 100\n", argv[0]);
        exit(EXIT_FAILURE);
     }

      /* Definizione del dominio */
      double realMin = -2;
      double realMax = 1;
      double imagMin = -1;
      double imagMax = 1;

      /* L'altezza dell'immagine ci è fornita e calcoliamo la larghezza */
      const int nrows = atoi(argv[3]); // atoi trasforma l'argomento in un intero
      const int ncols = 1.5 * nrows;

      /* Numero massimo di iterazioni */
      const int M = atoi(argv[2]);

      /* Nome del file di output */
      const char* filename = argv[1];

      /* Raggio di fuga */
      int r = 2;


    /* Creo e salvo una griglia di complessi con i valori su definiti */
    struct ComplexGrid myComplexGrid = {nrows, ncols, realMin, realMax, imagMin, imagMax, NULL};

    createAndSaveComplexGrid(&myComplexGrid);
 
    /* Calcolo il set di Mandelbrot sulla griglia appena creata */
    mandelbrotSet(r, M, &myComplexGrid);

    /* Chiamo la funzione per calcolare la griglia con la scala di colori richiesta */
    calculateColourGrid(&myComplexGrid, M);

    /* Alloco la memoria per l' immagine */
    unsigned char *imageData = (unsigned char*)malloc(nrows * ncols * sizeof(unsigned char));
    if (imageData == NULL) {
        perror("Memory allocation failed");
        exit(EXIT_FAILURE);
    }
    
    /* Converto la griglia complessa in una immagine in scala di grigi */
    for (int i = 0; i < nrows; i++) {
        for (int j = 0; j < ncols; j++) {
            // Normalizzo i valori dei colori per renderli appartenenti al range [0, 255]
            imageData[i * ncols + j] = (unsigned char)creal(myComplexGrid.grid[i][j]);
        }
    }


    /* Salvo l'immagine in formato PGM */
    savePGM(filename, "pgm", imageData, nrows, ncols);
    
    /* Libero la memoria utilizzata */
    free(imageData);
    freeComplexGrid(&myComplexGrid);

    return 0;

}