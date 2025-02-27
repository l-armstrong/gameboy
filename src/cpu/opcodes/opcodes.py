# from cpu.cpu import Register, MMU

class Opcode(object):
    def __init__(self, code, mnemonic, length, tcycles, instruction=None):
        self.code = code
        self.mnemonic = mnemonic
        self.length = length
        self.tcycles = tcycles
        self.mcycles = tcycles // 4
        self.instruction = instruction

    def __repr__(self):
        return f"{hex(self.code)}: {self.mnemonic}"


class Opcodes(object):
    def __init__(self, regs, mmu):
        self.regs = regs
        self.mmu = mmu
        self.op_collection = self.init_opcodes()

    def init_opcodes(self):
        REG_A = "self.regs.a" 
        REG_B = "self.regs.b"
        REG_C = "self.regs.c" 
        REG_D = "self.regs.d" 
        REG_E = "self.regs.e" 
        REG_H = "self.regs.h" 
        REG_L = "self.regs.l"
        return {
            0x00: Opcode(0x00, "NOP", 1, 4),
            0x01: Opcode(0x01, "LD BC n16", 3, 12, lambda: self._ld_rr_nn("BC")),
            0x02: Opcode(0x02, "LD BC A", 1, 8, lambda: self._ld_bc_a()),
            0x03: Opcode(0x03, "INC BC", 1, 8, lambda: self._inc_rr("BC")),
            0x04: Opcode(0x04, "INC B", 1, 4, lambda: self._inc(REG_B)),
            0x05: Opcode(0x05, "DEC B", 1, 4, lambda: self._dec(REG_B)),
            0x06: Opcode(0x06, "LD B n8", 2, 8, lambda: self._ldn(REG_B)),
            0x07: Opcode(0x07, "RLCA", 1, 4),
            0x08: Opcode(0x08, "LD a16 SP", 3, 20),
            0x09: Opcode(0x09, "ADD HL BC", 1, 8),
            0x0A: Opcode(0x0A, "LD A BC", 1, 8, lambda: self._ld_a_bc()),
            0x0B: Opcode(0x0B, "DEC BC", 1, 8),
            0x0C: Opcode(0x0C, "INC C", 1, 4, lambda: self._inc(REG_C)),
            0x0D: Opcode(0x0D, "DEC C", 1, 4, lambda: self._dec(REG_C)),
            0x0E: Opcode(0x0E, "LD C n8", 2, 8, lambda: self._ldn(REG_C)),
            0x0F: Opcode(0x0F, "RRCA", 1, 4),
            0x10: Opcode(0x10, "STOP n8", 2, 4),
            0x11: Opcode(0x11, "LD DE n16", 3, 12, lambda: self._ld_rr_nn("DE")),
            0x12: Opcode(0x12, "LD DE A", 1, 8, lambda: self._ld_de_a()),
            0x13: Opcode(0x13, "INC DE", 1, 8, lambda: self._inc_rr("DE")),
            0x14: Opcode(0x14, "INC D", 1, 4, lambda: self._inc(REG_D)),
            0x15: Opcode(0x15, "DEC D", 1, 4, lambda: self._dec(REG_D)),
            0x16: Opcode(0x16, "LD D n8", 2, 8, lambda: self._ldn(REG_D)),
            0x17: Opcode(0x17, "RLA", 1, 4),
            0x18: Opcode(0x18, "JR e8", 2, 12),
            0x19: Opcode(0x19, "ADD HL DE", 1, 8),
            0x1A: Opcode(0x1A, "LD A DE", 1, 8, lambda: self._ld_a_de()),
            0x1B: Opcode(0x1B, "DEC DE", 1, 8),
            0x1C: Opcode(0x1C, "INC E", 1, 4, lambda: self._inc(REG_E)),
            0x1D: Opcode(0x1D, "DEC E", 1, 4, lambda: self._dec(REG_E)),
            0x1E: Opcode(0x1E, "LD E n8", 2, 8, lambda: self._ldn(REG_E)),
            0x1F: Opcode(0x1F, "RRA", 1, 4),
            0x20: Opcode(0x20, "JR NZ e8", 2, 12),
            0x21: Opcode(0x21, "LD HL n16", 3, 12, lambda: self._ld_rr_nn("HL")),
            0x22: Opcode(0x22, "LD HL+ A", 1, 8, lambda: self._ld_hl_a_inc()),
            0x23: Opcode(0x23, "INC HL", 1, 8, lambda: self._inc_rr("HL")),
            0x24: Opcode(0x24, "INC H", 1, 4, lambda: self._inc(REG_H)),
            0x25: Opcode(0x25, "DEC H", 1, 4, lambda: self._dec(REG_H)),
            0x26: Opcode(0x26, "LD H n8", 2, 8, lambda: self._ldn(REG_H)),
            0x27: Opcode(0x27, "DAA", 1, 4),
            0x28: Opcode(0x28, "JR Z e8", 2, 12),
            0x29: Opcode(0x29, "ADD HL HL", 1, 8),
            0x2A: Opcode(0x2A, "LD A HL+", 1, 8, lambda: self._ld_a_hl_inc()),
            0x2B: Opcode(0x2B, "DEC HL", 1, 8),
            0x2C: Opcode(0x2C, "INC L", 1, 4, lambda: self._inc(REG_L)),
            0x2D: Opcode(0x2D, "DEC L", 1, 4, lambda: self._dec(REG_L)),
            0x2E: Opcode(0x2E, "LD L n8", 2, 8, lambda: self._ldn(REG_L)),
            0x2F: Opcode(0x2F, "CPL", 1, 4),
            0x30: Opcode(0x30, "JR NC e8", 2, 12),
            0x31: Opcode(0x31, "LD SP n16", 3, 12, lambda: self._ld_rr_nn("SP")),
            0x32: Opcode(0x32, "LD HL- A", 1, 8, lambda: self._ld_hl_a_dec()),
            0x33: Opcode(0x33, "INC SP", 1, 8, lambda: self._inc_rr("SP")),
            0x34: Opcode(0x34, "INC (HL)", 1, 12),
            0x35: Opcode(0x35, "DEC HL", 1, 12),
            0x36: Opcode(0x36, "LD HL n8", 2, 12),
            0x37: Opcode(0x37, "SCF", 1, 4),
            0x38: Opcode(0x38, "JR C e8", 2, 12),
            0x39: Opcode(0x39, "ADD HL SP", 1, 8),
            0x3A: Opcode(0x3A, "LD A HL-", 1, 8, lambda: self._ld_a_hl_dec()),
            0x3B: Opcode(0x3B, "DEC SP", 1, 8),
            0x3C: Opcode(0x3C, "INC A", 1, 4, lambda: self._inc(REG_A)),
            0x3D: Opcode(0x3D, "DEC A", 1, 4, lambda: self._dec(REG_A)),
            0x3E: Opcode(0x3E, "LD A n8", 2, 8, lambda: self._ldn(REG_A)),
            0x3F: Opcode(0x3F, "CCF", 1, 4),
            0x40: Opcode(0x40, "LD B B", 1, 4, lambda: self._ld(REG_B, REG_B)),
            0x41: Opcode(0x41, "LD B C", 1, 4, lambda: self._ld(REG_B, REG_C)),
            0x42: Opcode(0x42, "LD B D", 1, 4, lambda: self._ld(REG_B, REG_D)),
            0x43: Opcode(0x43, "LD B E", 1, 4, lambda: self._ld(REG_B, REG_E)),
            0x44: Opcode(0x44, "LD B H", 1, 4, lambda: self._ld(REG_B, REG_H)),
            0x45: Opcode(0x45, "LD B L", 1, 4, lambda: self._ld(REG_B, REG_L)),
            0x46: Opcode(0x46, "LD B HL", 1, 8, lambda: self._ldr_hl(REG_B)),
            0x47: Opcode(0x47, "LD B A", 1, 4, lambda: self._ld(REG_B, REG_A)),
            0x48: Opcode(0x48, "LD C B", 1, 4, lambda: self._ld(REG_C, REG_B)),
            0x49: Opcode(0x49, "LD C C", 1, 4, lambda: self._ld(REG_C, REG_C)),
            0x4A: Opcode(0x4A, "LD C D", 1, 4, lambda: self._ld(REG_C, REG_D)),
            0x4B: Opcode(0x4B, "LD C E", 1, 4, lambda: self._ld(REG_C, REG_E)),
            0x4C: Opcode(0x4C, "LD C H", 1, 4, lambda: self._ld(REG_C, REG_H)),
            0x4D: Opcode(0x4D, "LD C L", 1, 4, lambda: self._ld(REG_C, REG_L)),
            0x4E: Opcode(0x4E, "LD C HL", 1, 8, lambda: self._ldr_hl(REG_C)),
            0x4F: Opcode(0x4F, "LD C A", 1, 4, lambda: self._ld(REG_C, REG_A)),
            0x50: Opcode(0x50, "LD D B", 1, 4, lambda: self._ld(REG_D, REG_B)),
            0x51: Opcode(0x51, "LD D C", 1, 4, lambda: self._ld(REG_D, REG_C)),
            0x52: Opcode(0x52, "LD D D", 1, 4, lambda: self._ld(REG_D, REG_D)),
            0x53: Opcode(0x53, "LD D E", 1, 4, lambda: self._ld(REG_D, REG_E)),
            0x54: Opcode(0x54, "LD D H", 1, 4, lambda: self._ld(REG_D, REG_H)),
            0x55: Opcode(0x55, "LD D L", 1, 4, lambda: self._ld(REG_D, REG_L)),
            0x56: Opcode(0x56, "LD D HL", 1, 8, lambda: self._ldr_hl(REG_D)),
            0x57: Opcode(0x57, "LD D A", 1, 4, lambda: self._ld(REG_D, REG_A)),
            0x58: Opcode(0x58, "LD E B", 1, 4, lambda: self._ld(REG_E, REG_B)),
            0x59: Opcode(0x59, "LD E C", 1, 4, lambda: self._ld(REG_E, REG_C)),
            0x5A: Opcode(0x5A, "LD E D", 1, 4, lambda: self._ld(REG_E, REG_D)),
            0x5B: Opcode(0x5B, "LD E E", 1, 4, lambda: self._ld(REG_E, REG_E)),
            0x5C: Opcode(0x5C, "LD E H", 1, 4, lambda: self._ld(REG_E, REG_H)),
            0x5D: Opcode(0x5D, "LD E L", 1, 4, lambda: self._ld(REG_E, REG_L)),
            0x5E: Opcode(0x5E, "LD E HL", 1, 8, lambda: self._ldr_hl(REG_E)),
            0x5F: Opcode(0x5F, "LD E A", 1, 4, lambda: self._ld(REG_E, REG_A)),
            0x60: Opcode(0x60, "LD H B", 1, 4, lambda: self._ld(REG_H, REG_B)),
            0x61: Opcode(0x61, "LD H C", 1, 4, lambda: self._ld(REG_H, REG_C)),
            0x62: Opcode(0x62, "LD H D", 1, 4, lambda: self._ld(REG_H, REG_D)),
            0x63: Opcode(0x63, "LD H E", 1, 4, lambda: self._ld(REG_H, REG_E)),
            0x64: Opcode(0x64, "LD H H", 1, 4, lambda: self._ld(REG_H, REG_H)),
            0x65: Opcode(0x65, "LD H L", 1, 4, lambda: self._ld(REG_H, REG_L)),
            0x66: Opcode(0x66, "LD H HL", 1, 8),
            0x67: Opcode(0x67, "LD H A", 1, 4, lambda: self._ld(REG_H, REG_A)),
            0x68: Opcode(0x68, "LD L B", 1, 4, lambda: self._ld(REG_L, REG_B)),
            0x69: Opcode(0x69, "LD L C", 1, 4, lambda: self._ld(REG_L, REG_C)),
            0x6A: Opcode(0x6A, "LD L D", 1, 4, lambda: self._ld(REG_L, REG_D)),
            0x6B: Opcode(0x6B, "LD L E", 1, 4, lambda: self._ld(REG_L, REG_E)),
            0x6C: Opcode(0x6C, "LD L H", 1, 4, lambda: self._ld(REG_L, REG_H)),
            0x6D: Opcode(0x6D, "LD L L", 1, 4, lambda: self._ld(REG_L, REG_L)),
            0x6E: Opcode(0x6E, "LD L HL", 1, 8, lambda: self._ldr_hl(REG_L)),
            0x6F: Opcode(0x6F, "LD L A", 1, 4, lambda: self._ld(REG_L, REG_A)),
            0x70: Opcode(0x70, "LD HL B", 1, 8, lambda: self._ldhl_r(REG_B)),
            0x71: Opcode(0x71, "LD HL C", 1, 8, lambda: self._ldhl_r(REG_C)),
            0x72: Opcode(0x72, "LD HL D", 1, 8, lambda: self._ldhl_r(REG_D)),
            0x73: Opcode(0x73, "LD HL E", 1, 8, lambda: self._ldhl_r(REG_E)),
            0x74: Opcode(0x74, "LD HL H", 1, 8, lambda: self._ldhl_r(REG_H)),
            0x75: Opcode(0x75, "LD HL L", 1, 8, lambda: self._ldhl_r(REG_L)),
            0x76: Opcode(0x76, "HALT", 1, 4),
            0x77: Opcode(0x77, "LD HL A", 1, 8, lambda: self._ldhl_r(REG_A)),
            0x78: Opcode(0x78, "LD A B", 1, 4, lambda: self._ld(REG_A, REG_B)),
            0x79: Opcode(0x79, "LD A C", 1, 4, lambda: self._ld(REG_A, REG_C)),
            0x7A: Opcode(0x7A, "LD A D", 1, 4, lambda: self._ld(REG_A, REG_D)),
            0x7B: Opcode(0x7B, "LD A E", 1, 4, lambda: self._ld(REG_A, REG_E)),
            0x7C: Opcode(0x7C, "LD A H", 1, 4, lambda: self._ld(REG_A, REG_H)),
            0x7D: Opcode(0x7D, "LD A L", 1, 4, lambda: self._ld(REG_A, REG_L)),
            0x7E: Opcode(0x7E, "LD A HL", 1, 8, lambda: self._ldr_hl(REG_A)),
            0x7F: Opcode(0x7F, "LD A A", 1, 4, lambda: self._ld(REG_A, REG_A)),
            0x80: Opcode(0x80, "ADD A B", 1, 4, lambda: self._add(self.regs.b)),
            0x81: Opcode(0x81, "ADD A C", 1, 4, lambda: self._add(self.regs.c)),
            0x82: Opcode(0x82, "ADD A D", 1, 4, lambda: self._add(self.regs.d)),
            0x83: Opcode(0x83, "ADD A E", 1, 4, lambda: self._add(self.regs.e)),
            0x84: Opcode(0x84, "ADD A H", 1, 4, lambda: self._add(self.regs.h)),
            0x85: Opcode(0x85, "ADD A L", 1, 4, lambda: self._add(self.regs.l)),
            0x86: Opcode(0x86, "ADD A HL", 1, 8, lambda: self._add(self.mmu.read_byte(self.regs.hl()))),
            0x87: Opcode(0x87, "ADD A A", 1, 4, lambda: self._add(self.regs.a)),
            0x88: Opcode(0x88, "ADC A B", 1, 4, lambda: self._adc(self.regs.b)),
            0x89: Opcode(0x89, "ADC A C", 1, 4, lambda: self._adc(self.regs.c)),
            0x8A: Opcode(0x8A, "ADC A D", 1, 4, lambda: self._adc(self.regs.d)),
            0x8B: Opcode(0x8B, "ADC A E", 1, 4, lambda: self._adc(self.regs.e)),
            0x8C: Opcode(0x8C, "ADC A H", 1, 4, lambda: self._adc(self.regs.h)),
            0x8D: Opcode(0x8D, "ADC A L", 1, 4, lambda: self._adc(self.regs.l)),
            0x8E: Opcode(0x8E, "ADC A HL", 1, 8, lambda: self._adc(self.mmu.read_byte(self.regs.hl()))),
            0x8F: Opcode(0x8F, "ADC A A", 1, 4, lambda: self._adc(self.regs.a)),
            0x90: Opcode(0x90, "SUB A B", 1, 4, lambda: self._sub(self.regs.b)),
            0x91: Opcode(0x91, "SUB A C", 1, 4, lambda: self._sub(self.regs.c)),
            0x92: Opcode(0x92, "SUB A D", 1, 4, lambda: self._sub(self.regs.d)),
            0x93: Opcode(0x93, "SUB A E", 1, 4, lambda: self._sub(self.regs.e)),
            0x94: Opcode(0x94, "SUB A H", 1, 4, lambda: self._sub(self.regs.h)),
            0x95: Opcode(0x95, "SUB A L", 1, 4, lambda: self._sub(self.regs.l)),
            0x96: Opcode(0x96, "SUB A HL", 1, 8, lambda: self._sub(self.mmu.read_byte(self.regs.hl()))),
            0x97: Opcode(0x97, "SUB A A", 1, 4, lambda: self._sub(self.regs.a)),
            0x98: Opcode(0x98, "SBC A B", 1, 4, lambda: self._subc(self.regs.b)),
            0x99: Opcode(0x99, "SBC A C", 1, 4, lambda: self._subc(self.regs.c)),
            0x9A: Opcode(0x9A, "SBC A D", 1, 4, lambda: self._subc(self.regs.d)),
            0x9B: Opcode(0x9B, "SBC A E", 1, 4, lambda: self._subc(self.regs.e)),
            0x9C: Opcode(0x9C, "SBC A H", 1, 4, lambda: self._subc(self.regs.h)),
            0x9D: Opcode(0x9D, "SBC A L", 1, 4, lambda: self._subc(self.regs.l)),
            0x9E: Opcode(0x9E, "SBC A HL", 1, 8, lambda: self._subc(self.mmu.read_byte(self.regs.hl()))),
            0x9F: Opcode(0x9F, "SBC A A", 1, 4, lambda: self._subc(self.regs.a)),
            0xA0: Opcode(0xA0, "AND A B", 1, 4, lambda: self._and(self.regs.b)),
            0xA1: Opcode(0xA1, "AND A C", 1, 4, lambda: self._and(self.regs.c)),
            0xA2: Opcode(0xA2, "AND A D", 1, 4, lambda: self._and(self.regs.d)),
            0xA3: Opcode(0xA3, "AND A E", 1, 4, lambda: self._and(self.regs.e)),
            0xA4: Opcode(0xA4, "AND A H", 1, 4, lambda: self._and(self.regs.h)),
            0xA5: Opcode(0xA5, "AND A L", 1, 4, lambda: self._and(self.regs.l)),
            0xA6: Opcode(0xA6, "AND A HL", 1, 8, lambda: self._and(self.mmu.read_byte(self.regs.hl()))),
            0xA7: Opcode(0xA7, "AND A A", 1, 4, lambda: self._and(self.regs.a)),
            0xA8: Opcode(0xA8, "XOR A B", 1, 4, lambda: self._xor(self.regs.b)),
            0xA9: Opcode(0xA9, "XOR A C", 1, 4, lambda: self._xor(self.regs.c)),
            0xAA: Opcode(0xAA, "XOR A D", 1, 4, lambda: self._xor(self.regs.d)),
            0xAB: Opcode(0xAB, "XOR A E", 1, 4, lambda: self._xor(self.regs.e)),
            0xAC: Opcode(0xAC, "XOR A H", 1, 4, lambda: self._xor(self.regs.h)),
            0xAD: Opcode(0xAD, "XOR A L", 1, 4, lambda: self._xor(self.regs.l)),
            0xAE: Opcode(0xAE, "XOR A HL", 1, 8, lambda: self._xor(self.mmu.read_byte(self.regs.hl()))),
            0xAF: Opcode(0xAF, "XOR A A", 1, 4, lambda: self._xor(self.regs.a)),
            0xB0: Opcode(0xB0, "OR A B", 1, 4, lambda: self._or(self.regs.b)),
            0xB1: Opcode(0xB1, "OR A C", 1, 4, lambda: self._or(self.regs.c)),
            0xB2: Opcode(0xB2, "OR A D", 1, 4, lambda: self._or(self.regs.d)),
            0xB3: Opcode(0xB3, "OR A E", 1, 4, lambda: self._or(self.regs.e)),
            0xB4: Opcode(0xB4, "OR A H", 1, 4, lambda: self._or(self.regs.h)),
            0xB5: Opcode(0xB5, "OR A L", 1, 4, lambda: self._or(self.regs.l)),
            0xB6: Opcode(0xB6, "OR A HL", 1, 8, lambda: self._or(self.mmu.read_byte(self.regs.hl()))),
            0xB7: Opcode(0xB7, "OR A A", 1, 4, lambda: self._or(self.regs.a)),
            0xB8: Opcode(0xB8, "CP A B", 1, 4, lambda: self._cp(self.regs.b)),
            0xB9: Opcode(0xB9, "CP A C", 1, 4, lambda: self._cp(self.regs.c)),
            0xBA: Opcode(0xBA, "CP A D", 1, 4, lambda: self._cp(self.regs.d)),
            0xBB: Opcode(0xBB, "CP A E", 1, 4, lambda: self._cp(self.regs.e)),
            0xBC: Opcode(0xBC, "CP A H", 1, 4, lambda: self._cp(self.regs.h)),
            0xBD: Opcode(0xBD, "CP A L", 1, 4, lambda: self._cp(self.regs.l)),
            0xBE: Opcode(0xBE, "CP A HL", 1, 8, lambda: self._cp(self.mmu.read_byte(self.regs.hl()))),
            0xBF: Opcode(0xBF, "CP A A", 1, 4, lambda: self._cp(self.regs.a)),
            0xC0: Opcode(0xC0, "RET NZ", 1, 20),
            0xC1: Opcode(0xC1, "POP BC", 1, 12),
            0xC2: Opcode(0xC2, "JP NZ a16", 3, 16),
            0xC3: Opcode(0xC3, "JP a16", 3, 16),
            0xC4: Opcode(0xC4, "CALL NZ a16", 3, 24),
            0xC5: Opcode(0xC5, "PUSH BC", 1, 16),
            0xC6: Opcode(0xC6, "ADD A n8", 2, 8, lambda: self._add(self.mmu.read_byte(self.regs.read_pc_inc()))),
            0xC7: Opcode(0xC7, "RST $00", 1, 16),
            0xC8: Opcode(0xC8, "RET Z", 1, 20),
            0xC9: Opcode(0xC9, "RET", 1, 16),
            0xCA: Opcode(0xCA, "JP Z a16", 3, 16),
            0xCB: Opcode(0xCB, "PREFIX", 1, 4),
            0xCC: Opcode(0xCC, "CALL Z a16", 3, 24),
            0xCD: Opcode(0xCD, "CALL a16", 3, 24),
            0xCE: Opcode(0xCE, "ADC A n8", 2, 8, lambda: self._adc(self.mmu.read_byte(self.regs.read_pc_inc()))),
            0xCF: Opcode(0xCF, "RST $08", 1, 16),
            0xD0: Opcode(0xD0, "RET NC", 1, 20),
            0xD1: Opcode(0xD1, "POP DE", 1, 12),
            0xD2: Opcode(0xD2, "JP NC a16", 3, 16),
            0xD3: Opcode(0xD3, "ILLEGAL_D3", 1, 4),
            0xD4: Opcode(0xD4, "CALL NC a16", 3, 24),
            0xD5: Opcode(0xD5, "PUSH DE", 1, 16),
            0xD6: Opcode(0xD6, "SUB A n8", 2, 8, lambda: self._sub(self.mmu.read_byte(self.regs.read_pc_inc()))),
            0xD7: Opcode(0xD7, "RST $10", 1, 16),
            0xD8: Opcode(0xD8, "RET C", 1, 20),
            0xD9: Opcode(0xD9, "RETI", 1, 16),
            0xDA: Opcode(0xDA, "JP C a16", 3, 16),
            0xDB: Opcode(0xDB, "ILLEGAL_DB", 1, 4),
            0xDC: Opcode(0xDC, "CALL C a16", 3, 24),
            0xDD: Opcode(0xDD, "ILLEGAL_DD", 1, 4),
            0xDE: Opcode(0xDE, "SBC A n8", 2, 8, lambda: self._subc(self.mmu.read_byte(self.regs.read_pc_inc()))),
            0xDF: Opcode(0xDF, "RST $18", 1, 16),
            0xE0: Opcode(0xE0, "LDH a8 A", 2, 12),
            0xE1: Opcode(0xE1, "POP HL", 1, 12),
            0xE2: Opcode(0xE2, "LDH C A", 1, 8),
            0xE3: Opcode(0xE3, "ILLEGAL_E3", 1, 4),
            0xE4: Opcode(0xE4, "ILLEGAL_E4", 1, 4),
            0xE5: Opcode(0xE5, "PUSH HL", 1, 16),
            0xE6: Opcode(0xE6, "AND A n8", 2, 8, lambda: self._and(self.mmu.read_byte(self.regs.read_pc_inc()))),
            0xE7: Opcode(0xE7, "RST $20", 1, 16),
            0xE8: Opcode(0xE8, "ADD SP e8", 2, 16),
            0xE9: Opcode(0xE9, "JP HL", 1, 4),
            0xEA: Opcode(0xEA, "LD a16 A", 3, 16),
            0xEB: Opcode(0xEB, "ILLEGAL_EB", 1, 4),
            0xEC: Opcode(0xEC, "ILLEGAL_EC", 1, 4),
            0xED: Opcode(0xED, "ILLEGAL_ED", 1, 4),
            0xEE: Opcode(0xEE, "XOR A n8", 2, 8, lambda: self._xor(self.mmu.read_byte(self.regs.read_pc_inc()))),
            0xEF: Opcode(0xEF, "RST $28", 1, 16),
            0xF0: Opcode(0xF0, "LDH A a8", 2, 12),
            0xF1: Opcode(0xF1, "POP AF", 1, 12),
            0xF2: Opcode(0xF2, "LDH A C", 1, 8),
            0xF3: Opcode(0xF3, "DI", 1, 4),
            0xF4: Opcode(0xF4, "ILLEGAL_F4", 1, 4),
            0xF5: Opcode(0xF5, "PUSH AF", 1, 16),
            0xF6: Opcode(0xF6, "OR A n8", 2, 8, lambda: self._or(self.mmu.read_byte(self.regs.read_pc_inc()))),
            0xF7: Opcode(0xF7, "RST $30", 1, 16),
            0xF8: Opcode(0xF8, "LD HL SP e8", 2, 12),
            0xF9: Opcode(0xF9, "LD SP HL", 1, 8),
            0xFA: Opcode(0xFA, "LD A a16", 3, 16),
            0xFB: Opcode(0xFB, "EI", 1, 4),
            0xFC: Opcode(0xFC, "ILLEGAL_FC", 1, 4),
            0xFD: Opcode(0xFD, "ILLEGAL_FD", 1, 4),
            0xFE: Opcode(0xFE, "CP A n8", 2, 8, lambda: self._cp(self.mmu.read_byte(self.regs.read_pc_inc()))),
            0xFF: Opcode(0xFF, "RST $38", 1, 16),
        }

    def _and(self, value):
        # perform bitwise and on 8bit values and reg a.
        self.regs.a = self.regs.a & value
        # clear flags
        self.regs.f = 0
        # check if regs a is zero
        if self.regs.a == 0: self.regs.f |= self.regs.ZERO_FLAG
        # set half carry
        self.regs.f |= self.regs.HALF_CARRY_FLAG
    
    def _or(self, value):
        # perform bitwise or on 8bit values and reg a.
        self.regs.a = self.regs.a | value
        # clear flags
        self.regs.f = 0
        # check if regs a is zero
        if self.regs.a == 0: self.regs.f |= self.regs.ZERO_FLAG
        # check if regs a is zero
        
    def _xor(self, value):
        # perform bitwise or on 8bit values and reg a.
        self.regs.a = self.regs.a ^ value
        # clear flags
        self.regs.f = 0
        # check if regs a is zero
        if self.regs.a == 0: self.regs.f |= self.regs.ZERO_FLAG
        # check if regs a is zero
        
    def _add(self, value):
        # perform add operation on 8bit values and reg a.
        res = self.regs.a + value
        # clear flags
        self.regs.f = 0
        # check if result was zero
        if not (res & 0xFF): self.regs.f |= self.regs.ZERO_FLAG
        # check if result has a half carry
        if ((self.regs.a & 0x0F) + (value & 0x0F)) > 0x0F:
            self.regs.f |= self.regs.HALF_CARRY_FLAG
        # check if result has a carry
        if res > 255: self.regs.f |= self.regs.CARRY_FLAG
        # set regs.a, may wrap around since type(self.regs.a) == np.uint8
        self.regs.a = res
    
    def _adc(self, value):
        # perform add operation on 8bit values, carry and reg a.
        # check if carry bit is set
        carry = 1 if (self.regs.f >> 4) & 0xF else 0
        res = self.regs.a + value + carry
        # clear flags
        self.regs.f = 0
        # check if result was zero
        if not (res & 0xFF): self.regs.f |= self.regs.ZERO_FLAG
        # check if result has a half carry
        if ((self.regs.a & 0x0F) + (value & 0x0F)) + carry > 0x0F:
            self.regs.f |= self.regs.HALF_CARRY_FLAG
        # check if result has a carry
        if res > 255: self.regs.f |= self.regs.CARRY_FLAG
        # set regs.a, may wrap around since type(self.regs.a) == np.uint8
        self.regs.a = res
        
    def _sub(self, value):
        # perform sub operation on 8bit values and reg a.
        res = self.regs.a - value
        # clear flags
        self.regs.f = 0
        # check if result was zero
        if not (res & 0xFF): self.regs.f |= self.regs.ZERO_FLAG
        # "Negative"
        self.regs.f |= self.regs.SUB_FLAG
        # check if result has a half carry
        if ((self.regs.a & 0x0F) + (res & 0x0F)) > 0x0F: 
            self.regs.f |= self.regs.HALF_CARRY_FLAG
        # check if result has a carry
        if res > 255: self.regs.f |= self.regs.CARRY_FLAG
        # set regs.a, may wrap around since type(self.regs.a) == np.uint8
        self.regs.a = res

    def _subc(self, value):
        # perform sub operation on 8bit values, carry and reg a.
        carry = 1 if (self.regs.f >> 4) & 0xF else 0
        res = self.regs.a - value - carry 
        # clear flags
        self.regs.f = 0
        # check if result was zero
        if not (res & 0xFF): self.regs.f |= self.regs.ZERO_FLAG
        # "Negative"
        self.regs.f |= self.regs.SUB_FLAG
        # check if result has a half carry
        if (self.regs.a ^ value ^ (res & 0xFF) & (1 << 4)) != 0: 
            self.regs.f |= self.regs.HALF_CARRY_FLAG
        # check if result has a carry
        if res < 0: self.regs.f |= self.regs.CARRY_FLAG
        # set regs.a, may wrap around since type(self.regs.a) == np.uint8
        self.regs.a = res
    
    def _dec(self, reg):
        # Decrements data in the 8-bit register r.
        setattr(self, reg, getattr(self, reg) - 1)
        self.regs.f = 0
        # check for zero
        if (not getattr(self, reg)): self.regs.f |= self.regs.ZERO_FLAG
        # set sub flag
        self.regs.f |= self.regs.SUB_FLAG
        # set half carry flag
        if (getattr(self, reg) & 0x0F) == 0: self.regs.f |= self.regs.HALF_CARRY_FLAG

    def _inc(self, reg):
        # increments data in the 8-bit register r.
        setattr(self, reg, getattr(self, reg) + 1)
        self.regs.f = 0
        # check for zero
        if (not getattr(self, reg)): self.regs.f |= self.regs.ZERO_FLAG
        # set sub flag
        self.regs.f |= self.regs.SUB_FLAG
        # set half carry flag
        if (getattr(self, reg) & 0x0F) == 0x0F: self.regs.f |= self.regs.HALF_CARRY_FLAG
    
    def _inc_rr(self, regs):
        # Increments data in the 16-bit register rr.
        match regs:
            case "BC": self.regs.set_bc(self.regs.bc() + 1)
            case "DE": self.regs.set_de(self.regs.de() + 1)
            case "HL": self.regs.set_hl(self.regs.hl() + 1)
            case "SP": self.regs.set_sp(self.regs.sp() + 1)
    
    def _cp(self, value):
        # subtracts from a registers and updates
        res = self.regs.a - value
        # clear flags
        self.regs.f = 0
        # check if result was zero
        if not (res & 0xFF): self.regs.f |= self.regs.ZERO_FLAG
        # "Negative"
        self.regs.f |= self.regs.SUB_FLAG
        # check if result has a half carry
        if ((self.regs.a & 0x0F) + (res & 0x0F)) > 0x0F: 
            self.regs.f |= self.regs.HALF_CARRY_FLAG
        # check if result has a carry
        if res > 255: self.regs.f |= self.regs.CARRY_FLAG
    
    def _ld(self, dst, src):
        # Load to the 8-bit register dst, data from the 8-bit register src
        setattr(self, dst, getattr(self, src))
    
    def _ldn(self, dst):
        # Load to the 8-bit register dst, data from the 8-bit value in memory
        value = self.mmu.read_byte(self.regs.pc)
        setattr(self, dst, value)
        self.regs.pc += 1
    
    def _ldr_hl(self, dst):
        # load to the 8-bit register r, data from mem address in HL.
        value = self.mmu.read_byte(self.regs.hl())
        setattr(self, dst, value)
    
    def _ldhl_r(self, src):
        # load to the mem address in HL data form 8-bit register r.
        self.mmu.write_byte(self.regs.hl(), getattr(self, src))
    
    def _ld_bc_a(self):
        # Load to address in BC data from the 8-bit A register.
        self.mmu.write_byte(self.regs.bc(), self.regs.a)

    def _ld_de_a(self):
        # Load to address in DE data from the 8-bit A register.
        self.mmu.write_byte(self.regs.de(), self.regs.a)
    
    def _ld_a_bc(self):
        # Load to the 8-bit A register, data from the absolute address specified by the 16-bit register BC
        self.regs.a = self.mmu.read_byte(self.regs.bc())

    def _ld_a_de(self): 
        # Load to the 8-bit A register, data from the absolute address specified by the 16-bit register DE
        self.regs.a = self.mmu.read_byte(self.regs.de())
    
    def _ld_rr_nn(self, regs):
        # Load to the 16-bit register rr, the immediate 16-bit data nn.
        lsb = self.mmu.read_byte(self.regs.pc)
        self.pc += 1
        msb = self.mmu.read_byte(self.regs.pc)
        self.pc += 1
        nn = (msb << 8) | lsb
        match regs:
            case "BC": self.regs.set_bc(nn)
            case "DE": self.regs.set_de(nn)
            case "HL": self.regs.set_hl(nn)
            case "SP": self.regs.set_sp(nn)
    
    def _ld_hl_a_inc(self):
        # Load to the absolute address specified by the 16-bit register HL, 
        # data from the 8-bit A register. The value of HL is decremented after the memory write.
        self.mmu.write_byte(self.regs.hl(), self.regs.a)
        self.regs.set_hl(self.regs.hl() + 1)

    def _ld_hl_a_dec(self):
        # Load to the absolute address specified by the 16-bit register HL, data from the 8-bit 
        # A register. The value of HL is decremented after the memory write
        self.mmu.write_byte(self.regs.hl(), self.regs.a)
        self.regs.set_hl(self.regs.hl() - 1)
    
    def _ld_a_hl_inc(self):
        # Load to the 8-bit A register, data from the absolute address specified by the 
        # 16-bit register HL. The value of HL is incremented after the memory read.
        self.regs.a = self.mmu.read_byte(self.regs.hl())
        self.regs.set_hl(self.regs.hl() + 1)

    def _ld_a_hl_dec(self):
        # Load to the 8-bit A register, data from the absolute address specified by the 
        # 16-bit register HL. The value of HL is decremented  after the memory read.
        self.regs.a = self.mmu.read_byte(self.regs.hl())
        self.regs.set_hl(self.regs.hl() - 1)
