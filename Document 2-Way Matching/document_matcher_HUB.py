""" HUB TO ALL DOCUMENT MATCHERS """

import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import threading
import re
import pdfplumber
import pytesseract
import importlib.util
import sys
import os
from PIL import Image, ImageTk

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

SUPPLIERS = {
    "DECKO": {
        "keywords": ["DECKO", "PORTES DECKO", "TAMARACK"],
        "module": "document_matcher_DECKO",
        "complete": True,
    },
    "ADFAST": {
        "keywords": ["ADFAST", "ADFAST CANADA"],
        "module": "document_matcher_ADFAST",
        "complete": True,
    },
    "FIT": {
        "keywords": ["FENÊTRES FIT", "FENETRES FIT", "RÉFÉRENCE : COMMANDE",
                     "SOLUTIONS DE QUINCAILLERIE FIT", "QUINCAILLERIE FIT",
                     "RAPPORT DE COMMANDE", "Commandé à"],
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
        "NOVATECH GLAZING + SLAB", "FORIMPEX", "ADFAST", "DECKO", "FIT",
         "LION", "NOVATECH RESIVER", "THERMOPLAST", "VISCAN",
    ]
    for supplier in priority_order:
        info = SUPPLIERS[supplier]
        for kw in info["keywords"]:
            if kw.upper() in text:
                return supplier
    return None


def load_matcher_module(module_name: str, base_dir: str):
    # When frozen, check _internal subfolder first, then base_dir itself
    candidates = [
        os.path.join(base_dir, "_internal", f"{module_name}.py"),
        os.path.join(base_dir, f"{module_name}.py"),
    ]
    module_path = None
    for path in candidates:
        if os.path.exists(path):
            module_path = path
            break
    if not module_path:
        raise FileNotFoundError(f"Matcher file not found: {module_path}")
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


class HubGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ALEXIS GUYENNON'S DOCUMENT MATCHER FOR DALMEN")
        self.root.geometry("1100x860")
        self.root.resizable(False, False)
        self.root.configure(bg=COL_BG)

        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
            internal = os.path.join(self.base_dir, '_internal')
            if os.path.exists(internal):
                self.base_dire = internal
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.match_log = ""
        self.file1_path = None
        self.file2_path = None
        self.detected_supplier = None
        self._cancelled = False
        self._matching = False
        self.doc1_raw_text = ""
        self.doc2_raw_text = ""

        self.dot_labels: dict[str, tk.Label] = {}
        self._build_ui()

    # ── UI CONSTRUCTION ────────────────────────────────────────────────────

    def _build_ui(self):
        BG_COLOUR = "#6E9EF0"
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
            tk.Label(topbar, image=self._logo_photo, bg=BG_COLOUR).pack(
                side=tk.LEFT, padx=(18, 4), pady=8)
        except Exception as e:
            print(f"[HUB] Logo failed to load: {e}")
            tk.Label(topbar, text="DALMEN", font=("Georgia", 18, "bold"),
                     bg=BG_COLOUR, fg=COL_ACCENT).pack(side=tk.LEFT, padx=(28, 4), pady=18)

        tk.Label(topbar, text="AG DOCUMENT MATCHER",
                 font=("Constantia", 13, "bold"), bg=BG_COLOUR, fg="#2c2e77"
                 ).pack(side=tk.LEFT, pady=18)
        tk.Label(topbar, text="V1.1  |  9 Current Suppliers",
                 font=FONT_SMALL, bg=BG_COLOUR, fg="#2c2e77"
                 ).pack(side=tk.RIGHT, padx=28, pady=18)

        body = tk.Frame(self.root, bg=COL_BG)
        body.pack(fill=tk.BOTH, expand=True, padx=28, pady=20)

        left = tk.Frame(body, bg=COL_CARD, width=230)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left.pack_propagate(False)
        self._build_supplier_panel(left)

        right = tk.Frame(body, bg=COL_BG)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._build_right_panel(right)

    def _build_supplier_panel(self, parent):
        TXT_COLOUR = "#6E9EF0"
        tk.Label(parent, text="SUPPLIERS / FOURNISSEURS",
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
            tk.Label(row, text=supplier, font=FONT_LABEL,
                     bg=COL_CARD, fg=COL_TEXT).pack(side=tk.LEFT)
            if not info["complete"]:
                tk.Label(row, text="UNFINISHED", font=("Arial", 5, "bold"),
                         bg=COL_CARD, fg=COL_YELLOW_DOT).pack(side=tk.RIGHT)

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
            parent, text="CLEAR & RESET", font=FONT_BTN,
            bg=COL_SURFACE, fg=COL_MUTED,
            activebackground=COL_BORDER, activeforeground=COL_TEXT,
            cursor="hand2", relief=tk.FLAT, padx=14, pady=12,
            command=self._reset
        )
        self.reset_btn.pack(fill=tk.X, padx=18, pady=(10, 0))

    def _build_right_panel(self, parent):
        # Banner
        self.banner_frame = tk.Frame(parent, bg=COL_SURFACE, height=48)
        self.banner_frame.pack(fill=tk.X, pady=(0, 16))
        self.banner_frame.pack_propagate(False)
        self.banner_label = tk.Label(
            self.banner_frame, text="Upload documents to begin",
            font=FONT_LABEL, bg=COL_SURFACE, fg=COL_MUTED)
        self.banner_label.pack(expand=True)

        # Upload cards
        cards_row = tk.Frame(parent, bg=COL_BG)
        cards_row.pack(fill=tk.X)
        cards_row.columnconfigure(0, weight=1)
        cards_row.columnconfigure(1, weight=1)
        self.card1_status = self._build_upload_card(
            cards_row, col=0, title="DOC 1",
            subtitle="Dalmen Purchase Order Document", file_num=1)
        self.card2_status = self._build_upload_card(
            cards_row, col=1, title="DOC 2",
            subtitle="Supplier Document (Confirmation/Facture)", file_num=2)

        # Single progress bar with custom style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Hub.Horizontal.TProgressbar",
                        troughcolor=COL_SURFACE,
                        background=COL_ACCENT,
                        thickness=6)
        self.progress = ttk.Progressbar(
            parent, mode="indeterminate",
            style="Hub.Horizontal.TProgressbar")

        # Match button
        self.match_btn = tk.Button(
            parent, text="⚡  BEGIN MATCHING",
            font=FONT_BTN, bg=COL_ACCENT, fg="white",
            activebackground="#4455dd", activeforeground="white",
            cursor="hand2", relief=tk.FLAT, padx=20, pady=14,
            state=tk.DISABLED, command=self._run_matcher)
        self.match_btn.pack(fill=tk.X, pady=(18, 0))

        # PO list frame — sits between button and results, never destroyed by result updates
        self.po_frame = tk.Frame(parent, bg=COL_BG)
        self.po_frame.pack(fill=tk.X)

        # Scrollable result area so long results never get cut off
        result_outer = tk.Frame(parent, bg=COL_BG)
        result_outer.pack(fill=tk.BOTH, expand=True, pady=(16, 0))

        result_canvas = tk.Canvas(result_outer, bg=COL_BG, highlightthickness=0)
        result_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.result_frame = tk.Frame(result_canvas, bg=COL_BG)
        self._result_window = result_canvas.create_window(
            (0, 0), window=self.result_frame, anchor="nw")

        def _on_frame_configure(event):
            result_canvas.configure(scrollregion=result_canvas.bbox("all"))

        def _on_canvas_configure(event):
            result_canvas.itemconfig(self._result_window, width=event.width)

        self.result_frame.bind("<Configure>", _on_frame_configure)
        result_canvas.bind("<Configure>", _on_canvas_configure)
        result_canvas.bind("<MouseWheel>",
                           lambda e: result_canvas.yview_scroll(
                               int(-1 * (e.delta / 120)), "units"))
        self._result_canvas = result_canvas

    def _build_upload_card(self, parent, col, title, subtitle, file_num) -> tk.Label:
        card = tk.Frame(parent, bg=COL_CARD)
        card.grid(row=0, column=col,
                  padx=(0, 10) if col == 0 else (10, 0),
                  sticky="nsew", pady=(0, 16))
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
            anchor="w", wraplength=270, justify="left")
        status_lbl.pack(fill=tk.X, pady=(0, 12))
        tk.Button(
            inner, text="📁  Browse PDF",
            font=FONT_BTN, bg=COL_ACCENT, fg="white",
            activebackground="#4455dd", activeforeground="white",
            cursor="hand2", relief=tk.FLAT, padx=14, pady=9,
            command=lambda n=file_num: self._browse(n)
        ).pack(fill=tk.X)
        return status_lbl

    # ── FILE BROWSING & DETECTION ──────────────────────────────────────────

    def _browse(self, file_num: int):
        path = filedialog.askopenfilename(
            title=f"Select Document {file_num}",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if not path:
            return

        display = path.replace("\\", "/").split("/")[-1]

        if file_num == 1:
            self.file1_path = path
            self.card1_status.config(text=f"✓ {display}", fg=COL_SUCCESS)
        else:
            self.file2_path = path
            self.card2_status.config(text=f"✓ {display}", fg=COL_SUCCESS)
            for w in self.result_frame.winfo_children():
                w.destroy()
            self._result_canvas.yview_moveto(0)
            self._show_po_loading()

        threading.Thread(
            target=self._detect_and_update,
            args=(path, file_num),
            daemon=True
        ).start()

    def _show_po_loading(self):
        for w in self.po_frame.winfo_children():
            w.destroy()
        frame = tk.Frame(self.po_frame, bg=COL_CARD)
        frame.pack(fill=tk.X, pady=(8, 0))
        tk.Frame(frame, bg=COL_ACCENT, height=2).pack(fill=tk.X)
        tk.Label(frame,
                 text="⏳  Scanning facture for PO numbers...",
                 font=FONT_BODY, bg=COL_CARD, fg=COL_MUTED,
                 padx=14, pady=10).pack(anchor="w")
        self._po_list_frame = frame

    def _detect_and_update(self, pdf_path: str, file_num: int):
        supplier = detect_supplier(pdf_path)
        po_list = []
        if supplier in ("DECKO", "THERMOPLAST") and pdf_path == self.file2_path:
            text = extract_text_from_pdf(pdf_path)
            if "FACTURE" in text.upper():
                po_list = self._scan_po_list(pdf_path, supplier)
        self.root.after(0, self._apply_detection, supplier, po_list, file_num)

    def _scan_po_list(self, pdf_path: str, supplier: str) -> list:
        if supplier == "DECKO":
            po_pattern = re.compile(r'\b(\d{3}-\d{5}-\d{2}-\d-\d)\b')
        else:
            po_pattern = re.compile(r'CUST[-\s]ORDER\s*[:\-]?\s*(\d{4})',
                                    re.IGNORECASE)
        found = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    if not text.strip():
                        img = page.to_image(resolution=350)
                        text = pytesseract.image_to_string(img.original)
                    for match in po_pattern.finditer(text):
                        po = match.group(1)
                        if po not in found:
                            found.append(po)
        except Exception as e:
            print(f"[HUB] PO scan error: {e}")
        return found

    def _show_decko_po_list(self, po_list: list):
        for w in self.po_frame.winfo_children():
            w.destroy()

        if not po_list:
            return

        self._po_list_frame = tk.Frame(self.po_frame, bg=COL_CARD)
        self._po_list_frame.pack(fill=tk.X, pady=(8, 0))
        tk.Frame(self._po_list_frame, bg=COL_ACCENT, height=2).pack(fill=tk.X)

        header = tk.Frame(self._po_list_frame, bg=COL_CARD, padx=14, pady=8)
        header.pack(fill=tk.X)
        tk.Label(header,
                 text=f"📋  {len(po_list)} POs detected in facture — check off as you go:",
                 font=FONT_LABEL, bg=COL_CARD, fg=COL_TEXT).pack(anchor="w")

        canvas = tk.Canvas(self._po_list_frame, bg=COL_CARD, height=200,
                           highlightthickness=0)
        scrollbar = tk.Scrollbar(self._po_list_frame, orient="vertical",
                                 command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,
                    padx=(14, 0), pady=(0, 10))

        inner = tk.Frame(canvas, bg=COL_CARD)
        canvas.create_window((0, 0), window=inner, anchor="nw")

        self._po_vars = {}
        for i, po in enumerate(po_list):
            row = tk.Frame(inner, bg=COL_CARD)
            row.grid(row=i // 5, column=i % 5, padx=8, pady=4, sticky="w")
            var = tk.BooleanVar()
            self._po_vars[po] = var
            tk.Checkbutton(
                row, text=po, variable=var,
                font=FONT_BODY, bg=COL_CARD, fg=COL_TEXT,
                selectcolor=COL_SURFACE, activebackground=COL_CARD,
                activeforeground=COL_TEXT, cursor="hand2",
            ).pack(side=tk.LEFT)

        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<MouseWheel>",
                    lambda e: canvas.yview_scroll(
                        int(-1 * (e.delta / 120)), "units"))
        self._po_canvas = canvas

    def _shrink_po_list(self):
        if hasattr(self, '_po_canvas') and self._po_canvas.winfo_exists():
            self._po_canvas.configure(height=110)

    def _apply_detection(self, supplier, po_list=None, file_num=2):
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

        if file_num == 2 and not po_list:
            for w in self.po_frame.winfo_children():
                w.destroy()

        if self.file1_path and self.file2_path and not self._matching:
            self.match_btn.config(state=tk.NORMAL)

        if po_list:
            self._show_decko_po_list(po_list)

    # ── MATCHING ───────────────────────────────────────────────────────────

    def _run_matcher(self):
        if not self.file1_path or not self.file2_path:
            return
        if self._matching:
            return

        self._matching = True
        self._cancelled = False

        for w in self.result_frame.winfo_children():
            w.destroy()
        self._result_canvas.yview_moveto(0)

        self.match_btn.config(state=tk.DISABLED, bg="#3a3f55", cursor="arrow", text="⏳  MATCHING IN PROGRESS, PLEASE WAIT...")
        self.progress.pack(fill=tk.X, pady=(4, 0))
        self.progress.start(10)

        threading.Thread(target=self._do_match, daemon=True).start()

    def _do_match(self):

        self.doc1_raw_text = ""
        self.doc2_raw_text = ""

        dummy = None
        try:
            if not self.detected_supplier:
                s1 = detect_supplier(self.file1_path) if self.file1_path else None
                s2 = detect_supplier(self.file2_path) if self.file2_path else None
                self.detected_supplier = s1 or s2

            if self._cancelled:
                return

            if not self.detected_supplier:
                self.root.after(0, self._show_error,
                                "Could not identify supplier.")
                return

            supplier    = self.detected_supplier
            module_name = SUPPLIERS[supplier]["module"]
            print(f"[HUB] Loading {module_name}...")

            mod = load_matcher_module(module_name, self.base_dir)

            if self._cancelled:
                return

            dummy = tk.Toplevel(self.root)
            dummy.withdraw()

            matcher = mod.DocumentMatcherGUI(dummy)
            matcher.file1_path = self.file1_path
            matcher.file2_path = self.file2_path

            if hasattr(matcher, 'parse_document'):
                doc1 = matcher.parse_document(self.file1_path)
                if self._cancelled:
                    dummy.destroy()
                    return
                import inspect
                sig = inspect.signature(matcher.parse_document)
                if 'dalmen_po' in sig.parameters:
                    doc2 = matcher.parse_document(
                        self.file2_path, dalmen_po=doc1.order_number)
                else:
                    doc2 = matcher.parse_document(self.file2_path)
                if self._cancelled:
                    dummy.destroy()
                    return
                raw_result = matcher.match_documents(doc1, doc2)
                if not raw_result.get("order2") or \
                        raw_result.get("order2") == "Undetected":
                    raw_result["order2"] = raw_result.get("order1", "-")
            else:
                raw_result = {}
                original_display = matcher.display_result

                def capture(result):
                    raw_result.update(result)

                matcher.display_result = capture
                import time
                matcher.run_comparison()
                timeout, elapsed = 30, 0
                while not raw_result and elapsed < timeout:
                    if self._cancelled:
                        matcher.display_result = original_display
                        dummy.destroy()
                        return
                    time.sleep(0.1)
                    elapsed += 0.1
                matcher.display_result = original_display
            
            self.doc1_raw_text = getattr(doc1, 'raw_text', '') if 'doc1' in dir() else ''
            self.doc2_raw_text = getattr(doc2, 'raw_text', '') if 'doc2' in dir() else ''

            self.match_log = getattr(matcher, "match_log", "")
            dummy.destroy()
            dummy = None

            if self._cancelled:
                return

            result = self.normalize_result(raw_result)
            self.root.after(0, self._display_result, result)

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print(tb)
            if dummy:
                try:
                    dummy.destroy()
                except Exception:
                    pass
            if not self._cancelled:
                self.root.after(0, self._show_error, f"{str(e)}\n\n{tb}")
        finally:
            self._matching = False

    # ── DISPLAY ────────────────────────────────────────────────────────────

    def _display_result(self, result: dict):
        if self._cancelled:
            return

        self.progress.stop()
        self.progress.pack_forget()
        self._matching = False
        self.match_btn.config(state=tk.NORMAL, bg=COL_ACCENT, cursor="hand2",
                      text="⚡  BEGIN MATCHING")
        self.log_btn.config(state=tk.NORMAL)

        for w in self.result_frame.winfo_children():
            w.destroy()
        self._result_canvas.yview_moveto(0)
        self._shrink_po_list()

        is_match = result["match"]
        accent   = COL_SUCCESS if is_match else COL_ERROR

        card = tk.Frame(self.result_frame, bg=COL_CARD)
        card.pack(fill=tk.X)
        tk.Frame(card, bg=accent, height=4).pack(fill=tk.X)

        inner = tk.Frame(card, bg=COL_CARD, padx=24, pady=18)
        inner.pack(fill=tk.BOTH, expand=True)

        top = tk.Frame(inner, bg=COL_CARD)
        top.pack(fill=tk.X)

        icon    = "✅" if is_match else "❌"
        verdict = "DOCUMENTS MATCH!" if is_match else "DOCUMENTS DO NOT MATCH."
        tk.Label(top, text=icon, font=("Arial", 26),
                 bg=COL_CARD).pack(side=tk.LEFT)
        tk.Label(top, text=verdict, font=("Courier New", 15, "bold"),
                 bg=COL_CARD, fg=accent).pack(side=tk.LEFT, padx=12)
        tk.Label(top, text=f"{result['confidence']:.0f}% confidence",
                 font=FONT_BODY, bg=COL_CARD, fg=COL_MUTED).pack(side=tk.RIGHT)

        tk.Frame(inner, bg=COL_BORDER, height=1).pack(fill=tk.X, pady=(14, 14))

        stats = tk.Frame(inner, bg=COL_CARD)
        stats.pack(fill=tk.X, pady=(0, 14))

        o1 = result["order1"].replace(" ", "")
        o2 = result["order2"].replace(" ", "")
        order_icon = "✅" if (o1 in o2 or o2 in o1 or o1 == o2) else "❌"

        if result.get("is_confirmation", False):
            price_stat = ("-", "-")
        else:
            price_stat = ("-", "-")
            for label, value in result["extras"].items():
                if "price" in label.lower() or "prix" in label.lower() \
                        or "qty" in label.lower():
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

        if not is_match:
            issues = []
            if not (o1 in o2 or o2 in o1 or o1 == o2):
                issues.append(
                    f"❌ Order numbers don't match "
                    f"({result['order1']} vs {result['order2']})")
            if result["matched"] < result["total"]:
                unmatched = result["total"] - result["matched"]
                issues.append(f"❌ {unmatched} item(s) could not be matched")
            for label, value in result["extras"].items():
                if "❌" in str(value):
                    issues.append(
                        f"❌ {label}: {value.replace('❌', '').strip()}")

            if issues:
                issue_frame = tk.Frame(inner, bg=COL_CARD)
                issue_frame.pack(fill=tk.X, pady=(8, 4))
                tk.Label(issue_frame, text="Issues found:",
                        font=FONT_LABEL, bg=COL_CARD,
                        fg=COL_ERROR).pack(anchor="w")
                tk.Label(issue_frame,
                        text="💡 Could be due to a special order — check extracted text for details!",
                        font=FONT_BODY, bg=COL_CARD, fg=COL_YELLOW_DOT,
                        wraplength=680, justify="left").pack(anchor="w", pady=(0, 6))
                for issue in issues:
                    tk.Label(issue_frame, text=issue,
                            font=FONT_BODY, bg=COL_CARD, fg=COL_ERROR,
                            wraplength=680, justify="left"
                            ).pack(anchor="w", pady=1)

        if self.detected_supplier:
            info = SUPPLIERS[self.detected_supplier]
            badge_col = COL_GREEN_DOT if info["complete"] else COL_YELLOW_DOT
            tk.Label(inner, text=f"Matched via: {self.detected_supplier}",
                     font=FONT_SMALL, bg=COL_CARD,
                     fg=badge_col).pack(anchor="w")

        if "voir soumission" in self.match_log.lower() or "custom package" in self.match_log.lower():
            tk.Label(inner,
            text="⚠️  Custom package detected — price verification skipped, manual review required.",
            font=FONT_BODY, bg=COL_CARD, fg=COL_YELLOW_DOT,
            wraplength=680, justify="left").pack(anchor="w", pady=(6, 0))

    def _show_error(self, msg: str):
        if self._cancelled:
            return
        self.progress.stop()
        self.progress.pack_forget()
        self._matching = False
        self.match_btn.config(state=tk.NORMAL, bg=COL_ACCENT, cursor="hand2",
                      text="⚡  BEGIN MATCHING")

        for w in self.result_frame.winfo_children():
            w.destroy()

        card = tk.Frame(self.result_frame, bg=COL_CARD)
        card.pack(fill=tk.X, pady=8)
        tk.Frame(card, bg=COL_ERROR, height=3).pack(fill=tk.X)
        tk.Label(card, text=f"❌  {msg}",
                 font=FONT_BODY, bg=COL_CARD, fg=COL_ERROR,
                 wraplength=640, justify="left", padx=18, pady=14
                 ).pack(anchor="w")

    # ── RESET ──────────────────────────────────────────────────────────────

    def _reset(self):
        self._cancelled = True
        self._matching = False

        self.file1_path = None
        self.file2_path = None
        self.detected_supplier = None
        self.match_log = ""

        self.card1_status.config(text="No file selected", fg=COL_MUTED)
        self.card2_status.config(text="No file selected", fg=COL_MUTED)
        self.banner_label.config(text="Upload documents to begin", fg=COL_MUTED)
        self.match_btn.config(state=tk.NORMAL, bg=COL_ACCENT, cursor="hand2",
                      text="⚡  BEGIN MATCHING")
        self.log_btn.config(state=tk.DISABLED)

        self.progress.stop()
        self.progress.pack_forget()

        for dot in self.dot_labels.values():
            dot.config(fg=COL_GREY_DOT)

        for w in self.result_frame.winfo_children():
            w.destroy()
        self._result_canvas.yview_moveto(0)

        for w in self.po_frame.winfo_children():
            w.destroy()

    # ── NORMALIZE ──────────────────────────────────────────────────────────

    def normalize_result(self, result: dict) -> dict:
        order1     = result.get("order1") or result.get("po1") or "—"
        order2     = result.get("order2") or result.get("po2") or "—"
        matched    = result.get("matched_items", result.get("matched", 0))
        total      = result.get("total_items",   result.get("total",   0))
        confidence = result.get("confidence", 0)
        is_match   = bool(result.get("match", False))

        extras = {}
        if "price_ok" in result and result["price_ok"] is not None:
            extras["Price Check"] = "✅ Pass" if result["price_ok"] else "❌ Fail"
        if "price_check_ok" in result:
            if result["price_check_ok"] is not None \
                    and not result.get("is_confirmation", False):
                extras["Price Match"] = \
                    "✅ Yes" if result["price_check_ok"] else "❌ No"
        if "qty_matched" in result and "qty_total" in result:
            extras["Qty Verified"] = \
                f"{result['qty_matched']} / {result['qty_total']}"
        if "color_match" in result:
            extras["Color"] = \
                "✅ Match" if result["color_match"] else "❌ No Match"
        if "config_match" in result and result.get("configuration"):
            extras["Config"] = \
                f"{'✅' if result['config_match'] else '❌'}  {result['configuration']}"
        if "order_match" in result:
            extras["Order Match"] = \
                "✅ Yes" if result["order_match"] else "❌ No"
        if "price_check_ok" in result and result["price_check_ok"] is not None:
            extras["Price Check"] = \
                "✅ Pass" if result["price_check_ok"] else "❌ Fail"
        if "price_match" in result and not result.get("is_confirmation", False):
            extras["Price match"] = \
                "✅ Yes" if result["price_match"] else "❌ No"
        if "color_match" in result:
            extras["Color Match"] = \
                "✅ Yes" if result["color_match"] else "❌ No"
        if "price_check" in result and isinstance(result["price_check"], dict):
            pc = result["price_check"]
            if pc.get("match") is True:
                extras["Price Check"] = "✅ Pass"
            elif pc.get("match") is False:
                extras["Price Check"] = "❌ Fail"
            elif pc.get("match") is None:
                extras["Price Check"] = "- No Prices"

        return {
            "match": is_match, "confidence": confidence,
            "matched": matched, "total": total,
            "order1": order1,   "order2": order2,
            "extras": extras,
            "is_confirmation": result.get("is_confirmation", False),
        }

    # ── LOG ────────────────────────────────────────────────────────────────

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

        ta = scrolledtext.ScrolledText(
            win, font=("Courier", 9), wrap=tk.WORD,
            padx=10, pady=10, bg=COL_SURFACE, fg=COL_TEXT)
        ta.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ta.insert(1.0, self.match_log)
        ta.config(state=tk.DISABLED)

        btn_row = tk.Frame(win, bg=COL_BG)
        btn_row.pack(pady=10)

        def show_extracted_text():
            txt_win = tk.Toplevel(win)
            txt_win.title("Extracted Document Text")
            txt_win.geometry("900x650")
            txt_win.configure(bg=COL_BG)

            hdr2 = tk.Frame(txt_win, bg=COL_ACCENT, padx=10, pady=10)
            hdr2.pack(fill=tk.X)
            tk.Label(hdr2, text="📄  Raw Extracted Text",
                    font=("Courier New", 13, "bold"),
                    bg=COL_ACCENT, fg="white").pack()

            ta2 = scrolledtext.ScrolledText(
                txt_win, font=("Courier", 10), wrap=tk.WORD,
                padx=16, pady=16, bg=COL_SURFACE, fg=COL_TEXT)
            ta2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            def clean_and_trim(text, filename):
                lines = text.split('\n')
                # Find first line containing a date pattern
                start = 0
                for i, line in enumerate(lines):
                    if re.search(r'\d{1,2}\s+\w+\s+\d{4}|\d{4}-\d{2}-\d{2}|Date\s*de\s*commande|Date:', line, re.IGNORECASE):
                        start = i
                        break
                trimmed = [l for l in lines[start:] if l.strip()]
                # Remove footer junk
                stop_keywords = ['Logiciel par', 'Page 1 de', 'Imprimé le', 'NOTRE PLATEFORME',
                                'POLITIQUE DE RETOUR', 'Cliquez ici', 'adfast.store',
                                'AUCUN RETOUR', 'Aucun retour', '• Aucun', '• 20%',
                                '• Le transport', '• Seules', '• Aucun remboursement']
                result = []
                for line in trimmed:
                    if any(kw in line for kw in stop_keywords):
                        break
                    result.append(f"    {line}")
                return '\n'.join(result)

            content = ""
            for file_num, (path, raw) in enumerate([(self.file1_path, self.doc1_raw_text),
                                                    (self.file2_path, self.doc2_raw_text)], 1):
                if not path:
                    continue
                fname = path.replace('\\', '/').split('/')[-1]
                content += f"{'━' * 55}\n"
                content += f"  DOC {file_num}  ▸  {fname}\n"
                content += f"{'━' * 55}\n"
                if raw:
                    content += clean_and_trim(raw, fname)
                else:
                    try:
                        raw_pdf = ""
                        with pdfplumber.open(path) as pdf:
                            for page in pdf.pages:
                                t = page.extract_text()
                                if t:
                                    raw_pdf += t + "\n"
                        content += clean_and_trim(raw_pdf, fname)
                    except Exception as e:
                        content += f"    Could not extract: {e}"
                content += "\n\n"

            ta2.insert(1.0, content)
            ta2.config(state=tk.DISABLED)

            tk.Button(txt_win, text="Close", font=FONT_BTN,
                    bg=COL_ACCENT, fg="white", cursor="hand2",
                    command=txt_win.destroy, relief=tk.FLAT,
                    padx=20, pady=10).pack(pady=10)

        file2_text = extract_text_from_pdf(self.file2_path) if self.file2_path else ""
        is_multi_po_facture = self.detected_supplier in ("DECKO", "THERMOPLAST") and "FACTURE" in file2_text.upper()

        if not is_multi_po_facture:
            tk.Button(btn_row, text="📄  View Extracted Text", font=FONT_BTN,
                bg=COL_SURFACE, fg=COL_TEXT, cursor="hand2",
                command=show_extracted_text, relief=tk.FLAT,
                padx=20, pady=10).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(btn_row, text="Close", font=FONT_BTN,
                bg=COL_ACCENT, fg="white", cursor="hand2",
                command=win.destroy, relief=tk.FLAT,
                padx=20, pady=10).pack(side=tk.LEFT) 


# ── ENTRY POINT ────────────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    HubGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()