# FILE: binary.py
import sys
from Token import tokenize_file
from analise import analise

##modificar 

# Mapeamento de instruções para códigos de operação do Simpletron
INSTRUCTION_MAP = {
    'input': 10,
    'print': 11,
    'let': 20,  # let será tratado de forma especial
    'goto': 40,
    'if': 42,  # if será tratado de forma especial
    'end': 43,
    'rem': 0   # rem será ignorado
}

def convert_to_machine_code(tokens):
    machine_code = []
    variable_map = {}
    variable_counter = 0  # Inicialmente zero, será ajustado depois

    tokens = list(tokens)  # Convertendo iterador para lista para reutilização
    token_iter = iter(tokens)

    for token in token_iter:
        print(token)
        if token.type == 'NUMBER':
            line_number = int(token.value)
        elif token.type == 'INSTRUCTION':
            instruction = token.value
            if instruction == 'input':
                variable = next(token_iter).value
                if variable not in variable_map:
                    variable_map[variable] = variable_counter
                    variable_counter += 1
                    print(variable_map)
                machine_code.append(f"+{INSTRUCTION_MAP[instruction]:02}{variable_map[variable]:02}")
            elif instruction == 'print':
                variable = next(token_iter).value
                if variable not in variable_map:
                    variable_map[variable] = variable_counter
                    variable_counter += 1
                machine_code.append(f"+{INSTRUCTION_MAP[instruction]:02}{variable_map[variable]:02}")
            elif instruction == 'let':
                variable = next(token_iter).value
                next(token_iter)  # Skip '=' token
                expr_tokens = []
                while True:
                    token = next(token_iter, None)
                    print("let token", token)
                    if token is None or token.type not in ['NUMBER', 'VARIABLE', 'OPERATOR']:
                        break
                    if token.type == 'NUMBER' or token.type == 'VARIABLE':
                        if token.value not in variable_map:
                            variable_map[token.value] = variable_counter
                            variable_counter += 1
                            print(variable_map)
                        expr_tokens.append(variable_map[token.value])
                    elif token.type == 'OPERATOR':
                        expr_tokens.append(token.value)
                # Converter a expressão aritmética para código de máquina
                # Supondo que a expressão é simples e não precisa de precedência de operadores
                if variable not in variable_map:
                    variable_map[variable] = variable_counter
                    variable_counter += 1
                result_var = variable_map[variable]
                print("expr_token:",expr_tokens)
                for i in range(0, len(expr_tokens), 2):
                    if i == 0:
                        machine_code.append(f"+20{expr_tokens[i]:02}")  # LOAD
                        print(f"LOAD :{expr_tokens[i]:02}" )
                    else:
                        operator = expr_tokens[i-1]
                        if operator == '+':
                            machine_code.append(f"+30{expr_tokens[i]:02}")  # ADD
                        elif operator == '-':
                            machine_code.append(f"+31{expr_tokens[i]:02}")  # SUBTRACT
                        elif operator == '*':
                            machine_code.append(f"+33{expr_tokens[i]:02}")  # MULTIPLY
                        elif operator == '/':
                            machine_code.append(f"+32{expr_tokens[i]:02}")  # DIVIDE
                machine_code.append(f"+21{result_var:02}")  # STORE
            elif instruction == 'goto':
                line_number = next(token_iter).value
                machine_code.append(f"+{INSTRUCTION_MAP[instruction]:02}{int(line_number):02}")
            elif instruction == 'if':
                # Supondo que a condição é simples e não precisa de precedência de operadores
                left_operand = next(token_iter).value
                comparator = next(token_iter).value
                right_operand = next(token_iter).value
                next(token_iter)  # Skip 'goto' token
                target_line = next(token_iter).value
                if left_operand not in variable_map:
                    variable_map[left_operand] = variable_counter
                    variable_counter += 1
                if right_operand not in variable_map:
                    variable_map[right_operand] = variable_counter
                    variable_counter += 1
                if comparator == '<':
                    machine_code.append(f"+20{variable_map[left_operand]:02}")  # LOAD left_operand
                    print(f"LOAD left_operand :{variable_map[left_operand]:02}" )
                    machine_code.append(f"+31{variable_map[right_operand]:02}")  # SUBTRACT right_operand
                    machine_code.append(f"+41{int(target_line):02}")  # BRANCHNEG
                elif comparator == '>':
                    machine_code.append(f"+20{variable_map[right_operand]:02}")  # LOAD right_operand
                    print(f"LOAD right_operand :{variable_map[left_operand]:02}" )
                    machine_code.append(f"+31{variable_map[left_operand]:02}")  # SUBTRACT left_operand
                    machine_code.append(f"+41{int(target_line):02}")  # BRANCHNEG
                elif comparator == '==':
                    machine_code.append(f"+20{variable_map[left_operand]:02}")  # LOAD left_operand
                    machine_code.append(f"+31{variable_map[right_operand]:02}")  # SUBTRACT right_operand
                    machine_code.append(f"+42{int(target_line):02}")  # BRANCHZERO
            elif instruction == 'end':
                machine_code.append(f"+{INSTRUCTION_MAP[instruction]:02}00")

    # Ajustar o contador de variáveis para o número de linhas resultantes
    variable_counter = len(machine_code)

    # Adicionar variáveis no final do arquivo
    for variable, address in sorted(variable_map.items(), key=lambda item: item[1]):
        machine_code.append(f"+{variable_counter:04}")
        variable_counter += 1

    return machine_code

def main(input_file, output_file):
    # Step 1: Tokenize the input file
    tokens = tokenize_file(input_file)
    
    # Step 2: Analyze tokens
    with open(input_file, 'r') as source:
        analise(source)
    
    # Step 3: Convert tokens to machine code
    machine_code = convert_to_machine_code(iter(tokens))
    
    # Save the machine code to the output file
    with open(output_file, 'w') as out_file:
        for instruction in machine_code:
            out_file.write(f"{instruction}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python binary.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)