""" HUB TO ALL DOCUMENT MATCHERS """

import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import threading
import pdfplumber
import pytesseract
import importlib.util
import sys
import os
from PIL import Image, ImageTk

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Array of all suppliers

SUPPLIERS = {

    "DECKO": {
        "keywords": ["DECKO", "PORTES DECKO", "TAMARACK"],
        "module": "document_matcher_DECKO",
        "complete": True,
    },
    "ADFAST": {
        "keywords": ["ADFAST", "ADFAST CANADA", "CONFIRMATION DE COMMANDE"],
        "module": "document_matcher_ADFAST",
        "complete": False,
    },
    "FIT": {
        "keywords": ["FENÊTRES FIT", "FENETRES FIT", "RÉFÉRENCE : COMMANDE"],
        "module": "document_matcher_FIT",
        "complete": True,
    },
    "FORIMPEX": {
        "keywords": ["FORIMPEX", "SAINT-JOSEPH-DE-BEAUCE", "Saint-Joseph-de-Beauce"],
        "module": "document_matcher_FORIMPEX",
        "complete": True,
    },
    "LION": {
        "keywords": ["QUINCAILLERIE LION", "LIONHARDWARE", "WWW.LIONHARDWARE.COM"],
        "module": "document_matcher_LION",
        "complete": True,
    },
    "NOVATECH GLAZING + SLAB": {
        "keywords": ["COMMANDE DE VITRAUX", "NOVATECH GLAZING", "COUPE-FEU", "ANNEXE PR"],
        "module": "document_matcher_NOVAGLAZSLAB",
        "complete": True,
    },
    "NOVATECH RESIVER": {
        "keywords": ["RESIVER", "RES1VER"],
        "module": "document_matcher_NOVATECH",
        "complete": False,
    },
    "THERMOPLAST": {
        "keywords": ["THERMOPLAST", "CUST-ORDER", "CUST ORDER"],
        "module": "document_matcher_THERMOPLAST",
        "complete": True,
    },
    "VISCAN": {
        "keywords": ["VISCAN", "COMMANDE CLIENT"],
        "module": "document_matcher_VISCAN",
        "complete": True,
    },
}

# Set Colours

COL_BG         = "#0f1117"
COL_SURFACE    = "#1a1d27"
COL_CARD       = "#20232f"
COL_BORDER     = "#2e3247"
COL_ACCENT     = "#5b6af0"
COL_TEXT       = "#e8eaf6"
COL_MUTED      = "#6b7280"
COL_GREY_DOT   = "#3a3f55"
COL_GREEN_DOT  = "#22c55e"
COL_YELLOW_DOT = "#eab308"
COL_SUCCESS    = "#22c55e"
COL_ERROR      = "#ef4444"
FONT_LABEL     = ("Segoe UI", 9, "bold")
FONT_BODY      = ("Segoe UI", 9)
FONT_BTN       = ("Segoe UI", 10, "bold")
FONT_SMALL     = ("Segoe UI", 8)

#Helping Logic

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        if not text.strip():
            with pdfplumber.open(pdf_path) as pdf:
                if pdf.pages:
                    img = pdf.pages[0].to_image(resolution=300)
                    text = pytesseract.image_to_string(img.original)
    except Exception as e:
        print(f"[HUB] Text extract error: {e}")
    return text


def detect_supplier(pdf_path: str) -> str | None:
    text = extract_text_from_pdf(pdf_path).upper()

    priority_order = [
        "NOVATECH GLAZING + SLAB",
        "ADFAST",
        "DECKO",
        "FIT",
        "FORIMPEX",
        "LION",
        "NOVATECH RESIVER",
        "THERMOPLAST",
        "VISCAN",
    ]

    for supplier in priority_order:
        info = SUPPLIERS[supplier]
        for kw in info["keywords"]:
            if kw.upper() in text:
                return supplier
    return None


def load_matcher_module(module_name: str, base_dir: str):
    module_path = os.path.join(base_dir, f"{module_name}.py")
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Matcher file not found: {module_path}")
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


