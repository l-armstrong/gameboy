class Z80(object):
    def __init__(self):
        # Time clock
        # m and two are two clocks
        self._clock_m = 0
        self._clock_t = 0

        # Registers 
        # 8 bit regs
        self._r_a = 0
        self._r_b = 0
        self._r_c = 0
        self._r_d = 0
        self._r_e = 0
        self._r_h = 0
        self._r_l = 0
        # The f register is used for flags
        # calc. bits depending on the result of prev
        # operation
        # Zero (0x80): set if the last operation result is 0
        # Operation (0x40): Set if last operation was subtraction
        # Half-carry (0x20): Set if the last operation result overflowed past 15
        # Carry (0x10): Set if the last operation result was over 255 for adding or under 0 for sub.
        self._r_f = 0
        # 16 bit regs
        self._r_pc = 0
        self._r_sp = 0
        # Clock for last instruction
        self._r_m = 0
        self._r_t = 0
    
    def add_e_a(self):
        # Add register e to register a
        self._r_a += self._r_e
        # Clear flags
        self._r_f = 0
        # Check for zero
        if not (self._r_a & 255):
            self._r_f |= 0x80
        # Check for carry
        if self._r_a > 255:
            self._r_f |= 0x10
        # Mask to 8-bits
        self._r_a &= 255
        # Op. took 1 Machine cycle
        self._r_m = 1
        self._r_t = 4