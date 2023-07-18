# Lexical, Syntax and Semantic Analysis.

### Quick look.

>#### This code was based on the book " Compilers - Principles, Techniques, & Tools - Second Edition, by: Alfred V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman, and the grandmaster of bits, and with the help of the master of bits https://github.com/Casperento, who provided some ideas about the project.

### MiniPascal
>#### The code in question is related to the implementation over a MiniPascal language, the grammar of which will be demonstrated below.

### Grammar:

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

# Build Instructions

o build and test the MiniPascal compiler you need to execute the following commands:

- -t table.txt

where the -t parameter is to generate the symbol table and then the name of the file where the information will be saved.


[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/ZampiereMaciente)
