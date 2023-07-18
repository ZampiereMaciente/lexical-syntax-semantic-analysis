# Este codigo recebe um arquivo de entrada e analisa seus caracteres montando os lexemas e classificando seus tokens.

'''
   Linguagem MiniPascal    

    Gramatica:

    P= {
    PROG → programa id pvirg DECLS C-COMP
    DECLS → lambda | variaveis LIST-DECLS
    LIST-DECLS → DECL-TIPO D
    D → lambda | LIST-DECLS
    DECL-TIPO → LIST-ID dpontos TIPO pvirg
    LIST-ID → id E
    E → lambda | virg LIST-ID
    TIPO → inteiro | real | logico | caracter
    C-COMP → abrech LISTA-COMANDOS fechach LISTA-COMANDOS → COMANDOS G
    G → lambda | LISTA-COMANDOS
    COMANDOS → IF | WHILE | READ | WRITE | ATRIB
    IF → se abrepar EXPR fechapar C-COMP H
    H → lambda | senao C-COMP
    WHILE → enquanto abrepar EXPR fechapar C-COMP
    READ → leia abrepar LIST-ID fechapar pvirg
    ATRIB → id atrib EXPR pvirg
    WRITE → escreva abrepar LIST-W fechapar pvirg
    LIST-W → ELEM-W L
    L → lambda | virg LIST-W
    ELEM-W → EXPR | cadeia
    EXPR → SIMPLES P
    P → lambda | oprel SIMPLES
    SIMPLES → TERMO R
    R → lambda | opad SIMPLES
    TERMO → FAT S
    S → lambda | opmul TERMO
    FAT → id | cte | abrepar EXPR fechapar | verdadeiro | falso | opneg FAT}


    Tokens:

    G1 = {{PROG, DECLS, C-COMP, LIST-DECLS, DECL-TIPO, D, LIST-ID, E, TIPO, LISTA-COMANDOS, G, COMANDOS, IF, WHILE, READ, ATRIB, WRITE, EXPR, H, LIST-W, L, ELEM-W, SIMPLES, P, R, TERMO, S, FAT}
    {programa, id, variaveis, inteiro, real, logico, caracter, abrepar, fechapar, se, abrech, fechach, senao, enquanto, leia, atrib, escreva, cadeia, cte, verdadeiro, falso, oprel, opad, opmul, opneg, pvirg, virg, dpontos}, P, PROG}

'''
import re
from os import path
from tabela import TabelaSimbolos

class TipoToken:
    ID = (1, 'ID')
    OPREL = (2, 'OPREL')
    PTOVIRG = (3, 'PTVIRG')
    OPAD = (4, 'OPAD')
    OPMUL = (5, 'OPMUL')
    OPENPAR = (6, 'OPENPAR')
    CLOSEPAR = (7, 'CLOSEPAR')
    CTE = (8, 'CTE')
    ERROR = (9, 'ERRO')
    FIMARQ = (10, 'fim-de-arquivo')
    ABRECH = (11, 'ABRECH')
    FECHACH = (12, 'FECHACH')
    DPONTOS = (13, 'DPONTOS')
    VIRG = (14, 'VIRG')
    OPNEG = (15, 'OPNEG')
    ATRIB = (16, 'ATRIB')
    PROGRAMA = (17, 'PROGRAMA')
    VARIAVEIS = (18, 'VARIAVEIS')
    INTEIRO = (19, 'INTEIRO')
    REAL = (20, 'REAL')
    LOGICO = (21, 'LOGICO')
    CARACTER = (22, 'CARACTER')
    SE = (23, 'SE')
    SENAO = (24, 'SENAO')
    ENQUANTO = (25, 'ENQUANTO')
    LEIA = (26, 'LEIA')
    ESCREVA = (27, 'ESCREVA')
    FALSO = (28, 'FALSO')
    VERDADEIRO = (29, 'VERDADEIRO')
    CADEIA = (30, 'CADEIA')

class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema
        self.linha = linha
        self.tipoVar = ''

