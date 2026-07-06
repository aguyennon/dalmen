"""
AI Document Matcher - Novatech Slab + Glazing Version
Upload any 2 PDFs and check if they match
NOVATECH - SLAB AND GLAZING 
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
import pandas as pd

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
    annexe_pr: str
    description: str
    quantity: int = 1
    unit_price: float = 0.0

@dataclass
class OrderDocument:
    order_number: str
    line_items: List[LineItem]
    provider: str = "NOVATECH_WINDOWS"


class DocumentMatcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Glazing/Slab Matcher")
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
            text="Glazing/Slab Matcher",
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
            text="Match Dalmen window orders with Novatech confirmations",
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
        tk.Label(inner1, text="Dalmen Window Order",
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
        tk.Label(inner2, text="Novatech Confirmation / Receipt",
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
            print("Starting window order comparison...")
            print(f"File 1: {self.file1_path}")
            print(f"File 2: {self.file2_path}")

            doc1 = self.parse_document(self.file1_path)
            print(f"Doc1 parsed: {len(doc1.line_items)} items found")

            doc2 = self.parse_document(self.file2_path)
            print(f"Doc2 parsed: {len(doc2.line_items)} items found")

            result = self.match_documents(doc1, doc2)
            print(f"Match result: {result}")

            self.root.after(0, self.display_result, result)
            print("Done!")

        except Exception as e:
            import traceback
            print("ERROR OCCURRED:")
            print(traceback.format_exc())
            error_details = traceback.format_exc()
            self.root.after(0, self.display_error, f"{str(e)}\n\nDetails:\n{error_details}")

    def extract_pdf_text(self, pdf_path: str) -> str:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if len(text.strip()) < 100:
            print("DEBUG: PDF appears image-based, running OCR fallback...")
            text = self._ocr_pdf(pdf_path)

        return text

    def _ocr_pdf(self, pdf_path: str) -> str:
        from pdf2image import convert_from_path
        poppler_path = r"C:\poppler\Library\bin"
        text = ""
        images = convert_from_path(pdf_path, dpi=400, poppler_path=poppler_path)
        for i, img in enumerate(images):
            print(f"DEBUG: OCR page {i+1}/{len(images)}...")
            text += pytesseract.image_to_string(img, config='--psm 1') + "\n"
        return text
    
    def extract_order_number(self, text: str, doc_type: str) -> str:
        if doc_type == "DALMEN":
            match = re.search(r'Num[ée]ro\s+de\s+PO\.:?\s*(V-\d+)', text, re.IGNORECASE)
            if match:
                return match.group(1)
        else:  # NOVATECH
            match = re.search(r'Votre no\.\s+de commande\s+(V-\d+)', text)
            if match:
                return match.group(1)

            match = re.search(r'(V-\d+)', text)
            if match:
                return match.group(1)
        
        return "Unknown"
    
    def parse_glaze_dalmen_order(self, text: str, target_po: str) -> List[LineItem]:
        items = []
        lines = [l.strip() for l in text.split('\n')]

        print(f"\nDEBUG: Parsing Dalmen order...")

        is_decorative_lites = "Decorative lites order" in text or "Item number :" in text
        print(f"DEBUG: Format detected: {'Decorative lites (English)' if is_decorative_lites else 'Standard French'}")

        for i, line in enumerate(lines):

            if is_decorative_lites:
                match = re.match(r'^(\d{2}-\d{3}-\d{3}-\w+)\s+(\d+)\s+([\d][\d\-]+-\d+)$', line)
                if not match:
                    continue

                product_code = match.group(1)
                quantity = int(match.group(2))
                annexe_pr = match.group(3)
                description = lines[i - 1] if i > 0 else ""

                print(f"  Found: {product_code} | Annexe: {annexe_pr} | Qty: {quantity} | DESC: {description[:50]}")

                items.append(LineItem(
                    product_code=product_code,
                    annexe_pr=annexe_pr,
                    description=description,
                    quantity=quantity
                ))

            else:
                match1 = re.match(r'^([\d\-]+)\s+(\d+)\s+([\d\-]+)\s+(.+)$', line)
                if match1:
                    product_code = match1.group(1).strip()
                    quantity = int(match1.group(2))
                    annexe_pr = match1.group(3).strip()
                    description = match1.group(4).strip()
                    desc_clean   = re.sub(r'^[\d\-]+\s*-\s*', '', description)

                    print(f" Found item: {product_code} | Annexe: {annexe_pr} | DESC: {desc_clean[:50]}")

                    items.append(LineItem(
                        product_code=product_code,
                        annexe_pr=annexe_pr,
                        description=desc_clean,
                        quantity=quantity
                    ))
                    continue

                # Other page format
                match2 = re.match(r'^([\d\-]+)\s+(\d+)\s+([\d\-]+)\s+(.+)$', line)
                if match2:
                    product_code = match2.group(1).strip()
                    quantity = int(match2.group(2))
                    annexe_pr = match2.group(3).strip()
                    description = match2.group(4).strip()
                    desc_clean = re.sub(r'^[\d\-]+\s*-\s*', '', description)

                    print(f" Found item: {product_code} | Annexe: {annexe_pr} | DESC: {desc_clean[:50]}")

                    items.append(LineItem(
                        product_code=product_code,
                        annexe_pr=annexe_pr,
                        description=desc_clean,
                        quantity=quantity
                    ))
                    continue

                match3 = re.match(r'^([\d\-]+)\s+(\d+)\s+([\d\-]+)$', line)
                if match3:
                    product_code = match3.group(1).strip()
                    quantity = int(match3.group(2))
                    annexe_pr = match3.group(3).strip()

                    description = ""
                    if i > 0:
                        prev_line = lines[i-1].strip()
                        if prev_line.startswith(product_code):
                            description = re.sub(r'^[\d\-]+\s*-\s*', '', prev_line)

                    if not description:
                        description = f"{product_code} (no description found)"

                    print(f" Found item: {product_code} | Annexe: {annexe_pr} | DESC: {description[:50]}")

                    items.append(LineItem(
                        product_code=product_code,
                        annexe_pr=annexe_pr,
                        description=description,
                        quantity=quantity
                    ))

        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items

    def parse_glaze_novatech_facture(self, text: str, target_po: str) -> List[LineItem]:
        items = []
        lines = text.split('\n')

        print(f"\nDEBUG: Parsing Novatech facture...")

        for i, line in enumerate(lines):
            line = line.strip()

            match = re.match(r'^\d+\s+(\d{2}-\d{3}-\d{3}-\d{3})\s+(.+)', line)
            if match:
                product_code = match.group(1).strip()
                description = match.group(2).strip()

                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if not re.match(r'^\d+\s+\d{2}-\d{3}', next_line) and not next_line.startswith('Tag Client'):
                        description += " " + next_line

                annexe_pr = ""
                for j in range(i, min(i+5, len(lines))):
                    tag_match = re.search(r'Tag Client:\s*([\d\-]+)', lines[j])
                    if tag_match:
                        annexe_pr = tag_match.group(1).strip()
                        break

                print(f"  Found: {product_code} | Annexe: {annexe_pr} | DESC: {description[:50]}")

                unit_price = 0.0
                price_match = re.search(r'CH\s+(\d+\.\d{2})', description)
                if price_match:
                    unit_price = float(price_match.group(1))
                    print(f" Unit Price: ${unit_price:.2f}")

                items.append(LineItem(
                    product_code=product_code,
                    annexe_pr=annexe_pr,
                    description=description,
                    quantity=1,
                    unit_price=unit_price
                ))

        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items

    def parse_slab_novatech_facture(self, text: str, target_po: str) -> List[LineItem]:
        items = []
        lines = text.split('\n')

        print(f"DEBUG: Parsing through Novatech Slab Facture...")

        in_table = False

        for i, line in enumerate(lines):
            line = line.strip()

            if 'Produit' in line and 'Description' in line:
                in_table = True
                continue

            if 'Facture Sous-Total' in line or 'Facture TOTAL' in line or 'Expédié à:' in line:
                print(f" DEBUG: Reached end of items at line {i}")
                break

            if not in_table:
                continue

            match = re.match(r'^\d+\s+(\d{2}-\d{3}-\d{3}-\d{3}(?:-\d{3})?)\s+(.+?)\s+\d+\s+\d+\s+CH\s+(\d+\.\d{2})\s+\d+\.\d{2}$', line)
            if match:
                product_code = match.group(1).strip()
                description = match.group(2).strip()
                unit_price = float(match.group(3))

                annexe_pr = ""
                for k in range(i+1, min(i+10, len(lines))):
                    tag_match = re.search(r'Tag Client:\s*([\d\-]+)', lines[k])
                    if tag_match:
                        annexe_pr = tag_match.group(1).strip()
                        break

                print(f" Found: {product_code} | Annexe: {annexe_pr} | Price: ${unit_price:.2f} | DESC: {description[:50]}")

                items.append(LineItem(
                    product_code=product_code,
                    annexe_pr=annexe_pr,
                    description=description,
                    quantity=1,
                    unit_price=unit_price
                ))

        print(f"DEBUG: Total SLAB facture items extracted: {len(items)}\n")
        return items

    def parse_glaze_novatech_confirmation(self, text: str, target_po: str) -> List[LineItem]:
        """Parse Novatech confirmation (handles multi-page)"""
        items = []
        lines = [l.strip() for l in text.split('\n')]

        print("DEBUG: Full OCR line dump:")
        for idx, l in enumerate(lines):
            if l:
                print(f"[{idx}] {l}")
        
        print(f"\nDEBUG: Parsing Novatech confirmation...")

        is_ocr_format = any(re.search(r'Annexe PR:', l) for l in lines)
        print(f"DEBUG: Confirmation format: {'OCR/Scanned' if is_ocr_format else 'Text-based'}")

        if is_ocr_format:
            for i, line in enumerate(lines):
                annexe_match = re.search(r'Annexe PR:\s*([\d\-]+)', line)
                if not annexe_match:
                    continue

                annexe_pr = annexe_match.group(1).strip()

                product_code = ""

                for j in range(i - 1, max(i - 6, -1), -1):
                    code_match = re.match(r'^(\d{2}-\d{3}-\d{3}-\d{3})$', lines[j])
                    if code_match:
                        product_code = code_match.group(1)
                        break

                if not product_code:
                    for j in range(i + 1, min(i + 4, len(lines))):
                        code_match = re.search(r'(\d{2}-\d{3}-\d{3}-\d{3})', lines[j])
                        if code_match:
                            product_code = code_match.group(1)
                            break

                    else:
                        for j in range(i + 1, min(i + 4, len(lines))):
                            code_match = re.search(r'(\d{2}-\d{3}-\d{3}-\d{3})', lines[j])
                            if code_match:
                                product_code = code_match.group(1)
                                break   
                
                print(f"  Found: {product_code} | Annexe: {annexe_pr}")

                items.append(LineItem(
                    product_code=product_code,
                    annexe_pr=annexe_pr,
                    description="",
                    quantity=1
                ))
        
        else:
            in_order_section = False

            for i, line in enumerate(lines):
                if target_po in line:
                    in_order_section = True
                    print(f" Found target PO {target_po} at line {i}")
                    continue

                if in_order_section:
                    if re.match(r'^V-\d+', line) and target_po not in line:
                        print(f" Reached next order at line {i}, stopping")
                        break
                    if "Tag Client" in line or "Sous-Total" in line or 'TOTAL' in line:
                        print(f" Reached end of items at line {i}")
                        break

                if not in_order_section:
                    continue

                line = line.strip()

                match = re.search(r'V-\d+\s+[\d\.]+\s+\d+\s+([\d\-]+)\s+(.+?)(?:\d{4}-\d{2}-\d{2}|$)', line)
                if match:
                    product_code = match.group(1).strip()
                    description = match.group(2).strip()

                    annexe_pr = ""
                    for j in range(i+1, min(i+6, len(lines))):
                        annexe_match = re.search(r'Annexe PR:\s*([\d\-]+)', lines[j])
                        if annexe_match:
                            annexe_pr = annexe_match.group(1)
                            break

                    print(f" Found item: {product_code} | Annexe: {annexe_pr} | DESC: {description[:50]}")

                    items.append(LineItem(
                        product_code=product_code,
                        annexe_pr=annexe_pr,
                        description=description,
                        quantity=1
                    ))

        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items
    
    def parse_slab_dalmen_order(self, text: str, target_po: str) -> List[LineItem]:
        items = []
        lines = text.split('\n')

        print(f"\nDEBUG: Parsing Dalmen SLAB order...")

        for line in lines:
            line = line.strip()

            match = re.match(r'^(\d{2}-\d{3}-\d{3}-\w+)\s+(\d+)\s+([\d\-]+)\s+(.+)$', line)

            if match: 
                product_code = match.group(1).strip()
                quantity = int(match.group(2))
                annexe_pr = match.group(3).strip()
                description = match.group(4).strip()

                print(f" Found item: {product_code} | Annexe: {annexe_pr} | DESC: {description[:50]}")

                items.append(LineItem(
                    product_code=product_code,
                    annexe_pr=annexe_pr,
                    description=description,
                    quantity=quantity
                ))

        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items

    def parse_slab_novatech_confirmation(self, text: str, target_po: str) -> List[LineItem]:
        items = []
        lines = [l.strip() for l in text.split('\n')]

        print(f"\nDEBUG: Parsing Novatech SLAB confirmation... (Filtering for PO: {target_po})")

        is_ocr_format = any(re.search(r'Annexe PR:', l) for l in lines)
        print(f"DEBUG: Confirmation format: {'OCR/Scanned' if is_ocr_format else 'Text-based'}")

        if is_ocr_format:
            for i, line in enumerate(lines):
                annexe_match = re.search(r'Annexe PR:\s*([\d\-]+)', line)
                if not annexe_match:
                    continue

                annexe_pr = annexe_match.group(1).split()
                product_code = ""
                
                for j in range(i - 1, max(i - 6, -1), -1):
                    code_match = re.search(r'(\d{2}-\d{3}-\d{3}-\d{3})', lines[j])
                    if code_match:
                        product_code = code_match.group(1)
                        break
                else:
                    for j in range(i + 1, min(i + 4, len(lines))):
                        code_match = re.search(r'(\d{2}-\d{3}-\d{3}-\d{3})', lines[j])
                        if code_match:
                            product_code = code_match.group(1)
                            break

                if not product_code:
                    print(f"  WARNING: annexe {annexe_pr} found but no product code nearby")
                    continue

                print(f"  Found: {product_code} | Annexe: {annexe_pr}")

                items.append(LineItem(
                    product_code=product_code,
                    annexe_pr=annexe_pr,
                    description="",
                    quantity=1
                ))

        else:
            in_order_section = False

            for i, line in enumerate(lines):
                if target_po in line:
                    in_order_section = True
                    print(f" Found target PO {target_po} at line {i}")
                    continue

                if in_order_section:
                    if re.match(r'^V-\d+', line) and target_po not in line:
                        print(f" Reached next order at line {i}, stopping")
                        break
                    if 'Tag Client' in line or 'Sous-Total' in line or 'TOTAL' in line:
                        print(f" Reached end of items at line {i}")
                        break

                if not in_order_section:
                    continue

                line = line.strip()

                match = re.search(r'V-\d+\s+[\d\.]+\s+\d+\s+([\d\-]+)\s+(.+?)(?:\d{4}-\d{2}-\d{2}|$)', line)
                if match:
                    product_code = match.group(1).strip()
                    description = match.group(2).strip()

                    annexe_pr = ""
                    for j in range(i+1, min(i+11, len(lines))):
                        annexe_match = re.search(r'Annexe PR:\s*([\d\-]+)', lines[j])
                        if annexe_match:
                            annexe_pr = annexe_match.group(1)
                            break
                    
                    print(f" Found: {product_code} | Annexe: {annexe_pr} | DESC: {description[:50]}")

                    items.append(LineItem(
                        product_code=product_code,
                        annexe_pr=annexe_pr,
                        description=description,
                        quantity=1
                    ))

            print(f"DEBUG: Total items extracted: {len(items)}\n")
            return items

    def find_price_in_catalog(self, product_code: str, pdf_path: str) -> float:
        try:
            print(f" Searching catalog (this may take a bit)...")

            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)

                for page_num, page in enumerate(pdf.pages, 1):
                    if page_num % 20 == 0:
                        print(f" Scanning page {page_num}/{total_pages}...")

                    img = page.to_image(resolution=300)
                    pil_img = img.original

                    text = pytesseract.image_to_string(pil_img)

                    if product_code in text:
                        print(f" Found {product_code} on page")

                        lines = text.split('\n')
                        for line in lines:
                            if product_code in line:
                                print(f" Line: {line[:100]}")

                                pattern = rf'{re.escape(product_code)}\s+(\d+\.\d{{2}})\s+\d+'
                                price_match = re.search(pattern, line)

                                if price_match:
                                    price = float(price_match.group(1))
                                    print(f" Extracted price: ${price:.2f}")
                                    return price

                                print(f" Trying fallback extraction...")
                                all_numbers = re.findall(r'(\d+\.\d{2})', line)
                                prices = [float(n) for n in all_numbers if float(n) > 10.0]

                                if prices:
                                    price = prices[0]
                                    print(f" Extracted price (fallback): ${price:.2f}")
                                    return price
                                else:
                                    print(f" No valid prices found (numbers: {all_numbers})")
           

                                all_prices = re.findall(fr'(\d+\.\d{2})', line)
                                if all_prices:
                                    for p in reversed(all_prices):
                                        if float(p) > 10:
                                            price = float(p)
                                            print(f" Extracted price (fallback): ${price:.2f}")
                                            return price
                                    
                       
            print(f" {product_code} not found after scanning {total_pages} pages")
            return None
            
        except Exception as e:
            print(f" Error searching for {product_code}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def verify_prices(self, doc2_items: List[LineItem]) -> None:
        pdf_path = r"\\10.0.7.2\Group\Taxi\2026 PRICE LIST\NOVATECH GLAZING 2026.pdf"

        print(f"\n{'='*60}")
        print("PRICE VERIFICATION (GLAZING)")
        print(f"{'='*60}")

        for item in doc2_items:
            code = item.product_code
            facture_price = item.unit_price

            print(f"\nSearching catalog for {code}...")
            catalog_price = self.find_price_in_catalog(code, pdf_path)

            if catalog_price:
                markup = ((facture_price - catalog_price) / catalog_price) * 100
                print(f" Catalog: ${catalog_price:.2f}")
                print(f" Facture: ${facture_price:.2f}")
                print(f" Markup: {markup:.2f}%")

                if abs(markup - 27.87) > 2.0:
                    print(f" Markup OUTSIDE expected range (25.87% - 29.87%)")
                else:
                    print(f" Markup OK")
            else:
                print(f" Not found in catalog")

    def load_novatech_price_catalog(self) -> Dict[str, float]:
        try:
            excel_path = r"\\10.0.7.2\Group\Taxi\2026 PRICE LIST\NOVATECH GLAZING PRICE LIST 2026 EXCEL VERSION.xlsx"

            print(f"DEBUG: Loading Novatech price catalog from Excel...")

            df = pd.read_excel(excel_path,sheet_name="Novatech_Prix_2026_Part1_Pages1")

            if 'Code' in df.columns:
                code_col = 'Code'
            elif 'code' in df.columns:
                code_col = 'code'
            else:
                code_col = df.columns[6]

            if 'Prix' in df.columns:
                price_col = 'Prix'
            elif 'prix' in df.columns:
                price_col = 'prix'
            else:
                price_col = df.columns[7]

            print(f"DEBUG: Using columns - Code: {code_col}, Prix: {price_col}")
            

            catalog = {}
            for idx, row in df.iterrows():
                code = str(row[code_col]).strip()
                price = row[price_col]

                if pd.notna(code) and pd.notna(price) and '-' in code:
                    try:
                        catalog[code] = float(price)
                    except:
                        continue

            print(f"DEBUG: Loaded {len(catalog)} codes from catalog")
            print(f"DEBUG: Sample codes: {list(catalog.keys())[:5]}")
            return catalog

        except Exception as e:
            print(f"WARNING: Could not load Novatech price catalog: {e}")
            return {}

    def load_novatech_slab_price_catalog(self) -> Dict[str, Dict]:
        try:
            excel_path = r"\\10.0.7.2\Group\Taxi\2026 PRICE LIST\Novatech_Prix_2026_SLAB.xlsx"

            print(f"DEBUG: Loading Novatech SLAB price catalog from Excel...")


            xl_file = pd.ExcelFile(excel_path)
            available_sheets = xl_file.sheet_names
            print(f"DEBUG: Available sheets: {available_sheets}")

            sheets = [s for s in available_sheets if s.startswith('N')]
            print(f"DEBUG: Loading sheets: {sheets}")

            catalog = {}

            for sheet_name in sheets:
                try:
                    df = pd.read_excel(excel_path, sheet_name=sheet_name)

                    price_col = df.columns[5]
                    code_col = df.columns[6]

                    sheet_count = 0
                    for idx, row in df.iterrows():
                        code = str(row[code_col]).strip()
                        price = row[price_col]

                        if pd.notna(code) and pd.notna(price) and '-' in code:
                            try:
                                parts = code.split('-')
                                if len(parts) >= 3:
                                    base_code = '-'.join(parts[:3])

                                    catalog[base_code] = {
                                    'price': float(price),
                                    'section': sheet_name,
                                    'full_code': code
                                }
                                sheet_count += 1
                            except:
                                continue

                    print(f"DEBUG: Total SLAB codes loaded {len(catalog)}")
                    print(f"DEBUG: Sample codes: {list(catalog.keys())[:5]}")

                    # DEBUG: Search for the specific code
                    print(f"\nDEBUG: Searching for codes starting with '75-076'...")
                    matching_codes = [k for k in catalog.keys() if k.startswith('75-076')]
                    print(f"DEBUG: Found {len(matching_codes)} codes starting with 75-076")
                    if matching_codes:
                        print(f"DEBUG: Matches: {matching_codes[:10]}")
                        # Show which section they're in
                        for code in matching_codes[:5]:
                            print(f"  {code} → Section: {catalog[code]['section']}, Full: {catalog[code]['full_code']}, Price: {catalog[code]['price']}")

                            print(f" {sheet_name}: Loaded {sheet_count} codes")

                except Exception as e:
                    print(f" WARNING: Could not load sheet {sheet_name}: {e}")
                    continue

            print(f"DEBUG: Total SLAB codes loaded {len(catalog)}")
            print(f"DEBUG: Sample codes: {list(catalog.keys())[:5]}")
            return catalog
        
        except Exception as e:
            print(f" WARNING: Could not load Novatech SLAB price catalog: {e}")
            import traceback
            traceback.print_exc()
            return {}


    def parse_document(self, pdf_path: str, doc_type: str = None) -> OrderDocument:
   
        text = self.extract_pdf_text(pdf_path)

        print(f"\nDEBUG: Text preview (first 500 chars):\n{text[:500]}\n")

        if not doc_type:
            if ("Commande de vitraux" in text or "Fournisseur :" in text
                    or "Decorative lites order" in text
                    or "Supplier : NOVATECH" in text):
                doc_type = "DALMEN"
            elif "GROUPE NOVATECH" in text or "Novatech" in text:
                doc_type = "NOVATECH"
            else:
                doc_type = "UNKNOWN"

        print(f"DEBUG: Detected document type: {doc_type}")

        is_slab = False
        if "Coupe-FEU" in text or "COUPE FEU" in text or "N600" in text or "N700" in text or "N900" in text or "VOG" in text:
            is_slab = True
            print("DEBUG: Document detected as SLAB")
        else:
            print("DEBUG: Document detected as GLAZING")

        order_number = self.extract_order_number(text, doc_type)
        print(f"DEBUG: Extracted order number: {order_number}")

        is_facture = False
        if doc_type == "NOVATECH":
            if "Facture" in text or "FACTURE" in text or "Numéro de facture" in text or "Votre no. de commande" in text:
                is_facture = True
                print("DEBUG: Document detected as NOVATECH FACTURE")
            else:
                print("DEBUG: Document detected as NOVATECH CONFIRMATION")
            print(f"DEBUG: is_facture = {is_facture}")

        if doc_type == "DALMEN":
            if is_slab:
                line_items = self.parse_slab_dalmen_order(text, order_number)
            else:
                line_items = self.parse_glaze_dalmen_order(text, order_number)
        elif doc_type == "NOVATECH":
            if is_facture:
                if is_slab:
                    line_items = self.parse_slab_novatech_facture(text, order_number)
                else:
                    line_items = self.parse_glaze_novatech_facture(text, order_number)
            else:
                if is_slab:
                    line_items = self.parse_slab_novatech_confirmation(text, order_number)
                else:
                    line_items = self.parse_glaze_novatech_confirmation(text, order_number)
        else:
            line_items = []

        doc = OrderDocument(
            order_number=order_number,
            line_items=line_items,
            provider="NOVATECH_WINDOWS"
        )
        doc.is_facture = is_facture
        return doc

    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def match_documents(self, doc1: OrderDocument, doc2: OrderDocument) -> Dict:
        if doc1.line_items is None:
            doc1.line_items = []
        if doc2.line_items is None:
            doc2.line_items = []

        print("DEBUG: Doc2 items check:")
        for item in doc2.line_items:
            print(f"  product_code='{item.product_code}' | annexe_pr='{item.annexe_pr}'")

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
            left  = f"  {doc1.line_items[i].product_code} | Annexe: {doc1.line_items[i].annexe_pr}" if i < len(doc1.line_items) else ""
            right = f"  {doc2.line_items[i].product_code} | Annexe: {doc2.line_items[i].annexe_pr}" if i < len(doc2.line_items) else ""
            log.append(f"{left:<{col_width}}  {right}")

        log.append("")
        po_str = "✅ MATCH" if order_match else "❌ NO MATCH"
        log.append(f"  Order Numbers — Doc1: {doc1.order_number}  |  Doc2: {doc2.order_number}  →  {po_str}")

        # ── FILTER BY COMMON ANNEXE BASES ─────────────────────────────────
        doc1_bases = set()
        for item in doc1.line_items:
            if item.annexe_pr and len(item.annexe_pr.split('-')) >= 2:
                doc1_bases.add('-'.join(item.annexe_pr.split('-')[:2]))

        doc2_bases = set()
        for item in doc2.line_items:
            if item.annexe_pr and len(item.annexe_pr.split('-')) >= 2:
                doc2_bases.add('-'.join(item.annexe_pr.split('-')[:2]))

        common_bases = doc1_bases & doc2_bases

        if not common_bases:
            log.append("")
            log.append("  ⚠️  No common Annexe PR bases found between both documents.")
        else:
            log.append(f"  Common Annexe bases: {common_bases}")

        doc1_filtered = [item for item in doc1.line_items
                        if item.annexe_pr and '-'.join(item.annexe_pr.split('-')[:2]) in common_bases]
        doc2_filtered = [item for item in doc2.line_items
                        if item.annexe_pr and '-'.join(item.annexe_pr.split('-')[:2]) in common_bases]

        log.append(f"  Filtered Doc1: {len(doc1.line_items)} → {len(doc1_filtered)} items")
        log.append(f"  Filtered Doc2: {len(doc2.line_items)} → {len(doc2_filtered)} items")

        doc1.line_items = doc1_filtered
        doc2.line_items = doc2_filtered

        # ── MATCHING PROCESS ──────────────────────────────────────────────
        log.append("")
        log.append("=" * 60)
        log.append("MATCHING PROCESS")
        log.append("=" * 60)

        matched     = 0
        total_items = max(len(doc1.line_items), len(doc2.line_items)) if doc1.line_items or doc2.line_items else 0

        is_slab_matching = any('N900' in item.description or 'N600' in item.description or
                            'Coupe-FEU' in item.description
                            for item in doc1.line_items + doc2.line_items)

        for item1 in doc1.line_items:
            best_score = 0
            best_match = None

            for item2 in doc2.line_items:
                score = 0
                if item1.annexe_pr and item2.annexe_pr and item1.annexe_pr == item2.annexe_pr:
                    score += 50
                code_sim = self.calculate_similarity(item1.product_code, item2.product_code)
                if code_sim > 0.8:
                    score += 30
                if not is_slab_matching:
                    desc_sim = self.calculate_similarity(item1.description, item2.description)
                    if desc_sim > 0.6:
                        score += 20
                if score > best_score:
                    best_score = score
                    best_match = item2

            log.append("")
            result_str = "✅ MATCH" if best_match and best_score >= 50 else "❌ NO MATCH"
            sim_str    = f"(Score: {best_score}/100)"

            if best_match:
                log.append(f"  {item1.product_code:<25}  →  {best_match.product_code:<25}  {sim_str:<16}  {result_str}")
                log.append(f"  Annexe: {item1.annexe_pr}  →  {best_match.annexe_pr}")
                if best_score >= 50:
                    matched += 1
            else:
                log.append(f"  {item1.product_code:<25}  →  no match found")

        match_percentage = (matched / total_items * 100) if total_items > 0 else 0
        documents_match  = match_percentage >= 70 and order_match

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
        is_glazing = not any('N900' in item.description or 'N900v2' in item.description or
                            'N600' in item.description or 'N700' in item.description or
                            'N300' in item.description or 'Coupe-FEU' in item.description
                            for item in doc1.line_items + doc2.line_items)
        is_slab = not is_glazing
        price_issues = []

        is_facture = getattr(doc2, 'is_facture', False)

        if is_glazing and is_facture:
            log.append("")
            log.append("=" * 60)
            log.append("PRICE VERIFICATION  (GLAZING)")
            log.append("=" * 60)

            catalog          = self.load_novatech_price_catalog()
            expected_markup  = 27.87
            tolerance        = 2.0

            for item in doc2.line_items:
                code          = item.product_code
                facture_price = item.unit_price
                log.append("")

                if facture_price == 0:
                    log.append(f"  {code:<30}  ⚠️  No price extracted")
                    continue

                catalog_price = catalog.get(code)
                if catalog_price:
                    actual_markup = ((catalog_price - facture_price) / facture_price) * 100
                    ok     = abs(actual_markup - expected_markup) <= tolerance
                    status = "✅ OK" if ok else "❌ OUTSIDE TOLERANCE"
                    log.append(f"  {code:<30}  Catalog: ${catalog_price:<8.2f}  Facture: ${facture_price:<8.2f}  Markup: {actual_markup:.1f}%  {status}")
                    if not ok:
                        price_issues.append(code)
                else:
                    log.append(f"  {code:<30}  ❌ Not found in catalog")
                    price_issues.append(code)

            log.append("")
            log.append(f"  {'✅ All prices verified!' if not price_issues else '⚠️  ' + str(len(price_issues)) + ' item(s) with pricing issues'}")

        if is_slab and is_facture:
            log.append("")
            log.append("=" * 60)
            log.append("PRICE VERIFICATION  (SLAB)")
            log.append("=" * 60)

            catalog = self.load_novatech_slab_price_catalog()
            section_markups = {
                'N300': {'discount': 0.478, 'tolerance': 2.0},
                'N600': {'discount': 0.535, 'tolerance': 2.0},
                'N700': {'discount': 0.535, 'tolerance': 2.0},
                'N900': {'discount': 0.598, 'tolerance': 2.0},
            }

            for item in doc2.line_items:
                code          = item.product_code
                facture_price = item.unit_price
                log.append("")

                if facture_price == 0:
                    log.append(f"  {code:<30}  ⚠️  No price extracted")
                    continue

                parts      = code.split('-')
                base_code  = '-'.join(parts[:3]) if len(parts) >= 3 else code
                entry      = catalog.get(base_code)

                if entry:
                    catalog_price = entry['price']
                    section       = entry['section']
                    info          = section_markups.get(section, section_markups['N900'])
                    expected      = catalog_price * info['discount']
                    diff          = abs(facture_price - expected)
                    ok            = diff <= info['tolerance']
                    status        = "✅ OK" if ok else "❌ OUTSIDE TOLERANCE"
                    log.append(f"  {code:<30}  [{section}]  Catalog: ${catalog_price:<8.2f}  Expected: ${expected:<8.2f}  Facture: ${facture_price:<8.2f}  Diff: ${diff:.2f}  {status}")
                    if not ok:
                        price_issues.append(code)
                else:
                    log.append(f"  {code:<30}  ❌ Not found in catalog")
                    price_issues.append(code)

            log.append("")
            log.append(f"  {'✅ All prices verified!' if not price_issues else '⚠️  ' + str(len(price_issues)) + ' item(s) with pricing issues'}")

        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        return {
            "match": documents_match,
            "confidence": match_percentage,
            "matched_items": matched,
            "total_items": total_items,
            "order1": doc1.order_number,
            "order2": doc2.order_number,
            "order_match": order_match,
            "price_check_ok": len(price_issues) == 0 if (is_glazing or is_slab) and is_facture else None,
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

        order_icon = "✅" if result.get('order_match') else "❌"
        stat_box(stats, "Order Numbers",  f"{order_icon}  {result['order1']} / {result['order2']}", 0)
        stat_box(stats, "Items Matched",  f"{result['matched_items']} / {result['total_items']}", 1)
        stat_box(stats, "Confidence",     f"{result['confidence']:.1f}%", 2)
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