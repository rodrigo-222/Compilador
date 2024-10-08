import sys

instrucoes = ["input", "print", "let", "goto", "if", "end", "rem"]  
linhas = []
variaveis = {}

def analise(input):
    pulos = []
    line = input.readline().split()
    previous = -1
    while line :
        if not line[0].isdecimal():
            print("Erro léxico: Linha não é um número '" + line[0] + "'")
        elif int(line[0]) <= previous:
            print("Erro semântico: Linha " + line[0] + " fora de ordem")
        else:
            previous = int(line[0])
            linhas.append(previous)
        if line[1] not in instrucoes:
            print('Erro léxico (linha ' + line[0] + '): Instrução inválida ("' + line[1] + '")')
        if line[1] == "input":
            if len(line) != 3:
                print('Erro sintático (linha ' + line[0] + '): Número inválido de argumentos da instrução input')
            else:
                if len(line[2]) > 1 or line[2].isupper() or not line[2].isalpha():
                    print('Erro léxico (linha ' + line[0] + '): Nome de variável inválido ("' + line[2] + '")')
                else:
                    variaveis[line[2]] = 0                    
        elif line[1] == "print":
            if len(line) != 3:
                print('Erro sintático (linha ' + line[0] + '): Número inválido de argumentos da instrução print')
            else:
                if len(line[2]) > 1 or line[2].isupper() or not line[2].isalpha():
                    print('Erro léxico (linha ' + line[0] + '): Nome de variável inválido ("' + line[2] + '")')
                else:
                    variaveis[line[2]] = 0
        elif line[1] == "let":
            if len(line[2]) > 1 or line[2].isupper() or not line[2].isalpha():
                print('Erro léxico (linha ' + line[0] + '): Nome de variável inválido ("' + line[2] + '")')
            if line[3] != "=":
                print('Erro sintático (linha ' + line[0] + '): Atribuição inválida ("' + line[3] + '"), esperava "="')
            aritmetica(line[4:], line[0])
        elif line[1] == "goto":
            if len(line) != 3:
                print('Erro sintático (linha ' + line[0] + '): Número inválido de argumentos da instrução goto')
            else:
                if not line[2].isdecimal():
                    print('Erro léxico (linha ' + line[0] + '): Pulando para linha inválida ("' + line[2] + '")')
                else:
                    pulos.append(int(line[2]))
        elif line[1] == "if":
            if line[-2] != "goto":
                print('Erro sintático (linha ' + line[0] + '): Comando if/goto sem goto')
            condicoes(line[2 : -2], line[0])
            if not line[-1].isdecimal():
                print('Erro léxico (linha ' + line[0] + '): Pulando para linha inválida ("' + line[-1] + '")')
            else:
                pulos.append(int(line[-1]))
        
        elif line[1] == len(line) and line[1] != "end":
            print('Erro sintático (linha ' + line[0] + '): Falta da instrução end' + line[1])

        elif line[1] == "end":
            if len(line) != 2:
                print('Erro sintático (linha ' + line[0] + '): Número inválido de argumentos da instrução end')
        elif line[1] == "rem":
            pass

        line = input.readline().split()

    for pulo in pulos:
        if pulo not in linhas:
            print('Erro semântico: Pulando para linha inexistente (' + str(pulo) + ')')

def aritmetica(expr, linha):
    if(len(expr) == 1):
        if expr[0].isdecimal() or (expr[0][0] == '-' and expr[0][1:].isdecimal()):
            return
        if len(expr[0]) > 1 or expr[0].isupper() or not expr[0].isalpha():
            print('Erro léxico (linha ' + linha + '): Operando inválido ("' + expr[0] + '")')
            return
    else:
        if len(expr) % 2 == 0:
            print('Erro sintático (linha ' + linha + '): Expressão aritmética inválida')
            return
        for i in range(0, len(expr), 2):
            if (not expr[i].isdecimal()) and (len(expr[i]) > 1 or expr[i].isupper() or not expr[i].isalpha()):
                print('Erro léxico (linha ' + linha + '): Operando inválido ("' + expr[i] + '")')
            else:
                variaveis[expr[i]] = 0
            if (i+1 < len(expr)) and expr[i + 1] not in ["+", "-", "*", "/", "%"]:
                print('Erro léxico (linha ' + linha + '): Operador inválido ("' + expr[i + 1] + '")')
            
            if (i+1 < len(expr)) and expr[i + 1] in ["/", "%"] and expr[i + 2] == "0":
                print('Erro semântico (linha ' + linha + '): Divisão por zero')

def condicoes(expr, linha):
    comparadores = ["==", "!=", ">", "<", ">=", "<="]
    sep = -1
    for comparador in comparadores:
        if comparador in expr:
            if sep != -1:
                print('Erro sintático (linha ' + linha + '): Múltiplos comparadores na expressão booleana')
                return
            sep = expr.index(comparador)
    if sep == -1:
        print('Erro sintático (linha ' + linha + '): Nenhum comparador na expressão booleana')
        return
    aritmetica(expr[:sep], linha)
    aritmetica(expr[sep + 1:], linha)
            
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 1:
        print("Por favor, informe apenas o arquivo a ser compilado!", file=sys.stderr)
        sys.exit(1)
    elif len(args) == 0:
        print("Por favor, informe o arquivo a ser compilado!", file=sys.stderr)
        sys.exit(1)
    else:
        with open(args[0], 'r') as source:
            analise(source)