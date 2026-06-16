"""
AI Document Matcher - GUI Version
Upload any 2 PDFs and check if they match
FORIMPEX - 2-Way Matching for FORIMPEX Provider
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import scrolledtext
import pdfplumber
import re
from typing import Dict, List
from dataclasses import dataclass
from difflib import SequenceMatcher
import threading
import pytesseract

import sys, os 
def get_tesseract_path():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
        bundled = os.path.join(base, '_internal', 'tesseract', 'tesseract.exe')
        if os.path.exists(bundled):
            os.environ['TESSDATA_PREFIX'] = os.path.join(base, '_internal', 'tessdata')
            return bundled
    return r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

@dataclass
class LineItem:
    product_code: str
    description: str
    quantity: int = 1
    unit_price: float = 0.0
    raw_code: str = ""

@dataclass
class OrderDocument:
    order_number: str
    line_items: List[LineItem]
    provider: str = "FORIMPEX"
    doc_type: str = "UNKNOWN"

class DocumentMatcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Forimpex Matcher")
        self.root.geometry("820x680")
        self.root.resizable(False, False)
        self.bg_color = "#f0f0f0"
        self.primary_color = "#667eea"
        self.success_color = "#4caf50"
        self.error_color = "#f44336"
 
        self.root.configure(bg=self.bg_color)
 
        self.file1_path = None
        self.file2_path = None
        self.match_log = ""

        self.load_forimpex_price_list()
        self.create_widgets()

    
    def load_forimpex_price_list(self):
        self.forimpex_qty_per_pack = {}
        price_list_path = r"\\10.0.7.2\Group\2026 PRICE LIST\ListePrix_FORIMPEX_LATEST.pdf"
        try:
            with pdfplumber.open(price_list_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            if not row or len(row) < 4:
                                continue
                            code = str(row[0]).strip().upper()
                            qty_cell = row[3]
                            if not code.startswith('FX') or not qty_cell:
                                continue
                            try:
                                self.forimpex_qty_per_pack[code] = int(str(qty_cell).strip())
                            except (ValueError, TypeError):
                                continue
                    text = page.extract_text()
                    if not text:
                        continue
                    for line in text.split('\n'):
                        m = re.match(r'^(FX[\w\-]+)\s+.+?\s+(BAR|UN|PC)\s+(\d+)\s+\d', line, re.IGNORECASE)
                        if m: 
                            code = m.group(1).upper()
                            if code not in self.forimpex_qty_per_pack:
                                self.forimpex_qty_per_pack[code] = int(m.group(3))
            print(f"Loaded {len(self.forimpex_qty_per_pack)} FORIMPEX price list entries")
        except Exception as e:
            print(f"WARNING: Could not load FORIMPEX price list: {e}")
            self.forimpex_qty_per_pack = {}
 
    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg=self.primary_color)
        header.pack(fill=tk.X)
 
        tk.Label(
            header,
            text="Forimpex Matcher",
            font=("Arial", 22, "bold"),
            bg=self.primary_color, fg="white"
        ).pack(side=tk.LEFT, padx=24, pady=16)
 
        self.log_btn = tk.Button(
            header,
            text="📋  View Log",
            font=("Arial", 10, "bold"),
            bg="#5568d3", fg="white",
            cursor="hand2",
            command=self.show_log_window,
            relief=tk.FLAT, padx=14, pady=8,
            state=tk.DISABLED
        )
        self.log_btn.pack(side=tk.RIGHT, padx=20, pady=14)
 
        tk.Label(
            header,
            text="Match Dalmen orders with Forimpex confirmations",
            font=("Arial", 10),
            bg=self.primary_color, fg="#ccd4ff"
        ).pack(side=tk.RIGHT, padx=4, pady=14)
 
        # Body
        body = tk.Frame(self.root, bg=self.bg_color, padx=24, pady=20)
        body.pack(fill=tk.BOTH, expand=True)
 
        # Side-by-side doc panels
        docs_row = tk.Frame(body, bg=self.bg_color)
        docs_row.pack(fill=tk.X)
        docs_row.columnconfigure(0, weight=1)
        docs_row.columnconfigure(1, weight=1)
 
        # Doc 1 card
        card1 = tk.Frame(docs_row, bg="white", bd=1, relief=tk.SOLID)
        card1.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
 
        tk.Frame(card1, bg=self.primary_color, height=4).pack(fill=tk.X)
 
        inner1 = tk.Frame(card1, bg="white", padx=18, pady=16)
        inner1.pack(fill=tk.BOTH, expand=True)
 
        tk.Label(inner1, text="DOC 1", font=("Arial", 9, "bold"),
                 bg="white", fg=self.primary_color).pack(anchor="w")
        tk.Label(inner1, text="Dalmen Purchase Order",
                 font=("Arial", 8), bg="white", fg="#888").pack(anchor="w", pady=(0, 10))
 
        self.file1_label = tk.Label(
            inner1, text="No file selected",
            font=("Arial", 9), bg="white", fg="#aaa", anchor="w",
            wraplength=260, justify="left"
        )
        self.file1_label.pack(fill=tk.X, pady=(0, 12))
 
        tk.Button(
            inner1, text="📁  Browse PDF",
            font=("Arial", 10, "bold"),
            bg=self.primary_color, fg="white",
            cursor="hand2", command=lambda: self.browse_file(1),
            relief=tk.FLAT, padx=16, pady=9
        ).pack(fill=tk.X)
 
        # Doc 2 card
        card2 = tk.Frame(docs_row, bg="white", bd=1, relief=tk.SOLID)
        card2.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
 
        tk.Frame(card2, bg=self.primary_color, height=4).pack(fill=tk.X)
 
        inner2 = tk.Frame(card2, bg="white", padx=18, pady=16)
        inner2.pack(fill=tk.BOTH, expand=True)
 
        tk.Label(inner2, text="DOC 2", font=("Arial", 9, "bold"),
                 bg="white", fg=self.primary_color).pack(anchor="w")
        tk.Label(inner2, text="Forimpex Confirmation",
                 font=("Arial", 8), bg="white", fg="#888").pack(anchor="w", pady=(0, 10))
 
        self.file2_label = tk.Label(
            inner2, text="No file selected",
            font=("Arial", 9), bg="white", fg="#aaa", anchor="w",
            wraplength=260, justify="left"
        )
        self.file2_label.pack(fill=tk.X, pady=(0, 12))
 
        tk.Button(
            inner2, text="📁  Browse PDF",
            font=("Arial", 10, "bold"),
            bg=self.primary_color, fg="white",
            cursor="hand2", command=lambda: self.browse_file(2),
            relief=tk.FLAT, padx=16, pady=9
        ).pack(fill=tk.X)
 
        # Compare button
        self.compare_btn = tk.Button(
            body,
            text="⚡  Compare Documents",
            font=("Arial", 13, "bold"),
            bg=self.primary_color, fg="white",
            cursor="hand2", command=self.compare_documents,
            relief=tk.FLAT, padx=30, pady=14,
            state=tk.DISABLED
        )
        self.compare_btn.pack(fill=tk.X, pady=(18, 0))
 
        # Progress bar
        self.progress = ttk.Progressbar(body, mode='indeterminate')
 
        # Result area
        self.result_frame = tk.Frame(body, bg=self.bg_color)
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=(16, 0))
 
    def browse_file(self, file_num):
        filename = filedialog.askopenfilename(
            title=f"Select Document {file_num}",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            display_name = filename.replace('\\', '/').split('/')[-1]
            if file_num == 1:
                self.file1_path = filename
                self.file1_label.config(text=f"✓ {display_name}", fg=self.success_color)
            else:
                self.file2_path = filename
                self.file2_label.config(text=f"✓ {display_name}", fg=self.success_color)
 
            if self.file1_path and self.file2_path:
                self.compare_btn.config(state=tk.NORMAL)

    
    def compare_documents(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        self.progress.pack(pady=20)
        self.progress.start(10)
        self.compare_btn.config(state=tk.DISABLED)

        thread = threading.Thread(target=self.run_comparison)
        thread.daemon = True
        thread.start()

    def run_comparison(self): # For the log
        try:
            print("Starting Forimpex order comparison...")
            print(f"File 1: {self.file1_path}")
            print(f"File 2: {self.file2_path}")

            doc1 = self.parse_document(self.file1_path)
            print(f" Doc1 parsed: {len(doc1.line_items)} item found")
            
            doc2 = self.parse_document(self.file2_path)
            print(f" Doc2 parsed: {len(doc2.line_items)} items found")

            result = self.match_documents(doc1, doc2)
            print(f"Match result: {result}")

            self.root.after(0, self.display_result, result)
            print("Done!")

        except Exception as e:
            import traceback
            print("ERROR OCCURED:")
            print(traceback.format_exc())
            error_details = traceback.format_exc()
            self.root.after(0, self.display_error, f"{str(e)}\n\nDetails:\n{error_details}")


    def extract_pdf_text(self, pdf_path: str, page_num: int = None) -> str:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            if page_num is not None:
                # Extract specific page (0-indexed)
                if page_num < len(pdf.pages):
                    page_text = pdf.pages[page_num].extract_text()
                    if page_text:
                        text = page_text
            else:
                # Extract all pages
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        return text

    def extract_order_number(self, text: str, doc_type: str) -> str:
        patterns = [
            r'Bon de Commande\s*\n\s*#\s*(\d{5,})',
            r'#\s*(\d{5,6})\s*\n',
            r'NO DE COMMANDE\s+EXP[^\n]*\n[^\n]*\n\s*(\d{5,})',
            r'NO DE COMMANDE CLIENT\s*(\d+)',
            r'NO DE COMMANDE\b[^\n]*?(\b\d{5,}\b)',
            r'NO DE COMMANDE\s*\n?\s*(\d+)',
            r'Numéro de PO\s*(\d+)',
            r'Purchase Order\s*#?\s*(\d+)',
            r'Bon de Commande\s*#?\s*(\d+)',
            r'(?<!\d)#\s*(\d{5,6})(?!\d)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
            BLACKLIST = {'5630', '2268', '3070', '5250', '4350'}

            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    candidate = match.group(1).strip()
                    if candidate not in BLACKLIST:
                        return candidate

            return "Unknown"

    
    def extract_keywords(self, description: str) -> set:
        desc = description.upper()
        keywords = set()

        keywords.update(re.findall(r'\d+\s+\d+/\d+', desc))
        keywords.update(re.findall(r'\d+"', desc))

        for word in ['NOIR', 'BLANC', 'ALUMINIUM', 'BK', 'WH', 'LAMELLE', 'NOIRES']:
            if word in desc:
                keywords.add(word)

        return keywords


    def normalize_forimpex_code(self, code: str) -> str: # To filter out diff types of code combinations
        code = code.upper().strip().replace(' ', '').replace('¥', 'X')
        if not code:
            return code

        code = code.upper().strip().replace(' ', '')

        # Strip ALL OCR junk letters between FX and the first digit (handles FxX532, FXX-5183, etc.)
        code = re.sub(r'^FX[A-Z]+-?', 'FX-', code)
        code = re.sub(r'^FX(\d)', r'FX-\1', code)

        # Extract just the numeric part after FX-
        m = re.match(r'^FX-(\d+)', code)
        if m:
            return f"FX - {m.group(1)}"

        return code

    
    def parse_dalmen_order(self, text: str, pdf_path: str, target_po: str) -> List[LineItem]:
        items = []

        print(f"DEBUG: Parsing Dalmen order...")

        table_items = self._parse_dalmen_via_tables(pdf_path)
        if table_items:
            print(f"DEBUG: Table strategy found {len(table_items)} items")
            return table_items

        print(f"DEBUG: Table strategy found nothing — falling back to text parsing")
        print(f"DEBUG PO full text:\n{text}")

        lines = text.split('\n')
        for i, line in enumerate(lines):
            line = line.strip().replace('¥', 'X')

            match1 = re.match(
                r'^(\d+)\s+(?:PAQUETS?|BOITES?|BOITE)\s+DE\s+(FX[A-Z]*-?[\d][\w\-]*)\s+(.+)$',
                line, re.IGNORECASE
            )
            match2 = re.match(
                r'^(?:PAQUETS?|BOITES?|BOITE)\s+DE\s+(FX[A-Z]*-?[\d][\w\-]*)',
                line, re.IGNORECASE
            )

            if match1:
                quantity = int(match1.group(1))
                product_code = match1.group(2)
                description = line
            elif match2:
                product_code = match2.group(1)
                description = line
                leading_qty = re.match(r'^(\d+)\s+', line)
                if leading_qty:
                    quantity = int(leading_qty.group(1))
                else:
                    quantity = 1
                    for prev in reversed(lines[max(0, i - 5):i]):
                        prev_stripped = prev.strip()
                        lone_num = re.match(r'^\s*(\d+)\s*$', prev_stripped)
                        if lone_num:
                            quantity = int(lone_num.group(1))
                            break
                        end_num = re.search(r'\s(\d+)\s*$', prev_stripped)
                        if end_num and not re.search(r'(FX|PAQUETS|BOITES|tél|fax)', prev_stripped, re.IGNORECASE):
                            quantity = int(end_num.group(1))
                            break
            else:
                continue

            normalized_code = self.normalize_forimpex_code(product_code)
            print(f"  Found item: {product_code} (normalized: {normalized_code}) | Qty: {quantity} | DESC: {description[:50]}")
            items.append(LineItem(
                product_code=normalized_code,
                description=description,
                quantity=quantity,
                raw_code=product_code,
            ))

        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items


    def _parse_dalmen_via_tables(self, pdf_path: str) -> List[LineItem]:
        items = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    for table in tables:
                        qty_col = None
                        desc_col = None

                        for row in table:
                            if not row:
                                continue

                            row_upper = [str(c).upper() if c else "" for c in row]
                            if qty_col is None:
                                for ci, cell in enumerate(row_upper):
                                    if 'QTÉ' in cell or 'QTY' in cell:
                                        qty_col = ci
                                    if 'DESCRIPTION' in cell:
                                        desc_col = ci
                                if qty_col is not None:
                                    print(f"  [TABLE] Page {page_num+1}: qty_col={qty_col}, desc_col={desc_col}")
                                continue

                            effective_qty_col  = qty_col  if qty_col  is not None else 0
                            effective_desc_col = desc_col if desc_col is not None else 1

                            if effective_desc_col >= len(row):
                                continue

                            desc_cell = str(row[effective_desc_col] or "").strip().replace('¥', 'X')

                            if not re.search(r'(?:PAQUETS?|BOITES?|BOITE)\s+DE\s+FX', desc_cell, re.IGNORECASE):
                                continue

                            qty_cell = str(row[effective_qty_col] or "").strip() if effective_qty_col < len(row) else ""
                            try:
                                quantity = int(qty_cell)
                            except (ValueError, TypeError):
                                quantity = None
                                print(f"  [TABLE] ⚠️ Qty cell unreadable: '{qty_cell}' for → {desc_cell[:50]}")

                            code_match = re.search(r'(FX[A-Z]*-?[\d][\w\-]*)', desc_cell, re.IGNORECASE)
                            if not code_match:
                                continue
                            product_code = code_match.group(1)
                            normalized_code = self.normalize_forimpex_code(product_code)

                            print(f"  [TABLE] {product_code} (norm: {normalized_code}) | Qty: {quantity} | {desc_cell[:50]}")

                            items.append(LineItem(
                                product_code=normalized_code,
                                description=desc_cell,
                                quantity=quantity if quantity is not None else 0,
                                raw_code=product_code,
                            ))

        except Exception as e:
            print(f"  [TABLE] extract_tables() failed: {e}")

        return items


    def parse_forimpex_confirmation(self, text: str, target_po: str) -> List[LineItem]:
        items = []
        lines = text.split('\n')

        print(f"DEBUG: Parsing Forimpex confirmation...")

        in_table = False

        for i, line in enumerate(lines):
            line = line.strip()

            if "NO D'INVENTAIRE" in line or "NO D\'INVENTAIRE" in line:
                in_table = True
                print(f" Found table at line {i}")
                print(f"DEBUG: Next 10 lines after table header:")
                for j in range(i+1, min(i+11, len(lines))):
                    print(f" Line {j}: {lines[j][:100]}")
                continue

            if not in_table:
                continue
            
            if re.match(r'^FX[\d\-]+', line):
                print(f" DEBUG: Found FX line at {i}: {line[:100]}")
                parts = line.split(None, 1)
                if len(parts) >= 2:
                    product_code = parts[0].strip()
                    rest = parts[1].strip()

                    desc_match = re.match(r'^(.+?)\s+\d{4}-\d{2}-\d{2}', rest)
                    if desc_match:
                        description = desc_match.group(1).strip()
                    else:
                        description = rest
                        
                    qty_match = re.search(r'\d{4}-\d{2}-\d{2}\s+(\d+)\.00', line)
                    if qty_match:
                        quantity = int(qty_match.group(1))
                    else:
                        quantity = 1

                    normalized_code = self.normalize_forimpex_code(product_code)

                    print(f"Found: {product_code} (normalized: {normalized_code}) | Qty: {quantity} | DESC: {description[:50]}")

                    items.append(LineItem(
                        product_code=normalized_code,
                        description=description,
                        quantity=quantity
                    ))
 
        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items

    
    def parse_forimpex_facture(self, text: str, target_po: str) -> List[LineItem]:
        items = []
        lines = text.split('\n')
        in_table = False

        print(f"DEBUG: Parsing Forimpex facture...")


        for i, line in enumerate(lines):
            line_stripped = line.strip()

            if "NO D'INVENTAIRE" in line_stripped or "NO D\'INVENTAIRE" in line_stripped:
                in_table = True
                print(f" Found table at line {i}")
                continue

            if not in_table or not line_stripped:
                continue

            fx_match = re.search(r'(FX-[\w\-]+)', line_stripped, re.IGNORECASE)
            if not fx_match:
                continue

            fx_match = re.search(r'(FX-[\w\-]+)', line_stripped, re.IGNORECASE)
            if not fx_match:
                continue

            product_code = fx_match.group(1)
            if product_code.upper().startswith('PAL'):
                continue

            rest = line_stripped[fx_match.end():].strip()


            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not re.search(r'FX-', next_line) and not re.search(r'\d+\.\d+\$', next_line):
                    rest = rest + ' ' + next_line

            desc_match = re.match(r'^(.+?)\s+[\d,]+\.\d+\$', rest)
            description = desc_match.group(1).strip() if desc_match else rest

            normalized_code = self.normalize_forimpex_code(product_code)
            print(f" Found: {product_code} (normalized: {normalized_code}) | DESC: {description[:60]}")

            before_fx = line_stripped[:fx_match.start()].strip()
            qty_nums = re.findall(r'\d+', before_fx)
            if len(qty_nums) >= 2:
                qty_shipped = int(qty_nums[1])
            elif len(qty_nums) == 1:
                qty_shipped = int(qty_nums[0])
            else:
                qty_shipped = 0

            price_match = re.search(r'([\d,]+\.\d{2})\$', rest)
            unit_price = float(price_match.group(1).replace(',', '')) if price_match else 0.0

            items.append(LineItem(
                product_code=normalized_code,
                description=description,
                quantity=qty_shipped,
                unit_price=unit_price,
                raw_code=product_code,
            ))
        
        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items


    def parse_document(self, pdf_path: str, doc_type: str = None) -> OrderDocument:
        # just to detect doc type
        text = self.extract_pdf_text(pdf_path)

        if not doc_type:
            if "FACTURE" in text:
                doc_type = "FORIMPEX_FACTURE"
            elif "Forimpex" in text or "Saint-Joseph-de-Beauce" in text:
                doc_type = "FORIMPEX"
            elif "Dalmen Portes" in text or "Purchase Order" in text or "Bon de Commande" in text:
                doc_type = "DALMEN"
            else:
                doc_type = "DALMEN"  # default assumption if pdfplumber got nothing

        print(f"DEBUG: Detected document type: {doc_type}")

        # For Dalmen POs — always OCR page 2
        if doc_type == "DALMEN":
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    page = pdf.pages[1] if len(pdf.pages) > 1 else pdf.pages[0]
                    img = page.to_image(resolution=400)
                    text = pytesseract.image_to_string(
                        img.original,
                        config='--psm 6 --oem 3 preserve_interword_spaces=1'
                    )
                    print(f"DEBUG: OCR extracted {len(text)} chars")
            except Exception as e:
                print(f"DEBUG: OCR failed: {e}")

        print(f"\nDEBUG: Text preview (first 500 chars):\n{text[:500]}\n")

        order_number = self.extract_order_number(text, doc_type)
        print(f"DEBUG: Extracted order number: {order_number}")

        if doc_type == "DALMEN":
            line_items = self.parse_dalmen_order(text, pdf_path, order_number)
        elif doc_type == "FORIMPEX":
            line_items = self.parse_forimpex_confirmation(text, order_number)
        elif doc_type == "FORIMPEX_FACTURE":
            line_items = self.parse_forimpex_facture(text, order_number)
        else:
            line_items = []

        return OrderDocument(
            order_number=order_number,
            line_items=line_items,
            provider="FORIMPEX",
            doc_type=doc_type
        )

    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


    def match_documents(self, doc1: OrderDocument, doc2: OrderDocument) -> Dict:
        log = []

        order_match = doc1.order_number == doc2.order_number

        # ── SUMMARY ───────────────────────────────────────────────────────
        log.append("=" * 60)
        log.append("SUMMARY")
        log.append("=" * 60)

        col_width = 38
        log.append(f"{'Doc1 — ' + str(len(doc1.line_items)) + ' items':<{col_width}}  {'Doc2 — ' + str(len(doc2.line_items)) + ' items'}")
        log.append("-" * 60)

        for i in range(max(len(doc1.line_items), len(doc2.line_items))):
            left  = f"  {doc1.line_items[i].product_code} | Qty: {doc1.line_items[i].quantity}" if i < len(doc1.line_items) else ""
            right = f"  {doc2.line_items[i].product_code} | Qty: {doc2.line_items[i].quantity}" if i < len(doc2.line_items) else ""
            log.append(f"{left:<{col_width}}  {right}")

        log.append("")
        po_str = "✅ MATCH" if order_match else "❌ NO MATCH"
        log.append(f"  Order Numbers — Doc1: {doc1.order_number}  |  Doc2: {doc2.order_number}  →  {po_str}")

        # ── MATCHING PROCESS ──────────────────────────────────────────────
        log.append("")
        log.append("=" * 60)
        log.append("MATCHING PROCESS")
        log.append("=" * 60)

        matched     = 0
        total_items = max(len(doc1.line_items), len(doc2.line_items))
        qty_matched = 0
        qty_total   = 0
        facture_mode = doc1.doc_type == "FORIMPEX_FACTURE" or doc2.doc_type == "FORIMPEX_FACTURE"

        if len(doc1.line_items) == 0 or len(doc2.line_items) == 0:
            log.append("")
            if len(doc1.line_items) == 0:
                log.append("  ⚠️  No items found in Doc1 (Dalmen order)")
            if len(doc2.line_items) == 0:
                log.append("  ⚠️  No items found in Doc2 (Forimpex confirmation)")
            match_percentage = 0
            documents_match  = False
        else:
            for item1 in doc1.line_items:
                best_score = 0
                best_match = None
                kw1 = self.extract_keywords(item1.description)

                for item2 in doc2.line_items:
                    score = 0
                    if item1.product_code == item2.product_code:
                        score += 60

                    if facture_mode:
                        def get_dim(code):
                            m = re.search(r'-(\d{2,3})"?$', code.replace(' ', ''))
                            return m.group(1) if m else None

                        dim1 = get_dim(item1.raw_code)
                        dim2 = get_dim(item2.raw_code)
                        desc_dims1 = set(re.findall(r'\d+\s+\d+/\d+|\d+"', item1.description.upper()))
                        desc_dims2 = set(re.findall(r'\d+\s+\d+/\d+|\d+"', item2.description.upper()))

                        if dim1 and dim2:
                            if dim1 == dim2:
                                score += 25
                        elif desc_dims1 and desc_dims2:
                            if desc_dims1 & desc_dims2:
                                score += 25

                        finish = {'NOIR', 'BLANC', 'BK', 'WH', 'NOIRES', 'ALUMINIUM'}
                        kw2 = self.extract_keywords(item2.description)
                        if kw1 & finish & kw2:
                            score += 15
                    else:
                        kw2 = self.extract_keywords(item2.description)
                        dim1 = set(re.findall(r'\d+\s+\d+/\d+|\d+"', item1.description.upper()))
                        dim2 = set(re.findall(r'\d+\s+\d+/\d+|\d+"', item2.description.upper()))
                        if dim1 and dim2 and dim1 & dim2:
                            score += 20
                        finish = {'NOIR', 'BLANC', 'BK', 'WH', 'NOIRES', 'ALUMINIUM',
                                'RECOUVREMENT', 'REVETEMENT', 'BALAI'}
                        if kw1 & finish & kw2:
                            score += 10

                    if score > best_score:
                        best_score = score
                        best_match = item2

                log.append("")
                result_str = "✅ MATCH" if best_match and best_score >= 70 else "❌ NO MATCH"
                sim_str    = f"(Score: {best_score}/100)"

                if best_match:
                    log.append(f"  {item1.product_code:<20}  →  {best_match.product_code:<20}  {sim_str:<18}  {result_str}")
                    log.append(f"  PO Qty: {item1.quantity} paquets   |   Shipped: {best_match.quantity} units")

                    if best_score >= 70:
                        matched += 1
                        if facture_mode and best_match.quantity > 0:
                            facture_full_code = best_match.raw_code.upper() if best_match.raw_code else ""
                            qty_per_pack = self.forimpex_qty_per_pack.get(facture_full_code)
                            if qty_per_pack:
                                qty_total += 1
                                po_qty = item1.quantity
                                po_qty_unreadable = (po_qty == 0) or (po_qty == 1 and best_match.quantity > qty_per_pack)

                                if po_qty_unreadable:
                                    reverse = best_match.quantity / qty_per_pack
                                    if reverse == int(reverse):
                                        inferred_qty = int(reverse)
                                        qty_matched += 1
                                        log.append(f"  📦 PO qty unreadable — inferred: {best_match.quantity} ÷ {qty_per_pack}/pqt = {inferred_qty} paquets  ✅")
                                    else:
                                        log.append(f"  📦 PO qty unreadable — reverse-calc not whole ({best_match.quantity} ÷ {qty_per_pack} = {best_match.quantity / qty_per_pack:.2f})  ⚠️ VERIFY MANUALLY")
                                else:
                                    expected = po_qty * qty_per_pack
                                    actual   = best_match.quantity
                                    qty_ok   = abs(expected - actual) <= max(1, expected * 0.1)
                                    if qty_ok:
                                        qty_matched += 1
                                    log.append(f"  📦 {po_qty} paquets × {qty_per_pack}/pqt = {expected} expected  |  {actual} shipped  →  {'✅ OK' if qty_ok else '❌ MISMATCH'}")
                            else:
                                log.append(f"  📦 No price list entry for {facture_full_code} — qty check skipped")
                else:
                    log.append(f"  {item1.product_code:<20}  →  no match found")

            match_percentage = (matched / total_items * 100) if total_items > 0 else 0
            if total_items <= 5:
                documents_match = matched >= (total_items - 1) and order_match
            else:
                documents_match = match_percentage >= 70 and (order_match or match_percentage >= 80)

        # ── FINAL RESULT ──────────────────────────────────────────────────
        log.append("")
        log.append("=" * 60)
        log.append("FINAL RESULT")
        log.append("=" * 60)
        log.append(f"  {matched}/{total_items} items matched ({match_percentage:.1f}%)")
        log.append(f"  Order numbers: {'✅ MATCH' if order_match else '❌ NO MATCH'}")
        log.append(f"  Documents match: {'✅ YES' if documents_match else '❌ NO'}")
        log.append("=" * 60)

        # ── PRICE VERIFICATION ────────────────────────────────────────────
        if facture_mode:
            log.append("")
            log.append("=" * 60)
            log.append("PRICE VERIFICATION")
            log.append("=" * 60)

            price_list_path = r"G:\2026 PRICE LIST\ListePrix_FORIMPEX_LATEST.pdf"
            catalog = {}
            try:
                with pdfplumber.open(price_list_path) as pdf:
                    for page in pdf.pages:
                        tables = page.extract_tables()
                        for table in tables:
                            for row in table:
                                if not row or len(row) < 2:
                                    continue
                                code = str(row[0]).strip().upper()
                                price_cell = row[-1]
                                if not code.startswith('FX') or not price_cell:
                                    continue
                                try:
                                    catalog[code] = float(
                                        str(price_cell).replace(',', '.').replace('$', '').strip()
                                    )
                                except:
                                    continue
            except Exception as e:
                log.append(f"  ⚠️  Could not load price list: {e}")

            facture_doc = doc2 if doc2.doc_type == "FORIMPEX_FACTURE" else doc1
            for item in facture_doc.line_items:
                facture_price = item.unit_price
                full_code     = item.raw_code.upper() if item.raw_code else ""

                # 1. Exact match
                catalog_price = catalog.get(full_code)

                # 2. Strip trailing size suffix and match prefix
                if not catalog_price:
                    stripped = re.sub(r'-\d{3,4}$', '', full_code)
                    if stripped:
                        for cat_code, price in catalog.items():
                            if cat_code.startswith(stripped):
                                catalog_price = price
                                break

                # 3. Base number only — flag ambiguous
                if not catalog_price:
                    base = re.match(r'^(FX-\d+)', full_code)
                    if base:
                        matches = [(c, p) for c, p in catalog.items() if c.startswith(base.group(1))]
                        if len(matches) == 1:
                            catalog_price = matches[0][1]
                        elif len(matches) > 1:
                            log.append("")
                            log.append(f"  {item.product_code:<20}  ⚠️  Ambiguous — {len(matches)} catalog entries match {base.group(1)}, manual review needed")
                            continue

                log.append("")
                if catalog_price and facture_price > 0:
                    diff   = abs(facture_price - catalog_price)
                    # price difference threshold
                    tol    = 0.50
                    status = "✅ PASS" if diff <= tol else "❌ FAIL"
                    log.append(f"  {item.product_code:<20}  Catalog: ${catalog_price:<10.2f}  Facture: ${facture_price:<10.2f}  Diff: ${diff:.2f}  {status}")
                elif facture_price == 0:
                    log.append(f"  {item.product_code:<20}  ⚠️  No price extracted from facture")
                else:
                    log.append(f"  {item.product_code:<20}  ❌  Not found in price list")

        if facture_mode:
            passed = sum(1 for item in facture_doc.line_items if item.unit_price > 0)
            failed = sum(1 for item in facture_doc.line_items if item.unit_price > 0 and abs(item.unit_price - (catalog.get(item.raw_code.upper() 
                            if item.raw_code else "", 0) or 0)) > 0.50)
            price_check_ok = (failed / passed) < 0.5 if passed > 0 else None
        else:
            price_check_ok = None

        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        return {
            "match": documents_match,
            "confidence": match_percentage,
            "matched_items": matched,
            "qty_matched": qty_matched,
            "qty_total": qty_total,
            "total_items": total_items,
            "price_check_ok": price_check_ok,
            "order1": doc1.order_number,
            "order2": doc2.order_number,
            "order_match": order_match,
        }

    
    def display_result(self, result):
        self.progress.stop()
        self.progress.pack_forget()
        self.compare_btn.config(state=tk.NORMAL)
        self.log_btn.config(state=tk.NORMAL)
 
        for widget in self.result_frame.winfo_children():
            widget.destroy()
 
        is_match = result['match']
        accent = self.success_color if is_match else self.error_color
 
        # Result card
        card = tk.Frame(self.result_frame, bg="white", bd=1, relief=tk.SOLID)
        card.pack(fill=tk.BOTH, expand=True)
 
        # Coloured top stripe
        tk.Frame(card, bg=accent, height=5).pack(fill=tk.X)
 
        inner = tk.Frame(card, bg="white", padx=24, pady=18)
        inner.pack(fill=tk.BOTH, expand=True)
 
        # Icon + verdict + confidence
        top_row = tk.Frame(inner, bg="white")
        top_row.pack(fill=tk.X)
 
        icon = "✅" if is_match else "❌"
        verdict = "DOCUMENTS MATCH" if is_match else "DOCUMENTS DO NOT MATCH"
 
        tk.Label(top_row, text=icon, font=("Arial", 28),
                 bg="white").pack(side=tk.LEFT)
 
        tk.Label(top_row, text=verdict,
                 font=("Arial", 16, "bold"), bg="white", fg=accent
                 ).pack(side=tk.LEFT, padx=12)
 
        tk.Label(top_row,
                 text=f"{result['confidence']:.0f}% confidence",
                 font=("Arial", 11), bg="white", fg="#666"
                 ).pack(side=tk.RIGHT)
 
        # Divider
        tk.Frame(inner, bg="#e0e0e0", height=1).pack(fill=tk.X, pady=(14, 14))
 
        # Stats row
        stats = tk.Frame(inner, bg="white")
        stats.pack(fill=tk.X, pady=(0, 14))
 
        def stat_box(parent, label, value, col):
            box = tk.Frame(parent, bg="#f8f8f8", padx=14, pady=10, bd=1, relief=tk.SOLID)
            box.grid(row=0, column=col, padx=(0 if col == 0 else 8, 0), sticky="ew")
            parent.columnconfigure(col, weight=1)
            tk.Label(box, text=value, font=("Arial", 14, "bold"),
                     bg="#f8f8f8", fg="#222").pack()
            tk.Label(box, text=label, font=("Arial", 8),
                     bg="#f8f8f8", fg="#888").pack()
 
        order_icon = "✅" if result.get('order_match') else "❌"
        stat_box(stats, "Order Numbers",  f"{order_icon}  {result['order1']} / {result['order2']}", 0)
        stat_box(stats, "Items Matched",  f"{result['matched_items']} / {result['total_items']}", 1)
        stat_box(stats, "Quantity Verified",  f"{result.get('qty_matched', 0)} / {result.get('qty_total', 0)}", 2)
        stat_box(stats, "Order Match",    f"{order_icon}  {'Yes' if result.get('order_match') else 'No'}", 3)
 
        # View Log button
        tk.Button(
            inner,
            text="📋  View Detailed Log",
            font=("Arial", 10, "bold"),
            bg=self.primary_color, fg="white",
            cursor="hand2", command=self.show_log_window,
            relief=tk.FLAT, padx=18, pady=9
        ).pack(fill=tk.X)
 
    def display_error(self, error_msg):
        self.progress.stop()
        self.progress.pack_forget()
        self.compare_btn.config(state=tk.NORMAL)
        messagebox.showerror("Error", f"Failed to process documents:\n\n{error_msg}")
 
    def show_log_window(self):
        win = tk.Toplevel(self.root)
        win.title("Detailed Matching Log")
        win.geometry("800x600")
 
        header = tk.Frame(win, bg=self.primary_color, padx=10, pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text="Detailed Matching Log", font=("Arial", 16, "bold"),
                 bg=self.primary_color, fg="white").pack()
 
        ta = scrolledtext.ScrolledText(win, font=("Courier", 9), wrap=tk.WORD, padx=10, pady=10)
        ta.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ta.insert(1.0, self.match_log)
        ta.config(state=tk.DISABLED)
 
        tk.Button(win, text="Close", font=("Arial", 11, "bold"), bg=self.primary_color,
                  fg="white", cursor="hand2", command=win.destroy,
                  relief=tk.FLAT, padx=20, pady=10).pack(pady=10)
 
 
def main():
    root = tk.Tk()
    DocumentMatcherGUI(root)
    root.mainloop()
 
 
if __name__ == "__main__":
    main()