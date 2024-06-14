#include <stdio.h>
#include <stdlib.h>
#include "estruturas.h"

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

int main()
{
    struct mapa* mapaJogadorUm = (struct mapa*)malloc(sizeof(struct mapa));;
    inicializaMapa(mapaJogadorUm);
    struct mapa* mapaJogadorDois = (struct mapa*)malloc(sizeof(struct mapa));;
    inicializaMapa(mapaJogadorDois);
    int tipo;
    int orientacao;

    for(int i = 0; i < 1; i++)
    {
        struct navio* novoNavioJogadorUm = (struct navio*)malloc(sizeof(struct navio));
        printf("Digite o tipo do navio: ");
        scanf("%d", &tipo);
        printf("Digite a orientação do navio: ");
        scanf("%d", &orientacao);
        inicializaNavio(novoNavioJogadorUm, tipo, orientacao);

        insereNavioJogador(mapaJogadorUm, novoNavioJogadorUm);
        imprimirMeuMapa(mapaJogadorUm);
    }
    
    for(int i = 0; i < 1; i++)
    {
        struct navio* novoNavioJogadorDois = (struct navio*)malloc(sizeof(struct navio));
        printf("Digite o tipo do navio: ");
        scanf("%d", &tipo);
        printf("Digite a orientação do navio: ");
        scanf("%d", &orientacao);
        inicializaNavio(novoNavioJogadorDois, tipo, orientacao);

        insereNavioJogador(mapaJogadorDois, novoNavioJogadorDois);
        imprimirMeuMapa(mapaJogadorDois);

    }
    while(1)
    {
        printf("\t\tTurno do jogador 1!!!!!!!!\n\n");
        imprimirMeuMapa(mapaJogadorUm);
        realizarTiroJogador(mapaJogadorDois);
        imprimirMapaAdversario(mapaJogadorDois);
        printf("\t\tTurno do jogador 2!!!!!!!!\n\n");
        imprimirMeuMapa(mapaJogadorDois);
        realizarTiroJogador(mapaJogadorUm);
        imprimirMapaAdversario(mapaJogadorUm);

    }
}