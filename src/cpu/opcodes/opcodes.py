class Opcode(object):
    def __init__(self, code, mnemonic, length, tcycles, instructions):
        self.code = code
        self.mnemonic = mnemonic
        self.length = length
        self.tcycles = tcycles
        self.mcycles = tcycles // 4
        self.instructions = instructions
