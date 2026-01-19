import customtkinter as ctk
from tkinter import filedialog
import threading
import time
from analyzer import BinaryCore

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class Loader(ctk.CTkToplevel):
    def __init__(self, p):
        super().__init__(p)
        self.geometry("400x250")
        self.overrideredirect(True)
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"400x250+{(sw//2)-200}+{(sh//2)-125}")
        self.configure(fg_color="#080808")
        self.L1 = ctk.CTkLabel(self, text="VORTEX", font=("Impact", 40), text_color="#00E676")
        self.L1.pack(expand=True, pady=(20,0))
        self.L2 = ctk.CTkLabel(self, text="SYSTEM INITIALIZATION", font=("Consolas", 10), text_color="#555")
        self.L2.pack(pady=(0,20))
        self.bar = ctk.CTkProgressBar(self, width=300, height=2, progress_color="#00E676")
        self.bar.pack(pady=20)
        self.bar.set(0)

class Root(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.overrideredirect(True)
        self.core = BinaryCore()
        self.splash = Loader(self)
        self.after(100, self.boot)
        self.x_off = 0
        self.y_off = 0

    def boot(self):
        threading.Thread(target=self._seq).start()

    def _seq(self):
        for i in range(101):
            time.sleep(0.015)
            self.splash.bar.set(i/100)
        self.splash.destroy()
        self.deiconify()
        self.ui()

    def ui(self):
        self.geometry("1200x800")
        self.configure(fg_color="#101010")
        
        # Custom Title Bar
        self.bar = ctk.CTkFrame(self, height=30, corner_radius=0, fg_color="#050505")
        self.bar.pack(fill="x", side="top")
        self.bar.bind("<Button-1>", self.drag_start)
        self.bar.bind("<B1-Motion>", self.drag_move)
        
        ctk.CTkLabel(self.bar, text=" VORTEX LOGIC", font=("Consolas", 12, "bold"), text_color="#666").pack(side="left", padx=10)
        
        cls_btn = ctk.CTkButton(self.bar, text="X", width=40, fg_color="transparent", hover_color="#C00", command=self.destroy)
        cls_btn.pack(side="right")
        
        # Main Layout
        self.body = ctk.CTkFrame(self, corner_radius=0, fg_color="#101010")
        self.body.pack(fill="both", expand=True)
        
        self.body.grid_columnconfigure(1, weight=1)
        self.body.grid_rowconfigure(0, weight=1)

        self.nav = ctk.CTkFrame(self.body, width=250, corner_radius=0, fg_color="#121212")
        self.nav.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.nav, text="VORTEX", font=("Impact", 32), text_color="#00E676").pack(pady=40)
        
        self.btn = ctk.CTkButton(self.nav, text="LOAD BINARY", command=self.ask, height=50, 
                                 fg_color="#00E676", text_color="#000", font=("Roboto", 14, "bold"), hover_color="#00C853")
        self.btn.pack(padx=20, fill="x")
        
        self.meta_lbl = ctk.CTkLabel(self.nav, text="NO FILE", font=("Consolas", 11), text_color="#444")
        self.meta_lbl.pack(pady=20)

        self.main = ctk.CTkTabview(self.body, fg_color="#101010", text_color="#ccc")
        self.main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.pages = {}
        for t in ["DASHBOARD", "SECTIONS", "IMPORTS", "CODE_VIEW", "HEX_DUMP"]:
            self.pages[t] = self.main.add(t)

        self.build_dash()
        self.build_sects()
        self.build_code()
        self.build_hex()

    def drag_start(self, event):
        self.x_off = event.x
        self.y_off = event.y

    def drag_move(self, event):
        x = self.winfo_pointerx() - self.x_off
        y = self.winfo_pointery() - self.y_off
        self.geometry(f"+{x}+{y}")

    def build_dash(self):
        self.dash = ctk.CTkScrollableFrame(self.pages["DASHBOARD"], fg_color="transparent")
        self.dash.pack(fill="both", expand=True)
        self.kv_store = {}
        ks = ["Machine", "EntryPoint", "ImageBase", "Sections", "Built", "FileSize", "MD5", "SHA256"]
        for k in ks:
            f = ctk.CTkFrame(self.dash, fg_color="#181818")
            f.pack(fill="x", pady=4)
            ctk.CTkLabel(f, text=k.upper(), width=120, font=("Consolas", 12, "bold"), text_color="#666").pack(side="left", padx=10, pady=10)
            v = ctk.CTkLabel(f, text="-", font=("Consolas", 12), text_color="#eee")
            v.pack(side="left", padx=10)
            self.kv_store[k] = v

    def build_sects(self):
        self.sect_box = ctk.CTkScrollableFrame(self.pages["SECTIONS"], fg_color="transparent")
        self.sect_box.pack(fill="both", expand=True)

    def build_code(self):
        self.code_txt = ctk.CTkTextbox(self.pages["CODE_VIEW"], font=("Consolas", 13), fg_color="#000", text_color="#00E676")
        self.code_txt.pack(fill="both", expand=True)

    def build_hex(self):
        self.hex_txt = ctk.CTkTextbox(self.pages["HEX_DUMP"], font=("Consolas", 13), fg_color="#151515", text_color="#aaa")
        self.hex_txt.pack(fill="both", expand=True)

    def ask(self):
        t = filedialog.askopenfilename()
        if t: self.load(t)

    def load(self, path):
        if not self.core.load(path): return
        self.meta_lbl.configure(text=path.split("/")[-1])
        d = self.core.meta()
        h = self.core.hashes()
        full = {**d, **h}
        for k, v in full.items():
            if k in self.kv_store:
                self.kv_store[k].configure(text=str(v))
        for w in self.sect_box.winfo_children(): w.destroy()
        hf = ctk.CTkFrame(self.sect_box, fg_color="transparent")
        hf.pack(fill="x")
        for h in ["NAME", "RVA", "VSIZE", "ENTROPY"]:
            ctk.CTkLabel(hf, text=h, width=100, font=("Consolas", 11, "bold"), text_color="#555").pack(side="left", padx=5)
        for s in self.core.sections():
            r = ctk.CTkFrame(self.sect_box, fg_color="#181818")
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=s["Name"], width=100, font=("Consolas", 12)).pack(side="left", padx=5)
            ctk.CTkLabel(r, text=s["RVA"], width=100, font=("Consolas", 12)).pack(side="left", padx=5)
            ctk.CTkLabel(r, text=s["VSize"], width=100, font=("Consolas", 12)).pack(side="left", padx=5)
            ent = float(s["Entropy"])
            c = "#ff3333" if ent > 7 else "#00E676"
            ctk.CTkLabel(r, text=f"{ent:.2f}", width=100, font=("Consolas", 12, "bold"), text_color=c).pack(side="left", padx=5)
        self.code_txt.delete("0.0", "end")
        asm = self.core.disassembly()
        buf = ""
        for i in asm:
            buf += f"{i['addr']:<12}   {i['bytes']:<24}   {i['mnem']:<6} {i['op']}\n"
        self.code_txt.insert("0.0", buf)
        self.hex_txt.delete("0.0", "end")
        self.hex_txt.insert("0.0", self.core.hexdump())

if __name__ == "__main__":
    app = Root()
    app.mainloop()
