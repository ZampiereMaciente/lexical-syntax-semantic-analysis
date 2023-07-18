# Este codigo recebe um arquivo de entrada e o analisa de acordo com as regras da gramatica da linguagem em questão, Mini Pascal.

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
import sys
from lexico import Token, Lexico, TipoToken as tt


class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None
        self.deuErro = False

    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            self.PROG()
            self.consome(tt.FIMARQ)
            print("Program compile successfully")

            self.lex.fechaArquivo()

    def atualIgual(self, token):
        (const, msg) = token
        return self.tokenAtual.const == const
    
    def imprimiErro(self, msg):
        if type(msg) is not list:
            msg = [msg]
        print(f'ERRO DE SINTAXE [linha {self.tokenAtual.linha}]: era esperado ', end='')
        for i,r in enumerate(msg): # i,r é igual a (indice,objeto)
            if i == len(msg)-1:
                print(f'"{r[1]}" ', end='')
            else:
                print(f'"{r[1]}" ou ', end='')
        print(f'mas veio "{self.tokenAtual.lexema}"')
        sys.exit(1)
        
    def consome(self, token):
        if self.atualIgual(token):
            self.tokenAtual = self.lex.getToken()
        else:
            #(const, msg) = token
            self.imprimiErro(token)

    def salvaLexema(self):
        return self.tokenAtual.lexema

    def salvaLinha(self):
        return self.tokenAtual.linha
    
    def imprimiErroSemantico(self, msg, linha):
        print(f'ERRO SEMANTICO [linha {linha}]: {msg}')

    def testaVarNaoDeclarada(self, var, linha):
        if self.deuErro:
            return
        if not self.lex.tabelaSimbolos.existeIdent(var):
            self.deuErro = True
            msg = "Variavel " + var + " nao declarada."
            self.imprimiErroSemantico(msg, linha)
            sys.exit(1)

    def PROG(self):
        self.consome(tt.PROGRAMA)
        self.consome(tt.ID)
        self.lex.tabelaSimbolos.atualizaVarTipo('ID')
        self.consome(tt.PTOVIRG)
        self.DECLS()
        self.C_COMP()

    def DECLS(self):
        if self.atualIgual(tt.VARIAVEIS):
            self.consome(tt.VARIAVEIS)
            self.LIST_DECLS()
        else:
            pass

    def LIST_DECLS(self):
        self.DECL_TIPO()
        self.D()

    def D(self):
        if self.atualIgual(tt.ERROR):
            self.imprimiErro([tt.ID])
        if self.atualIgual(tt.ID):
            self.LIST_DECLS()
        else:
            pass
            
    def DECL_TIPO(self):
        self.LIST_ID()
        self.consome(tt.DPONTOS)
        self.TIPO()
        self.consome(tt.PTOVIRG)

    def LIST_ID(self):
        self.consome(tt.ID)
        self.E()

    def E(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_ID()
        else:
            pass

    def TIPO(self):
        if self.atualIgual(tt.INTEIRO):
            self.lex.tabelaSimbolos.atualizaVarTipo('INTEIRO')
            self.consome(tt.INTEIRO)
        elif self.atualIgual(tt.REAL):
            self.lex.tabelaSimbolos.atualizaVarTipo('REAL')
            self.consome(tt.REAL)
        elif self.atualIgual(tt.LOGICO):
            self.lex.tabelaSimbolos.atualizaVarTipo('LOGICO')
            self.consome(tt.LOGICO)
        elif self.atualIgual(tt.CARACTER):
            self.lex.tabelaSimbolos.atualizaVarTipo('CARACTER')
            self.consome(tt.CARACTER)
        else:
            self.imprimiErro([tt.INTEIRO, tt.REAL, tt.LOGICO, tt.CARACTER])

    def C_COMP(self):
        self.consome(tt.ABRECH)
        self.LISTA_COMANDOS()
        self.consome(tt.FECHACH)

    def LISTA_COMANDOS(self):
        self.COMANDOS()
        self.G()

    def G(self):
        if self.atualIgual(tt.ERROR):
            self.imprimiErro([tt.SE, tt.ENQUANTO, tt.LEIA, tt.ESCREVA, tt.ID])
        if self.atualIgual(tt.SE) or self.atualIgual(tt.ENQUANTO) or self.atualIgual(tt.LEIA) or self.atualIgual(tt.ESCREVA) or self.atualIgual(tt.ID):
            self.LISTA_COMANDOS()
        else:
            pass

    def COMANDOS(self):
        if self.atualIgual(tt.SE):
            self.IF()
        elif self.atualIgual(tt.ENQUANTO):
            self.WHILE()
        elif self.atualIgual(tt.LEIA):
            self.READ()
        elif self.atualIgual(tt.ESCREVA):
            self.WRITE()
        elif self.atualIgual(tt.ID):
            self.ATRIB()
        else:
            self.imprimiErro([tt.SE, tt.ENQUANTO, tt.LEIA, tt.ESCREVA, tt.ID])
        
        
    def IF(self):
        self.consome(tt.SE)
        self.consome(tt.OPENPAR)
        self.EXPR()
        self.consome(tt.CLOSEPAR)
        self.C_COMP()
        self.H()

    def H(self):
        if self.atualIgual(tt.SENAO):
            self.consome(tt.SENAO)
            self.C_COMP()
        else:
            pass

    def WHILE(self):
        self.consome(tt.ENQUANTO)
        self.consome(tt.OPENPAR)
        self.EXPR()
        self.consome(tt.CLOSEPAR)
        self.C_COMP()

    def READ(self):
        self.consome(tt.LEIA)
        self.consome(tt.OPENPAR)
        self.LIST_ID()
        self.consome(tt.CLOSEPAR)
        self.consome(tt.PTOVIRG)

    def ATRIB(self):
        var = self.salvaLexema()
        linha = self.salvaLinha()
        self.testaVarNaoDeclarada(var, linha)       
        self.consome(tt.ID)
        self.consome(tt.ATRIB)
        self.EXPR()
        self.consome(tt.PTOVIRG)

    def WRITE(self):
        self.consome(tt.ESCREVA)
        self.consome(tt.OPENPAR)
        self.LIST_W()
        self.consome(tt.CLOSEPAR)
        self.consome(tt.PTOVIRG)

    def LIST_W(self):
        self.ELEM_W()
        self.L()

    def L(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_W()
        else:
            pass

    def ELEM_W(self):
        if self.atualIgual(tt.ERROR):
            self.imprimiErro(tt.CADEIA)
        if self.atualIgual(tt.CADEIA):
            self.consome(tt.CADEIA)
        else:
            self.EXPR()
        
    def EXPR(self):
        self.SIMPLES()
        self.P()

    def P(self):
        if self.atualIgual(tt.OPREL):
            self.consome(tt.OPREL)
            self.SIMPLES()
        else:
            pass

    def SIMPLES(self):
        self.TERMO()
        self.R()

    def R(self):
        if self.atualIgual(tt.OPAD):
            self.consome(tt.OPAD)
            self.SIMPLES()
        else:
            pass

    def TERMO(self):
        self.FAT()
        self.S()

    def S(self):
        if self.atualIgual(tt.OPMUL):
            self.consome(tt.OPMUL)
            self.TERMO()
        else:
            pass

    def FAT(self):
        if self.atualIgual(tt.ID):
            var = self.salvaLexema()
            linha = self.salvaLinha()
            self.testaVarNaoDeclarada(var, linha)
            self.consome(tt.ID)
        elif self.atualIgual(tt.CTE):
            self.consome(tt.CTE)
        elif self.atualIgual(tt.OPENPAR):
            self.consome(tt.OPENPAR)
            self.EXPR()
            self.consome(tt.CLOSEPAR)
        elif self.atualIgual(tt.VERDADEIRO):
            self.consome(tt.VERDADEIRO)
        elif self.atualIgual(tt.FALSO):
            self.consome(tt.FALSO)
        elif self.atualIgual(tt.OPNEG):
            self.consome(tt.OPNEG)
            self.FAT()
        else:
            self.imprimiErro([tt.ID, tt.CTE, tt.OPENPAR, tt.CLOSEPAR, tt.VERDADEIRO, tt.FALSO, tt.OPNEG])

if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'exemplo1.txt'
   if not nome.endswith('.txt'):
       nome += '.txt'
   parser = Sintatico()
   parser.interprete(nome)
   
