# Este código obtem uma classe TabelaSimbolos que é usada para criar e modelar a tabela de simbolos usadas no analisador lexico e sintatico

class TabelaSimbolos:

    def __init__(self):
        self.tabela = dict()

    def existeIdent(self, nome):
        if nome in self.tabela and self.tabela[nome].tipoVar != '':
            return True
        else:
            return False

    def declaraIdent(self, nome, valor):
        if not self.existeIdent(nome):
            self.tabela[nome] = valor
            return True
        else:
            return False

    def pegaValor(self, nome):
        return self.tabela[nome]

    def atribuiValor(self, nome, valor):
        if nome not in self.tabela:
            self.tabela[nome] = valor

    def atualizaVarTipo(self, tipo):
        for v in self.tabela.values():
            if v.tipoVar == '':
                v.tipoVar = tipo
    
    def imprimi(self):
        tab = f'{"Classe".center(14, "-")}|{"Tipo".center(12, "-")}|{"Valor".center(13, "-")}\n'
        for v in self.tabela.values():
            tab += f'{v.tipo[1].ljust(14, " ")}|{v.tipoVar.center(12, " ")}|{v.lexema.center(13, " ")}\n'
        return tab
