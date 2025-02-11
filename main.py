import pygame
import numpy as np

class GPU(object):
    def __init__(self):
        self.screen = None
        self.surface = None
        self.pixels = None

        self._mode = 0
        self._modeclock = 0
        self._line = 0
    
    def reset(self):
        pygame.init()
        self.screen = pygame.display.set_mode((160,144))
        self.surface = pygame.Surface((160,144), pygame.SRCALPHA)
        # set all pixels to white
        self.pixels = np.full((144, 160, 4), (255, 255, 255, 255), dtype=np.uint8)
        self.update_surface()
    
    def update_surface(self):
        # blit array doesn't support alpha
        rgb_pixels = np.transpose(self.pixels[:, :, :3], (1,0,2))
        pygame.surfarray.blit_array(self.surface, rgb_pixels)
        # contruct alpha channel manually 
        alpha_surface = self.surface.copy()
        alpha_surface.fill((0, 0, 0, 0))
        for y in range(144):
            for x in range(160):
                r, g, b, a = self.pixels[y, x]
                alpha_surface.set_at((x, y), (r,g,b,a))
        # pygame.surfarray.blit_array(alpha_surface, self.pixels)
        self.screen.blit(alpha_surface, (0, 0))
        pygame.display.flip()
    
    def set_pixel(self, x, y, color):
        if 0 <= x < 160 and 0 <= y < 144:
            self.pixels[y, x] = color
            self.update_surface()
    
    def render_scan(self): pass

    def step(self):
        self._modeclock += z80._r_t
        match self._mode:
            case 2:
                if self._modeclock >= 80:
                    self._modeclock = 0
                    self._mode = 3
            case 3:
                if self._modeclock >= 172:
                    self._modeclock = 0
                    self._mode = 0
                    self.render_scan()
            case 0:
                if self._modeclock >= 204:
                    self._modeclock = 0
                    self._line += 1

                    if self._line == 143:
                        self._mode = 1
                        pygame.display.flip()
                    else:
                        self._mode = 2
            case 1:
                if self._modeclock >= 456:
                    self._modeclock = 0
                    self._line += 1

                    if self._line > 153:
                        self._mode = 2
                        self._line = 0


