class MMU(object):
    def __init__(self):
        # BIOS code is run upon CPU start
        self._bios = [
            0x31, 0xFE, 0xFF, 0xAF, 0x21, 0xFF, 0x9F, 0x32, 0xCB, 0x7C, 0x20, 0xFB, 0x21, 0x26, 0xFF, 0x0E,
            0x11, 0x3E, 0x80, 0x32, 0xE2, 0x0C, 0x3E, 0xF3, 0xE2, 0x32, 0x3E, 0x77, 0x77, 0x3E, 0xFC, 0xE0,
            0x47, 0x11, 0x04, 0x01, 0x21, 0x10, 0x80, 0x1A, 0xCD, 0x95, 0x00, 0xCD, 0x96, 0x00, 0x13, 0x7B,
            0xFE, 0x34, 0x20, 0xF3, 0x11, 0xD8, 0x00, 0x06, 0x08, 0x1A, 0x13, 0x22, 0x23, 0x05, 0x20, 0xF9,
            0x3E, 0x19, 0xEA, 0x10, 0x99, 0x21, 0x2F, 0x99, 0x0E, 0x0C, 0x3D, 0x28, 0x08, 0x32, 0x0D, 0x20,
            0xF9, 0x2E, 0x0F, 0x18, 0xF3, 0x67, 0x3E, 0x64, 0x57, 0xE0, 0x42, 0x3E, 0x91, 0xE0, 0x40, 0x04,
            0x1E, 0x02, 0x0E, 0x0C, 0xF0, 0x44, 0xFE, 0x90, 0x20, 0xFA, 0x0D, 0x20, 0xF7, 0x1D, 0x20, 0xF2,
            0x0E, 0x13, 0x24, 0x7C, 0x1E, 0x83, 0xFE, 0x62, 0x28, 0x06, 0x1E, 0xC1, 0xFE, 0x64, 0x20, 0x06,
            0x7B, 0xE2, 0x0C, 0x3E, 0x87, 0xF2, 0xF0, 0x42, 0x90, 0xE0, 0x42, 0x15, 0x20, 0xD2, 0x05, 0x20,
            0x4F, 0x16, 0x20, 0x18, 0xCB, 0x4F, 0x06, 0x04, 0xC5, 0xCB, 0x11, 0x17, 0xC1, 0xCB, 0x11, 0x17,
            0x05, 0x20, 0xF5, 0x22, 0x23, 0x22, 0x23, 0xC9, 0xCE, 0xED, 0x66, 0x66, 0xCC, 0x0D, 0x00, 0x0B,
            0x03, 0x73, 0x00, 0x83, 0x00, 0x0C, 0x00, 0x0D, 0x00, 0x08, 0x11, 0x1F, 0x88, 0x89, 0x00, 0x0E,
            0xDC, 0xCC, 0x6E, 0xE6, 0xDD, 0xDD, 0xD9, 0x99, 0xBB, 0xBB, 0x67, 0x63, 0x6E, 0x0E, 0xEC, 0xCC,
            0xDD, 0xDC, 0x99, 0x9F, 0xBB, 0xB9, 0x33, 0x3E, 0x3c, 0x42, 0xB9, 0xA5, 0xB9, 0xA5, 0x42, 0x4C,
            0x21, 0x04, 0x01, 0x11, 0xA8, 0x00, 0x1A, 0x13, 0xBE, 0x20, 0xFE, 0x23, 0x7D, 0xFE, 0x34, 0x20,
            0xF5, 0x06, 0x19, 0x78, 0x86, 0x23, 0x05, 0x20, 0xFB, 0x86, 0x20, 0xFE, 0x3E, 0x01, 0xE0, 0x50
        ]
        # BIOS is removed when ran 
        self._running_bios = True

        self._rom = []
        self._wram = []
        self._eram = []
        self._zram = []
    
    def load(self, rom):
        with open(rom, 'rb') as program:
            self._rom = program.read()

    
    def read_byte(self, addr):
        match addr & 0xF000:
            # bios 
            case 0x0000:
                if self._running_bios:
                    if addr < 0x100:
                      return self._bios[addr]
                    # TODO: comeback and fixed this
                    elif self._pc:
                        pass
                return self._rom[addr]  
            # ROM0
            case 0x1000 | 0x2000 | 0x3000:
                return self._rom[addr]
            # ROM1 cartridge ROM, different banks will be available
            # here 
            case 0x4000 | 0x5000 | 0x6000 | 0x7000:
                return self._rom[addr]
            # 2^13 = (8K) = 0x1FFF
            # Graphics VRAM (8K): Data required for the backgrounds and sprites
            case 0x8000 | 0x9000: 
                # TODO: come back and fix this
                return self._gpu_vram[addr & 0x1FFF]
            # External RAM (8K)
            case 0xA000 | 0xB000:
                return self._eram[addr & 0x1FFF]
            # Working RAM (8K)
            case 0xC000 | 0xD000:
                return self._wram[addr & 0x1FFF]
            # Working RAM shadow
            case 0xE000:
                return self._wram[addr & 0x1FFF]
            # Working RAM shadow
            case 0xF000:
                match addr & 0x0F00:
                    # Working RAM shadow
                    case 0x000 | 0x100 | 0x200 | 0x300:
                        return self._wram[addr & 0x1FFF]
                    case 0x400 | 0x500 | 0x600 | 0x700:
                        return self._wram[addr & 0x1FFF]
                    case 0x800 | 0x900 | 0xA00 | 0xB00:
                        return self._wram[addr & 0x1FFF]
                    case 0xC00 | 0xD00:
                        return self._wram[addr & 0x1FFF]
                    
                    # Graphcs: object attribute memory
                    # OAM is 160 bytes, 
                    case 0xE00:
                        if addr < 0xFEA0:
                            # TODO: come back to fix this 
                            return self.gru_oam[addr & 0xFF]
                        else:
                            return 0
                    # zero page
                    case 0xF00:
                        if addr >= 0xFF80:
                            return self._zram[addr & 0x7F]
                        else:
                            # IO unhandled.
                            return 0
                        
    def read_word(self, addr):
        return self.read_byte(addr) + (self.read_byte(addr + 1) << 8)

    def write_byte(self, addr, val):
        match addr & 0xF000:
            # bios 
            case 0x0000:
                if self._running_bios and addr < 0x0100:
                    return 
            # ROM0
            case 0x1000 | 0x2000 | 0x3000:
                return
            # ROM1 cartridge ROM, different banks will be available
            # here 
            case 0x4000 | 0x5000 | 0x6000 | 0x7000:
                return
            # 2^13 = (8K) = 0x1FFF
            # Graphics VRAM (8K): Data required for the backgrounds and sprites
            case 0x8000 | 0x9000: 
                # TODO: come back and fix this
                self._gpu_vram[addr & 0x1FFF] = val
                self._gpu_updatetile(addr & 0x1FFF, val)
            # External RAM (8K)
            case 0xA000 | 0xB000:
                self._eram[addr & 0x1FFF] = val
            # Working RAM (8K)
            case 0xC000 | 0xD000 | 0xE000:
                self._wram[addr & 0x1FFF] = val
            # Working RAM shadow
            case 0xF000:
                match addr & 0x0F00:
                    # Working RAM shadow
                    case 0x000 | 0x100 | 0x200 | 0x300:
                        self._wram[addr & 0x1FFF] = val
                    case 0x400 | 0x500 | 0x600 | 0x700:
                        self._wram[addr & 0x1FFF] = val
                    case 0x800 | 0x900 | 0xA00 | 0xB00:
                        self._wram[addr & 0x1FFF] = val
                    case 0xC00 | 0xD00:
                        self._wram[addr & 0x1FFF] = val
                    
                    # Graphcs: object attribute memory
                    # OAM is 160 bytes, 
                    case 0xE00:
                        if (addr & 0xFF) < 0xA0:
                            # TODO: come back to fix this 
                            self.gpu_oam[addr & 0xFF] = val 
                        self.gpu_update_oam(addr, val)
                    # zero page
                    case 0xF00:
                        if addr > 0xFF7F:
                            self._zram[addr&0xFF] = val
                        else:
                            pass 

    def write_word(self, addr, val):
        self.write_byte(addr, val & 255)
        self.write_byte(addr+1, val >> 8)

