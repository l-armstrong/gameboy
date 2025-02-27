from opcodes.opcodes import Opcodes
import numpy as np

class Register(object):
    def __init__(self):
        # 8 bit regs
        self.a = np.uint8(0)
        self.b = np.uint8(0)
        self.c = np.uint8(0)
        self.d = np.uint8(0)
        self.e = np.uint8(0)
        self.h = np.uint8(0)
        self.l = np.uint8(0)
        # The f register is used for flags
        # calc. bits depending on the result of prev
        # operation
        # Zero (0x80): set if the last operation result is 0
        # Operation (0x40): Set if last operation was subtraction
        # Half-carry (0x20): Set if the last operation result overflowed past 15
        # Carry (0x10): Set if the last operation result was over 255 for adding or under 0 for sub.
        self.f = np.uint8(0)
        self.ZERO_FLAG = 0x80
        self.SUB_FLAG = 0x40
        self.HALF_CARRY_FLAG = 0x20
        self.CARRY_FLAG = 0x10
        # 16 bit regs
        self.pc = np.uint16(0)
        self.sp = np.uint16(0)
    
    def hl(self): return (self.h << 8) | self.l
    def bc(self): return (self.b << 8) | self.c 
    def de(self): return (self.d << 8) | self.e
    def set_hl(self, value): 
        self.h = (value & 0xFF00) >> 8
        self.l = (value & 0x00FF)
    def set_bc(self, value):
        self.b = (value & 0xFF00) >> 8
        self.c = (value & 0x00FF)
    def set_de(self, value):
        self.d = (value & 0xFF00) >> 8
        self.e = (value & 0x00FF)
    def set_sp(self, value): self.sp = value
    
    def read_pc_inc(self):
        value = np.uint16(self.pc)
        self.pc += 1
        return value

class MMU(object):
    def __init__(self):
        self.memory = np.zeros(65536, dtype=np.uint8)
    
    def read_byte(self, address):
        return self.memory[address]
    
    def write_byte(self, address, value):
        self.memory[address] = np.uint8(value)

    def read_word(self, address):
        return self.read_byte(address) | (self.read_byte(address + 1) << 8)

class CPU(object):
    def __init__(self, regs, mmu):
        self.mmu = mmu
        self.regs = regs
        self.op = Opcodes(self.regs, self.mmu)
