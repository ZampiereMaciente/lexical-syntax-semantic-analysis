# Este codigo e o main dos analisadores lexico, sintatico e semantico, nele sera possivel a criacao de um arquivo contendo a tabela de simbolos.


import sys
from sintatico import Sintatico

if __name__== "__main__":

    # Verifica se foram fornecidos argumentos suficientes
    if len(sys.argv) < 2:
        nome = input("Entre com o nome do arquivo: ")
        #nome = 'exemplo1.txt'
        if not nome.endswith('.txt'):
            nome += '.txt'
        parser = Sintatico()
        parser.interprete(nome)
    elif sys.argv[1] == '-t':
        #nome = input("Entre com o nome do arquivo: ")
        nome = 'exemplo1.txt'
        if not nome.endswith('.txt'):
            nome += '.txt'
        parser = Sintatico()
        parser.interprete(nome)

        nomeArquivo = sys.argv[2]
        # Abre o arquivo para escrita
        arquivo_saida = open(nomeArquivo, 'w')

        arquivo_saida.write(parser.lex.tabelaSimbolos.imprimi())

        arquivo_saida.close()

