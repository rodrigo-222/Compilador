import re
import sys

# Define the types of tokens
TOKEN_TYPES = {
    'NUMBER': r'\d+',
    'INSTRUCTION': r'\b(input|print|let|goto|if|end|rem)\b',
    'VARIABLE': r'\b[a-z]\b',
    'OPERATOR': r'[+\-*/%]',
    'COMPARATOR': r'(==|!=|>|<|>=|<=)',
    'ASSIGNMENT': r'=',
    'GOTO': r'goto',
    'END': r'end',
    'WHITESPACE': r'\s+',
    'EOL': r'$',
    'UNKNOWN': r'.'
}

# Token class to represent each token
class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line})"

# Function to tokenize a single line
def tokenize_line(line, line_number):
    tokens = []
    while line:
        match = None
        for token_type, pattern in TOKEN_TYPES.items():
            regex = re.compile(pattern)
            match = regex.match(line)
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE':  # Ignore whitespace tokens
                    tokens.append(Token(token_type, value, line_number))
                line = line[len(value):]
                break
        if not match:
            raise ValueError(f"Unexpected character in line {line_number}: {line[0]}")
    tokens.append(Token('EOL', '', line_number))  # Add EOL token at the end of the line
    return tokens

# Function to tokenize an entire file
def tokenize_file(filename):
    tokens = []
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line_tokens = tokenize_line(line.strip(), line_number)
            tokens.extend(line_tokens)
    return tokens

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tokenizer.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        tokens = tokenize_file(filename)
        for token in tokens:
            print(token)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)