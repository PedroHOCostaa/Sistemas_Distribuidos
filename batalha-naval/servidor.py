class Tabuleiro:
    def __init__(self):
        self.matriz = [[0 for _ in range(8)] for _ in range(8)]
    
class Navio:
    def __init__(self, tamanho, time):
        self.time = time
        self.tamanho = tamanho
        self.atingidos = 0
        self.segmentos = [1 for _ in range(tamanho)]
class NavioPequeno(Navio):
    def __init__(self):
        super().__init__(2)  # Navio pequeno tem tamanho 2

class NavioMedio(Navio):
    def __init__(self):
        super().__init__(3)  # Navio médio tem tamanho 3

class NavioGrande(Navio):
    def __init__(self):
        super().__init__(4)  # Navio grande tem tamanho 4