# Main HUB GUI

class HubGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ALEXIS GUYENNON DOCUMENT MATCHER -> DALMEN")
        self.root.geometry("1100x780")
        self.root.resizable(False, False)
        self.root.configure(bg=COL_BG)

        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.match_log = ""
        self.file1_path = None
        self.file2_path = None
        self.detected_supplier = None

        self.dot_labels: dict[str, tk.Label] = {}
        self._build_ui()


# Construction of UI

    def _build_ui(self):

        BG_COLOUR = "#6E9EF0"
        # Top bar
        topbar = tk.Frame(self.root, bg=BG_COLOUR, height=64)
        topbar.pack(fill=tk.X)
        topbar.pack_propagate(False)

        self.log_btn = tk.Button(
            topbar, text="📋  VIEW LOG",
            font=FONT_LABEL, bg="#2e3247", fg="#ffffff",
            cursor="hand2", relief=tk.FLAT, padx=14, pady=8,
            state=tk.DISABLED, command=self._show_log
        )
        self.log_btn.pack(side=tk.RIGHT, padx=(0, 12), pady=14)
    
        try:
            logo_path = os.path.join(self.base_dir, "dalmen_logo.png")
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((120, 48), Image.LANCZOS)
            self._logo_photo = ImageTk.PhotoImage(logo_img)
            tk.Label(topbar, image=self._logo_photo,
                    bg=BG_COLOUR).pack(side=tk.LEFT, padx=(18, 4), pady=8)
        except Exception as e:
            print(f"[HUB] Logo failed to load: {e}")
            tk.Label(topbar, text="DALMEN",
                    font=("Georgia", 18, "bold"),
                    bg=BG_COLOUR, fg=COL_ACCENT).pack(side=tk.LEFT, padx=(28, 4), pady=18)
    
        tk.Label(
            topbar, text="AG DOCUMENT MATCHER",
            font=("Arial", 13, "bold"), bg=BG_COLOUR, fg="#2c2e77"
        ).pack(side=tk.LEFT, pady=18)
    
        tk.Label(
            topbar, text="V1.1  |  9 Current Suppliers",
            font=FONT_SMALL, bg=BG_COLOUR, fg="#2c2e77"
        ).pack(side=tk.RIGHT, padx=28, pady=18)
    
        # Body
        body = tk.Frame(self.root, bg=COL_BG)
        body.pack(fill=tk.BOTH, expand=True, padx=28, pady=20)
    
        # Left column: supplier status panel
        left = tk.Frame(body, bg=COL_CARD, width=230)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left.pack_propagate(False)
        self._build_supplier_panel(left)
    
        # Right column: upload + action
        right = tk.Frame(body, bg=COL_BG)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._build_right_panel(right)


    def _build_supplier_panel(self, parent):
        TXT_COLOUR = "#6E9EF0"
        tk.Label(
            parent, text="SUPPLIERS / FOURNISSEURS",
            font=FONT_LABEL, bg=COL_CARD, fg=TXT_COLOUR
        ).pack(anchor="w", padx=18, pady=(18, 10))
    
        tk.Frame(parent, bg=COL_BORDER, height=1).pack(fill=tk.X, padx=18)
    
        for supplier, info in SUPPLIERS.items():
            row = tk.Frame(parent, bg=COL_CARD)
            row.pack(fill=tk.X, padx=18, pady=6)
    
            dot = tk.Label(row, text="●", font=("Arial", 11),
                            bg=COL_CARD, fg=COL_GREY_DOT)
            dot.pack(side=tk.LEFT, padx=(0, 10))
            self.dot_labels[supplier] = dot
    
            tk.Label(
                row, text=supplier,
                font=FONT_LABEL, bg=COL_CARD, fg=COL_TEXT
            ).pack(side=tk.LEFT)
    
            if not info["complete"]:
                tk.Label(
                    row, text="UNFINISHED",
                    font=("Arial", 5, "bold"),
                    bg=COL_CARD, fg=COL_YELLOW_DOT
                ).pack(side=tk.RIGHT)
    
        tk.Frame(parent, bg=COL_BORDER, height=1).pack(fill=tk.X, padx=18, pady=(10, 0))
    
        legend = tk.Frame(parent, bg=COL_CARD)
        legend.pack(fill=tk.X, padx=18, pady=10)
        for colour, label in [
            (COL_GREY_DOT,   "Not detected"),
            (COL_GREEN_DOT,  "Detected ✓"),
            (COL_YELLOW_DOT, "Unfinished"),
        ]:
            row = tk.Frame(legend, bg=COL_CARD)
            row.pack(anchor="w", pady=1)
            tk.Label(row, text="●", font=("Arial", 9),
                        bg=COL_CARD, fg=colour).pack(side=tk.LEFT, padx=(0, 6))
            tk.Label(row, text=label, font=FONT_SMALL,
                        bg=COL_CARD, fg=COL_MUTED).pack(side=tk.LEFT) 

        tk.Frame(parent, bg=COL_BORDER, height=1).pack(fill=tk.X, padx=18, pady=(10, 0))

        self.reset_btn = tk.Button(
            parent, text = "CLEAR & RESET", font = FONT_BTN, bg=COL_SURFACE, fg=COL_MUTED,
            activebackground=COL_BORDER, activeforeground=COL_TEXT, cursor="hand2",
            relief=tk.FLAT, padx=14, pady=12,
            command=self._reset
        )
        self.reset_btn.pack(fill=tk.X, padx=18, pady=(10, 0))   


    def _build_right_panel(self, parent):
        # Detected supplier banner
        self.banner_frame = tk.Frame(parent, bg=COL_SURFACE, height=48)
        self.banner_frame.pack(fill=tk.X, pady=(0, 16))
        self.banner_frame.pack_propagate(False)
 
        self.banner_label = tk.Label(
            self.banner_frame,
            text="Upload documents to begin",
            font=FONT_LABEL, bg=COL_SURFACE, fg=COL_MUTED
        )
        self.banner_label.pack(expand=True)
 
        # Upload cards row
        cards_row = tk.Frame(parent, bg=COL_BG)
        cards_row.pack(fill=tk.X)
        cards_row.columnconfigure(0, weight=1)
        cards_row.columnconfigure(1, weight=1)
 
        self.card1_status = self._build_upload_card(
            cards_row, col=0, title="DOC 1",
            subtitle="Dalmen Purchase Order Document", file_num=1
        )
        self.card2_status = self._build_upload_card(
            cards_row, col=1, title="DOC 2",
            subtitle="Supplier Document (Confirmation/Facture)", file_num=2
        )
 
        # Progress bar
        self.progress = ttk.Progressbar(parent, mode="indeterminate")
 
        # Match button
        self.match_btn = tk.Button(
            parent,
            text="⚡  BEGIN MATCHING",
            font=FONT_BTN,
            bg=COL_ACCENT, fg="white",
            activebackground="#4455dd", activeforeground="white",
            cursor="hand2", relief=tk.FLAT,
            padx=20, pady=14,
            state=tk.DISABLED,
            command=self._run_matcher
        )
        self.match_btn.pack(fill=tk.X, pady=(18, 0))
 
        # Result area
        self.result_frame = tk.Frame(parent, bg=COL_BG)
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=(16, 0))


    def _build_upload_card(self, parent, col, title, subtitle, file_num) -> tk.Label:
        card = tk.Frame(parent, bg=COL_CARD)
        card.grid(
            row=0, column=col,
            padx=(0, 10) if col == 0 else (10, 0),
            sticky="nsew", pady=(0, 16)
        )
 
        tk.Frame(card, bg=COL_ACCENT, height=3).pack(fill=tk.X)
 
        inner = tk.Frame(card, bg=COL_CARD, padx=18, pady=16)
        inner.pack(fill=tk.BOTH, expand=True)
 
        tk.Label(inner, text=title, font=FONT_LABEL,
                 bg=COL_CARD, fg=COL_ACCENT).pack(anchor="w")
        tk.Label(inner, text=subtitle, font=FONT_SMALL,
                 bg=COL_CARD, fg=COL_MUTED).pack(anchor="w", pady=(2, 10))
 
        status_lbl = tk.Label(
            inner, text="No file selected",
            font=FONT_BODY, bg=COL_CARD, fg=COL_MUTED,
            anchor="w", wraplength=270, justify="left"
        )
        status_lbl.pack(fill=tk.X, pady=(0, 12))
 
        tk.Button(
            inner, text="📁  Browse PDF",
            font=FONT_BTN,
            bg=COL_ACCENT, fg="white",
            activebackground="#4455dd", activeforeground="white",
            cursor="hand2", relief=tk.FLAT,
            padx=14, pady=9,
            command=lambda n=file_num: self._browse(n)
        ).pack(fill=tk.X)
 
        return status_lbl

    
