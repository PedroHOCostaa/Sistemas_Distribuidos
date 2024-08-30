#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include "estruturas.h"

#define PORT "8080"
#define HOST "127.0.0.1"

void insereNavioJogador(struct mapa* mapaJogador, struct navio* novoNavio)
{
    int ancoraColuna;
    int ancoraLinha;
    while (1)
    {
        printf("Digite a linha em que a âncora será posicionada: ");
        scanf("%d", &ancoraColuna);
        printf("Digite a coluna em que a âncora será posicionada: ");
        scanf("%d", &ancoraLinha);
        if(insereNavio(mapaJogador, novoNavio, ancoraColuna, ancoraLinha) == 0)
        {
            break;
        }
    }
}

int realizarTiroJogador(struct mapa* mapaAdversario)
{
    int colunaAlvo, linhaAlvo;
    printf("Digite a linha em que o tiro será disparado: ");
    scanf("%d", &colunaAlvo);
    printf("Digite a coluna em que o tiro será disparado: ");
    scanf("%d", &linhaAlvo);
    int resultado = realizarTiro(mapaAdversario, colunaAlvo, linhaAlvo);
    
    return resultado;
}


void jogo()
{

    struct mapa* mapaJogadorUm = (struct mapa*)malloc(sizeof(struct mapa));;
    inicializaMapa(mapaJogadorUm);
    struct mapa* mapaJogadorDois = (struct mapa*)malloc(sizeof(struct mapa));;
    inicializaMapa(mapaJogadorDois);
    int tipoJogo, qtdNavios[4], qtdTiros;
    printf("Digite o tipo do jogo\n");
    if(tipoJogo == 1)
    {
        qtdNavios[0] = 1;
        qtdNavios[1] = 1;
        qtdNavios[2] = 1;
        qtdNavios[3] = 1;
        qtdTiros = 1;
    }
    if(tipoJogo == 1)
    {
        qtdNavios[0] = 2;
        qtdNavios[1] = 2;
        qtdNavios[2] = 1;
        qtdNavios[3] = 1;
        qtdTiros = 3;
    }
    

    int tipo, orientacao, ancoraColuna, ancoraLinha;
    printf("Jogador 1\n");
    while(1)
    {
        printf("Escolha o Tipo do navio: \n");
        scanf("%d", &tipo);
    }

}

int main()
{
    pthread_t thread_id;
    if (pthread_create(&thread_id, NULL, jogo, NULL) != 0) {
        fprintf(stderr, "Falha ao criar thread.\n");
        return 1;
    }




    pthread_join(thread_id, NULL);
    return 0;
}