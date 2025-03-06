# TODO: move Opcode into folder
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

class CB_Opcodes(object):
    def __init__(self, regs, mmu):
        self.regs = regs
        self.mmu = mmu
        self.op_collection = self.init_cb_opcodes()
    
    def init_cb_opcodes(self):
        REG_A = "self.regs.a" 
        REG_B = "self.regs.b"
        REG_C = "self.regs.c" 
        REG_D = "self.regs.d" 
        REG_E = "self.regs.e" 
        REG_H = "self.regs.h" 
        REG_L = "self.regs.l"
        return {
            0x00: Opcode(0x00, "RLC B", 2, 8, lambda: self._rlc(REG_B)),
            0x01: Opcode(0x01, "RLC C", 2, 8, lambda: self._rlc(REG_C)),
            0x02: Opcode(0x02, "RLC D", 2, 8, lambda: self._rlc(REG_D)),
            0x03: Opcode(0x03, "RLC E", 2, 8, lambda: self._rlc(REG_E)),
            0x04: Opcode(0x04, "RLC H", 2, 8, lambda: self._rlc(REG_H)),
            0x05: Opcode(0x05, "RLC L", 2, 8, lambda: self._rlc(REG_L)),
            0x06: Opcode(0x06, "RLC HL", 2, 16),
            0x07: Opcode(0x07, "RLC A", 2, 8, lambda: self._rlc(REG_A)),
            0x08: Opcode(0x08, "RRC B", 2, 8, lambda: self._rrc(REG_B)),
            0x09: Opcode(0x09, "RRC C", 2, 8, lambda: self._rrc(REG_C)),
            0x0A: Opcode(0x0A, "RRC D", 2, 8, lambda: self._rrc(REG_D)),
            0x0B: Opcode(0x0B, "RRC E", 2, 8, lambda: self._rrc(REG_E)),
            0x0C: Opcode(0x0C, "RRC H", 2, 8, lambda: self._rrc(REG_H)),
            0x0D: Opcode(0x0D, "RRC L", 2, 8, lambda: self._rrc(REG_L)),
            0x0E: Opcode(0x0E, "RRC HL", 2, 16),
            0x0F: Opcode(0x0F, "RRC A", 2, 8, lambda: self._rrc(REG_A)),
            0x10: Opcode(0x10, "RL B", 2, 8, lambda: self._rl(REG_B)),
            0x11: Opcode(0x11, "RL C", 2, 8, lambda: self._rl(REG_C)),
            0x12: Opcode(0x12, "RL D", 2, 8, lambda: self._rl(REG_D)),
            0x13: Opcode(0x13, "RL E", 2, 8, lambda: self._rl(REG_E)),
            0x14: Opcode(0x14, "RL H", 2, 8, lambda: self._rl(REG_H)),
            0x15: Opcode(0x15, "RL L", 2, 8, lambda: self._rl(REG_L)),
            0x16: Opcode(0x16, "RL HL", 2, 16),
            0x17: Opcode(0x17, "RL A", 2, 8, lambda: self._rl(REG_A)),
            0x18: Opcode(0x18, "RR B", 2, 8, lambda: self._rr(REG_B)),
            0x19: Opcode(0x19, "RR C", 2, 8, lambda: self._rr(REG_C)),
            0x1A: Opcode(0x1A, "RR D", 2, 8, lambda: self._rr(REG_D)),
            0x1B: Opcode(0x1B, "RR E", 2, 8, lambda: self._rr(REG_E)),
            0x1C: Opcode(0x1C, "RR H", 2, 8, lambda: self._rr(REG_H)),
            0x1D: Opcode(0x1D, "RR L", 2, 8, lambda: self._rr(REG_L)),
            0x1E: Opcode(0x1E, "RR HL", 2, 16),
            0x1F: Opcode(0x1F, "RR A", 2, 8, lambda: self._rr(REG_A)),
            0x20: Opcode(0x20, "SLA B", 2, 8, lambda: self._sla(REG_B)),
            0x21: Opcode(0x21, "SLA C", 2, 8, lambda: self._sla(REG_C)),
            0x22: Opcode(0x22, "SLA D", 2, 8, lambda: self._sla(REG_D)),
            0x23: Opcode(0x23, "SLA E", 2, 8, lambda: self._sla(REG_E)),
            0x24: Opcode(0x24, "SLA H", 2, 8, lambda: self._sla(REG_H)),
            0x25: Opcode(0x25, "SLA L", 2, 8, lambda: self._sla(REG_L)),
            0x26: Opcode(0x26, "SLA HL", 2, 16),
            0x27: Opcode(0x27, "SLA A", 2, 8, lambda: self._sla(REG_A)),
            0x28: Opcode(0x28, "SRA B", 2, 8, lambda: self._sra(REG_B)),
            0x29: Opcode(0x29, "SRA C", 2, 8, lambda: self._sra(REG_C)),
            0x2A: Opcode(0x2A, "SRA D", 2, 8, lambda: self._sra(REG_D)),
            0x2B: Opcode(0x2B, "SRA E", 2, 8, lambda: self._sra(REG_E)),
            0x2C: Opcode(0x2C, "SRA H", 2, 8, lambda: self._sra(REG_H)),
            0x2D: Opcode(0x2D, "SRA L", 2, 8, lambda: self._sra(REG_L)),
            0x2E: Opcode(0x2E, "SRA HL", 2, 16),
            0x2F: Opcode(0x2F, "SRA A", 2, 8, lambda: self._sra(REG_A)),
            0x30: Opcode(0x30, "SWAP B", 2, 8, lambda: self._swap(REG_B)),
            0x31: Opcode(0x31, "SWAP C", 2, 8, lambda: self._swap(REG_C)),
            0x32: Opcode(0x32, "SWAP D", 2, 8, lambda: self._swap(REG_D)),
            0x33: Opcode(0x33, "SWAP E", 2, 8, lambda: self._swap(REG_E)),
            0x34: Opcode(0x34, "SWAP H", 2, 8, lambda: self._swap(REG_H)),
            0x35: Opcode(0x35, "SWAP L", 2, 8, lambda: self._swap(REG_L)),
            0x36: Opcode(0x36, "SWAP HL", 2, 16),
            0x37: Opcode(0x37, "SWAP A", 2, 8, lambda: self._swap(REG_A)),
            0x38: Opcode(0x38, "SRL B", 2, 8, lambda: self._srl(REG_B)),
            0x39: Opcode(0x39, "SRL C", 2, 8, lambda: self._srl(REG_C)),
            0x3A: Opcode(0x3A, "SRL D", 2, 8, lambda: self._srl(REG_D)),
            0x3B: Opcode(0x3B, "SRL E", 2, 8, lambda: self._srl(REG_E)),
            0x3C: Opcode(0x3C, "SRL H", 2, 8, lambda: self._srl(REG_H)),
            0x3D: Opcode(0x3D, "SRL L", 2, 8, lambda: self._srl(REG_L)),
            0x3E: Opcode(0x3E, "SRL HL", 2, 16),
            0x3F: Opcode(0x3F, "SRL A", 2, 8, lambda: self._srl(REG_A)),
            0x40: Opcode(0x40, "BIT 0 B", 2, 8, lambda: self._bit(REG_B, 0)),
            0x41: Opcode(0x41, "BIT 0 C", 2, 8, lambda: self._bit(REG_C, 0)),
            0x42: Opcode(0x42, "BIT 0 D", 2, 8, lambda: self._bit(REG_D, 0)),
            0x43: Opcode(0x43, "BIT 0 E", 2, 8, lambda: self._bit(REG_E, 0)),
            0x44: Opcode(0x44, "BIT 0 H", 2, 8, lambda: self._bit(REG_H, 0)),
            0x45: Opcode(0x45, "BIT 0 L", 2, 8, lambda: self._bit(REG_L, 0)),
            0x46: Opcode(0x46, "BIT 0 HL", 2, 12),
            0x47: Opcode(0x47, "BIT 0 A", 2, 8, lambda: self._bit(REG_A, 0)),
            0x48: Opcode(0x48, "BIT 1 B", 2, 8, lambda: self._bit(REG_B, 1)),
            0x49: Opcode(0x49, "BIT 1 C", 2, 8, lambda: self._bit(REG_C, 1)),
            0x4A: Opcode(0x4A, "BIT 1 D", 2, 8, lambda: self._bit(REG_D, 1)),
            0x4B: Opcode(0x4B, "BIT 1 E", 2, 8, lambda: self._bit(REG_E, 1)),
            0x4C: Opcode(0x4C, "BIT 1 H", 2, 8, lambda: self._bit(REG_H, 1)),
            0x4D: Opcode(0x4D, "BIT 1 L", 2, 8, lambda: self._bit(REG_L, 1)),
            0x4E: Opcode(0x4E, "BIT 1 HL", 2, 12),
            0x4F: Opcode(0x4F, "BIT 1 A", 2, 8, lambda: self._bit(REG_A, 1)),
            0x50: Opcode(0x50, "BIT 2 B", 2, 8, lambda: self._bit(REG_B, 2)),
            0x51: Opcode(0x51, "BIT 2 C", 2, 8, lambda: self._bit(REG_C, 2)),
            0x52: Opcode(0x52, "BIT 2 D", 2, 8, lambda: self._bit(REG_D, 2)),
            0x53: Opcode(0x53, "BIT 2 E", 2, 8, lambda: self._bit(REG_E, 2)),
            0x54: Opcode(0x54, "BIT 2 H", 2, 8, lambda: self._bit(REG_H, 2)),
            0x55: Opcode(0x55, "BIT 2 L", 2, 8, lambda: self._bit(REG_L, 2)),
            0x56: Opcode(0x56, "BIT 2 HL", 2, 12),
            0x57: Opcode(0x57, "BIT 2 A", 2, 8, lambda: self._bit(REG_A, 2)),
            0x58: Opcode(0x58, "BIT 3 B", 2, 8, lambda: self._bit(REG_B, 3)),
            0x59: Opcode(0x59, "BIT 3 C", 2, 8, lambda: self._bit(REG_C, 3)),
            0x5A: Opcode(0x5A, "BIT 3 D", 2, 8, lambda: self._bit(REG_D, 3)),
            0x5B: Opcode(0x5B, "BIT 3 E", 2, 8, lambda: self._bit(REG_E, 3)),
            0x5C: Opcode(0x5C, "BIT 3 H", 2, 8, lambda: self._bit(REG_H, 3)),
            0x5D: Opcode(0x5D, "BIT 3 L", 2, 8, lambda: self._bit(REG_L, 3)),
            0x5E: Opcode(0x5E, "BIT 3 HL", 2, 12),
            0x5F: Opcode(0x5F, "BIT 3 A", 2, 8, lambda: self._bit(REG_A, 3)),
            0x60: Opcode(0x60, "BIT 4 B", 2, 8, lambda: self._bit(REG_B, 4)),
            0x61: Opcode(0x61, "BIT 4 C", 2, 8, lambda: self._bit(REG_C, 4)),
            0x62: Opcode(0x62, "BIT 4 D", 2, 8, lambda: self._bit(REG_D, 4)),
            0x63: Opcode(0x63, "BIT 4 E", 2, 8, lambda: self._bit(REG_E, 4)),
            0x64: Opcode(0x64, "BIT 4 H", 2, 8, lambda: self._bit(REG_H, 4)),
            0x65: Opcode(0x65, "BIT 4 L", 2, 8, lambda: self._bit(REG_L, 4)),
            0x66: Opcode(0x66, "BIT 4 HL", 2, 12),
            0x67: Opcode(0x67, "BIT 4 A", 2, 8, lambda: self._bit(REG_A, 4)),
            0x68: Opcode(0x68, "BIT 5 B", 2, 8, lambda: self._bit(REG_B, 5)),
            0x69: Opcode(0x69, "BIT 5 C", 2, 8, lambda: self._bit(REG_C, 5)),
            0x6A: Opcode(0x6A, "BIT 5 D", 2, 8, lambda: self._bit(REG_D, 5)),
            0x6B: Opcode(0x6B, "BIT 5 E", 2, 8, lambda: self._bit(REG_E, 5)),
            0x6C: Opcode(0x6C, "BIT 5 H", 2, 8, lambda: self._bit(REG_H, 5)),
            0x6D: Opcode(0x6D, "BIT 5 L", 2, 8, lambda: self._bit(REG_L, 5)),
            0x6E: Opcode(0x6E, "BIT 5 HL", 2, 12),
            0x6F: Opcode(0x6F, "BIT 5 A", 2, 8, lambda: self._bit(REG_A, 5)),
            0x70: Opcode(0x70, "BIT 6 B", 2, 8, lambda: self._bit(REG_B, 6)),
            0x71: Opcode(0x71, "BIT 6 C", 2, 8, lambda: self._bit(REG_C, 6)),
            0x72: Opcode(0x72, "BIT 6 D", 2, 8, lambda: self._bit(REG_D, 6)),
            0x73: Opcode(0x73, "BIT 6 E", 2, 8, lambda: self._bit(REG_E, 6)),
            0x74: Opcode(0x74, "BIT 6 H", 2, 8, lambda: self._bit(REG_H, 6)),
            0x75: Opcode(0x75, "BIT 6 L", 2, 8, lambda: self._bit(REG_L, 6)),
            0x76: Opcode(0x76, "BIT 6 HL", 2, 12),
            0x77: Opcode(0x77, "BIT 6 A", 2, 8, lambda: self._bit(REG_A, 6)),
            0x78: Opcode(0x78, "BIT 7 B", 2, 8, lambda: self._bit(REG_B, 7)),
            0x79: Opcode(0x79, "BIT 7 C", 2, 8, lambda: self._bit(REG_C, 7)),
            0x7A: Opcode(0x7A, "BIT 7 D", 2, 8, lambda: self._bit(REG_D, 7)),
            0x7B: Opcode(0x7B, "BIT 7 E", 2, 8, lambda: self._bit(REG_E, 7)),
            0x7C: Opcode(0x7C, "BIT 7 H", 2, 8, lambda: self._bit(REG_H, 7)),
            0x7D: Opcode(0x7D, "BIT 7 L", 2, 8, lambda: self._bit(REG_L, 7)),
            0x7E: Opcode(0x7E, "BIT 7 HL", 2, 12),
            0x7F: Opcode(0x7F, "BIT 7 A", 2, 8, lambda: self._bit(REG_A, 7)),
            0x80: Opcode(0x80, "RES 0 B", 2, 8, lambda: self._res(REG_B, 0)),
            0x81: Opcode(0x81, "RES 0 C", 2, 8, lambda: self._res(REG_C, 0)),
            0x82: Opcode(0x82, "RES 0 D", 2, 8, lambda: self._res(REG_D, 0)),
            0x83: Opcode(0x83, "RES 0 E", 2, 8, lambda: self._res(REG_E, 0)),
            0x84: Opcode(0x84, "RES 0 H", 2, 8, lambda: self._res(REG_H, 0)),
            0x85: Opcode(0x85, "RES 0 L", 2, 8, lambda: self._res(REG_L, 0)),
            0x86: Opcode(0x86, "RES 0 HL", 2, 16),
            0x87: Opcode(0x87, "RES 0 A", 2, 8, lambda: self._res(REG_A, 0)),
            0x88: Opcode(0x88, "RES 1 B", 2, 8, lambda: self._res(REG_B, 1)),
            0x89: Opcode(0x89, "RES 1 C", 2, 8, lambda: self._res(REG_C, 1)),
            0x8A: Opcode(0x8A, "RES 1 D", 2, 8, lambda: self._res(REG_D, 1)),
            0x8B: Opcode(0x8B, "RES 1 E", 2, 8, lambda: self._res(REG_E, 1)),
            0x8C: Opcode(0x8C, "RES 1 H", 2, 8, lambda: self._res(REG_H, 1)),
            0x8D: Opcode(0x8D, "RES 1 L", 2, 8, lambda: self._res(REG_L, 1)),
            0x8E: Opcode(0x8E, "RES 1 HL", 2, 16),
            0x8F: Opcode(0x8F, "RES 1 A", 2, 8, lambda: self._res(REG_A, 1)),
            0x90: Opcode(0x90, "RES 2 B", 2, 8, lambda: self._res(REG_B, 2)),
            0x91: Opcode(0x91, "RES 2 C", 2, 8, lambda: self._res(REG_C, 2)),
            0x92: Opcode(0x92, "RES 2 D", 2, 8, lambda: self._res(REG_D, 2)),
            0x93: Opcode(0x93, "RES 2 E", 2, 8, lambda: self._res(REG_E, 2)),
            0x94: Opcode(0x94, "RES 2 H", 2, 8, lambda: self._res(REG_H, 2)),
            0x95: Opcode(0x95, "RES 2 L", 2, 8, lambda: self._res(REG_L, 2)),
            0x96: Opcode(0x96, "RES 2 HL", 2, 16),
            0x97: Opcode(0x97, "RES 2 A", 2, 8, lambda: self._res(REG_A, 2)),
            0x98: Opcode(0x98, "RES 3 B", 2, 8, lambda: self._res(REG_B, 3)),
            0x99: Opcode(0x99, "RES 3 C", 2, 8, lambda: self._res(REG_C, 3)),
            0x9A: Opcode(0x9A, "RES 3 D", 2, 8, lambda: self._res(REG_D, 3)),
            0x9B: Opcode(0x9B, "RES 3 E", 2, 8, lambda: self._res(REG_E, 3)),
            0x9C: Opcode(0x9C, "RES 3 H", 2, 8, lambda: self._res(REG_H, 3)),
            0x9D: Opcode(0x9D, "RES 3 L", 2, 8, lambda: self._res(REG_L, 3)),
            0x9E: Opcode(0x9E, "RES 3 HL", 2, 16),
            0x9F: Opcode(0x9F, "RES 3 A", 2, 8, lambda: self._res(REG_A, 3)),
            0xA0: Opcode(0xA0, "RES 4 B", 2, 8, lambda: self._res(REG_B, 4)),
            0xA1: Opcode(0xA1, "RES 4 C", 2, 8, lambda: self._res(REG_C, 4)),
            0xA2: Opcode(0xA2, "RES 4 D", 2, 8, lambda: self._res(REG_D, 4)),
            0xA3: Opcode(0xA3, "RES 4 E", 2, 8, lambda: self._res(REG_E, 4)),
            0xA4: Opcode(0xA4, "RES 4 H", 2, 8, lambda: self._res(REG_H, 4)),
            0xA5: Opcode(0xA5, "RES 4 L", 2, 8, lambda: self._res(REG_L, 4)),
            0xA6: Opcode(0xA6, "RES 4 HL", 2, 16),
            0xA7: Opcode(0xA7, "RES 4 A", 2, 8, lambda: self._res(REG_A, 4)),
            0xA8: Opcode(0xA8, "RES 5 B", 2, 8, lambda: self._res(REG_B, 5)),
            0xA9: Opcode(0xA9, "RES 5 C", 2, 8, lambda: self._res(REG_C, 5)),
            0xAA: Opcode(0xAA, "RES 5 D", 2, 8, lambda: self._res(REG_D, 5)),
            0xAB: Opcode(0xAB, "RES 5 E", 2, 8, lambda: self._res(REG_E, 5)),
            0xAC: Opcode(0xAC, "RES 5 H", 2, 8, lambda: self._res(REG_H, 5)),
            0xAD: Opcode(0xAD, "RES 5 L", 2, 8, lambda: self._res(REG_L, 5)),
            0xAE: Opcode(0xAE, "RES 5 HL", 2, 16),
            0xAF: Opcode(0xAF, "RES 5 A", 2, 8, lambda: self._res(REG_A, 5)),
            0xB0: Opcode(0xB0, "RES 6 B", 2, 8, lambda: self._res(REG_B, 6)),
            0xB1: Opcode(0xB1, "RES 6 C", 2, 8, lambda: self._res(REG_C, 6)),
            0xB2: Opcode(0xB2, "RES 6 D", 2, 8, lambda: self._res(REG_D, 6)),
            0xB3: Opcode(0xB3, "RES 6 E", 2, 8, lambda: self._res(REG_E, 6)),
            0xB4: Opcode(0xB4, "RES 6 H", 2, 8, lambda: self._res(REG_H, 6)),
            0xB5: Opcode(0xB5, "RES 6 L", 2, 8, lambda: self._res(REG_L, 6)),
            0xB6: Opcode(0xB6, "RES 6 HL", 2, 16),
            0xB7: Opcode(0xB7, "RES 6 A", 2, 8, lambda: self._res(REG_A, 6)),
            0xB8: Opcode(0xB8, "RES 7 B", 2, 8, lambda: self._res(REG_B, 7)),
            0xB9: Opcode(0xB9, "RES 7 C", 2, 8, lambda: self._res(REG_C, 7)),
            0xBA: Opcode(0xBA, "RES 7 D", 2, 8, lambda: self._res(REG_D, 7)),
            0xBB: Opcode(0xBB, "RES 7 E", 2, 8, lambda: self._res(REG_E, 7)),
            0xBC: Opcode(0xBC, "RES 7 H", 2, 8, lambda: self._res(REG_H, 7)),
            0xBD: Opcode(0xBD, "RES 7 L", 2, 8, lambda: self._res(REG_L, 7)),
            0xBE: Opcode(0xBE, "RES 7 HL", 2, 16),
            0xBF: Opcode(0xBF, "RES 7 A", 2, 8, lambda: self._res(REG_A, 7)),
            0xC0: Opcode(0xC0, "SET 0 B", 2, 8),
            0xC1: Opcode(0xC1, "SET 0 C", 2, 8),
            0xC2: Opcode(0xC2, "SET 0 D", 2, 8),
            0xC3: Opcode(0xC3, "SET 0 E", 2, 8),
            0xC4: Opcode(0xC4, "SET 0 H", 2, 8),
            0xC5: Opcode(0xC5, "SET 0 L", 2, 8),
            0xC6: Opcode(0xC6, "SET 0 HL", 2, 16),
            0xC7: Opcode(0xC7, "SET 0 A", 2, 8),
            0xC8: Opcode(0xC8, "SET 1 B", 2, 8),
            0xC9: Opcode(0xC9, "SET 1 C", 2, 8),
            0xCA: Opcode(0xCA, "SET 1 D", 2, 8),
            0xCB: Opcode(0xCB, "SET 1 E", 2, 8),
            0xCC: Opcode(0xCC, "SET 1 H", 2, 8),
            0xCD: Opcode(0xCD, "SET 1 L", 2, 8),
            0xCE: Opcode(0xCE, "SET 1 HL", 2, 16),
            0xCF: Opcode(0xCF, "SET 1 A", 2, 8),
            0xD0: Opcode(0xD0, "SET 2 B", 2, 8),
            0xD1: Opcode(0xD1, "SET 2 C", 2, 8),
            0xD2: Opcode(0xD2, "SET 2 D", 2, 8),
            0xD3: Opcode(0xD3, "SET 2 E", 2, 8),
            0xD4: Opcode(0xD4, "SET 2 H", 2, 8),
            0xD5: Opcode(0xD5, "SET 2 L", 2, 8),
            0xD6: Opcode(0xD6, "SET 2 HL", 2, 16),
            0xD7: Opcode(0xD7, "SET 2 A", 2, 8),
            0xD8: Opcode(0xD8, "SET 3 B", 2, 8),
            0xD9: Opcode(0xD9, "SET 3 C", 2, 8),
            0xDA: Opcode(0xDA, "SET 3 D", 2, 8),
            0xDB: Opcode(0xDB, "SET 3 E", 2, 8),
            0xDC: Opcode(0xDC, "SET 3 H", 2, 8),
            0xDD: Opcode(0xDD, "SET 3 L", 2, 8),
            0xDE: Opcode(0xDE, "SET 3 HL", 2, 16),
            0xDF: Opcode(0xDF, "SET 3 A", 2, 8),
            0xE0: Opcode(0xE0, "SET 4 B", 2, 8),
            0xE1: Opcode(0xE1, "SET 4 C", 2, 8),
            0xE2: Opcode(0xE2, "SET 4 D", 2, 8),
            0xE3: Opcode(0xE3, "SET 4 E", 2, 8),
            0xE4: Opcode(0xE4, "SET 4 H", 2, 8),
            0xE5: Opcode(0xE5, "SET 4 L", 2, 8),
            0xE6: Opcode(0xE6, "SET 4 HL", 2, 16),
            0xE7: Opcode(0xE7, "SET 4 A", 2, 8),
            0xE8: Opcode(0xE8, "SET 5 B", 2, 8),
            0xE9: Opcode(0xE9, "SET 5 C", 2, 8),
            0xEA: Opcode(0xEA, "SET 5 D", 2, 8),
            0xEB: Opcode(0xEB, "SET 5 E", 2, 8),
            0xEC: Opcode(0xEC, "SET 5 H", 2, 8),
            0xED: Opcode(0xED, "SET 5 L", 2, 8),
            0xEE: Opcode(0xEE, "SET 5 HL", 2, 16),
            0xEF: Opcode(0xEF, "SET 5 A", 2, 8),
            0xF0: Opcode(0xF0, "SET 6 B", 2, 8),
            0xF1: Opcode(0xF1, "SET 6 C", 2, 8),
            0xF2: Opcode(0xF2, "SET 6 D", 2, 8),
            0xF3: Opcode(0xF3, "SET 6 E", 2, 8),
            0xF4: Opcode(0xF4, "SET 6 H", 2, 8),
            0xF5: Opcode(0xF5, "SET 6 L", 2, 8),
            0xF6: Opcode(0xF6, "SET 6 HL", 2, 16),
            0xF7: Opcode(0xF7, "SET 6 A", 2, 8),
            0xF8: Opcode(0xF8, "SET 7 B", 2, 8),
            0xF9: Opcode(0xF9, "SET 7 C", 2, 8),
            0xFA: Opcode(0xFA, "SET 7 D", 2, 8),
            0xFB: Opcode(0xFB, "SET 7 E", 2, 8),
            0xFC: Opcode(0xFC, "SET 7 H", 2, 8),
            0xFD: Opcode(0xFD, "SET 7 L", 2, 8),
            0xFE: Opcode(0xFE, "SET 7 HL", 2, 16),
            0xFF: Opcode(0xFF, "SET 7 A", 2, 8),
        }        
    
    def _rlc(self, reg):
        # rotate reg val to left (circular)
        val = getattr(self, reg)
        # rotate bits
        res = np.uint8((val << 1) | (val >> 7)) # type: ignore
        # clear flahs
        self.regs.f = 0
        if (not res): self.regs.f |= self.regs.ZERO_FLAG
        if (val & (1 << 7)) == (1 << 7): self.regs.f |= self.regs.CARRY_FLAG
        setattr(self, val, res)
    
    def _rrc(self, reg):
        # rotate reg val to right (circular)
        val = getattr(self, reg)
        # rotate bits
        res = np.uint8((val >> 1) | (val << 7)) # type: ignore
        # clear flahs
        self.regs.f = 0
        if (not res): self.regs.f |= self.regs.ZERO_FLAG
        if (val & 1) == 0x1: self.regs.f |= self.regs.CARRY_FLAG
        setattr(self, val, res)

    def _rl(self, reg): 
        # rotate left
        carry = 1 if self.regs.f & (1 << 4) else 0
        val = getattr(self, reg)
        # rotate bits
        res = np.uint8((val << 1) | carry) # type: ignore
        # clear flags
        self.regs.f = 0
        if (not res): self.regs.f |= self.regs.ZERO_FLAG
        if (val & (1 << 7)) == (1 << 7): self.regs.f |= self.regs.CARRY_FLAG
        setattr(self, val, res)

    def _rr(self, reg):
        # rotate left
        carry = (1 << 7) if self.regs.f & (1 << 4) else 0
        val = getattr(self, reg)
        # rotate bits
        res = np.uint8((val >> 1) | carry) # type: ignore
        # clear flags
        self.regs.f = 0
        if (not res): self.regs.f |= self.regs.ZERO_FLAG
        if (val & 0x1) == 0x1: self.regs.f |= self.regs.CARRY_FLAG
        setattr(self, val, res)
    
    def _sra(self, reg):
        # shift right arithmetic
        val = getattr(self, reg)
        # rotate bits
        res = np.uint8((val >> 1) | (val & 0x80)) # type: ignore
        # clear flags
        self.regs.f = 0
        if (not res): self.regs.f |= self.regs.ZERO_FLAG
        if (val & 0x1) == 0x1: self.regs.f |= self.regs.CARRY_FLAG
        setattr(self, val, res)

    def _sla(self, reg):
        # shift left arithmetic 
        val = getattr(self, reg)
        # rotate bits
        res = np.uint8(val << 1) # type: ignore
        # clear flags
        self.regs.f = 0
        if (not res): self.regs.f |= self.regs.ZERO_FLAG
        if (val & (1 << 7)) == (1 << 7): self.regs.f |= self.regs.CARRY_FLAG
        setattr(self, val, res)

    def _srl(self, reg):
        # shift right logical 
        val = getattr(self, reg)
        # rotate bits
        res = np.uint8(val >> 1) # type: ignore
        # clear flags
        self.regs.f = 0
        if (not res): self.regs.f |= self.regs.ZERO_FLAG
        if (val & 0x1) != 0x0: self.regs.f |= self.regs.CARRY_FLAG
        setattr(self, val, res)

    def _swap(self, reg):
        # swap nibbles
        val = getattr(self, reg)
        res = np.uint8(((val & 0xF0) >> 4) | ((val & 0x0F) << 4)) # type: ignore
        self.regs.f = 0
        if (not res): self.regs.f |= self.regs.ZERO_FLAG
        setattr(self, val, res)
    
    def _set(self, reg, pos):
        # set bit pos in reg val
        setattr(self, reg, getattr(self, reg) | (1 << pos))
    
    def _res(self, reg, pos):
        # reset bit pos in reg val
        setattr(self, reg, getattr(self, reg) & ~(1 << pos))
    
    def _bit(self, reg, pos):
        # test bit
        val = getattr(self, reg)
        self.regs.f |= self.regs.HALF_CARRY_FLAG
        if ((val >> pos) & 0x1) == 0: self.regs.f |= self.regs.ZERO_FLAG
        # turn off N
        self.regs.f &= ~(1 << 6)