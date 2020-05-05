"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
# If equal flag is set (true), jump to the address stored in the given register.
JEQ = 0b01010101
# If E flag is clear (false, 0), jump to the address stored in the given register.
JNE = 0b01010110




class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.power_status = True
        self.sp = 7
        self.reg[self.sp] = 0xF4
        self.flag = 0b00000000


    def ram_read(self, address):
        value = self.ram[address]
        return value

    def ram_write(self, address, value):
        self.ram[address] = value

    def hlt_operation(self):
        self.power_status = False
        sys.exit()

    def ldi_operation(self, register, value):
        # print(self.reg)
        self.reg[register] = value
        self.pc += 3
        # print(self.reg)
        

    def prn_operation(self, register):
        value = self.reg[register]
        print(value)
        self.pc += 2

    def mul_operation(self, register_a, register_b):
        value = self.reg[register_a] * self.reg[register_b]
        self.reg[register_a] = value
        self.pc += 3

    def push_operation(self, register):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[register]
        self.pc += 2

    def pop_operation(self, register):
        self.reg[register] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1
        self.pc += 2

    def call_operation(self, register):
        self.reg[self.sp] -= 1
        sp = self.reg[self.sp]
        self.ram_write(sp, self.pc + 2)

        self.pc = self.reg[register]

    def ret_operation(self):
        sp = self.reg[self.sp]
        return_address = self.ram_read(sp)

        self.pc = return_address

    def jmp_operation(self, register):
        self.pc = self.reg[register]

    def jeq_operation(self, register):
        # print("JEQ")
        if (self.flag & 0b00000001) == 1:
            self.pc = self.reg[register]
        else:
            self.pc += 2
    
    def jne_operation(self, register):
        # print("JNE")
        if (self.flag & 0b00000001) == 0:
            self.pc = self.reg[register]
        else:
            self.pc += 2

    def load(self, file):
        """Load a program into memory."""

        address = 0

        f = open(file, "r")

        for line in f.readlines():
            split_line = line.split("#")[0]
            if split_line is "" or split_line is "\n":
                continue
            conversion = int(split_line, 2)
            self.ram[address] = conversion
            address += 1

        f.close()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        # elif op == "SUB": etc
        elif op == "CMP":
            # print("CMP")
            # print(self.pc)
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]: 
                self.flag = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            self.pc += 3
            # print(self.pc)

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
        while self.power_status is True:
            IR = self.ram_read(self.pc)
            # print(f"IR: {IR}")
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print(self.E)
            if IR is HLT:
                self.hlt_operation()
            elif IR is LDI:
                self.ldi_operation(operand_a, operand_b)
            elif IR is PRN:
                self.prn_operation(operand_a)
            elif IR is MUL:
                self.mul_operation(operand_a, operand_b)
            elif IR is ADD:
                self.alu("ADD", operand_a, operand_b)
            elif IR is PUSH:
                self.push_operation(operand_a)
            elif IR is POP:
                self.pop_operation(operand_a)
            elif IR is CALL:
                self.call_operation(operand_a)
            elif IR is RET:
                self.ret_operation()
            elif IR is CMP:
                self.alu("CMP", operand_a, operand_b)
            elif IR is JEQ:
                self.jeq_operation(operand_a)
            elif IR is JNE:
                self.jne_operation(operand_a)
            elif IR is JMP:
                self.jmp_operation(operand_a)
            
