class MMU(object):
    def __init__(self):
        pass

    def read_byte(self, addr):
        pass

    def read_word(self, addr):
        pass

    def write_byte(self, addr, val):
        pass

    def write_word(self, addr, val):
        pass

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
        self._pc = 0
        self._sp = 0
        # Clock for last instruction
        self._r_m = 0
        self._r_t = 0
    
    def reset(self):
        # Reset routine to restart CPU
        self._clock_t = self._clock_m = 0
        self._r_c = self._r_b = self._r_a = 0
        self._r_h = self._r_e = self._r_d = 0
        self._r_f = self._r_l = 0
        self._sp = self._pc = 0
        self._r_t = self._r_m = 0
    
    def nop(self):
        # NOP
        # 1 M-cycle
        self._r_m = 1
        self._r_t = 4
    
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
        # Op. took 4 t-states
        self._r_t = 4
    
    def cmp_b(self):
        # compare b to a, sett flags
        # get copy of A
        tmp = self._r_a
        # sub. B from tmp (reg. a)
        tmp -= self._r_b
        # Set sub flag
        self._r_f |= 0x40
        # check if result was zero
        if not (tmp & 255):
            self._r_f |= 0x80
        # check if result underflowed
        if tmp < 0:
            self._r_f |= 0x10
        # 1 M-cycle taken
        self._r_m = 1
        # 4 t-states
        self._r_t = 4
    
    def push_bc(self, mmu: MMU):
        # push reg b and c on stack
        # decrement sp to add reg b
        self._sp -= 1
        # write b to stack
        mmu.write_byte(self._sp, self._r_b)
        # decrement sp to add reg c
        self._sp -= 1
        # write c to stack
        mmu.write_byte(self._sp, self._r_c)
        # 3 M-cycles
        self._r_m = 3
        # 12 t-states
        self._r_t = 12
    
    def pop_hl(self, mmu: MMU):
        # pop values into reg h and l off stack
        # read in l
        self._r_l = mmu.read_byte(self._sp)
        # move up stack
        self._sp += 1
        # read in h
        self._r_h = mmu.read_byte(self._sp)
        # move up stack
        self._sp += 1
        # 3 M-cycles
        self._r_m = 3
        # 12 t-states
        self._r_t = 12
    
    def lda_nn(self, mmu: MMU):
        # Read a byte from address into reg a
        # read word
        addr = mmu.read_word(self._pc)
        # advance pc by 2 bytes
        self._pc += 2
        # read byte from address
        self._r_a = mmu.read_byte(addr)
        # 4 M-cycles 
        self._r_m = 4
        # 16 t-states
        self._r_t = 16