class MMU(object):
    def __init__(self, rom):
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
        
        self.load(rom)
        self._wram = [0] * (8192)
        self._eram = [0] * (8192)
        self._zram = [0] * (128) # Off by one?
    
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
                    elif z80._pc == 0x100:
                        self._running_bios = False
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
                            self._zram[addr & 0x7F] = val
                        else:
                            pass 

    def write_word(self, addr, val):
        self.write_byte(addr, val & 255)
        self.write_byte(addr+1, val >> 8)

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
        self.ZERO_FLAG = 0x80
        self.SUB_FLAG = 0x40
        self.HALF_CARRY_FLAG = 0x20
        self.CARRY_FLAG = 0x10
        # 16 bit regs
        self._pc = 0
        self._sp = 0
        # Clock for last instruction
        self._r_m = 0
        self._r_t = 0
        # TODO: should this be 1?
        self._ime = 0

    def reset(self):
        # Reset routine to restart CPU
        self._clock_t = self._clock_m = 0
        self._r_c = self._r_b = self._r_a = 0
        self._r_h = self._r_e = self._r_d = 0
        self._r_f = self._r_l = 0
        self._sp = self._pc = 0
        self._r_t = self._r_m = 0
        self._ime = 1
    
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
        setattr(self, reg1, mmu.read_byte(self._pc))
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

    # Load to the 8-bit register r, data from the absolute address specified 
    #   by the 16-bit register HL
    def ldr_hl(self, reg):
        setattr(self, reg, mmu.read_byte((self._r_h << 8) + self._r_l))
        self._r_m = 2
        self._r_t = 8
    
    def ldb_hl(self): self.ldr_hl("_r_b")
    def ldc_hl(self): self.ldr_hl("_r_c")
    def ldd_hl(self): self.ldr_hl("_r_d")
    def lde_hl(self): self.ldr_hl("_r_e")
    def ldh_hl(self): self.ldr_hl("_r_h")
    def ldl_hl(self): self.ldr_hl("_r_l")
    def lda_hl(self): self.ldr_hl("_r_a")

    # Load to the absolute address specified by the 16-bit register HL, data 
    #   from the 8-bit register r. 
    def ldhl_r(self, reg):
        mmu.write_byte((self._r_h << 8) + self._r_l, getattr(self, reg))
        self._r_m = 2
        self._r_t = 8
    
    def ldhl_b(self): self.ldhl_r("_r_b")
    def ldhl_c(self): self.ldhl_r("_r_c")
    def ldhl_d(self): self.ldhl_r("_r_d")
    def ldhl_e(self): self.ldhl_r("_r_e")
    def ldhl_h(self): self.ldhl_r("_r_h")
    def ldhl_l(self): self.ldhl_r("_r_l")
    def ldhl_a(self): self.ldhl_r("_r_a")

    # Load to the absolute address specified by the 16-bit register HL, the immediate data n
    def ldhl_n(self):
        mmu.write_byte((self._r_h << 8) + self._r_l, mmu.read_byte(self._pc))
        self._pc += 1
        self._r_m = 3
        self._r_t = 12
    
    # Load to the 8-bit A register, data from the absolute address specified by the 16-bit register BC.
    def lda_bc(self):
        self._r_a = mmu.read_byte((self._r_b << 8) + self._r_c)
        self._r_m = 2
        self._r_t = 8
    
    # Load to the 8-bit A register, data from the absolute address specified by the 16-bit register DE.
    def lda_de(self):
        self._r_a = mmu.read_byte((self._r_d << 8) + self._r_e)
        self._r_m = 2
        self._r_t = 8

    # Load to the absolute address specified by the 16-bit register BC, data from the 8-bit A register
    def ldbc_a(self):
        mmu.write_byte((self._r_b << 8) + self._r_c, self._r_a)
        self._r_m = 2
        self._r_t = 8
    
    # Load to the absolute address specified by the 16-bit register DE, data from the 8-bit A register
    def ldde_a(self):
        mmu.write_byte((self._r_d << 8) + self._r_e, self._r_a)
        self._r_m = 2
        self._r_t = 8

    # Load to the 8-bit A register, data from the absolute address specified by the 16-bit operand nn.
    def lda_nn(self):
        self._r_a = mmu.read_byte(mmu.read_word(self._pc))
        self._pc += 2
        self._r_m = 4
        self._r_t = 16

    # Load to the absolute address specified by the 16-bit operand nn, data from the 8-bit A register.
    def ldnn_a(self):
        mmu.write_byte(mmu.read_word(self._pc), self._r_a)
        self._pc += 2
        self._r_m = 4
        self._r_t = 16
    
    # Load to the 8-bit A register, data from the address specified by the 8-bit C register. The full
    # 16-bit absolute address is obtained by setting the most significant byte to 0xFF and the least
    # significant byte to the value of C, so the possible range is 0xFF00-0xFFFF
    def ldha_c(self):
        self._r_a = mmu.read_byte(0xFF00 + self._r_c)
        self._r_m = 2
        self._r_t = 8
    
    # Load to the address specified by the 8-bit C register, data from the 8-bit A register. The full
    # 16-bit absolute address is obtained by setting the most significant byte to 0xFF and the least
    # significant byte to the value of C, so the possible range is 0xFF00-0xFFFF.
    def ldhc_a(self):
        mmu.write_byte(0xFF00 + self._r_c, self._r_a)
        self._r_m = 2
        self._r_t = 8

    # Load to the 8-bit A register, data from the address specified by the 8-bit immediate data n. The
    # full 16-bit absolute address is obtained by setting the most significant byte to 0xFF and the
    # least significant byte to the value of n, so the possible range is 0xFF00-0xFFFF.
    def ldha_n(self):
        self._r_a = mmu.read_byte(0xFF00 + mmu.read_byte(self._pc))
        self._pc += 1
        self._r_m = 3
        self._r_t = 12
    
    # Load to the address specified by the 8-bit immediate data n, data from the 8-bit A register. The
    # full 16-bit absolute address is obtained by setting the most significant byte to 0xFF and the
    # least significant byte to the value of n, so the possible range is 0xFF00-0xFFFF.
    def ldhn_a(self):
        mmu.write_byte(0xFF00 + mmu.read_byte(self._pc), self._r_a)
        self._pc += 1
        self._r_m = 3
        self._r_t = 12

    # Load to the 8-bit A register, data from the absolute address specified by the 16-bit register HL.
    # The value of HL is decremented after the memory read.
    def lda_hl_dec(self):
        self._r_a = mmu.read_byte((self._r_h << 8) + self._r_l)
        self._r_l = (self._r_l - 1) & 0xFF
        # check for underflow
        if self._r_l == 255:
            self._r_h = (self._r_h - 1) & 0xFF
        self._r_m = 2
        self._r_t = 8
    
    # Load to the absolute address specified by the 16-bit register HL, data from the 8-bit A register.
    # The value of HL is decremented after the memory write.
    def ldhl_a_dec(self):
        mmu.write_byte((self._r_h << 8) + self._r_l, self._r_a)
        self._r_l = (self._r_l - 1) & 0xFF
        # check for underflow
        if self._r_l == 255:
            self._r_h = (self._r_h - 1) & 0xFF
        self._r_m = 2
        self._r_t = 8

    # Load to the 8-bit A register, data from the absolute address specified by the 16-bit register HL.
    # The value of HL is incremented after the memory read
    def lda_hl_inc(self):
        self._r_a = mmu.read_byte((self._r_h << 8) + self._r_l)
        self._r_l = (self._r_l + 1) & 0xFF
        # check for overflow
        if self._r_l == 0:
            self._r_h = (self._r_h + 1) & 0xFF
        self._r_m = 2
        self._r_t = 8

    # Load to the absolute address specified by the 16-bit register HL, data from the 8-bit A register.
    # The value of HL is decremented after the memory write.
    def ldhl_a_inc(self):
        mmu.write_byte((self._r_h << 8) + self._r_l, self._r_a)
        self._r_l = (self._r_l + 1) & 0xFF
        # check for overflow
        if self._r_l == 255:
            self._r_h = (self._r_h + 1) & 0xFF
        self._r_m = 2
        self._r_t = 8    

    # Load to the 16-bit register rr, the immediate 16-bit data nn.
    def ldrr_nn(self, lower_reg, upper_reg):
        setattr(self, lower_reg, mmu.read_byte(self._pc))
        setattr(self, upper_reg, mmu.read_byte(self._pc + 1))
        self._pc += 2
        self._r_m = 3
        self._r_t = 12
    
    def ldrr_bc(self): self.ldrr_nn("_r_c", "_r_b")
    def ldrr_de(self): self.ldrr_nn("_r_e", "_r_d")
    def ldrr_hl(self): self.ldrr_nn("_r_l", "_r_h")

    def ldrr_sp(self):
        self._sp = mmu.read_word(self._pc)
        self._pc += 2
        self._r_m = 3
        self._r_t = 12
    
    # Load to the absolute address specified by the 16-bit operand nn, data from the 16-bit SP register
    def ld_16_pc(self):
        nn = mmu.read_word(self._pc)
        self._pc += 2
        mmu.write_word(nn, self._sp)
        self._r_m = 5
        self._r_t = 20
        
    # Load to the 16-bit SP register, data from the 16-bit HL register.
    def ld_sp_hl(self):
        # TODO: check if this is correct
        self._sp = mmu.read_word((self._r_h << 8) + self._r_l)
        self._r_m = 2
        self._r_t = 8

    # Push to the stack memory, data from the 16-bit register rr
    def push_rr(self, upper, lower):
        self._sp -= 1
        mmu.write_byte(self._sp, getattr(self, upper))
        self._sp -= 1
        mmu.write_byte(self._sp, getattr(self, lower))
        # TODO: check if this is cycle accurate
        self._r_m = 4
        self._r_t = 16
    
    def push_bc(self): self.push_rr("_r_b", "_r_c")
    def push_de(self): self.push_rr("_r_d", "_r_e")
    def push_hl(self): self.push_rr("_r_h", "_r_l")
    def push_af(self): self.push_rr("_r_a", "_r_f")

    # Pops to the 16-bit register rr, data from the stack memory.
    def pop_rr(self, upper, lower):
        setattr(self, lower, mmu.read_byte(self._sp))
        self._sp += 1
        setattr(self, upper, mmu.read_byte(self._sp))
        self._sp += 1
        self._r_m = 3
        self._r_t = 12

    def pop_bc(self): self.pop_rr("_r_b", "_r_c")
    def pop_de(self): self.pop_rr("_r_d", "_r_e")
    def pop_hl(self): self.pop_rr("_r_h", "_r_l")
    def pop_af(self): self.pop_rr("_r_a", "_r_f")
    
    # Load to the HL register, 16-bit data calculated by adding the signed 8-bit operand e to the 16-
    #   bit value of the SP register.
    def ldhl_sp_e(self):
        e = mmu.read_byte(self._pc)
        if e > 127: e = -((~e + 1) & 255)
        e += self._sp
        self._r_h = (e >> 8) & 255
        self._r_l = (e & 255)
        self._pc += 1
        # TODO: update flags
        self._r_m = 3
        self._r_t = 12

    # Unconditional jump to the absolute address specified by the 16-bit immediate operand nn.
    def jp_nn(self):
        self._pc = mmu.read_word(self._pc)
        self._r_m = 3
        self._r_t = 12

    # Performs a bitwise XOR operation between the 8-bit A register and the 8-bit register r, and
    # stores the result back into the A register.
    def xor_r(self, reg):
        self._r_a = (self._r_a ^ getattr(self, reg)) & 255
        self._r_f = 0
        if not (self._r_a & 255):
            self._r_f |= 0x80
        self._r_m = 1
        self._r_t = 4
    
    def xor_b(self): self.xor_r('_r_b')
    def xor_c(self): self.xor_r('_r_c')
    def xor_d(self): self.xor_r('_r_d')
    def xor_e(self): self.xor_r('_r_e')
    def xor_h(self): self.xor_r('_r_h')
    def xor_l(self): self.xor_r('_r_l')
    def xor_a(self): self.xor_r('_r_a')

    # Decrements data in the 8-bit register r.
    def dec_r(self, reg):
        setattr(self, reg, (getattr(self, reg) - 1) & 255)
        self._r_f = 0
        # check for zero
        if (not getattr(self, reg)):
            self._r_f |= self.ZERO_FLAG
        # set sub flag
        self._r_f |= self.SUB_FLAG
        self._r_m = 1
        self._r_t = 4

    def dec_b(self): self.dec_r('_r_b')
    def dec_c(self): self.dec_r('_r_c')
    def dec_d(self): self.dec_r('_r_d')
    def dec_e(self): self.dec_r('_r_e')
    def dec_h(self): self.dec_r('_r_h')
    def dec_l(self): self.dec_r('_r_l')
    def dec_a(self): self.dec_r('_r_a')

    # Conditional jump to the relative address specified by the signed 8-bit operand e, depending on
    # the condition cc.
    # Note that the operand (relative address offset) is read even when the condition is false!
    def jrcc_e(self):
        e = mmu.read_byte(self._pc)
        # convert unsinged 8-bit value to signed (-128 to 127)
        if (e > 127): e = -((~e + 1) & 255)
        self._pc += 1
        self._r_m = 2
        self._r_t = 8

        if (not (self._r_f & self.ZERO_FLAG)):
            self._pc += e
            self._r_m += 1
            self._r_t += 4
    
    # Disables interrupt handling by setting IME=0 and cancelling any scheduled effects of the EI
    # instruction if any.
    def di(self):
        self._ime = 0
        self._r_m = 1
        self._r_t = 3

    # Subtracts from the 8-bit A register, the immediate data n, and updates flags based on the result.
    # This instruction is basically identical to SUB n, but does not update the A register.
    def cpn(self):
        c = self._r_a 
        c -= mmu.read_byte(self._pc)
        self._pc += 1
        self._r_f = 0
        self._r_f |= self.SUB_FLAG
        if (c < 0): self._r_f |= self.CARRY_FLAG
        # TODO: delete this?
        c &= 255
        self._r_m = 2
        self._r_t = 8


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


