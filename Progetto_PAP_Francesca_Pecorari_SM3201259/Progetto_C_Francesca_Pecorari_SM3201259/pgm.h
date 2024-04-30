
/*    Francesca  Pecorari  SM3201259    */

#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/mman.h>
#include "mandelbrot.h"


#ifndef _PGM_H
#define _PGM_H


/*

    pgm_image: 
        Questa struttura rappresenta un'immagine nel formato PGM (Portable Gray Map). 
        Contiene le dimensioni dell'immagine (ncols per il numero di colonne e nrows per il numero di righe), 
        il file descriptor (fd) per il file associato all'immagine 
        e un puntatore ai dati dell'immagine (data).

*/

struct _pgm_image {
    int ncols;
    int nrows;
    int fd;      
    char *data;
};

/*

    pgm e pgm_ptr: 
        Vengono definiti due tipi, pgm e pgm_ptr, entrambi equivalenti a struct _pgm_image. 
        pgm è un alias per struct _pgm_image
        pgm_ptr è un puntatore a una struttura pgm_image

*/

typedef struct _pgm_image pgm;
typedef struct _pgm_image * pgm_ptr;

// Funzione per salvare un'immagine nel formato PGM
void savePGM(const char *filename, const char *extension, unsigned char *map, int nrows, int ncols);

// Funzione per aprire un'immagine nel formato PGM
int openPGM(const char *path, pgm_ptr img);

// funzione per creare un'immagine PGM vuota
int emptyPGM(const char *path, pgm_ptr img, int nrows, int ncols);

//  Funzione per ottenere il valore di un pixel in un'immagine PGM
char *pixelAtPGM(pgm_ptr img, int x, int y);

// Funzione per chiudere un'immagine PGM precedentemente aperta
int closePGM(pgm_ptr img);

#endif