class Z80(object):
    def __init__(self, mmu: MMU):
        # Memory to interface with
        self.mmu = mmu
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

    def ldrr_nn(self, reg1, reg2):
        # load byte from reg 2 to 1
        setattr(self, reg1, getattr(self, reg2))
        # 1 M-Cycle
        self._r_m = 1
        self._r_t = 4
    
    # load byte to reg b from reg "X"
    def ldrr_bb(self): self.ldrr_nn("_r_b", "_r_b")
    def ldrr_bc(self): self.ldrr_nn("_r_b", "_r_c")
    def ldrr_bd(self): self.ldrr_nn("_r_b", "_r_d")
    def ldrr_be(self): self.ldrr_nn("_r_b", "_r_e")
    def ldrr_bh(self): self.ldrr_nn("_r_b", "_r_h")
    def ldrr_bl(self): self.ldrr_nn("_r_b", "_r_l")
    def ldrr_ba(self): self.ldrr_nn("_r_b", "_r_a")

    # load byte to reg c from reg "X"
    def ldrr_cb(self): self.ldrr_nn("_r_c", "_r_b")
    def ldrr_cc(self): self.ldrr_nn("_r_c", "_r_c")
    def ldrr_cd(self): self.ldrr_nn("_r_c", "_r_d")
    def ldrr_ce(self): self.ldrr_nn("_r_c", "_r_e")
    def ldrr_ch(self): self.ldrr_nn("_r_c", "_r_h")
    def ldrr_cl(self): self.ldrr_nn("_r_c", "_r_l")
    def ldrr_ca(self): self.ldrr_nn("_r_c", "_r_a")

    # load byte to reg d from reg "X"
    def ldrr_db(self): self.ldrr_nn("_r_d", "_r_b")
    def ldrr_dc(self): self.ldrr_nn("_r_d", "_r_c")
    def ldrr_dd(self): self.ldrr_nn("_r_d", "_r_d")
    def ldrr_de(self): self.ldrr_nn("_r_d", "_r_e")
    def ldrr_dh(self): self.ldrr_nn("_r_d", "_r_h")
    def ldrr_dl(self): self.ldrr_nn("_r_d", "_r_l")
    def ldrr_da(self): self.ldrr_nn("_r_d", "_r_a")

    # load byte to reg e from reg "X"
    def ldrr_eb(self): self.ldrr_nn("_r_e", "_r_b")
    def ldrr_ec(self): self.ldrr_nn("_r_e", "_r_c")
    def ldrr_ed(self): self.ldrr_nn("_r_e", "_r_d")
    def ldrr_ee(self): self.ldrr_nn("_r_e", "_r_e")
    def ldrr_eh(self): self.ldrr_nn("_r_e", "_r_h")
    def ldrr_el(self): self.ldrr_nn("_r_e", "_r_l")
    def ldrr_ea(self): self.ldrr_nn("_r_e", "_r_a")

    # load byte to reg h from reg "X"
    def ldrr_hb(self): self.ldrr_nn("_r_h", "_r_b")
    def ldrr_hc(self): self.ldrr_nn("_r_h", "_r_c")
    def ldrr_hd(self): self.ldrr_nn("_r_h", "_r_d")
    def ldrr_he(self): self.ldrr_nn("_r_h", "_r_e")
    def ldrr_hh(self): self.ldrr_nn("_r_h", "_r_h")
    def ldrr_hl(self): self.ldrr_nn("_r_h", "_r_l")
    def ldrr_ha(self): self.ldrr_nn("_r_h", "_r_a")

    # load byte to reg l from reg "X"
    def ldrr_lb(self): self.ldrr_nn("_r_l", "_r_b")
    def ldrr_lc(self): self.ldrr_nn("_r_l", "_r_c")
    def ldrr_ld(self): self.ldrr_nn("_r_l", "_r_d")
    def ldrr_le(self): self.ldrr_nn("_r_l", "_r_e")
    def ldrr_lh(self): self.ldrr_nn("_r_l", "_r_h")
    def ldrr_ll(self): self.ldrr_nn("_r_l", "_r_l")
    def ldrr_la(self): self.ldrr_nn("_r_l", "_r_a")

    # load byte to reg a from reg "X"
    def ldrr_ab(self): self.ldrr_nn("_r_a", "_r_b")
    def ldrr_ac(self): self.ldrr_nn("_r_a", "_r_c")
    def ldrr_ad(self): self.ldrr_nn("_r_a", "_r_d")
    def ldrr_ae(self): self.ldrr_nn("_r_a", "_r_e")
    def ldrr_ah(self): self.ldrr_nn("_r_a", "_r_h")
    def ldrr_al(self): self.ldrr_nn("_r_a", "_r_l")
    def ldrr_aa(self): self.ldrr_nn("_r_a", "_r_a")

    # Load to the 8-bit register r, the immediate data n.
    def ldr_n(self, reg1):
        setattr(self, reg1, self.mmu.read_byte(self._pc))
        self._pc += 1
        # 2 M-Cycle
        self._r_m = 2
        # 8 T-Cycles
        self._r_t = 8
    
    def ldr_b(self): self.ldr_n("_r_b")
    def ldr_c(self): self.ldr_n("_r_c")
    def ldr_d(self): self.ldr_n("_r_d")
    def ldr_e(self): self.ldr_n("_r_e")
    def ldr_h(self): self.ldr_n("_r_h")
    def ldr_l(self): self.ldr_n("_r_l")
    def ldr_a(self): self.ldr_n("_r_a")

    
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
        # read byte from address into reg a
        self._r_a = mmu.read_byte(addr)
        # 4 M-cycles 
        self._r_m = 4
        # 16 t-states
        self._r_t = 16
