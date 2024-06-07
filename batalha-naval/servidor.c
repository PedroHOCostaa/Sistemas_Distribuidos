#include <stdio.h>
#include <stdlib.h>

#define NAVIO_PEQUENO_X 2
#define NAVIO_PEQUENO_Y 1
#define NAVIO_MEDIO_X 3
#define NAVIO_MEDIO_Y 1
#define NAVIO_GRANDE_X 4
#define NAVIO_GRANDE_Y 1
#define NAVIO_LARGO_X 3
#define NAVIO_LARGO_Y 2
#define TAMANHO_TABULEIRO_LINHAS 10
#define TAMANHO_TABULEIRO_COLUNAS 10

struct navio {
    int xAncora, yAncora, xTamanho, yTamanho;
    int orientacao;
    int tipo;
    int **parte;
};

struct tile {
    int* pedaco;
    int tipo;
};

struct tabuleiro {
    struct tile mapa[10][10];
};

int posiciona_navio(int xAncora, int yAncora, int orientacao, struct tabuleiro* tabuleiroAtual, int tipo, struct navio* novoNavio){
    novoNavio->xAncora = xAncora;
    novoNavio->yAncora = yAncora;
    novoNavio->orientacao = orientacao;
    novoNavio->tipo = tipo;
    if(tipo == 1){
        novoNavio->xTamanho = NAVIO_PEQUENO_X;
        novoNavio->yTamanho = NAVIO_PEQUENO_Y;
    } else if(tipo == 2){
        novoNavio->xTamanho = NAVIO_MEDIO_X;
        novoNavio->yTamanho = NAVIO_MEDIO_Y;
    } else if(tipo == 3){
        novoNavio->xTamanho = NAVIO_GRANDE_X;
        novoNavio->yTamanho = NAVIO_GRANDE_Y;
    } else if(tipo == 4){
        novoNavio->xTamanho = NAVIO_LARGO_X;
        novoNavio->yTamanho = NAVIO_LARGO_Y;
    }
    
    if(orientacao == 1)
        {
            int aux = novoNavio->xTamanho;
            novoNavio->xTamanho = novoNavio->yTamanho;
            novoNavio->yTamanho = aux;
        }

    if(xAncora < 0 || xAncora + novoNavio->xTamanho > 10)
        return 1; // Erro 1: Posição X inválida em alguma parte do navio, inicio menor que zero ou fim maior que 9

    if(yAncora < 0 || yAncora + novoNavio->yTamanho > 10)
        return 2; // Erro 2: Posição Y inválida em alguma parte do navio, inicio menor que zero ou fim maior que 9

    for(int i = 0; i < novoNavio->xTamanho; i++)
        for(int j = 0; j < novoNavio->yTamanho; j++)
            if(tabuleiroAtual->mapa[yAncora + i][xAncora + j].tipo != 0)
                return 3; // Erro 3: Posição inválida em alguma parte do navio, já existe um navio nessa posição
    
    novoNavio->parte = (int**) malloc(novoNavio->yTamanho * sizeof(int*));
    for(int i = 0; i < novoNavio->yTamanho; i++)
    {
        novoNavio->parte[i] = (int*) malloc(novoNavio->xTamanho * sizeof(int));
        for(int j = 0; j < novoNavio->xTamanho; j++)
            novoNavio->parte[i][j] = tipo;
    }
    for(int i = 0; i < novoNavio->xTamanho; i++)
        for(int j = 0; j < novoNavio->yTamanho; j++)
            {
                tabuleiroAtual->mapa[yAncora + i][xAncora + j].pedaco = &(novoNavio->parte[j][i]);
                tabuleiroAtual->mapa[yAncora + i][xAncora + j].tipo = tipo;
            }
    return 0; // A função deve retornar um int, então retornamos 0 para indicar sucesso
}



void inicializaTabuleiro(struct tabuleiro* tabuleiroAtual){
    for(int i = 0; i < 10; i++)
        for(int j = 0; j < 10; j++)
            {
                tabuleiroAtual->mapa[i][j].pedaco = NULL;
                tabuleiroAtual->mapa[i][j].tipo = 0;
            }
    printf("tabuleiro inicializado\n");
}

void liberaMemoriaBarco(struct navio* navioAtual){
    for(int i = 0; i < navioAtual->yTamanho; i++)
        free(navioAtual->parte[i]);
    free(navioAtual->parte);
}


void imprimeTabuleiro(struct tabuleiro* tabuleiroAtual){
    for(int i = 0; i < 10; i++)
        {
            for(int j = 0; j < 10; j++)
                printf("%d ", *(tabuleiroAtual->mapa[i][j].pedaco));
            printf("\n");
        }
}

int main(){
    printf("inicio\n");
    struct tabuleiro tabuleiroJogador1;
    inicializaTabuleiro(&tabuleiroJogador1);
    struct navio navioPequeno;
    imprimeTabuleiro(&tabuleiroJogador1);
    int erro = posiciona_navio(0, 0, 0, &tabuleiroJogador1, 1, &navioPequeno)!=0;
    if (erro != 0)
        printf("Erro ao posicionar navio pequeno codigo %d\n", erro);
    else
        printf("Navio pequeno posicionado com sucesso\n");
    imprimeTabuleiro(&tabuleiroJogador1);
    struct navio navioMedio;
    erro = posiciona_navio(0, 7, 0, &tabuleiroJogador1, 2, &navioMedio)!=0;
    if (erro != 0)
        printf("Erro ao posicionar navio medio codigo %d\n", erro);
    else
        printf("Navio medio posicionado com sucesso\n");
    
    imprimeTabuleiro(&tabuleiroJogador1);







    liberaMemoriaBarco(&navioPequeno);
}