if __name__ == '__main__':
    mmu = MMU('Tetris.gb')
    z80 = Z80()
    gpu = GPU()
    gpu.reset()

    def not_implmented():
        print(f'${hex(op)} not implemented')
        exit(1)

    opcodes = [
    # 00
    z80.nop,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    z80.dec_b,
    z80.ldr_b,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    z80.dec_c,
    z80.ldr_c,
    not_implmented,

    # 10
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,

    # 20
    z80.jrcc_e,
    z80.ldrr_hl,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,

    # 30
    not_implmented,
    not_implmented,
    z80.ldhl_a_dec,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    z80.ldr_a,
    not_implmented,

    # 40
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,

    # 50
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,

    # 60
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,

    # 70
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,

    # 80
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,

    # 90
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,

    # a0
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    z80.xor_a,

    # b0
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,

    # c0
    not_implmented,
    not_implmented,
    not_implmented,
    z80.jp_nn,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,

    # d0
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,

    # e0
    z80.ldhn_a,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,

    # f0
    z80.ldha_n,
    not_implmented,
    not_implmented,
    z80.di,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    not_implmented,
    z80.cpn,
    not_implmented,
]
    c = 0
    # TODO: check pc, this may be wrong
    # print(len(mmu._bios))
    # exit(1)
    while True:
        op = mmu.read_byte(z80._pc)
        z80._pc += 1

        if z80._pc > 0x100:
            print(f'instr {hex(z80._pc - 1)} -- opcode: {hex(op)}')
            opcodes[op]()
            z80._pc &= 65535
            z80._clock_m += z80._r_m
            z80._clock_t += z80._r_t
            gpu.step()
            # c += 1
            # if c == 10: exit(1)