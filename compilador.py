import sys
import os
import decimal

class Simpletron:
    MEMORY_SIZE = 100
    READ = 10
    WRITE = 11
    LOAD = 20
    STORE = 21
    ADD = 30
    SUBTRACT = 31
    DIVIDE = 32
    MULTIPLY = 33
    MODULE = 34
    BRANCH = 40
    BRANCHNEG = 41
    BRANCHZERO = 42
    HALT = 43

    def __init__(self):
        self.memory = [0] * self.MEMORY_SIZE
        self.accumulator = 0
        self.instruction_counter = 0
        self.operation_code = 0
        self.operand = 0
        self.processing = False
        self.current_line = 0

    def load(self, filename):
        try:
            with open(filename, "r") as file:
                counter = 0
                for line in file:
                    word = int(line.strip())
                    if -9999 <= word <= 9999:
                        self.memory[counter] = word
                        counter += 1
                    else:
                        raise ValueError(f"Invalid instruction at line {counter}")
            print("Simpletron loading completed!")
        except FileNotFoundError:
            raise Exception("error: file not found!")
        except IOError:
            raise Exception("error: invalid file!")
        except ValueError as e:
            raise Exception(f"error: {e}")

    def read_instruction(self):
        try:
            number = int(input("input : "))
            if -9999 <= number <= 9999:
                self.memory[self.operand] = number
                self.instruction_counter += 1
            else:
                print(f"error at line {self.current_line}: invalid number!")
        except ValueError:
            print(f"error at line {self.current_line}: invalid number!")

    def write_instruction(self):
        print(f"output: {self.memory[self.operand]:+05}")
        self.instruction_counter += 1

    def load_instruction(self):
        self.accumulator = self.memory[self.operand]
        self.instruction_counter += 1

    def store_instruction(self):
        self.memory[self.operand] = self.accumulator
        self.instruction_counter += 1

    def add_instruction(self):
        self.accumulator += self.memory[self.operand]
        if -9999 <= self.accumulator <= 9999:
            self.instruction_counter += 1
        else:
            raise Exception(f"error at line {self.current_line}: accumulator overflow!")

    def subtract_instruction(self):
        self.accumulator -= self.memory[self.operand]
        if -9999 <= self.accumulator <= 9999:
            self.instruction_counter += 1
        else:
            raise Exception(f"error at line {self.current_line}: accumulator overflow!")

    def divide_instruction(self):
        if self.memory[self.operand] != 0:
            self.accumulator //= self.memory[self.operand]
            self.instruction_counter += 1
        else:
            raise Exception(f"error at line {self.current_line}: divide by zero!")

    def multiply_instruction(self):
        self.accumulator *= self.memory[self.operand]
        if -9999 <= self.accumulator <= 9999:
            self.instruction_counter += 1
        else:
            raise Exception(f"error at line {self.current_line}: accumulator overflow!")

    def module_instruction(self):
        self.accumulator %= self.memory[self.operand]
        if -9999 <= self.accumulator <= 9999:
            self.instruction_counter += 1
        else:
            raise Exception(f"error at line {self.current_line}: accumulator overflow!")

    def branch_instruction(self):
        self.instruction_counter = self.operand

    def branchneg_instruction(self):
        if self.accumulator < 0:
            self.instruction_counter = self.operand
        else:
            self.instruction_counter += 1

    def branchzero_instruction(self):
        if self.accumulator == 0:
            self.instruction_counter = self.operand
        else:
            self.instruction_counter += 1

    def halt_instruction(self):
        self.processing = False

    def interpret(self):
        print("Simpletron execution begins!")
        self.processing = True
        while self.processing:
            self.current_line = self.instruction_counter  # Atualizar a linha atual
            instruction_register = self.memory[self.instruction_counter]
            self.operation_code = instruction_register // 100
            self.operand = instruction_register % 100
            if self.operation_code == self.READ:
                self.read_instruction()
            elif self.operation_code == self.WRITE:
                self.write_instruction()
            elif self.operation_code == self.LOAD:
                self.load_instruction()
            elif self.operation_code == self.STORE:
                self.store_instruction()
            elif self.operation_code == self.ADD:
                self.add_instruction()
            elif self.operation_code == self.SUBTRACT:
                self.subtract_instruction()
            elif self.operation_code == self.DIVIDE:
                self.divide_instruction()
            elif self.operation_code == self.MULTIPLY:
                self.multiply_instruction()
            elif self.operation_code == self.MODULE:
                self.module_instruction()
            elif self.operation_code == self.BRANCH:
                self.branch_instruction()
            elif self.operation_code == self.BRANCHNEG:
                self.branchneg_instruction()
            elif self.operation_code == self.BRANCHZERO:
                self.branchzero_instruction()
            elif self.operation_code == self.HALT:
                self.halt_instruction()
            else:
                raise Exception(f"error at line {self.current_line}: unknown instruction!")
        print("Simpletron execution terminated!")

    def dump(self):
        print("\nREGISTERS:")
        print(f"{self.accumulator:+05} Accumulator")
        print(f"{self.instruction_counter:02} Instruction Counter")
        print(f"{self.memory[self.instruction_counter]:+05} Instruction Register")
        print(f"{self.operation_code:02} Operation Code")
        print(f"{self.operand:02} Operand")
        print("\nMEMORY:")
        for i in range(0, self.MEMORY_SIZE, 10):
            print(f"{i // 10} ", end="")
            for j in range(i, i + 10):
                print(f"{self.memory[j]:+05} ", end="")
            print()

    def print_memory(self, title):
        print(f"\n{title}")
        for i in range(0, self.MEMORY_SIZE, 10):
            print(f"{i // 10} ", end="")
            for j in range(i, i + 10):
                print(f"{self.memory[j]:+05} ", end="")
            print()

    def execute(self, filename):
        print("Welcome to Simpletron!")
        try:
            self.load(filename)
            self.print_memory("Initial Memory State")
            self.interpret()
        except Exception as e:
            print(e)
            print("Simpletron execution abnormally terminated!")
        finally:
            self.print_memory("Final Memory State")
            self.dump()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compilador.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    simpletron = Simpletron()
    simpletron.execute(filename)