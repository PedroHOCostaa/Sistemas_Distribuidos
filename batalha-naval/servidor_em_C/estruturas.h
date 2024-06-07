#include <stdio.h>
#include <stdlib.h>

struct navio;
struct celula;
struct mapa;
struct no;

void inserirFinalLista(struct no* lista, struct navio* novonavio);
int inicializaNavio(struct navio* novoNavio, int tipo, int orientacao);
int inicializaMapa(struct mapa* novoMapa);
int insereBarco(struct mapa* meuMapa, struct navio* novoNavio, int ancoraColuna, int ancoraLinha);



struct no {
    struct navio* navio;
    struct no* prox;
};

struct navio {
    int ancoraColuna, ancoraLinha, tamanhoColuna, tamanhoLinha;         // exemplo1: para um barco {{1, 1}} possui tamanhoColuna 1 e tamanhoLinha 2 e se ancora estiver em {0,0} 
    int orientacao;                                                     // o barco estará em {0,0} e {0,1}
    int tipo;                                                           // exemplo2: para um barco {{1,1,1},{1,1,1}} possui tamanhoColuna 2 e tamanhoLinha 3 e se ancora estiver em {0,0}
    int** estrutura;                                                    // o barco estará em {0,0}, {0,1}, {0,2}, {1,0}, {1,1}, {1,2}
};

void inserirFinalLista(struct no* lista, struct navio* novonavio)
{
    if(lista->prox == NULL)                                             // Verifica se é o ultimo da lista
    {
        lista->prox = (struct no*)malloc(sizeof(struct no));            // Aloca memória para o novo nó
        lista = lista->prox;
        lista->navio = novonavio;
        lista->prox = NULL;
    }else
        inserirFinalLista(lista->prox, novonavio);                          // Chama a função recursivamente para o próximo nó
}

int inicializaNavio(struct navio* novoNavio, int tipo, int orientacao)
{
    novoNavio->tipo = tipo;
    if(tipo == 1)
    {
        novoNavio->tamanhoColuna = 1;
        novoNavio->tamanhoLinha = 2;
    } 
    else if(tipo == 2)
    {
        novoNavio->tamanhoColuna = 1;
        novoNavio->tamanhoLinha = 3;
    } 
    else if(tipo == 3)
    {
        novoNavio->tamanhoColuna = 1;
        novoNavio->tamanhoLinha = 4;
    } 
    else if(tipo == 4)
    {
        novoNavio->tamanhoColuna = 2;
        novoNavio->tamanhoLinha = 3;
    }
    if (orientacao == 1)                            // Se orientacao vale 1 então gira o navio      
    {
        int aux = novoNavio->tamanhoColuna;
        novoNavio->tamanhoColuna = novoNavio->tamanhoLinha;
        novoNavio->tamanhoLinha = aux;
    }
    novoNavio->estrutura = (int**)calloc(novoNavio->tamanhoColuna, sizeof(int*));               // Aloca memória para a estrutura do navio, vetor das linhas
    for (int i = 0; i < novoNavio->tamanhoColuna; i++)
    {
        novoNavio->estrutura[i] = (int*)calloc(novoNavio->tamanhoLinha, sizeof(int));           // Aloca memória para a estrutura do navio, vetor das partes
        for (int j = 0; j < novoNavio->tamanhoLinha; j++)
        {
            novoNavio->estrutura[i][j] = 1;                                                     // Estrutura do navio, 1 se interira 0 se atingida     
        }
    }
    return 0;
}

struct celula {
    int indicador;
    struct navio* superficie;
};

struct mapa {
    struct no* listaBarcos;
    int numBarcos;
    struct celula tabuleiro[10][10];
};

int inicializaMapa(struct mapa* novoMapa)
{
    novoMapa->numBarcos = 0;
    for(int i = 0; i < 10; i++)
    {
        for(int j = 0; j < 10; j++)
        {
            novoMapa->tabuleiro[i][j].indicador = 0;
            novoMapa->tabuleiro[i][j].superficie = NULL;
        }
    }
}

int insereBarco(struct mapa* meuMapa, struct navio* novoNavio, int ancoraColuna, int ancoraLinha)
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
    if(meuMapa->numBarcos == 0)
        {
            meuMapa->listaBarcos = (struct no*)malloc(sizeof(struct no));
            meuMapa->listaBarcos->navio = novoNavio;
            meuMapa->listaBarcos->prox = NULL;
        }else{
            inserirFinalLista(meuMapa->listaBarcos, novoNavio);
        }
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