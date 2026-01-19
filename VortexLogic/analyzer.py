import pefile
import hashlib
import re
import datetime
from capstone import *

class BinaryCore:
    def __init__(self):
        self.pe = None
        self.raw = None
        self.path = ""

    def load(self, fpath):
        try:
            self.pe = pefile.PE(fpath)
            self.path = fpath
            with open(fpath, 'rb') as f:
                self.raw = f.read()
            return True
        except:
            return False

    def meta(self):
        if not self.pe: return {}
        h = self.pe.FILE_HEADER
        o = self.pe.OPTIONAL_HEADER
        return {
            "Machine": hex(h.Machine),
            "EntryPoint": hex(o.AddressOfEntryPoint),
            "ImageBase": hex(o.ImageBase),
            "Sections": h.NumberOfSections,
            "Built": datetime.datetime.fromtimestamp(h.TimeDateStamp).strftime('%Y-%m-%d %H:%M:%S'),
            "Subsystem": hex(o.Subsystem),
            "FileSize": f"{len(self.raw) / 1024:.2f} KB"
        }

    def hashes(self):
        if not self.raw: return {}
        return {
            "MD5": hashlib.md5(self.raw).hexdigest(),
            "SHA256": hashlib.sha256(self.raw).hexdigest()
        }

    def sections(self):
        if not self.pe: return []
        out = []
        for s in self.pe.sections:
            n = s.Name.decode(errors='ignore').strip('\x00')
            ent = s.get_entropy()
            out.append({
                "Name": n,
                "RVA": hex(s.VirtualAddress),
                "VSize": hex(s.Misc_VirtualSize),
                "RSize": hex(s.SizeOfRawData),
                "Entropy": ent
            })
        return out

    def strings(self, min_sz=4):
        if not self.raw: return []
        a = re.findall(b"[\x20-\x7e]{" + str(min_sz).encode() + b",}", self.raw)
        u = re.findall(b"(?:[\x20-\x7e]\x00){" + str(min_sz).encode() + b",}", self.raw)
        r = [x.decode(errors='ignore') for x in a] + [x.decode('utf-16', errors='ignore') for x in u]
        return r[:2000]

    def disassembly(self, limit=512):
        if not self.pe: return []
        ep = self.pe.OPTIONAL_HEADER.AddressOfEntryPoint
        base = self.pe.OPTIONAL_HEADER.ImageBase
        
        try:
            off = self.pe.get_offset_from_rva(ep)
        except:
            return []

        code = self.raw[off:off+2048]
        is_64 = self.pe.FILE_HEADER.Machine == 0x8664
        mode = CS_MODE_64 if is_64 else CS_MODE_32
        md = Cs(CS_ARCH_X86, mode)
        
        out = []
        count = 0
        for i in md.disasm(code, base + ep):
            if count >= limit: break
            b_str = " ".join(f"{b:02X}" for b in i.bytes)
            out.append({
                "addr": f"0x{i.address:X}",
                "bytes": b_str,
                "mnem": i.mnemonic,
                "op": i.op_str
            })
            count += 1
        return out

    def hexdump(self, size=1024):
        if not self.raw: return ""
        buffer = self.raw[:size]
        lines = []
        for i in range(0, len(buffer), 16):
            chunk = buffer[i:i+16]
            h = " ".join(f"{b:02X}" for b in chunk)
            t = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            lines.append(f"{i:08X}  {h:<48}  {t}")
        return "\n".join(lines)
