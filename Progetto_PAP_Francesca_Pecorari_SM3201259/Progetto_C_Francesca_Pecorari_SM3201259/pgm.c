
/*    Francesca  Pecorari  SM3201259    */

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h> 
#include <omp.h>
#include <sys/stat.h>
#include "pgm.h"
#include "mandelbrot.h"



/*

    savePGM: 
        Questa funzione prende in input:
        - un nome file filename 
        - un'estensione extension
        - un puntatore a una mappa di pixel map
        -  il numero di righe nrows 
        - il numero di colonne ncols dell'immagine. 
        Apre un file in modalità scrittura, scrive gli header PGM 
        (tipo di immagine, dimensioni e profondità di colore) 
        e quindi scrive i pixel dell'immagine nel file. 
        Infine, chiude il file.

*/

void savePGM(const char *filename, const char *extension, unsigned char *map, int nrows, int ncols) {
  
    // Dichiaro un array di caratteri per contenere il nome completo del file
    char fullFilename[100];
  
    // Creo il nome completo del file concatenando il nome e l'estensione
    snprintf(fullFilename, sizeof(fullFilename), "%s.%s", filename, extension);

    // Apro il file in modalità di creazione, scrittura e troncamento
    // con i permessi di lettura e scrittura per l'utente corrente
    int file;
    file = open(fullFilename, O_CREAT | O_WRONLY | O_TRUNC, S_IRUSR | S_IWUSR);
    if (file == -1) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }
    // Scrittura dell'intestazione del file PGM
    dprintf(file, "P5\n");
    // Scrittura delle dimensioni dell'immagine (numero di colonne e righe)
    dprintf(file, "%d %d\n", ncols, nrows);
    // Scrittura del valore massimo di intensità dei pixel (255 in questo caso)
    dprintf(file, "255\n");

    // Scrittura dei dati dell'immagine nel file
    write(file, map, nrows * ncols);

    close(file);
}


/*

    openPGM:
        Questa funzione prende in input un percorso path per un file PGM 
        e un puntatore a una struttura pgm_ptr che rappresenta l'immagine. 
        Apre il file in modalità lettura/scrittura, ottiene le dimensioni dell'immagine dal file 
        e mappa l'area di memoria contenente i dati dell'immagine. 
        Restituisce 0 in caso di successo e un codice di errore in caso di fallimento.

*/

int openPGM(const char *path, pgm_ptr img) {
    
    // Apro il file specificato in modalità lettura e scrittura
    img->fd = open(path, O_RDWR);

    // Controllo se l'apertura del file ha avuto successo
    if (img->fd == -1) {
        return -1;
    }

    // Ottengo le informazioni sul file
    struct stat sbuf;
    fstat(img->fd, &sbuf);

    // Calcolo il numero di righe dell'immagine dividendo la dimensione totale per il numero di colonne
    img->nrows = sbuf.st_size / img->ncols;
    
    // Mappo il file in memoria
    img->data = mmap((void *)0, sbuf.st_size, PROT_READ | PROT_WRITE, MAP_SHARED, img->fd, 0);
    
    // Controllo se la mappatura è riuscita
    if (img->data == MAP_FAILED) {
        close(img->fd);
        return -2;
    }

    return 0;
}

/* 
    emptyPGM: 
        Questa funzione crea un nuovo file PGM vuoto con le dimensioni specificate 
        e lo prepara per l'utilizzo. 
        Scrive gli header PGM nel file e poi imposta la dimensione del file per 
        ospitare l'intero set di dati dell'immagine. 
        Infine, chiama openPGM per aprire l'immagine e salvarla in memoria. 
        Restituisce 0 in caso di successo e -1 in caso di fallimento.

*/

int emptyPGM(const char *path, pgm_ptr img, int nrows, int ncols) {
    // Apro il file specificato in modalità di scrittura, 
    // creando il file se non esiste e troncandolo se esiste già
    FILE *fd = fopen(path, "w+");
    
    // Controllo se l'apertura del file ha avuto successo
    if (fd == NULL) {
        return -1;
    }

    // Scrivo gli header PGM nel file
    int written = fprintf(fd, "P5\n%d %d\n255\n", ncols, nrows);

        // Controllo se la scrittura degli header ha avuto successo
    if (written < 0) {
        perror("Error writing headers"); // Stampo un messaggio di errore con la causa dell'errore
        fclose(fd); // Chiudo il file
        return -1; // Restituisco un codice di errore (-1) se la scrittura fallisce
    }


    // Tronco il file alla dimensione corretta
    if (ftruncate(fileno(fd), written + nrows * ncols) != 0) {
        perror("Error truncating file");
        fclose(fd);
        return -1;
    }

  fclose(fd);

  return openPGM(path, img);
}

/* 

    pixelAtPGM: 
        Questa funzione restituisce un puntatore al valore di un pixel specificato 
        dalle coordinate (x, y) nell'immagine PGM rappresentata dalla struttura pgm_ptr. 
        Controlla se le coordinate sono all'interno delle dimensioni dell'immagine 
        e restituisce il puntatore al pixel corrispondente.

*/

char *pixelAtPGM(pgm_ptr img, int x, int y) {

  // se il puntatore all'immagine è nullo ritorna NULL
  if (img == NULL) {
    return NULL;
  }

  if (x < 0 || x >= img->ncols) {
    return NULL;
  }

  if (y < 0 || y >= img->nrows) {
    return NULL;
  }

  return &img->data[y * img->ncols + x];
}

/*

    closePGM: 
        Questa funzione chiude un file PGM precedentemente aperto. 
        Utilizza munmap per liberare la memoria mappata e close per chiudere il file.

*/

int closePGM(pgm_ptr img) {
  if (img == NULL) {
    return -1;
  }

  munmap(img->data, img->nrows * img->ncols);
  close(img->fd);

  return 0;
}

