#include <stdio.h>
#include <stdlib.h>
#include "estruturas.h"

void inserirFinalLista(struct no* lista, struct navio* novonavio)
{
    if(lista->prox == NULL)                                             // Verifica se é o ultimo da lista
    {
        lista->prox = (struct no*)malloc(sizeof(struct no));            // Aloca memória para o novo nó
        lista = lista->prox;
        lista->navio = novonavio;
        lista->prox = NULL;
    }else
        inserirFinalLista(lista->prox, novonavio);                      // Chama a função recursivamente para o próximo nó
}


/// Recebe um ponteiro de navio, um inteiro para determinar o tamanho do navio, e um inteiro para determinar a orientação do navio
/// Carrega as informações do navio depedendo do tipo e da orientação, e aloca memória para a estrutura do navio que servirá para determinar se o navio foi afundado
int inicializaNavio(struct navio* novoNavio, int tipo, int orientacao)
{
    novoNavio->tipo = tipo;
    novoNavio->orientacao = orientacao;
    if(tipo == 1)                                                       //Navio {{0, 0}}
    {
        novoNavio->tamanhoColuna = 1;
        novoNavio->tamanhoLinha = 2;
    } 
    else if(tipo == 2)                                                  //Navio {{0, 0, 0}}
    {
        novoNavio->tamanhoColuna = 1;
        novoNavio->tamanhoLinha = 3;
    } 
    else if(tipo == 3)                                                  //Navio {{0, 0, 0, 0}}
    {
        novoNavio->tamanhoColuna = 1;
        novoNavio->tamanhoLinha = 4;
    } 
    else if(tipo == 4)                                                  //Navio {{0, 0, 0},
    {                                                                   //       {0, 0, 0}}
        novoNavio->tamanhoColuna = 2;
        novoNavio->tamanhoLinha = 3;
    }
    if (orientacao == 1)                                                // Se orientacao vale 1 então gira o navio      
    {
        int aux = novoNavio->tamanhoColuna;
        novoNavio->tamanhoColuna = novoNavio->tamanhoLinha;
        novoNavio->tamanhoLinha = aux;
    }
    novoNavio->estrutura = (int**)calloc(novoNavio->tamanhoColuna, sizeof(int*));       // Aloca memória para a estrutura do navio, vetor das linhas
    for (int i = 0; i < novoNavio->tamanhoColuna; i++)
    {
        novoNavio->estrutura[i] = (int*)calloc(novoNavio->tamanhoLinha, sizeof(int));   // Aloca memória para a estrutura do navio, vetor das partes
    }
    return 0;
}


/// Recebe um ponteiro de mapa, seta o numero de barcos para 0 e inicializa todas as células do tabuleiro com indicador 0 e superficie NULL 
/// e a matriz mapa do adversario com todos os tiles valendo 0
void inicializaMapa(struct mapa* novoMapa)
{
    novoMapa->numBarcos = 0;
    for(int i = 0; i < 10; i++)
    {
        for(int j = 0; j < 10; j++)
        {
            novoMapa->tabuleiro[i][j].indicador = 0;
            novoMapa->tabuleiro[i][j].superficie = NULL;
            novoMapa->mapaAdversario[i][j] = 'O';
        }
    }
}


/// @brief                  Verifica se a posição que o jogador deseja inserir o navio é válida e se não há outro navio nessa posição, se é possivel atualiza o valor de ancoraColuna e ancoraLinha do navio, adiciona o navio na fila do mapa, e nas celulas em que ele sera posicionado atualizamos o indicador para 1 e a superficie aponta para o navio
/// @param meuMapa          Ponteiro para o mapa do jogador que irá inserir o navio 
/// @param novoNavio        Ponteiro para o navio que será inserido
/// @param ancoraColuna     Coluna onde o navio será ancorado
/// @param ancoraLinha      Linha onde o navio será ancorado
/// @return                 Retorna 0 se o navio foi inserido com sucesso, 1 se a posição da coluna é inválida, 2 se a posição da linha é inválida, 3 se a posição já está ocupada por outro navio
int insereNavio(struct mapa* meuMapa, struct navio* novoNavio, int ancoraColuna, int ancoraLinha)
{
    if(ancoraColuna < 0 || ancoraColuna + novoNavio->tamanhoColuna > 10)
        return 1;           // Erro 1: Posição Coluna inválida em alguma parte do navio, inicio menor que zero ou fim maior que 9

    if(ancoraLinha < 0 || ancoraLinha + novoNavio->tamanhoLinha > 10)
        return 2;           // Erro 2: Posição Linha  inválida em alguma parte do navio, inicio menor que zero ou fim maior que 9

    for(int i = 0; i < novoNavio->tamanhoColuna; i++)
    {
        for(int j = 0; j < novoNavio->tamanhoLinha; j++)
        {
            if(meuMapa->tabuleiro[ancoraColuna + i][ancoraLinha + j].indicador != 0)
                return 3;   // Erro 3: Posição inválida em alguma parte do navio, já existe um navio nessa posição
        }
    }

    novoNavio->ancoraColuna = ancoraColuna; 
    novoNavio->ancoraLinha = ancoraLinha;


    // adicona o novo nó ao inicio da lista e incrementa o numero de barcos
    struct no* novoNo = (struct no*)malloc(sizeof(struct no));
    novoNo->navio = novoNavio;
    novoNo->prox = meuMapa->listaBarcos;
    meuMapa->listaBarcos = novoNo;
    meuMapa->numBarcos++;

    for(int i = 0; i < novoNavio->tamanhoColuna; i++)
    {
        for(int j = 0; j < novoNavio->tamanhoLinha; j++)
        {
            meuMapa->tabuleiro[ancoraColuna + i][ancoraLinha + j].indicador = 1;
            meuMapa->tabuleiro[ancoraColuna + i][ancoraLinha + j].superficie = novoNavio;
        }
    }

    return 0;
}

