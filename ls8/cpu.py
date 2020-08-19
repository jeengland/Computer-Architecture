"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8

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
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        branches = {}

        def handle_HLT():
            return 0

        def handle_LDI():
            register_address = self.ram_read(pc + 1)
            value = self.ram_read(pc + 2)
            self.reg[register_address] = value
            return 3

        def handle_PRN():
            register_address = self.ram_read(pc + 1)
            value = self.reg[register_address]
            print(value)
            return 2

        def handle_MUL():
            reg_a = self.ram_read(pc + 1)
            reg_b = self.ram_read(pc + 2)
            self.alu('MUL', reg_a, reg_b)
            return 3

        def handle_PUSH():
            self.reg[7] -= 1
            self.reg[7] &= 0xff
            sp = self.reg[7]

            index = self.ram_read(pc + 1)
            value = self.reg[index]
            self.ram_write(sp, value)
            return 2

        def handle_POP():
            sp = self.reg[7]
            index = self.ram_read(pc + 1)
            value = self.ram_read(sp)
            self.reg[index] = value
            self.reg[7] += 1
            return 2

        branches[HLT] = handle_HLT
        branches[LDI] = handle_LDI
        branches[PRN] = handle_PRN
        branches[MUL] = handle_MUL
        branches[PUSH] = handle_PUSH
        branches[POP] = handle_POP

        pc = 0

        while running:
            opcode = self.ram_read(pc)
            op_length = branches[opcode]()
            if op_length == 0:
                running = False
            pc += op_length
