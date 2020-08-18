"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        file = open(filename, 'r')
        lines = file.readlines()
        inv = ['\n', '#']
        program = [int(line[:8], 2) for line in lines if line[0] not in inv]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111

        pc = 0

        op_length = 1

        while running:
            opcode = self.ram_read(pc)
            if opcode == HLT:
                running = False
            elif opcode == LDI:
                register_address = self.ram_read(pc + 1)
                value = self.ram_read(pc + 2)
                self.registers[register_address] = value
                op_length = 3
            elif opcode == PRN:
                register_address = self.ram_read(pc + 1)
                value = self.registers[register_address]
                print(value)
                op_length = 2
            else:
                raise Exception('Invalid Op Code')

            pc += op_length