void acertaNavio(struct navio* navio, int coluna, int linha)
{
    navio->estrutura[coluna - navio->ancoraColuna][linha - navio->ancoraLinha] = 1;
}

int atira(struct mapa* meuMapa, int coluna, int linha)
{
    if(meuMapa->tabuleiro[coluna][linha].indicador == 1)
    {
        struct navio* navioAlvo = meuMapa->tabuleiro[coluna][linha].superficie;
        acertaNavio(navioAlvo, coluna, linha);
        meuMapa->mapaAdversario[coluna][linha] = 'N';
        return 1;           // 1: Tiro em um navio
    }
    meuMapa->mapaAdversario[coluna][linha] = 'A';
    return 0;               // 0: Tiro na água
}

int verificarEstrtura(struct navio* navio)
{
    for(int i = 0; i < navio->tamanhoColuna; i++)
    {

        for(int j = 0; j < navio->tamanhoLinha; j++)
        {
            int estado_da_estrutura = navio->estrutura[i][j];
            if(estado_da_estrutura == 0)
                return 0;   // 0: Navio não destruido por completo
        }
    }
    return 1;               // 1: Navio foi destruido por completo
}

void pintaestrutura(struct mapa* meuMapa, struct navio* navio)
{
    for(int i = 0; i < navio->tamanhoColuna; i++)
    {
        for(int j = 0; j < navio->tamanhoLinha; j++)
        {
            meuMapa->mapaAdversario[navio->ancoraColuna + i][navio->ancoraLinha + j] = '0' + navio->tipo;
        }
    }
}

int realizarTiro(struct mapa* meuMapa, int coluna, int linha)
{
    
    if(atira(meuMapa, coluna, linha))
    {
        struct navio* navioAlvo = meuMapa->tabuleiro[coluna][linha].superficie;
    
        if(verificarEstrtura(navioAlvo) == 1)
        {
            pintaestrutura(meuMapa, navioAlvo);
            return 2;       // 2: Tipo acertado e navio destruido
        }    
        return 1;           // 1: Tiro acertado mas navio permanece 
    }else
    {                           
        return 0;           // 0: Tiro na água
    }
        
}

void imprimirMeuMapa(struct mapa* meuMapa)
{
    struct celula* celulaAtual;
    printf("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n");
    printf("\t\t\t\tMeu Mapa\n\n");
    for(int i = 0; i < 10; i++)

    {
        for(int j = 0; j < 10; j++)
        {
            celulaAtual = &(meuMapa->tabuleiro[i][j]);
            
            if(celulaAtual->indicador == 0)
            {
                printf("0\t");
            }else
            {
                printf("%d%d\t", celulaAtual->superficie->tipo, celulaAtual->superficie->estrutura[i - celulaAtual->superficie->ancoraColuna][j - celulaAtual->superficie->ancoraLinha]);    
            }
        }
        printf("\n\n");
    }
    printf("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n");

}

void imprimirMapaAdversario(struct mapa* meuMapa)
{
    printf("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n");
    printf("\t\t\t\tMapa do Adversário\n\n");
    for(int i = 0; i < 10; i++)
    {
        for(int j = 0; j < 10; j++)
        {
            printf("%c\t", meuMapa->mapaAdversario[i][j]);
        }
        printf("\n\n");
    }
    printf("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n");

}

void imprimeNavio(struct navio* navio)
{
    for(int i = 0; i < navio->tamanhoColuna; i++)
    {
        for(int j = 0; j < navio->tamanhoLinha; j++)
        {
            printf("%d\t", navio->estrutura[i][j]);
        }
        printf("\n\n");
    }
}
