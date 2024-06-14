#include <stdio.h>
#include <stdlib.h>

struct navio;
struct celula;
struct mapa;
struct no;

void inserirFinalLista(struct no* lista, struct navio* novonavio);
int inicializaNavio(struct navio* novoNavio, int tipo, int orientacao);
void inicializaMapa(struct mapa* novoMapa);
int insereNavio(struct mapa* meuMapa, struct navio* novoNavio, int ancoraColuna, int ancoraLinha);
int atira(struct mapa* meuMapa, int coluna, int linha);
void acertaNavio(struct navio* navio, int coluna, int linha);
int realizarTiro(struct mapa* meuMapa, int coluna, int linha);
int verificarEstrtura(struct navio* navio);
void pintaestrutura(struct mapa* meuMapa,struct navio* navio);
void imprimirMeuMapa(struct mapa* meuMapa);
void imprimirMapaAdversario(struct mapa* meuMapa);
void imprimeNavio(struct navio* navio);

/// @brief // Estrutura de lista encadeada
struct no {
    struct navio* navio;
    struct no* prox;
};

/// @brief // Estrutura de um navio
struct navio {
    int ancoraColuna, ancoraLinha, tamanhoColuna, tamanhoLinha;         // exemplo1: para um barco {{1, 1}} possui tamanhoColuna 1 e tamanhoLinha 2 e se ancora estiver em {0,0} 
    int orientacao;                                                     // o barco estará em {0,0} e {0,1}
    int tipo;                                                           // exemplo2: para um barco {{1,1,1},{1,1,1}} possui tamanhoColuna 2 e tamanhoLinha 3 e se ancora estiver em {0,0}
    int** estrutura;                                                    // o barco estará em {0,0}, {0,1}, {0,2}, {1,0}, {1,1}, {1,2}
};

struct celula {
    int indicador;
    struct navio* superficie;
};

struct mapa {
    struct no* listaBarcos;
    int numBarcos;
    struct celula tabuleiro[10][10];
    char mapaAdversario[10][10];
};
