# Definir o compilador
CC = gcc

# Flags do compilador
CFLAGS = -Wall -Wextra -pedantic -std=c11

# Nome do executável final
TARGET = servidor_processamento

# Arquivos objeto
OBJS = servidor_processamento.o estruturas.o

# Regra padrão
all: $(TARGET)

# Regra para criar o executável
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

# Regra para compilar servidor_processamento.c
servidor_processamento.o: servidor_processamento.c estruturas.h
	$(CC) $(CFLAGS) -c servidor_processamento.c

# Regra para compilar estrutura.c
estruturas.o: estruturas.c estruturas.h
	$(CC) $(CFLAGS) -c estruturas.c

# Regra para limpar os arquivos objeto e o executável
clean:
	rm -f $(OBJS) $(TARGET)