# For file browsing and detection

    def _browse(self, file_num: int):
        path = filedialog.askopenfilename(
            title=f"Select Document {file_num}",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if not path:
            return

        display = path.replace("\\", "/").split("/")[-1]

        if file_num == 1:
            self.file1_path = path
            self.card1_status.config(text=f"✓ {display}", fg=COL_SUCCESS)
        else:
            self.file2_path = path
            self.card2_status.config(text=f"✓ {display}", fg=COL_SUCCESS)

        threading.Thread(
            target=self._detect_and_update,
            args=(path,),
            daemon=True
        ).start()
    

    def _detect_and_update(self, pdf_path: str):
        supplier = detect_supplier(pdf_path)
        self.root.after(0, self._apply_detection, supplier)

    
    def _apply_detection(self, supplier):
        for dot in self.dot_labels.values():
            dot.config(fg=COL_GREY_DOT)

        if supplier:
            self.detected_supplier = supplier
            info = SUPPLIERS[supplier]
            dot_colour = COL_GREEN_DOT if info["complete"] else COL_YELLOW_DOT
            self.dot_labels[supplier].config(fg=dot_colour)

            if info["complete"]:
                self.banner_label.config(
                    text=f"Detected: {supplier}  —  ready to match",
                    fg=COL_GREEN_DOT)
            else:
                self.banner_label.config(
                    text=f"Detected: {supplier}  ⚠️  Price matching incomplete",
                    fg=COL_YELLOW_DOT)

        if self.file1_path and self.file2_path:
            self.match_btn.config(state=tk.NORMAL)


    def _run_matcher(self):
        if not self.file1_path or not self.file2_path:
            return

        for w in self.result_frame.winfo_children():
            w.destroy()

        self.progress.pack(pady=12)
        self.progress.start(10)
        self.match_btn.config(state=tk.DISABLED)

        threading.Thread(target=self._do_match, daemon=True).start()


    def _do_match(self):
        try:
            if not self.detected_supplier:
                s1 = detect_supplier(self.file1_path) if self.file1_path else None
                s2 = detect_supplier(self.file2_path) if self.file2_path else None
                self.detected_supplier = s1 or s2

            if not self.detected_supplier:
                self.root.after(0, self._show_error,
                                "Could not identify supplier.")
                return

            supplier    = self.detected_supplier
            module_name = SUPPLIERS[supplier]["module"]
            print(f"[HUB] Loading {module_name}...")

            mod = load_matcher_module(module_name, self.base_dir)

            dummy = tk.Toplevel(self.root)
            dummy.withdraw()

            matcher = mod.DocumentMatcherGUI(dummy)
            matcher.file1_path = self.file1_path
            matcher.file2_path = self.file2_path

            if hasattr(matcher, 'parse_document'):
                doc1 = matcher.parse_document(self.file1_path)
                import inspect
                sig = inspect.signature(matcher.parse_document)
                if 'dalmen_po' in sig.parameters:
                    doc2 = matcher.parse_document(self.file2_path, dalmen_po=doc1.order_number)
                else:
                    doc2 = matcher.parse_document(self.file2_path)
                raw_result = matcher.match_documents(doc1, doc2)
            else:
                # Store result via a callback hook
                raw_result = {}
                original_display = matcher.display_result
                def capture(result):
                    raw_result.update(result)
                matcher.display_result = capture
                matcher.run_comparison()
                matcher.display_result = original_display

            self.match_log = getattr(matcher, "match_log", "")

            # Clear toplevel window so it doesn't sit in memory
            dummy.destroy()

            result = self.normalize_result(raw_result)
            self.root.after(0, self._display_result, result)

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print(tb)
            self.root.after(0, self._show_error, f"{str(e)}\n\n{tb}")

    
    def _display_result(self, result: dict):
        self.progress.stop()
        self.progress.pack_forget()
        self.match_btn.config(state=tk.NORMAL)
        self.log_btn.config(state=tk.NORMAL)

        for w in self.result_frame.winfo_children():
            w.destroy()

        is_match = result["match"]
        accent   = COL_SUCCESS if is_match else COL_ERROR

        card = tk.Frame(self.result_frame, bg=COL_CARD)
        card.pack(fill=tk.X)
        tk.Frame(card, bg=accent, height=4).pack(fill=tk.X)

        inner = tk.Frame(card, bg=COL_CARD, padx=24, pady=18)
        inner.pack(fill=tk.BOTH, expand=True)

        top = tk.Frame(inner, bg=COL_CARD)
        top.pack(fill=tk.X)

        icon = "✅" if is_match else "❌"
        verdict = "DOCUMENTS MATCH!" if is_match else "DOCUMENTS DO NOT MATCH."
        tk.Label(top, text=icon, font=("Arial", 26), bg=COL_CARD).pack(side=tk.LEFT)
        tk.Label(top, text=verdict, font=("Courier New", 15, "bold"),
                bg=COL_CARD, fg=accent).pack(side=tk.LEFT, padx=12)
        tk.Label(top, text=f"{result['confidence']:.0f}% confidence",
                font=FONT_BODY, bg=COL_CARD, fg=COL_MUTED).pack(side=tk.RIGHT)

        tk.Frame(inner, bg=COL_BORDER, height=1).pack(fill=tk.X, pady=(14, 14))

        stats = tk.Frame(inner, bg=COL_CARD)
        stats.pack(fill=tk.X, pady=(0, 14))

        o1 = result["order1"].replace(" ", "")
        o2 = result["order2"].replace(" ", "")
        order_icon = "✅" if o1 in o2 or o2 in o1 or o1 == o2 else "❌"
        
        price_stat = ("-", "-")
        for label, value in result["extras"].items():
            if "price" in label.lower() or "prix" in label.lower() or "qty" in label.lower():
                price_stat = (label, value)
                break
        
        stat_defs = [
            ("Order Numbers", f"{order_icon}  {result['order1']} / {result['order2']}"),
            ("Items Matched",  f"{result['matched']} / {result['total']}"),
            ("Confidence",     f"{result['confidence']:.1f}%"),
            (price_stat[0],    price_stat[1]),
        ]

        for col_idx, (label, value) in enumerate(stat_defs):
            box = tk.Frame(stats, bg=COL_SURFACE, padx=14, pady=10)
            box.grid(row=0, column=col_idx,
                    padx=(0 if col_idx == 0 else 6, 0), sticky="ew")
            stats.columnconfigure(col_idx, weight=1)
            tk.Label(box, text=value, font=("Courier New", 13, "bold"),
                    bg=COL_SURFACE, fg=COL_TEXT).pack()
            tk.Label(box, text=label, font=FONT_SMALL,
                    bg=COL_SURFACE, fg=COL_MUTED).pack()

        if self.detected_supplier:
            info = SUPPLIERS[self.detected_supplier]
            badge_col = COL_GREEN_DOT if info["complete"] else COL_YELLOW_DOT
            tk.Label(inner, text=f"Matched via: {self.detected_supplier}",
                    font=FONT_SMALL, bg=COL_CARD, fg=badge_col).pack(anchor="w")


    def _reset(self):
        self.file1_path = None
        self.file2_path = None
        self.detected_supplier = None
        self.match_log = ""

        self.card1_status.config(text="No file selected", fg=COL_MUTED)
        self.card2_status.config(text="No file selected", fg=COL_MUTED)
        self.banner_label.config(text="Upload documents to begin", fg=COL_MUTED)
        self.match_btn.config(state=tk.DISABLED)
        self.log_btn.config(state=tk.DISABLED)

        for dot in self.dot_labels.values():
            dot.config(fg=COL_GREY_DOT)

        for w in self.result_frame.winfo_children():
            w.destroy()


    def normalize_result(self, result: dict) -> dict:
        order1 = result.get("order1") or result.get("po1") or "—"
        order2 = result.get("order2") or result.get("po2") or "—"
        matched = result.get("matched_items", result.get("matched", 0))
        total   = result.get("total_items",   result.get("total",   0))
        confidence = result.get("confidence", 0)
        is_match   = bool(result.get("match", False))

        extras = {}
        if "price_ok" in result and result["price_ok"] is not None:
            extras["Price Check"] = "✅ Pass" if result["price_ok"] else "❌ Fail"
        if "price_check_ok" in result:
            extras["Price Match"] = "✅ Yes" if result["price_check_ok"] else "❌ No"
        if "qty_matched" in result and "qty_total" in result:
            extras["Qty Verified"] = f"{result['qty_matched']} / {result['qty_total']}"
        if "color_match" in result:
            extras["Color"] = "✅ Match" if result["color_match"] else "❌ No Match"
        if "config_match" in result and result.get("configuration"):
            extras["Config"] = f"{'✅' if result['config_match'] else '❌'}  {result['configuration']}"
        if "order_match" in result:
            extras["Order Match"] = "✅ Yes" if result["order_match"] else "❌ No"

        return {
            "match": is_match, "confidence": confidence,
            "matched": matched, "total": total,
            "order1": order1,   "order2": order2,
            "extras": extras,
        }


    def _show_log(self):
        if not self.match_log:
            return
        win = tk.Toplevel(self.root)
        win.title("Detailed Matching Log")
        win.geometry("800x600")
        win.configure(bg=COL_BG)

        hdr = tk.Frame(win, bg=COL_ACCENT, padx=10, pady=10)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="Detailed Matching Log",
                font=("Courier New", 14, "bold"),
                bg=COL_ACCENT, fg="white").pack()

        ta = scrolledtext.ScrolledText(win, font=("Courier", 9),
                                    wrap=tk.WORD, padx=10, pady=10,
                                    bg=COL_SURFACE, fg=COL_TEXT)
        ta.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ta.insert(1.0, self.match_log)
        ta.config(state=tk.DISABLED)

        tk.Button(win, text="Close", font=FONT_BTN, bg=COL_ACCENT, fg="white",
                cursor="hand2", command=win.destroy,
                relief=tk.FLAT, padx=20, pady=10).pack(pady=10)

    def _show_error(self, msg: str):
        self.progress.stop()
        self.progress.pack_forget()
        self.match_btn.config(state=tk.NORMAL)

        for w in self.result_frame.winfo_children():
            w.destroy()

        card = tk.Frame(self.result_frame, bg=COL_CARD)
        card.pack(fill=tk.X, pady=8)
        tk.Frame(card, bg=COL_ERROR, height=3).pack(fill=tk.X)
        tk.Label(
            card, text=f"❌  {msg}",
            font=FONT_BODY, bg=COL_CARD, fg=COL_ERROR,
            wraplength=640, justify="left", padx=18, pady=14
        ).pack(anchor="w")
        

# The Entry Point

def main():
    root = tk.Tk()
    HubGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

        

    