class Lexico:
    # dicionario de palavras reservadas
    reservadas = { 'programa': TipoToken.PROGRAMA,'variaveis': TipoToken.VARIAVEIS, 'inteiro': TipoToken.INTEIRO, 
                   'real': TipoToken.REAL,'logico': TipoToken.LOGICO, 'caracter': TipoToken.CARACTER, 
                   'se': TipoToken.SE,'senao': TipoToken.SENAO, 'enquanto': TipoToken.ENQUANTO, 'leia': TipoToken.LEIA,
                   'escreva': TipoToken.ESCREVA, 'falso': TipoToken.FALSO, 'verdadeiro': TipoToken.VERDADEIRO }

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        self.tabelaSimbolos = TabelaSimbolos()
        # fila de caracteres 'deslidos' pelo ungetChar
        

    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
            self.buffer = ''
            self.linha = 1
        else:
            print(f'ERRO: Arquivo "{self.nomeArquivo}" inexistente.')
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    def getChar(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)
            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()
                if car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha = self.linha + 1
                elif len(re.findall(r'[A-Za-z]',car)) > 0: # reconheca todos os simbolos da RE, caso não reconhecer retorna uma lista vazia
                    estado = 2
                elif car.isdigit():
                    estado = 3
                elif car in {'"', '<', '>', ';', '+', '-', '*', '/', '(', ')', '{', '}', ':', ',', '!', '='}:
                    estado = 4
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = lexema + car
                car = self.getChar()
                if len(lexema) > 16: # indentificadores maiores de 16 sao invalidos
                    return Token(TipoToken.ERROR, lexema, self.linha)
                if car is None or (not car.isalnum()):
                    # terminou o nome
                    self.ungetChar(car)
                    #if lexema.count('ç') >= 1: # no caso de usar o isalpha utilize essa linha e a seguinte
                        #return Token(TipoToken.ERROR, lexema, self.linha)
                    if lexema in Lexico.reservadas:
                        self.tabelaSimbolos.atribuiValor(lexema,Token(Lexico.reservadas[lexema], lexema, self.linha))
                        self.tabelaSimbolos.tabela[lexema].tipoVar = 'Reservada'
                        return Token(Lexico.reservadas[lexema], lexema, self.linha)
                    else:
                        self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.ID, lexema, self.linha))
                        return Token(TipoToken.ID, lexema, self.linha)
            elif estado == 3:
                # estado que trata numeros inteiros e reais
                lexema = lexema + car
                car = self.getChar()
                if car == '.':
                    lexema = lexema + car
                    if lexema.count('.') >= 2:
                        self.ungetChar(car)
                        lexema = lexema[:-1]
                    car = self.getChar()
                if car is None or (not car.isdigit()):
                    # terminou o numero
                    self.ungetChar(car)
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.CTE, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'CTE'
                    return Token(TipoToken.CTE, lexema, self.linha)
            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                lexema = lexema + car
                if  car == '<':
                    car2 = self.getChar()
                    if car2 == '=' or car2 == '>':
                        lexema = lexema + car2
                    else:
                        self.ungetChar(car2)
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.OPREL, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'OPREL'
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif  car == '>':
                    car2 = self.getChar()
                    if car2 == '=':
                        lexema = lexema + car2
                    else:
                        self.ungetChar(car2)
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.OPREL, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'OPREL'
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '=':
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.OPREL, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'OPREL'
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == ';':
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.PTOVIRG, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'PTOVIRG'
                    return Token(TipoToken.PTOVIRG, lexema, self.linha)
                elif car == '+' or car == '-':
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.OPAD, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'OPAD'
                    return Token(TipoToken.OPAD, lexema, self.linha)
                elif car == '*':
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.OPMUL, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'OPMUL'
                    return Token(TipoToken.OPMUL, lexema, self.linha)
                elif car == '/':
                    car2 = self.getChar()
                    if car2 == '/':
                        lexema = lexema[:-1]
                        estado = 5
                    elif car2 == '*':
                        lexema = lexema[:-1]
                        estado = 6
                    else:
                        self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.OPMUL, lexema, self.linha))
                        self.tabelaSimbolos.tabela[lexema].tipoVar = 'OPMUL'
                        return Token(TipoToken.OPMUL, lexema, self.linha)
                elif car == '(':
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.OPENPAR, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'OPENPAR'
                    return Token(TipoToken.OPENPAR, lexema, self.linha)
                elif car == ')':
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.CLOSEPAR, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'CLOSEPAR'
                    return Token(TipoToken.CLOSEPAR, lexema, self.linha)
                elif car == '{':
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.ABRECH, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'ABRECH'
                    return Token(TipoToken.ABRECH, lexema, self.linha)
                elif car == '}':
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.FECHACH, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'FECHACH'
                    return Token(TipoToken.FECHACH, lexema, self.linha)
                elif car == '!':
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.OPNEG, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'OPNEG'
                    return Token(TipoToken.OPNEG, lexema, self.linha)
                elif car == ':':
                    car2 = self.getChar()
                    if car2 == '=':
                        lexema = lexema + car2
                        self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.ATRIB, lexema, self.linha))
                        self.tabelaSimbolos.tabela[lexema].tipoVar = 'ATRIB'
                        return Token(TipoToken.ATRIB, lexema, self.linha)
                    self.ungetChar(car2)
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.DPONTOS, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'DPONTOS'
                    return Token(TipoToken.DPONTOS, lexema, self.linha)
                elif car == ',':
                    self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.VIRG, lexema, self.linha))
                    self.tabelaSimbolos.tabela[lexema].tipoVar = 'VIRG'
                    return Token(TipoToken.VIRG, lexema, self.linha)
                elif car == '"':
                    car = self.getChar()
                    lexema = lexema + car
                    while car != '"' and car != '\n':
                        car = self.getChar()
                        lexema = lexema + car
                    if car == '\n' and car != '"':
                        return Token(TipoToken.ERROR, lexema, self.linha)
                    elif car == '"':
                        self.tabelaSimbolos.atribuiValor(lexema,Token(TipoToken.CADEIA, lexema, self.linha))
                        self.tabelaSimbolos.tabela[lexema].tipoVar = 'CADEIA'
                        return Token(TipoToken.CADEIA, lexema[1:-1], self.linha)
                    else:
                        return Token(TipoToken.ERROR, lexema, self.linha)   
                                        
            elif estado == 5:
                # consumindo comentario em linha
                while (not car is None) and (car != '\n'):
                    car = self.getChar()
                estado = 1
            elif estado == 6:
                # consumindo comentario em bloco
                car = ''
                car2 = ''
                while (not car is None) and (car != '*' or car2 != '/'):
                    car = self.getChar()
                    if car == '*':
                        car2 = self.getChar()
                        if car2 == '*':
                            self.ungetChar(car2)
                estado = 1


if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'exemplo1.txt'
   if not nome.endswith('.txt'):
       nome += '.txt'
   lex = Lexico(nome)
   lex.abreArquivo()

   while(True):
       token = lex.getToken()
       print(f"token= {token.msg} , lexema= ({token.lexema})")
       if token.const == TipoToken.FIMARQ[0]:
           break
   lex.fechaArquivo()

