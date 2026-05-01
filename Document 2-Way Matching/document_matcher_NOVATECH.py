"""
AI Document Matcher - GUI Version
Upload any 2 PDFs and check if they match
NOVATECH
** MAY NEED TO FIX COLOURS **
"""

from email.mime import text
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import scrolledtext
import pdfplumber
import re
from typing import Dict, List
from dataclasses import dataclass
from typing import Set
from difflib import SequenceMatcher
import threading
from collections import defaultdict
import os
from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@dataclass
class LineItem:
    product_code: str
    quantity: float
    unit_price: float
    total: float


@dataclass
class OrderDocument:
    order_number: str
    line_items: List[LineItem]
    total: float
    provider: str = "GENERIC"

@dataclass 
class ProductFingerprint:
    category: str = ""
    configuration: str = ""
    width: float = 0.0
    height: float = 0.0
    frame: str = ""
    glass_layers: int = 0
    low_e: bool = False
    argon: bool = False
    interior_color: str = ""
    exterior_color: str = ""
    extras: set[str] = None


class DocumentMatcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Resiver/Novatech Document Matcher")
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

        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg=self.primary_color)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Resiver/Novatech Document Matcher",
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
            text="Upload two PDF documents to compare",
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
        tk.Label(inner1, text="Dalmen Order or Novatech Confirmation",
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
        tk.Label(inner2, text="Dalmen Order or Novatech Confirmation",
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

    def run_comparison(self):
        try:
            print("Starting comparison...")
            print(f"File 1: {self.file1_path}")
            print(f"File 2: {self.file2_path}")
            
            print("Parsing first doc...")
            doc1 = self.parse_document(self.file1_path)
            print(f"Doc1 parsed: {len(doc1.line_items)} items found")
            print(f"Doc1 provider: {doc1.provider}")
            print(f"Doc1 has fingerprint: {hasattr(doc1, 'fingerprint') and doc1.fingerprint is not None}")
            
            print("Parsing second doc...")
            doc2 = self.parse_document(self.file2_path)
            print(f"Doc2 parsed: {len(doc2.line_items)} items found")
            print(f"Doc2 provider: {doc2.provider}")
            print(f"Doc2 has fingerprint: {hasattr(doc2, 'fingerprint') and doc2.fingerprint is not None}")

            print("Matching documents...")
            result = self.match_documents(doc1, doc2)
            print(f"Match result: {result}")
            
            print("Displaying result...")
            self.root.after(0, self.display_result, result)
            print("Done!")

        except Exception as e:
            import traceback
            print("ERROR OCCURRED:")
            print(traceback.format_exc())
            error_details = traceback.format_exc()
            self.root.after(0, self.display_error, f"{str(e)}\n\n{error_details}")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def extract_order_number(self, text: str) -> str:
        patterns = [
            r'Num[ée]ro?\s+de\s+bon\s*[\n\s]*([\d\-]+)',
            r'Votre\s+no\.\s+de\s+commande\s+([\d\-]+)',
            r'PO:\s*([\d\-]+)',
            r'ORDER\s*#\s*:\s*(\d+\-\d+)',
        ]
    
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                order_num = match.group(1).strip()
                if len(order_num) >= 8:
                    return order_num
        
        return "Unknown"
    
    def extract_total(self, text: str) -> float:
        patterns = [
            r'Total\s*:\s*([\d\s,\.]+)\s*\$',
            r'Total\s+([\d\s,\.]+)\s+CAD',
            r'Total\s*[:\s]*([\d\s,\.]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).replace(' ', '').replace(',', '.')
                try:
                    return float(value)
                except:
                    continue
        return 0.0
    
    def extract_line_items(self, text: str) -> List[LineItem]:
        items = []
        lines = text.split('\n')
        
        print(f"\nDEBUG: Parsing {len(lines)} lines")
        
        cleaned_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.endswith('-') and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if len(next_line) < 20 and next_line and not re.search(r'[\$,\.]', next_line):
                    print(f"  DEBUG: Joining '{line}' + '{next_line}'")
                    line = line + next_line
                    i += 1
            cleaned_lines.append(line)
            i += 1
        
        print(f"DEBUG: After line joining, have {len(cleaned_lines)} lines")
        
        for line in cleaned_lines:
            line = line.strip()
            
            if not any(x in line.upper() for x in ['CODE', 'DESCRIPTION', 'QTÉ', 'N° INTERNE']):
                decko_code_match = re.match(r'^([A-Z]+)\s*-\s*(\d+)', line)
                if decko_code_match:
                    product_code = f"{decko_code_match.group(1)}-{decko_code_match.group(2)}"
                    print(f"  Found [DECKO-CODE]: {product_code}")
                    if not any(item.product_code == product_code for item in items):
                        items.append(LineItem(
                            product_code=product_code,
                            quantity=1.0,
                            unit_price=0.0,
                            total=0.0
                        ))
                    continue
            
            m1 = re.match(r'^(\d+\s+)?\[([A-Z0-9\-\s\(\)]+)\]', line)
            if m1:
                product_code = m1.group(2).strip()
                total = None
                
                for idx, line in enumerate(cleaned_lines):
                    line_idx = idx
                for j in range(line_idx, min(line_idx + 10, len(cleaned_lines))):
                    pm = re.search(r'([\d\s,\.]+)\s+CAD', cleaned_lines[j])
                    if pm:
                        try:
                            val = pm.group(1).replace(' ', '').replace(',', '.')
                            t = float(val)
                            if t > 1:
                                total = t
                                break
                        except:
                            pass
                
                if product_code and total:
                    print(f"  Found [FIT]: {product_code} = ${total}")
                    items.append(LineItem(
                        product_code=product_code,
                        quantity=1.0,
                        unit_price=total,
                        total=total
                    ))
                    continue
            
            if re.search(r'\d+\.\d+\s*\$\s+[\d\s,\.]+\s*\$', line):
                code_match = re.match(r'^([A-Z0-9\-]+)', line)
                if code_match:
                    raw_code = code_match.group(1).strip()
                    product_code = raw_code.rstrip('-').strip()
                    
                    prices = re.findall(r'([\d\s,\.]+)\s*\$', line)
                    if prices and len(prices) >= 2:
                        total_str = prices[-1]
                        
                        try:
                            total = float(total_str.replace(' ', '').replace(',', '.'))
                            if total > 1 and product_code:
                                print(f"  Found [Dalmen]: {product_code} = ${total}")
                                items.append(LineItem(
                                    product_code=product_code,
                                    quantity=1.0,
                                    unit_price=total,
                                    total=total
                                ))
                                continue
                        except:
                            pass

            m2b = re.search(
                r'([A-Z]{2}\d{2}\.\d+).*?(\d+\.\d{2,4})\s*[A-Z]?$',
                line
            )       

            if m2b:
                product_code = m2b.group(1).strip()
                total_str = m2b.group(2).strip()

                try:
                    total = float(total_str.replace(',', ''))
                    if total > 1:
                        print(f" Found [DECKO]: {product_code} = ${total}")
                        items.append(LineItem(
                            product_code=product_code,
                            quantity=1.0,
                            unit_price=total,
                            total=total
                        ))
                        continue
                except:
                    pass

            m3 = re.match(r'^(\d+)\s+([A-Z0-9\.]+)\s+.+?\s+([\d,\.]+)$', line)
            if m3:
                product_code = m3.group(2).strip()
                total_str = m3.group(3).strip()

                try:
                    total = float(total_str.replace(',', '.'))
                    if total > 10:
                        print(f" Found [DECKO]: {product_code} = ${total}")
                        items.append(LineItem(
                            product_code=product_code,
                            quantity=1.0,
                            unit_price=total,
                            total=total
                        ))
                        continue
                except:
                    pass
            
            m4 = re.search(r'\b([A-Z]{2}\d{2}\.\d{4,}[A-Z]*)\b', line)
            if m4 and not any(x in line for x in ['TOTAL', 'PRIX', 'DESCRIPTION', 'QTE']):
                product_code = m4.group(1).strip()
                if not any(item.product_code == product_code for item in items):
                    print(f"  Found [DECKO-PO]: {product_code} (no total)")
                    items.append(LineItem(
                        product_code=product_code,
                        quantity=1.0,
                        unit_price=0.0,
                        total=0.0
                    ))
                    continue
        
        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items
    
    def detect_provider(self, text: str) -> str:
        t = text.upper()

        has_dalmen = "DALMEN" in t or "DA1LMEN" in t or "DALM EN" in t or "PRODUITS DALMEN" in t
        has_resiver = "RESIVER" in t or "RES1VER" in t
        has_novatech = "NOVATECH" in t

        if (has_resiver and has_dalmen) or (has_novatech and has_dalmen):
            return "RESIVER_NOVATECH"
        
        return "GENERIC"

    def extract_fingerprint(self, text: str) -> ProductFingerprint:
        t = text.upper()
        fp = ProductFingerprint(extras=set())

        print("\nDEBUG: Extracting fingerprint from text...")
        
        if "PATIO" in t or "PORTE-PATIO" in t or "PATIO DOOR" in t:
            fp.category = "PATIO_DOOR"
            print("  - Category: PATIO_DOOR")

        print(f"\nDEBUG: Searching for configuration...")
        print(f"  Text contains 'XO': {'XO' in t}")
        print(f"  Text contains '(XO)': {'(XO)' in t}")
        print(f"  Full text snippet: {t[:500]}")

        config_patterns = [
            r'2\s+OPENINGS?\s+\(([XO0]{4})\)',
            r'\(([XO0]{4})\)',
            r'\(([XO0]{2})\)',
            r'SECTIONS?,\s*([XO0]{2,4})',
            r'([XO0]{2,4}),\s*COLOR',
            r'([XO0]{2,4})\s*\(3013',
        ]
        
        for pattern in config_patterns:
            m = re.search(pattern, t)
            if m:
                config_text = m.group(1).upper()
                config_text = config_text.replace('0', 'O')
                fp.configuration = config_text
                print(f" - Configuration: {fp.configuration}")
                break

        if not fp.configuration:
            if re.search(r'\b(XO|X0)\b', t):
                fp.configuration = "XO"
                print(f"  - Configuration: XO (found standalone)")
            elif re.search(r'\b(OX|0X)\b', t):
                fp.configuration = "OX"
                print(f"  - Configuration: OX (found standalone)")

        print(f"\nDEBUG: Searching for dimensions...")
        for line in t.split('\n'):
            if re.search(r'\d+.*[Xx×].*\d+', line):
                print(f" Potential dim line: '{line}'")
    
        width_str = ""
        height_str = ""
        
        metric_match = re.search(r'(\d+)MM\s*\(\s*(\d+)\s+(\d+)/(\d+)\s*["\']?\s*\)\s*X\s*(\d+)MM\s*\(\s*(\d+)\s+(\d+)/(\d+)', t)
        if not metric_match:
            metric_match2 = re.search(r'(\d+)MM\s*\(\s*(\d+)\s+(\d+)/(\d+)\s*["\']?\s*\)\s*X\s*(\d+)MM\s*\(\s*(\d+)\s*["\']?\s*\)', t)
            if metric_match2:
                width_str = f"{metric_match2.group(2)} {metric_match2.group(3)}/{metric_match2.group(4)}"
                height_str = metric_match2.group(6)
                fp.width = float(metric_match2.group(2)) + float(metric_match2.group(3)) / float(metric_match2.group(4))
                fp.height = float(metric_match2.group(6))
                if 60 <= fp.width <= 200 and 70 <= fp.height <= 120:
                    print(f"  - Dimensions: {width_str}\" x {height_str}\"")
        
        if fp.width == 0.0 or fp.height == 0.0:
            metric_whole = re.search(r'(\d+)MM\s*\(\s*(\d+)\s*["\']?\s*\)\s*X\s*(\d+)MM\s*\(\s*(\d+)', t)
            if metric_whole:
                width_str = metric_whole.group(2)
                height_str = metric_whole.group(4)
                fp.width = float(metric_whole.group(2))
                fp.height = float(metric_whole.group(4))
                print(f"  - Dimensions: {width_str}\" x {height_str}\"")
        
        if fp.width == 0.0 or fp.height == 0.0:
            dim_patterns = [
                (r'(\d+)\s+(\d+)/(\d+)\s*[\"″\'\']\s*[Xx×]\s*(\d+)\s+(\d+)/(\d+)', 'both_fractions'),
                (r'(\d+)\s+(\d+)/(\d+)\s*[\"″\'\']?\s*[Xx×]\s*(\d+)', 'width_fraction'),
                (r'(\d{2,3})\s*[\"″\'\']?\s*[Xx×]\s*(\d{2,3})', 'simple'),
            ]
            
            for pattern, ptype in dim_patterns:
                dim = re.search(pattern, t)
                if dim:
                    try:
                        if ptype == 'both_fractions':
                            width_str = f"{dim.group(1)} {dim.group(2)}/{dim.group(3)}"
                            height_str = f"{dim.group(4)} {dim.group(5)}/{dim.group(6)}"
                            fp.width = float(dim.group(1)) + float(dim.group(2)) / float(dim.group(3))
                            fp.height = float(dim.group(4)) + float(dim.group(5)) / float(dim.group(6))
                        elif ptype == 'width_fraction':
                            width_str = f"{dim.group(1)} {dim.group(2)}/{dim.group(3)}"
                            height_str = dim.group(4)
                            fp.width = float(dim.group(1)) + float(dim.group(2)) / float(dim.group(3))
                            fp.height = float(dim.group(4))
                        else:
                            width_str = dim.group(1)
                            height_str = dim.group(2)
                            fp.width = float(dim.group(1))
                            fp.height = float(dim.group(2))
                        
                        if 60 <= fp.width <= 200 and 70 <= fp.height <= 120:
                            print(f"  - Dimensions: {width_str}\" x {height_str}\"")
                            break
                        else:
                            fp.width = 0.0
                            fp.height = 0.0
                    except:
                        continue

        frame_patterns = [
            (r'FRAME.*?VINYL', 'VINYL'),
            (r'VINYL.*?FRAME', 'VINYL'),
            (r'EXTERIOR\s+VINYL', 'VINYL'),
            (r'VINYL\s+ON', 'VINYL'),
            (r'FRAME.*?PVC', 'PVC'),
            (r'PVC.*?FRAME', 'PVC'),
            (r'CLADDING.*?PVC', 'PVC'),
            (r'PVC.*?CLADDING', 'PVC'),
            (r'FRAME.*?ALUMINUM', 'ALUMINUM'),
            (r'ALUMINUM.*?FRAME', 'ALUMINUM'),
            (r'EXTERIOR\s+ALUMINUM', 'ALUMINUM'),
            (r'FRAME.*?WOOD', 'WOOD'),
        ]

        for pattern, material in frame_patterns:
            if re.search(pattern, t):
                fp.frame = material
                print(f" - Frame: {material}")
                break

        low_e_patterns = [
            r'LOW-E',
            r'LOWE',
            r'LOW\s*E',
            r'80/71',
        ]
        
        for pattern in low_e_patterns:
            if re.search(pattern, t):
                fp.low_e = True
                print("  - Low-E: Yes")
                break
        
        argon_patterns = [
            r'ARGON',
            r'\bAR\b',
            r'\+\s*AR',
            r'AR,',
            r'AR\.',
        ]
        
        for pattern in argon_patterns:
            if re.search(pattern, t):
                fp.argon = True
                print("  - Argon: Yes")
                break
        
        t_oneline = t.replace('\n', ' ')

        color_patterns = [
            r'INT[/\s]*EXT[:\s]*([A-Z\s]+)[/]([A-Z\s]+)',
            r'COLOR\s+INT[/\s]*EXT[:\s]*([A-Z\s]+)[/]([A-Z\s]+)',
            r'([A-Z]+\s+[A-Z]+)[/]([A-Z]+)\s+K-',
            r'(WHITE)[/](BLACK)',
            r'(BLUE\s+WHITE)',
        ]
        
        for pattern in color_patterns:
            m = re.search(pattern, t_oneline)
            if m:
                if m.lastindex == 2:
                    interior = m.group(1).strip()
                    exterior = m.group(2).strip()
                    fp.interior_color = interior.replace(' ', '_')
                    fp.exterior_color = exterior.replace(' ', '_')
                    print(f" - Colors: Interior={fp.interior_color}, Exterior={fp.exterior_color}")
                    break
                elif m.lastindex == 1:
                    color = m.group(1).strip().replace(' ', '_')
                    fp.interior_color = color
                    fp.exterior_color = color
                    print(f" - Color: {color} (both sides)")
                    break

        if "SCREEN" in t or "WITH SCREEN" in t:
            fp.extras.add("SCREEN")
            print("  - Extra: SCREEN")

        if "BRICKMOULD" in t or "BRICK MOULD" in t or "SQUARE BRICKMOULD" in t:
            fp.extras.add("BRICKMOULD")
            print("- Extra: BRICKMOULD")

        if "NO BRICKMOULD" in t or "NO BRICKMOULD" in t:
            fp.extras.add("NO_BRICKMOULD")
            print("- Extra: NO_BRICKMOULD")
        
        if "NO PAINT" in t:
            fp.extras.add("NO_PAINT")
            print("  - Extra: NO_PAINT")
        
        if re.search(r'HANDLE[:\s]+\d+', t):
            fp.extras.add("HANDLE")
            print("  - Extra: HANDLE")
        
        return fp

    def compare_fingerprints(self, f1: ProductFingerprint, f2: ProductFingerprint) -> float:
        score = 0
        max_score = 0

        def cmp(a, b, weight):
            nonlocal score, max_score
            if a and b:
                max_score += weight
                if a == b:
                    score += weight
        
        cmp(f1.category, f2.category, 10)
        cmp(f1.configuration, f2.configuration, 10)

        if f1.width and f2.width:
            max_score += 10
            if abs(f1.width - f2.width) < 0.25:
                score += 10

        if f1.height and f2.height:
            max_score += 10
            if abs(f1.height - f2.height) < 0.25:
                score += 10
        
        cmp(f1.frame, f2.frame, 10)
        cmp(f1.glass_layers, f2.glass_layers, 10)

        if f1.low_e == f2.low_e:
            score += 5
        max_score += 5

        if f1.argon == f2.argon:
            score += 5
        max_score += 5

        extras_union = len(f1.extras | f2.extras)
        if extras_union:
            max_score += 10
            score += 10 * (len(f1.extras & f2.extras) / extras_union)
        
        return (score / max_score) * 100 if max_score else 0

    def match_resiver_documents(self, doc1, doc2):
        log = []
        log.append("="*60)
        log.append("RESIVER/NOVATECH FINGERPRINT MATCHING")
        log.append("="*60)
        
        score = 0
        
        log.append(f"\nOrder Numbers:")
        log.append(f"  Doc1: {doc1.order_number}")
        log.append(f"  Doc2: {doc2.order_number}")

        base1 = doc1.order_number.split('-')[:3]
        base2 = doc2.order_number.split('-')[:3]
        base1_str = '-'.join(base1) if len(base1) >= 3 else doc1.order_number
        base2_str = '-'.join(base2) if len(base2) >= 3 else doc2.order_number
        
        if doc1.order_number == doc2.order_number and doc1.order_number != "Unknown":
            score += 50
            log.append("  ✓ EXACT MATCH (+50 points)")
        elif base1_str == base2_str and base1_str != "Unknown":
            score += 48
            log.append(f"  ✓ BASE MATCH ({base1_str}, +48 points)")
        elif doc1.order_number != "Unknown" and doc2.order_number != "Unknown":
            if doc1.order_number in doc2.order_number or doc2.order_number in doc1.order_number:
                score += 45
                log.append("  ~ PARTIAL MATCH (+45 points)")
            else:
                similarity = self.calculate_similarity(doc1.order_number, doc2.order_number)
                if similarity > 0.7:
                    score += 40
                    log.append(f"  ~ SIMILAR ({similarity:.0%} match, +40 points)")
                else:
                    log.append("  ✗ Different order numbers (0 points)")
        else:
            log.append("  ✗ Order number missing from one document")
            log.append(" - Will rely on fingerprint matching")
            score += 20

        log.append(f"\n{'='*60}")
        log.append("PRODUCT FINGERPRINT COMPARISON:")
        log.append(f"{'='*60}")
        
        fp1 = doc1.fingerprint
        fp2 = doc2.fingerprint
        
        fingerprint_score = 0
        fingerprint_max = 0
        
        log.append(f"\n[CATEGORY]")
        log.append(f"  Doc1: {fp1.category or 'Not specified'}")
        log.append(f"  Doc2: {fp2.category or 'Not specified'}")
        if fp1.category and fp2.category:
            fingerprint_max += 5
            if fp1.category == fp2.category:
                fingerprint_score += 5
                log.append(f"  ✓ Match (+5)")
            else:
                log.append(f"  ✗ Different")
        
        log.append(f"\n[CONFIGURATION]")
        log.append(f"  Doc1: {fp1.configuration or 'Not specified'}")
        log.append(f"  Doc2: {fp2.configuration or 'Not specified'}")
        if fp1.configuration and fp2.configuration:
            fingerprint_max += 15
            if fp1.configuration == fp2.configuration:
                fingerprint_score += 15
                log.append(f"  ✓ Match (+15)")
            else:
                log.append(f"  ✗ Different")
        
        log.append(f"\n[DIMENSIONS]")
        log.append(f"  Doc1: {fp1.width:.2f}\" x {fp1.height:.2f}\"")
        log.append(f"  Doc2: {fp2.width:.2f}\" x {fp2.height:.2f}\"")
        if fp1.width and fp2.width and fp1.height and fp2.height:
            fingerprint_max += 15
            width_diff = abs(fp1.width - fp2.width)
            height_diff = abs(fp1.height - fp2.height)
            
            if width_diff < 0.5 and height_diff < 0.5:
                fingerprint_score += 15
                log.append(f"  ✓ Match within tolerance (+15)")
            elif width_diff < 1.0 and height_diff < 1.0:
                fingerprint_score += 10
                log.append(f"  ~ Close match (+10)")
            else:
                log.append(f"  ✗ Different (diff: {width_diff:.2f}\" x {height_diff:.2f}\")")
        
        log.append(f"\n[FRAME MATERIAL]")
        log.append(f"  Doc1: {fp1.frame or 'Not specified'}")
        log.append(f"  Doc2: {fp2.frame or 'Not specified'}")
        if fp1.frame and fp2.frame:
            fingerprint_max += 5
            if fp1.frame == fp2.frame:
                fingerprint_score += 5
                log.append(f"  ✓ Match (+5)")
            else:
                log.append(f"  ✗ Different")
        
        log.append(f"\n[GLASS CONFIGURATION]")
        log.append(f"  Doc1: Low-E: {fp1.low_e}, Argon: {fp1.argon}")
        log.append(f"  Doc2: Low-E: {fp2.low_e}, Argon: {fp2.argon}")
        fingerprint_max += 5
        if fp1.low_e == fp2.low_e and fp1.argon == fp2.argon:
            fingerprint_score += 5
            log.append(f"  ✓ Full match (+5)")
        elif fp1.low_e == fp2.low_e or fp1.argon == fp2.argon:
            fingerprint_score += 3
            log.append(f"  ~ Partial match (+3)")
        else:
            log.append(f"  ✗ Different")
        
        log.append(f"\n[COLORS]")
        log.append(f"  Doc1: Interior={fp1.interior_color or 'N/A'}, Exterior={fp1.exterior_color or 'N/A'}")
        log.append(f"  Doc2: Interior={fp2.interior_color or 'N/A'}, Exterior={fp2.exterior_color or 'N/A'}")
        
        if (fp1.interior_color or fp1.exterior_color) and (fp2.interior_color or fp2.exterior_color):
            fingerprint_max += 5
            color_match = True
            if fp1.interior_color and fp2.interior_color and fp1.interior_color != fp2.interior_color:
                color_match = False
            if fp1.exterior_color and fp2.exterior_color and fp1.exterior_color != fp2.exterior_color:
                color_match = False
            
            if color_match:
                fingerprint_score += 5
                log.append(f"  ✓ Colors match (+5)")
            else:
                log.append(f"  ✗ Different colors")
        
        log.append(f"\n[EXTRAS/OPTIONS]")
        log.append(f"  Doc1: {', '.join(sorted(fp1.extras)) if fp1.extras else 'None'}")
        log.append(f"  Doc2: {', '.join(sorted(fp2.extras)) if fp2.extras else 'None'}")
        
        if fp1.extras or fp2.extras:
            fingerprint_max += 10
            if fp1.extras and fp2.extras:
                extras_union = len(fp1.extras | fp2.extras)
                extras_intersect = len(fp1.extras & fp2.extras)
                if extras_union > 0:
                    extras_score = 10 * (extras_intersect / extras_union)
                    fingerprint_score += extras_score
                    log.append(f"  ~ Similarity: {extras_intersect}/{extras_union} ({extras_score:.1f} points)")
            else:
                log.append(f"  - Only one document has extras specified")
        
        if fingerprint_max > 0:
            fp_percentage = (fingerprint_score / fingerprint_max) * 100
            score += (fp_percentage / 100) * 50
            log.append(f"\nFingerprint Score: {fingerprint_score:.1f}/{fingerprint_max} = {fp_percentage:.1f}%")
            log.append(f"Contributes: {(fp_percentage / 100) * 50:.1f}")
        else:
            log.append(f"\n Warning: No comparable fingerprint data found")

        documents_match = score >= 70
        
        log.append("\n" + "="*60)
        log.append(f"FINAL SCORE: {score:.1f}/100")
        log.append(f"Threshold: 70 points")
        log.append(f"Result: {'✓ DOCUMENTS MATCH' if documents_match else '✗ DOCUMENTS DO NOT MATCH'}")
        log.append("="*60)
        
        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        fp1 = doc1.fingerprint
        fp2 = doc2.fingerprint
        config_match = bool(fp1.configuration and fp2.configuration and fp1.configuration == fp2.configuration)
        frame_match  = bool(fp1.frame and fp2.frame and fp1.frame == fp2.frame)

        # Order is considered matched for exact, base, partial, or similar
        order_match = score >= 40  # any branch that added ≥40 points means orders are related

        return {
            "match": documents_match,
            "confidence": score,
            "matched_items": 1,
            "total_items": 1,
            "order1": doc1.order_number,
            "order2": doc2.order_number,
            "total1": doc1.total,
            "total2": doc2.total,
            "total_diff": abs(doc1.total - doc2.total),
            "configuration": fp1.configuration or fp2.configuration or "N/A",
            "config_match": config_match,
            "frame": fp1.frame or fp2.frame or "N/A",
            "frame_match": frame_match,
            "order_match": order_match,
        }

    def needs_ocr(self, text):
        has_code = bool(re.search(r'[A-Z]{2,}\s*-\s*\d+', text))
        has_price = bool(re.search(r'\d+\.\d{2}', text))
        
        print(f"DEBUG needs_ocr: has_code={has_code}, has_price={has_price}")
        return not (has_code or has_price)
        
    def ocr_pdf(self, pdf_path):
        images = convert_from_path(
            pdf_path, 
            dpi=300,
            poppler_path=r"C:\poppler\Library\bin"
            )
        
        ocr_lines = []

        for img in images:
            text = pytesseract.image_to_string(
                img,
                config="--psm 4 -c preserve_interword_spaces=1"
            )
            ocr_lines.extend(
                line.strip() 
                for line in text.splitlines() 
                if line.strip()
            )

        return ocr_lines

    def normalize_ocr_line(self, line):
        fixes = {
            'V S': 'VS',
            'V A': 'VA',
            'O': '0',
            'I': '1',
            ',': '.'
        }
        for bad, good in fixes.items():
            line = line.replace(bad, good)
        return line

    def extract_pdf_text(self, pdf_path):
        all_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
        return all_text

    def contains_prices(self, text):
        return bool(re.search(r'\$\s*\d+\.\d{2}|\d+\.\d{2}', text))
    
    def normalize_price_text(self, text):
        t = text.upper()
        t = t.replace('O', '0').replace('S', '$')
        t = re.sub(r'(\d)\s+(\d)', r'\1\2', t)
        t = re.sub(r'(\d+),(\d{2})', r'\1.\2', t)
        t = re.sub(r'(\d)[,\.](\d{3})', r'\1\2', t)
        return t

    def parse_document(self, pdf_path: str) -> OrderDocument:
        text = self.extract_pdf_text(pdf_path)

        if not text or len(text.strip()) < 50:
            print("DEBUG: pdfplumber returned empty - forcing OCR")
            ocr_lines = self.ocr_pdf(pdf_path)
            text = "\n".join([self.normalize_ocr_line(l) for l in ocr_lines])
        
        print(f"DEBUG: Text preview (first 500 chars):")
        print(text[:500])
        print(f"DEBUG: Contains 'DALMEN': {'DALMEN' in text.upper()}")
        print(f"DEBUG: Contains 'DECKO': {'DECKO' in text.upper()}")
        print(f"DEBUG: Contains 'TAMARACK': {'TAMARACK' in text.upper()}")
        print(f"DEBUG: Contains 'Fournisseur': {'FOURNISSEUR' in text.upper()}")

        provider = self.detect_provider(text)
        print(f"DEBUG: Detected provider: {provider}")

        normalized_text = self.normalize_price_text(text)

        use_ocr = False
        if provider == "DECKO_DALMEN":
            has_content = bool(re.search(r'[A-Z]{2,}\s*-?\s*\d+|XO|OX|\d+\s*["\']?\s*[Xx]\s*\d+', text))
            print(f"DEBUG: DECKO doc has content: {has_content}")
            if not has_content:
                use_ocr = True
                print("DEBUG: OCR required for DECKO doc - missing product specs")
        else:
            if self.needs_ocr(normalized_text) or not self.contains_prices(normalized_text):
                use_ocr = True
                print("DEBUG: OCR required: missing prices or product codes...")
        
        if use_ocr:
            ocr_lines = self.ocr_pdf(pdf_path)
            text = "\n".join([self.normalize_ocr_line(l) for l in ocr_lines])
            normalized_text = self.normalize_price_text(text)
 
        fingerprint = None
        if provider == "RESIVER_NOVATECH":
            fingerprint = self.extract_fingerprint(text)
            print(f"DEBUG: Extracted fingerprint: {fingerprint}")

        order_number = self.extract_order_number(text)
        line_items = self.extract_line_items(normalized_text)
        total = self.extract_total(normalized_text)
    
        doc = OrderDocument(
            order_number=order_number,
            line_items=line_items,
            total=total,
            provider=provider
        )
        doc.fingerprint = fingerprint
        doc.raw_text = text
        return doc

    def normalize_code(self, code: str) -> str:
        code = code.upper()
        code = re.sub(r'\(.*?\)', '', code)
        code = re.sub(r'\s+', '', code)
        code = re.sub(r'^CL-', '', code)
        code = re.sub(r'([A-Z]{2}\d{2}\.\d{4,})([A-Z]+)$', r'\1', code)
        return code.strip()
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def base_code(self, code: str) -> str:
        return code.split()[0] if code else code
    
    def aggregate(self, items):
        agg = defaultdict(lambda: {"total": 0.0, "label": ""})
        for i in items:
            key = self.base_code(i.product_code)
            if i.total > 0:
                agg[key]["total"] += i.total
            if not agg[key]["label"]:
                agg[key]["label"] = i.product_code
        return agg

    def match_documents(self, doc1: OrderDocument, doc2: OrderDocument) -> Dict:
        if (doc1.provider == "RESIVER_NOVATECH" and doc2.provider == "RESIVER_NOVATECH" and
            hasattr(doc1, 'fingerprint') and hasattr(doc2, 'fingerprint') and
            doc1.fingerprint and doc2.fingerprint):
            
            print("Using RESIVER fingerprint matching...")
            return self.match_resiver_documents(doc1, doc2)
        
        log = []
        log.append("="*60)
        log.append("MATCHING ANALYSIS")
        log.append("="*60)
        
        agg1 = self.aggregate(doc1.line_items)
        agg2 = self.aggregate(doc2.line_items)
        
        log.append(f"\nDoc1 aggregated items: {len(agg1)}")
        for key, data in agg1.items():
            log.append(f"  {key}: {data['label']} = ${data['total']:.2f}")
        
        log.append(f"\nDoc2 aggregated items: {len(agg2)}")
        for key, data in agg2.items():
            log.append(f"  {key}: {data['label']} = ${data['total']:.2f}")

        matched = 0

        log.append("\n" + "-"*60)
        log.append("MATCHING PROCESS:")
        log.append("-"*60)

        for key1, data1 in agg1.items():
            total1 = data1["total"]
            label1 = data1["label"]
            best_match = None
            best_diff = float("inf")
            best_sim = 0

            for key2, data2 in agg2.items():
                total2 = data2["total"]
                label2 = data2["label"]

                sim = self.calculate_similarity(
                    self.normalize_code(label1),
                    self.normalize_code(label2)
                )
                diff = abs(total1 - total2)

                if total1 == 0 or total2 == 0:
                    if sim > 0.80 and sim > best_sim:
                        best_match = label2
                        best_diff = 0
                        best_sim = sim
                else:
                    if sim > 0.60 and diff < best_diff:
                        best_match = label2
                        best_diff = diff
                        best_sim = sim
            
            if total1 == 0 or (best_match and data2.get("total", 0) == 0):
                threshold = 0
            else:
                threshold = max(5.0, total1 * 0.10)
            
            matched_this = best_match and (best_diff <= threshold or threshold == 0)
            
            log.append(f"\n{label1} (${total1:.2f})")
            if best_match:            
                log.append(f"  Best match: {best_match} (${total1-best_diff:.2f})")
                log.append(f"  Similarity: {best_sim:.1%}, Diff: ${best_diff:.2f}, Threshold: ${threshold:.2f}")
                log.append(f"  Result: {'✓ MATCH' if matched_this else '✗ NO MATCH'}")
            else:
                log.append(f"  No match found")
            
            if matched_this:
                matched += 1
        
        total_items = max(len(agg1), len(agg2))
        match_percentage = (matched / total_items * 100) if total_items > 0 else 0
        documents_match = match_percentage >= 70
        
        log.append("\n" + "="*60)
        log.append(f"FINAL RESULT: {matched}/{total_items} items matched ({match_percentage:.1f}%)")
        log.append(f"Documents match: {documents_match}")
        log.append("="*60)
        
        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        return {
            "match": documents_match,
            "confidence": match_percentage,
            "matched_items": matched,
            "total_items": total_items,
            "order1": doc1.order_number,
            "order2": doc2.order_number,
            "total1": doc1.total,
            "total2": doc2.total,
            "total_diff": abs(doc1.total - doc2.total),
            "configuration": "N/A",
            "config_match": False,
            "frame": "N/A",
            "frame_match": False,
        }

    # ── UI DISPLAY ────────────────────────────────────────────────────────────

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

        order_icon  = "✅" if result.get('order_match', result['order1'] == result['order2']) else "❌"
        config_icon = "✅" if result.get('config_match') else "❌"
        frame_icon  = "✅" if result.get('frame_match')  else "❌"
        stat_box(stats, "Order Numbers",  f"{order_icon}  {result['order1']} / {result['order2']}", 0)
        stat_box(stats, "Items Matched",  f"{result['matched_items']} / {result['total_items']}", 1)
        stat_box(stats, "Configuration", f"{config_icon}  {result.get('configuration', 'N/A')}", 2)
        stat_box(stats, "Frame Material", f"{frame_icon}  {result.get('frame', 'N/A')}", 3)

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