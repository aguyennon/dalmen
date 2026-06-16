"""
AI Document Matcher - GUI Version
Upload any 2 PDFs and check if they match
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
from collections import defaultdict
import os
from pdf2image import convert_from_path
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


def get_poppler_path():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
        bundled = os.path.join(base, '_internal', 'poppler')
        if os.path.exists(bundled):
            return bundled
    return r"C:\poppler\Library\bin"

@dataclass
class LineItem:
    product_code: str
    quantity: float
    unit_price: float
    total: float
    specs: dict = None


@dataclass
class OrderDocument:
    order_number: str
    line_items: List[LineItem]
    total: float


class DocumentMatcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Document Matcher")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Configure colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#667eea"
        self.success_color = "#4caf50"
        self.error_color = "#f44336"
        
        self.root.configure(bg=self.bg_color)
        
        # File paths
        self.file1_path = None
        self.file2_path = None
        self.match_log = ""
        
        # Create UI
        self.create_widgets()

        self.load_viscan_price_list()

    def show_log_window(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("Detailed Log")
        log_window.geometry("800x600")

        header = tk.Frame(log_window, bg=self.primary_color, padx=10, pady=10)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Detailed Log",
            font=("Arial", 16, "bold"),
            bg=self.primary_color,
            fg="white"
        ).pack()

        from tkinter import scrolledtext
        text_area = scrolledtext.ScrolledText(
            log_window,
            font=("courier", 9),
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text_area.insert(1.0, self.match_log)
        text_area.config(state=tk.DISABLED)

        tk.Button(
            log_window,
            text="Close",
            font=("Arial", 11, "bold"),
            bg=self.primary_color,
            fg="white",
            cursor="hand2",
            command=log_window.destroy,
            relief=tk.FLAT,
            padx=20,
            pady=10
        ).pack(pady=10)


    def print_log(self):
        import tempfile

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("DOCUMENT MATCHER - DETAILED LOG\n")
            f.write("="*60 + "\n\n")
            f.write(self.match_log)
            temp_path = f.name
        
        try:
            if os.name == 'nt':
                os.startfile(temp_path, "print")
            else:
                os.system(f"lpr {temp_path}")

            messagebox.showinfo("Print", "Document sent to printer!")
        except Exception as e:
            messagebox.showerror("Print Error", f"Failed to print: {str(e)}")
            


    def create_widgets(self):
        header = tk.Frame(self.root, bg=self.primary_color)
        header.pack(fill=tk.X)

        tk.Label(header, text="VISCAN Matcher", font=("Arial", 22, "bold"),
                bg=self.primary_color, fg="white").pack(side=tk.LEFT, padx=24, pady=16)

        self.log_btn = tk.Button(header, text="📋  View Log", font=("Arial", 10, "bold"),
                                bg="#5568d3", fg="white", cursor="hand2",
                                command=self.show_log_window, relief=tk.FLAT,
                                padx=14, pady=8, state=tk.DISABLED)
        self.log_btn.pack(side=tk.RIGHT, padx=20, pady=14)

        tk.Label(header, text="Match Dalmen orders with Viscan invoices",
                font=("Arial", 10), bg=self.primary_color, fg="#ccd4ff").pack(side=tk.RIGHT, padx=4)

        body = tk.Frame(self.root, bg=self.bg_color, padx=24, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        docs_row = tk.Frame(body, bg=self.bg_color)
        docs_row.pack(fill=tk.X)
        docs_row.columnconfigure(0, weight=1)
        docs_row.columnconfigure(1, weight=1)

        card1 = tk.Frame(docs_row, bg="white", bd=1, relief=tk.SOLID)
        card1.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        tk.Frame(card1, bg=self.primary_color, height=4).pack(fill=tk.X)
        inner1 = tk.Frame(card1, bg="white", padx=18, pady=16)
        inner1.pack(fill=tk.BOTH, expand=True)
        tk.Label(inner1, text="DOC 1", font=("Arial", 9, "bold"),
                bg="white", fg=self.primary_color).pack(anchor="w")
        tk.Label(inner1, text="Dalmen Purchase Order", font=("Arial", 8),
                bg="white", fg="#888").pack(anchor="w", pady=(0, 10))
        self.file1_label = tk.Label(inner1, text="No file selected", font=("Arial", 9),
                                    bg="white", fg="#aaa", anchor="w", wraplength=260, justify="left")
        self.file1_label.pack(fill=tk.X, pady=(0, 12))
        tk.Button(inner1, text="📁  Browse PDF", font=("Arial", 10, "bold"),
                bg=self.primary_color, fg="white", cursor="hand2",
                command=lambda: self.browse_file(1), relief=tk.FLAT,
                padx=16, pady=9).pack(fill=tk.X)

        card2 = tk.Frame(docs_row, bg="white", bd=1, relief=tk.SOLID)
        card2.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        tk.Frame(card2, bg=self.primary_color, height=4).pack(fill=tk.X)
        inner2 = tk.Frame(card2, bg="white", padx=18, pady=16)
        inner2.pack(fill=tk.BOTH, expand=True)
        tk.Label(inner2, text="DOC 2", font=("Arial", 9, "bold"),
                bg="white", fg=self.primary_color).pack(anchor="w")
        tk.Label(inner2, text="Viscan Invoice", font=("Arial", 8),
                bg="white", fg="#888").pack(anchor="w", pady=(0, 10))
        self.file2_label = tk.Label(inner2, text="No file selected", font=("Arial", 9),
                                    bg="white", fg="#aaa", anchor="w", wraplength=260, justify="left")
        self.file2_label.pack(fill=tk.X, pady=(0, 12))
        tk.Button(inner2, text="📁  Browse PDF", font=("Arial", 10, "bold"),
                bg=self.primary_color, fg="white", cursor="hand2",
                command=lambda: self.browse_file(2), relief=tk.FLAT,
                padx=16, pady=9).pack(fill=tk.X)

        self.compare_btn = tk.Button(body, text="⚡  Compare Documents",
                                    font=("Arial", 13, "bold"), bg=self.primary_color,
                                    fg="white", cursor="hand2", command=self.compare_documents,
                                    relief=tk.FLAT, padx=30, pady=14, state=tk.DISABLED)
        self.compare_btn.pack(fill=tk.X, pady=(18, 0))

        self.progress = ttk.Progressbar(body, mode='indeterminate')

        self.result_frame = tk.Frame(body, bg=self.bg_color)
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=(16, 0))

    def compare_documents(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        self.progress.pack(pady=20)
        self.progress.start(10)
        self.compare_btn.config(state=tk.DISABLED)

        thread = threading.Thread(target=self.run_comparison)
        thread.daemon = True
        thread.start()
    
    def browse_file(self, file_num):
        filename = filedialog.askopenfilename(
            title=f"Select Document {file_num}",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if filename:
            if file_num == 1:
                self.file1_path = filename
                # Handle both forward and backslash
                display_name = filename.replace('\\', '/').split('/')[-1]
                self.file1_label.config(
                    text=f"✓ {display_name}",
                    fg=self.success_color
                )
            else:
                self.file2_path = filename
                display_name = filename.replace('\\', '/').split('/')[-1]
                self.file2_label.config(
                    text=f"✓ {display_name}",
                    fg=self.success_color
                )
            
            # Enable compare button if both files selected
            if self.file1_path and self.file2_path:
                self.compare_btn.config(state=tk.NORMAL)

    def run_comparison(self):
        try:
            print("Starting comparison...")
            print(f"File 1: {self.file1_path}")
            print(f"File 2: {self.file2_path}")
            
            print("Parsing first doc...")
            doc1 = self.parse_document(self.file1_path)
            print(f"Doc1 parsed: {len(doc1.line_items)} items found")
            
            print("Parsing second doc...")
            doc2 = self.parse_document(self.file2_path)
            print(f"Doc2 parsed: {len(doc2.line_items)} items found")

            print("Matching documents...")
            result = self.match_documents(doc1, doc2)
            result['order2'] = result['order1']
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
        """Extract all text from PDF"""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def extract_order_number(self, text: str) -> str:
        patterns = [
            r'COMMANDE\s+CLIENT\s*#?\s*\.?\s*(\d{5,})',
            r'Purchase\s+Order\s+Bon\s+de\s+Commande\s+#\s*(\d+)',
            r'Bon\s+de\s+Commande\s+#\s*(\d+)',
            r'Commande\s+n°\s*(\w+)',
            r'Numéro de PO\s+(\d+)',
            r'(?:Order|PO)\s*[#:]*\s*(\d+)',
            r'commande\s+(\d+)',
            r'#\s*(\d{5,})',
        ]

        print(f"\nDEBUG: Searching for order number...")
        print(f"DEBUG: Text preview: {text[:300]}")

        for i, pattern in enumerate(patterns):
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                order_num = match.group(1).strip()
                print(f" Pattern {i+1} matched: {order_num}")
                return order_num

        print(f" Not Found in any pattern")
        return "Unknown"

    def extract_viscan_specs(self, text: str) -> Dict[str, str]:
        specs = {}

        size_match = re.search(r'#?(\d+)\s*[Xx×]\s*(\d+)"?', text)
        if size_match:
            specs['size'] = f"{size_match.group(1)}X{size_match.group(2)}"

        head_types = ['TRUSS', 'FLAT', 'PANWASHER', 'FLATUNDERCUT', 'PAN', 'OVAL', 'ROUND']
        for head in head_types:  
            if re.search(rf"['\"]?{head}['\"]?", text, re.IGNORECASE):
                specs['head'] = head
                break
        
        return specs
    
    def extract_total(self, text: str) -> float:
        """Extract document total"""
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
        """Extract line items from document"""
        items = []
        lines = text.split('\n')
        
        print(f"\nDEBUG: Parsing {len(lines)} lines")
        
        # Join lines that are continuation
        cleaned_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # If line ends with hyphen and next line exists
            if line.endswith('-') and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # If next line is < 20 chars and alphanumeric, join them
                if len(next_line) < 20 and next_line and not re.search(r'[\$,\.]', next_line):
                    print(f"  DEBUG: Joining '{line}' + '{next_line}'")
                    line = line + next_line
                    i += 1  # Skip next line
            cleaned_lines.append(line)
            i += 1
        
        print(f"DEBUG: After line joining, have {len(cleaned_lines)} lines")
        
        for line in cleaned_lines:
            line = line.strip()

            if 'VA07' in line or '36.8' in line:
                print(f" DEBUG FACTURE LINE: '{line}")

            m_viscan_facture = re.search(r'([A-Z]{2}\d{2}\.\d+).+?(\d{2,}\.[\d]{4})\s*\|?\s*M', line)
            if m_viscan_facture:
                product_code = m_viscan_facture.group(1).strip()
                unit_price = float(m_viscan_facture.group(2))
                specs = self.extract_viscan_specs(line)
                print(f" Found [VISCAN-FACTURE]: {product_code} | unit: {unit_price}")
                items.append(LineItem(
                    product_code=product_code,
                    quantity=1.0,
                    unit_price=unit_price,
                    total=0.0
                ))
                continue

            m_viscan_po = re.match(r'^(\d+)\s+BOITE\s+DE\s+(\d+)\s+.+?\s+([A-Z]{2}\d{2}\.\d+)', line, re.IGNORECASE)
            if m_viscan_po:
                boxes = float(m_viscan_po.group(1))
                screws_per_box = float(m_viscan_po.group(2))
                product_code = m_viscan_po.group(3).strip()
                specs = self.extract_viscan_specs(line)
                print(f"  Found [VISCAN-PO]: {product_code} | boxes: {boxes} | per box: {screws_per_box}")
                items.append(LineItem(
                    product_code=product_code,
                    quantity=boxes,
                    unit_price=screws_per_box,
                    total=0.0
                ))
                continue

            # PATTERN 1: FIT format 
            m1 = re.match(r'^(\d+\s+)?\[([A-Z0-9\-\s\(\)]+)\]', line)
            if m1:
                product_code = m1.group(2).strip()
                total = None
                
                # Look in the NEXT 10 lines only (not all cleaned_lines)
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
                                break  # Stop at first valid total
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
                # Line has the price pattern, try to extract code
                code_match = re.match(r'^([A-Z0-9\-]+)', line)
                if code_match:
                    raw_code = code_match.group(1).strip()
                    # Clean up trailing hyphens and spaces
                    product_code = raw_code.rstrip('-').strip()
                    
                    # Extract the final price (last $ amount)
                    prices = re.findall(r'([\d\s,\.]+)\s*\$', line)
                    if prices and len(prices) >= 2:
                        total_str = prices[-1]  # Last price is the total
                        
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

                specs = self.extract_viscan_specs(line)

                try:
                    total = float(total_str.replace(',', ''))
                    if total > 1:
                        print(f" Found [VISCAN]: {product_code} = ${total}, specs={specs}")
                        item = LineItem(
                            product_code=product_code,
                            quantity=1.0,
                            unit_price=total,
                            total=total
                        )
                        item.specs = specs
                        items.append(item)
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
                        print(f" Found [VISCAN]: {product_code} = ${total}")
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
                # Check if we already have this code
                if not any(item.product_code == product_code for item in items):
                    specs = self.extract_viscan_specs(line)
                    print(f"  Found [VISCAN-PO]: {product_code} (no total), specs={specs}")

                    item = LineItem(
                        product_code=product_code,
                        quantity=1.0,
                        unit_price=0.0,
                        total=0.0
                    )
                    item.specs = specs
                    items.append(item)
                    continue
        
        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items

    
    def load_viscan_price_list(self):
        import pandas as pd
        self.viscan_prices = {}
        try:
            df = pd.read_excel(
                r"\\10.0.7.2\Group\Taxi\2026 PRICE LIST\VISCAN - Accumulated LIST.xlsx",
                sheet_name="Sheet1",
                usecols="E,I",
                header=0
            )
            df.columns = ["code", "price_per_1000"]
            df = df.dropna(subset=["code", "price_per_1000"])
            for _, row in df.iterrows():
                code = str(row["code"]).strip()
                self.viscan_prices[code] = float(row["price_per_1000"])
            print(f"Loaded {len(self.viscan_prices)} Viscan prices")
            print(f"DEBUG: Looking for VA07.1019 in price list: {'VA07.1019' in self.viscan_prices}")
            for k in self.viscan_prices:
                if '07' in k:
                    print(f"  Found similar: {k}")
        except Exception as e:
            print(f"Failed to load Viscan price list: {e}" )
            self.viscan_prices = {}
    
    def needs_ocr(self, lines):
        has_code = any(re.search(r'[A-Z]{2}\d{2}\.\d+', l) for l in lines)
        has_price = any(re.search(r'\d+\.\d{2}', l) for l in lines)
        return not (has_code and has_price)
        
    def ocr_pdf(self, pdf_path):
        images = convert_from_path(
            pdf_path, 
            dpi=300,
            poppler_path=get_poppler_path()
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
        lines = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    lines.extend(
                        line.strip()
                        for line in text.splitlines()
                        if line.strip()
                    )
            return lines


    def contains_prices(self, lines):
        return any(
        re.search(r'\$\s*\d+\.\d{2}', l) or
        re.search(r'\d+\.\d{2}', l)
        for l in lines
    )
    
    def normalize_price_text(self, text):
        t = text.upper()

        # Fix OCR letter → digit mistakes
        t = t.replace('O', '0').replace('S', '$')

        # Remove spaces inside numbers
        t = re.sub(r'(\d)\s+(\d)', r'\1\2', t)

        # Convert comma decimal to dot
        t = re.sub(r'(\d+),(\d{2})', r'\1.\2', t)

        # Remove thousand separators
        t = re.sub(r'(\d)[,\.](\d{3})', r'\1\2', t)

        return t


    def parse_document(self, pdf_path: str) -> OrderDocument:
        """Parse a PDF document"""
        lines = self.extract_pdf_text(pdf_path)
        lines = [self.normalize_price_text(line) for line in lines]

        if self.needs_ocr(lines) or not self.contains_prices(lines):
            print("OCR required: missing prices or product codes...")
            lines = self.ocr_pdf(pdf_path)
            print(f"DEBUG OCR lines:")
            for i, l in enumerate(lines):
                print(f"  [{i}]: {l}")
            lines = self.ocr_pdf(pdf_path)
            lines = [self.normalize_ocr_line(l) for l in lines]
 
        text = "\n".join(lines)

        order_number = self.extract_order_number(text)
        line_items = self.extract_line_items(text)
        total = self.extract_total(text)
    
        return OrderDocument(
        order_number=order_number,
        line_items=line_items,
        total=total
    )

    
    def normalize_code(self, code: str) -> str:
        """Normalize product code"""
        code = code.upper()
        code = re.sub(r'\(.*?\)', '', code)  # Remove parentheses
        code = re.sub(r'\s+', '', code)  # Remove spaces
        code = re.sub(r'^CL-', '', code)  # Remove CL- at the start

        code = re.sub(r'([A-Z]{2}\d{2}\.\d{4,})([A-Z]+)$', r'\1', code)
        
        return code.strip()
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def base_code(self, code: str) -> str:
        """Get base product code (first part before space)"""
        return code.split()[0] if code else code
    
    def aggregate(self, items):
        agg = defaultdict(lambda: {"total": 0.0, "unit_price": 0.0, "label": "", "specs": None})
        for i in items:
            key = self.base_code(i.product_code)
            if i.total > 0:
                agg[key]["total"] += i.total
            if i.unit_price > 0 and agg[key]["unit_price"] == 0.0:
                agg[key]["unit_price"] = i.unit_price
            if not agg[key]["label"]:  # Keep first label seen
                agg[key]["label"] = i.product_code
                agg[key]["specs"] = getattr(i, 'specs', None)  # Store specs from first item
        return agg


    def match_documents(self, doc1: OrderDocument, doc2: OrderDocument) -> Dict:
        log = []

        agg1 = self.aggregate(doc1.line_items)
        agg2 = self.aggregate(doc2.line_items)
        is_confirmation = not any(item.unit_price > 0 for item in doc2.line_items)

        # ── SUMMARY ───────────────────────────────────────────────────────
        log.append("=" * 60)
        log.append("SUMMARY")
        log.append("=" * 60)

        col_width = 38
        log.append(f"{'Doc1 — ' + str(len(agg1)) + ' items':<{col_width}}  {'Doc2 — ' + str(len(agg2)) + ' items'}")
        log.append("-" * 60)

        keys1 = list(agg1.items())
        keys2 = list(agg2.items())
        for i in range(max(len(keys1), len(keys2))):
            left  = f"  {keys1[i][1]['label']}: ${keys1[i][1]['total']:.2f}" if i < len(keys1) else ""
            right = f"  {keys2[i][1]['label']}: ${keys2[i][1]['total']:.2f}" if i < len(keys2) else ""
            log.append(f"{left:<{col_width}}  {right}")

        # ── MATCHING PROCESS ──────────────────────────────────────────────
        log.append("")
        log.append("=" * 60)
        log.append("MATCHING PROCESS")
        log.append("=" * 60)

        matched            = 0
        price_check_result = {}

        for key1, data1 in agg1.items():
            total1          = data1["total"]
            label1          = data1["label"]
            best_match      = None
            best_match_data = {}
            best_diff       = float("inf")
            best_sim        = 0

            for key2, data2 in agg2.items():
                total2 = data2["total"]
                label2 = data2["label"]

                sim = 1.0 if key1 == key2 else self.calculate_similarity(
                    self.normalize_code(label1), self.normalize_code(label2))

                specs1 = data1.get("specs")
                specs2 = data2.get("specs")
                if specs1 and specs2:
                    if specs1.get('size') == specs2.get('size'):
                        sim += 0.1
                    if specs1.get('head') == specs2.get('head'):
                        sim += 0.1

                diff = abs(total1 - total2)

                if total1 == 0 or total2 == 0:
                    if sim > best_sim:
                        best_match      = label2
                        best_match_data = data2
                        best_diff       = 0
                        best_sim        = sim
                else:
                    if sim > 0.60 and diff < best_diff:
                        best_match      = label2
                        best_match_data = data2
                        best_diff       = diff
                        best_sim        = sim

            threshold    = 0 if (total1 == 0 or (best_match and best_match_data.get("total", 0) == 0)) \
                        else max(5.0, total1 * 0.10)
            matched_this = best_match and (best_diff <= threshold or threshold == 0)

            facture_unit_price = best_match_data.get("unit_price", 0) if best_match else 0

            # Price check only for factures
            if not is_confirmation and best_match:
                if key1 in self.viscan_prices and facture_unit_price > 0:
                    expected_price = self.viscan_prices[key1]
                    price_match    = abs(expected_price - facture_unit_price) < 0.01
                    if not price_match:
                        matched_this = False
                    price_check_result = {
                        "code": key1, "list_price": expected_price,
                        "facture_price": facture_unit_price, "match": price_match
                    }
                elif key1 in self.viscan_prices and facture_unit_price == 0:
                    price_check_result = {
                        "code": key1, "list_price": self.viscan_prices[key1],
                        "facture_price": 0.0, "match": None
                    }
                elif facture_unit_price > 0:
                    price_check_result = {
                        "code": key1, "list_price": 0.0,
                        "facture_price": facture_unit_price, "match": False
                    }

            log.append("")
            result_str = "✅ MATCH" if matched_this else "❌ NO MATCH"
            sim_str    = f"(Similarity: {best_sim:.0%})"

            if best_match:
                log.append(f"  {label1:<20}  →  {best_match:<20}  {sim_str:<20}  {result_str}")
                log.append(f"  $ Price:  PO ${total1:<10.2f}  |  Facture ${total1 - best_diff:<10.2f}  |  Diff: ${best_diff:.2f}")

                if data1.get("specs") and best_match_data.get("specs"):
                    s1, s2 = data1["specs"], best_match_data["specs"]
                    if s1.get('size') == s2.get('size'):
                        log.append(f"  ✅ Size: {s1.get('size')}")
                    if s1.get('head') == s2.get('head'):
                        log.append(f"  ✅ Head: {s1.get('head')}")

                if not is_confirmation:
                    if key1 in self.viscan_prices and facture_unit_price > 0:
                        expected_price = self.viscan_prices[key1]
                        price_match    = abs(expected_price - facture_unit_price) < 0.01
                        log.append(f"  💲 List: ${expected_price:.4f}  |  Facture: ${facture_unit_price:.4f}  →  {'✅ MATCH' if price_match else '❌ MISMATCH'}")
                    elif facture_unit_price > 0:
                        log.append(f"  💲 Facture: ${facture_unit_price:.4f}  —  not in price list")
            else:
                log.append(f"  {label1:<20}  →  no match found")

            if matched_this:
                matched += 1

        # ── FINAL RESULT ──────────────────────────────────────────────────
        total_items      = len(agg2)
        match_percentage = (matched / total_items * 100) if total_items > 0 else 0
        documents_match  = match_percentage >= 70

        log.append("")
        log.append("=" * 60)
        log.append("FINAL RESULT")
        log.append("=" * 60)
        log.append(f"  {matched}/{total_items} items matched ({match_percentage:.1f}%)")
        log.append(f"  Documents match: {'✅ YES' if documents_match else '❌ NO'}")
        log.append("=" * 60)

        # ── PRICE VERIFICATION ────────────────────────────────────────────
        if not is_confirmation:
            log.append("")
            log.append("=" * 60)
            log.append("PRICE VERIFICATION")
            log.append("=" * 60)

            for key1, data1 in agg1.items():
                facture_unit_price = 0
                for key2, data2 in agg2.items():
                    if key1 == key2 or self.calculate_similarity(
                            self.normalize_code(data1['label']),
                            self.normalize_code(data2['label'])) > 0.60:
                        facture_unit_price = data2.get("unit_price", 0)
                        break

                log.append("")
                if key1 in self.viscan_prices and facture_unit_price > 0:
                    expected = self.viscan_prices[key1]
                    diff     = abs(facture_unit_price - expected)
                    status   = "✅ PASS" if diff < 0.01 else "❌ FAIL"
                    log.append(f"  {data1['label']:<20}  List: ${expected:<10.4f}  Facture: ${facture_unit_price:<10.4f}  Diff: ${diff:.4f}  {status}")
                elif facture_unit_price == 0:
                    log.append(f"  {data1['label']:<20}  ⚠️  No facture price found")
                else:
                    log.append(f"  {data1['label']:<20}  ❌  Not in price list  (Facture: ${facture_unit_price:.4f})")

        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        return {
            "match": documents_match,
            "confidence": match_percentage,
            "matched_items": matched,
            "total_items": total_items,
            "order1": doc1.order_number,
            "order2": doc1.order_number,
            "total1": doc1.total,
            "total2": doc2.total,
            "total_diff": abs(doc1.total - doc2.total),
            "price_check": price_check_result,
            "is_confirmation": is_confirmation,
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

        card = tk.Frame(self.result_frame, bg="white", bd=1, relief=tk.SOLID)
        card.pack(fill=tk.BOTH, expand=True)
        tk.Frame(card, bg=accent, height=5).pack(fill=tk.X)

        inner = tk.Frame(card, bg="white", padx=24, pady=18)
        inner.pack(fill=tk.BOTH, expand=True)

        top_row = tk.Frame(inner, bg="white")
        top_row.pack(fill=tk.X)

        icon = "✅" if is_match else "❌"
        verdict = "DOCUMENTS MATCH" if is_match else "DOCUMENTS DO NOT MATCH"

        tk.Label(top_row, text=icon, font=("Arial", 28), bg="white").pack(side=tk.LEFT)
        tk.Label(top_row, text=verdict, font=("Arial", 16, "bold"),
                bg="white", fg=accent).pack(side=tk.LEFT, padx=12)
        tk.Label(top_row, text=f"{result['confidence']:.0f}% confidence",
                font=("Arial", 11), bg="white", fg="#666").pack(side=tk.RIGHT)

        tk.Frame(inner, bg="#e0e0e0", height=1).pack(fill=tk.X, pady=(14, 14))

        stats = tk.Frame(inner, bg="white")
        stats.pack(fill=tk.X, pady=(0, 14))

        def stat_box(parent, label, value, col, font_size=14):
            box = tk.Frame(parent, bg="#f8f8f8", padx=14, pady=10, bd=1, relief=tk.SOLID)
            box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0 if col == 0 else 4, 0))
            tk.Label(box, text=value, font=("Arial", font_size, "bold"),
                    bg="#f8f8f8", fg="#222").pack()
            tk.Label(box, text=label, font=("Arial", 8),
                    bg="#f8f8f8", fg="#888").pack()

        pc = result.get('price_check', {})
        list_p = pc.get('list_price', 0)
        fact_p = pc.get('facture_price', 0)
        price_icon = "✅" if pc.get('match') else "❌"
        order_icon = "✅" if result['order1'] == result['order2'] else "❌"
        price_val = f"{price_icon} ${list_p: .2f} / ${fact_p:.2f}"

        stat_box(stats, "Order Numbers", f"{order_icon}  {result['order1']} / {result['order2']}", 0)
        stat_box(stats, "Items Matched", f"{result['matched_items']} / {result['total_items']}", 1)
        stat_box(stats, "Confidence", f"{result['confidence']:.1f}%", 2)
        stat_box(stats, "List → Facture", price_val, 3, font_size=9)

        tk.Button(inner, text="📋  View Detailed Log", font=("Arial", 10, "bold"),
                bg=self.primary_color, fg="white", cursor="hand2",
                command=self.show_log_window, relief=tk.FLAT,
                padx=18, pady=9).pack(fill=tk.X)
    
    
    def display_error(self, error_msg):
        """Display error message"""
        self.progress.stop()
        self.progress.pack_forget()
        self.compare_btn.config(state=tk.NORMAL)
        
        messagebox.showerror(
            "Error",
            f"Failed to process documents:\n\n{error_msg}"
        )


def main():
    root = tk.Tk()
    app = DocumentMatcherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
    