"""
AI Document Matcher - GUI Version
Upload any 2 PDFs and check if they match
THERMOPLAST - 2-Way Matching for Thermoplastics

TO BE CONTINUED LATER
**CURRENT ISSUE**: OCR not picking up third item in 3077, showing too much for 3089
REMOVE DEBUG LINE 281
"""

# The only supplier on the hub, alongside DECKO, with custom logic for the Facture part

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import pdfplumber
import re
from typing import Dict, List
from dataclasses import dataclass
from difflib import SequenceMatcher
import threading
import os
from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@dataclass
class LineItem:
    item_code: str
    quantity: float = 0.0
    unit_price: float = 0.0
    unit: str = ""
    raw_code: str = ""


@dataclass
class OrderDocument:
    po_number: str
    line_items: List[LineItem]
    total: float = 0.0


class DocumentMatcherGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("THERMOPLAST Order Matcher")
        self.root.geometry("820x680")
        self.root.resizable(False, False)

        self.bg_color = "#f0f0f0"
        self.primary_color = "#1e3a8a"
        self.success_color = "#4caf50"
        self.error_color = "#f44336"

        self.root.configure(bg=self.bg_color)

        self.file1_path = None
        self.file2_path = None
        self.match_log = ""
        self.thermoplast_prices = {}
        self.load_thermoplast_price_list()

        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg=self.primary_color)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="THERMOPLAST Order Matcher",
            font=("Arial", 22, "bold"),
            bg=self.primary_color, fg="white"
        ).pack(side=tk.LEFT, padx=24, pady=16)

        self.log_btn = tk.Button(
            header,
            text="📋  View Log",
            font=("Arial", 10, "bold"),
            bg="#0c2454", fg="white",
            cursor="hand2",
            command=self.show_log_window,
            relief=tk.FLAT, padx=14, pady=8,
            state=tk.DISABLED
        )
        self.log_btn.pack(side=tk.RIGHT, padx=20, pady=14)

        tk.Label(
            header,
            text="Match Dalmen orders with Thermoplast confirmations",
            font=("Arial", 10),
            bg=self.primary_color, fg="#a8c0ff"
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
        tk.Label(inner1, text="Dalmen Order",
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
        tk.Label(inner2, text="Thermoplast Confirmation",
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

            text1 = self.extract_pdf_text(self.file1_path)
            doc1 = self.parse_dalmen_order(text1)
            print(f"Doc1 parsed: {len(doc1.line_items)} items")

            text2 = self.extract_pdf_text(self.file2_path)

            if 'THERMOPLAST' in text2.upper() and 'FACTURE' in text2.upper():
                facture_groups = self.parse_facture_by_custorder(text2)

                if doc1.po_number in facture_groups:
                    print(f"\n Found matching CUST-ORDER {doc1.po_number} in facture")
                    facture_items = facture_groups[doc1.po_number]
                    doc2 = OrderDocument(
                        po_number=doc1.po_number,
                        line_items=facture_items,
                        total=0.0
                    )
                    doc2.is_facture = True
                else:
                    print(f" CUST-ORDER {doc1.po_number} not found in facture")
                    print(f" Available CUST-ORDERs: {list(facture_groups.keys())}")
                    doc2 = OrderDocument(
                        po_number="Unknown",
                        line_items=[],
                        total=0.0
                    )
                    doc2.is_facture = False

            elif 'CONFIRMATION' in text2.upper() or 'ENTRY' in text2.upper():
                doc2 = self.parse_confirmation(text2)
            else:
                doc2 = self.parse_dalmen_order(text2)

            print(f"Doc2 parsed: {len(doc2.line_items)} items")

            result = self.match_documents(doc1, doc2)
            print(f"Match result: {result}")

            self.root.after(0, self.display_result, result)
            print("Done!")

        except Exception as e:
            import traceback
            print("ERROR:")
            print(traceback.format_exc())
            error_details = traceback.format_exc()
            self.root.after(0, self.display_error, f"{str(e)}\n\n{error_details}")


    def extract_pdf_text(self, pdf_path: str) -> str:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                if tables:
                    print(f"DEBUG: Found {len(tables)} tables on page")
                    for table in tables:
                        for row in table:
                            if row:
                                text += " | ".join([cell or "" for cell in row]) + "\n"
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        print(f"DEBUG: pdfplumber extracted {len(text)} chars")
        print(f"DEBUG: First 1000 chars:\n{text[:1000]}")

        if not text or len(text.strip()) < 50:
            print("DEBUG: pdfplumber returned empty - using OCR...")
            try:
                from pdf2image import convert_from_path
                import pytesseract

                images = convert_from_path(
                pdf_path,
                dpi=400,
                poppler_path=r"C:\poppler\Library\bin"
            )
                ocr_text = ""

                for page_num, img in enumerate(images, 1):
                    print(f" OCR scanning page {page_num}...")
                    page_text = pytesseract.image_to_string(img, config='--psm 6')
                    ocr_text += page_text + "\n"
                    print(f" Page {page_num}: {len(page_text)} chars")
                # Purely to test (need to delete once done with ths debug )
                print(f"DEBUG: OCR extracted {len(ocr_text)} characters")
                if 'Q4560' in ocr_text or 'q4560' in ocr_text.lower():
                    print("\nDEBUG: Found 'Q4560' in OCR text!")
                    for i, line in enumerate(ocr_text.split('\n')):
                        if 'Q4560' in line.upper():
                            print(f"  Line {i}: {line}")
                else:
                    print("\nDEBUG: 'Q4560' NOT FOUND in entire OCR text")
                    print("DEBUG: Searching for similar patterns (Q followed by 4 digits)...")
                    for i, line in enumerate(ocr_text.split('\n')):
                        if re.search(r'Q\d{4}', line, re.IGNORECASE):
                            print(f"  Line {i}: {line}")
                print(f"\nDEBUG: Full text around CUST-ORDER 3077:")
                lines = ocr_text.split('\n')
                for i, line in enumerate(lines):
                    if 'CUST-ORDER:3077' in line or 'CUST ORDER:3077' in line or 'CUST-ORDER: 3077' in line:
                        print(f"\n*** Found at line {i} ***")
                        # Print 20 lines before and 30 lines after
                        for j in range(max(0, i-20), min(len(lines), i+30)):
                            print(f"  [{j}]: {lines[j]}")
                        break
                return ocr_text
            except Exception as e:
                print(f"DEBUG: OCR failed: {e}")
                return text
        return text

    def extract_po_number(self, text: str) -> str:
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'PO' in line and 'number' in line.lower():
                for j in range(i, min(i+3, len(lines))):
                    nums = re.findall(r'\b(\d{4})\b', lines[j])
                    for num in nums:
                        if num != '5630' and num != '2268' and num != '3070':
                            return num

        match = re.search(r':(\d{4})\b', text[:500])
        if match:
            return match.group(1)

        return "Unknown"

    def parse_dalmen_order(self, text: str) -> List[LineItem]:
        lines = text.split('\n')
        print("\nDEBUG: Parsing Dalmen order...")

        po_number = self.extract_po_number(text)
        print(f"  DEBUG: Extracted PO Number: {po_number}")

        items = []

        for i, line in enumerate(lines):
            line = line.strip()

            if re.search(r'^[A-Z]\d', line):
                print(f"  DEBUG: Checking line {i}: '{line}'")

            match = re.match(r'^([A-Z]\d+[\-\_A-Z0-9]*)\s+(.+?)\s+(\d+(?:\.\d+)?)\s+/', line)

            if not match:
                match = re.match(r'^([A-Z][A-Z0-9\-]+)\s+(.+?)\s+([\d\s,\.]+)\s+/', line)

            if match:
                full_code = match.group(1).strip()
                item_code = full_code.split('-')[0].split('_')[0]
                quantity_str = match.group(3).strip()
                quantity_str = quantity_str.replace(' ', '').replace(',', '.')
                try:
                    quantity = float(quantity_str)
                except:
                    quantity = 0.0

                print(f"  Found: {item_code} (from {full_code}) | Qty: {quantity}")

                items.append(LineItem(
                    item_code=item_code,
                    quantity=quantity
                ))
            elif re.search(r'^[A-Z]\d', line):
                print(f"  ✗ Failed to match: '{line}'")

        return OrderDocument(
            po_number=po_number,
            line_items=items,
            total=0.0
        )

    def parse_confirmation(self, text: str) -> OrderDocument:
        lines = text.split('\n')
        print("\nDEBUG: Parsing confirmation...")

        po_number = self.extract_po_number(text)
        po_match = re.search(r'(\d{4})', text[:500])
        if po_match and po_number == "Unknown":
            po_number = po_match.group(1)

        print(f"  DEBUG: Extracted PO Number: {po_number}")

        items = []

        for line in lines:
            line = line.strip()

            match = re.match(r'^(\d+(?:\.\d+)?)\s+\d+\s+[\d\.]+\s+([A-Z][A-Z0-9\-]+)', line)

            if match:
                quantity_str = match.group(1)
                full_code = match.group(2)

                item_code = full_code.split('_')[0]

                try:
                    quantity = float(quantity_str)
                except:
                    quantity = 0.0

                print(f"  Found: {item_code} | Qty: {quantity}")
                items.append(LineItem(item_code=item_code, quantity=quantity))

        print(f"DEBUG: Total items: {len(items)}\n")

        doc = OrderDocument(po_number=po_number, line_items=items, total=0.0)
        doc.is_facture = False
        return doc


    def parse_facture_by_custorder(self, text: str) -> Dict[str, List[LineItem]]:
        lines = text.split('\n')
        print("\nDEBUG: Parsing THERMOPLAST facture by CUST-ORDER...")

        grouped_items = {}
        current_cust_order = None
        stop_words = ['SOUS-TOTAL', 'SUB-TOTAL', 'COPIE DU', 'TOUS LES', 'ALL GOODS', 
                        'PAGE :', 'www.', 'FACTURE / INVOICE', 'CONNAISSEMENT', 'BILL OF LADING',
                        'NO DE PRODUIT', 'PRODUCT NO', 'UNITE', 'UNIT QTY']

        for i, line in enumerate(lines):
            line = line.strip()

            if any(skip in line for skip in stop_words):
                current_cust_order = None
                continue

            cust_match = re.search(r'CUST[-\s]ORDER\s*[:\-]?\s*(\d{4})', line, re.IGNORECASE)
            non_numeric_cust = re.search(r'CUST[-\s]ORDER\s*[:\-]?\s*([A-Z]{2,})', line, re.IGNORECASE)
            if cust_match:
                current_cust_order = cust_match.group(1)
                print(f" Found CUST-ORDER: {current_cust_order}")
                if current_cust_order not in grouped_items:
                    grouped_items[current_cust_order] = []
                continue
            elif non_numeric_cust:
                print(f" Skipping non-numeric CUST-ORDER: {non_numeric_cust.group(1)}")
                current_cust_order = None
                continue

            if not current_cust_order:
                continue

            if re.match(r'^(WHITE|BLACK|MIX|FLEX|TAPE|BLUE|WORK-ORDER|BLEU)', line, re.IGNORECASE):
                continue

            code_match = re.match(r'^([A-Z]{0,2}\d+[\-\_A-Z0-9]*)', line, re.IGNORECASE)
            if code_match:
                full_code = code_match.group(1).strip()
                base_code = full_code.split('-')[0].split('_')[0]

                suffix_match = re.match(r'^[A-Z]{0,2}\d+[\-\_](\d+)', full_code, re.IGNORECASE)
                suffix = suffix_match.group(1) if suffix_match else ""

                price_unit_match = re.search(r'([\d]+\s*\.[\d]{4})\s+(MPI|MPR|UNT|MPC)\s+', line)
                if price_unit_match:
                    unit_price = float(price_unit_match.group(1).replace(' ', ''))
                    unit = price_unit_match.group(2)
                else:
                    unit_price = 0.0
                    unit = ""

                print(f" -> Product: {base_code} (from {full_code}) suffix={suffix} unit={unit} price={unit_price} under CUST-ORDER {current_cust_order}")
                grouped_items[current_cust_order].append(LineItem(
                        item_code=base_code,
                        quantity=0.0,
                        unit_price=unit_price,
                        unit=unit,
                        raw_code=full_code
                    ))

        print(f"\nDEBUG: Found {len(grouped_items)} CUST-ORDERs")
        for co, items in grouped_items.items():
            print(f" CUST-ORDER {co}: {len(items)} items")
    
        return grouped_items


    def load_thermoplast_price_list(self):
        import pandas as pd
        self.load_thermoplast_price_list = {}
        try:
            df = pd.read_excel(r"\\10.0.7.2\Group\Taxi\2026 PRICE LIST\DALMEN PRIX 2 AVRIL 2026 - THERMOPLAST.xlsx",
            sheet_name="Feuil1",
            usecols="C,F",
            header=0)
            df.columns = ["code", "price"]
            df = df.dropna(subset=["code", "price"])
            for _, row in df.iterrows():
                code = str(row["code"]).strip()
                self.thermoplast_prices[code] = float(row["price"])
            print(f"Loaded {len(self.thermoplast_prices)} Thermoplast prices")
        except Exception as e:
            print(f"Failed to load Thermoplast price list: {e}")
            self.thermoplast_prices = {}

    
    def lookup_thermoplast_price(self, base_code: str, suffix: str, unit: str) -> float:
        unit_map = {"MPI": "MPI", "MPR": "MPR", "UNT": "PC"}
        pl_unit = unit_map.get(unit, unit)

        for code, price in self.thermoplast_prices.items():
            if (code.startswith(base_code) and
                f"-{suffix}-" in code and 
                code.endswith(f"-{pl_unit}")):
                return price
        return None


    def calculate_similarity(self, str1: str, str2: str) -> float:
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    def match_documents(self, doc1: OrderDocument, doc2: OrderDocument) -> Dict:
        log = []

        po_match = doc1.po_number == doc2.po_number

        # ── SUMMARY ───────────────────────────────────────────────────────
        log.append("=" * 60)
        log.append("SUMMARY")
        log.append("=" * 60)

        col_width = 38
        log.append(f"{'Doc1 — ' + str(len(doc1.line_items)) + ' items':<{col_width}}  {'Doc2 — ' + str(len(doc2.line_items)) + ' items'}")
        log.append("-" * 60)

        for i in range(max(len(doc1.line_items), len(doc2.line_items))):
            left  = f"  {doc1.line_items[i].item_code} | Qty: {doc1.line_items[i].quantity}" if i < len(doc1.line_items) else ""
            right = f"  {doc2.line_items[i].item_code} | Qty: {doc2.line_items[i].quantity}" if i < len(doc2.line_items) else ""
            log.append(f"{left:<{col_width}}  {right}")

        log.append("")
        po_str = "✅ MATCH" if po_match else "❌ NO MATCH"
        log.append(f"  PO Numbers — Doc1: {doc1.po_number}  |  Doc2: {doc2.po_number}  →  {po_str}")

        if len(doc1.line_items) == 0 or len(doc2.line_items) == 0:
            log.append("")
            if len(doc1.line_items) == 0:
                log.append("  ⚠️  No items found in Doc1")
            if len(doc2.line_items) == 0:
                log.append("  ⚠️  No items found in Doc2")

        # ── MATCHING PROCESS ──────────────────────────────────────────────
        log.append("")
        log.append("=" * 60)
        log.append("MATCHING PROCESS")
        log.append("=" * 60)

        matched       = 0
        total_items   = len(doc2.line_items)
        used_matches  = set()
        price_check_ok = True
        any_price_checked = False

        for item1 in doc1.line_items:
            best_match = None
            best_score = 0
            best_idx   = -1

            for idx, item2 in enumerate(doc2.line_items):
                if idx in used_matches:
                    continue
                score = 0
                if item1.item_code == item2.item_code:
                    score += 60
                elif item1.item_code.lstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZ') == \
                    item2.item_code.lstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                    score += 55
                else:
                    code_sim = self.calculate_similarity(item1.item_code, item2.item_code)
                    if code_sim > 0.75:
                        score += 50
                if item1.quantity > 0 and item2.quantity > 0:
                    if abs(item1.quantity - item2.quantity) < 1:
                        score += 10
                if score > best_score:
                    best_score = score
                    best_match = item2
                    best_idx   = idx

            log.append("")
            result_str = "✅ MATCH" if best_match and best_score >= 50 else "❌ NO MATCH"
            sim_str    = f"(Score: {best_score}/80)"

            if best_match and best_score >= 50:
                used_matches.add(best_idx)
                log.append(f"  {item1.item_code:<20}  →  {best_match.item_code:<20}  {sim_str:<16}  {result_str}")

                facture_price = best_match.unit_price
                if facture_price > 0 and best_match.unit:
                    suffix_match = re.search(r'-(\d+)$', best_match.raw_code)
                    suffix       = suffix_match.group(1) if suffix_match else ""
                    list_price   = self.lookup_thermoplast_price(
                        item1.item_code, suffix=suffix, unit=best_match.unit)
                    if list_price is not None:
                        any_price_checked = True
                        diff = abs(facture_price - list_price)
                        price_ok = diff <= 200
                        if not any_price_checked:
                            price_check_ok = True
                        elif not price_ok:
                            price_check_ok = False
                        status = "✅" if price_ok else "❌"
                        log.append(f"  💲 Facture: ${facture_price:.4f}  |  List: ${list_price:.4f}  |  Diff: ${diff:.2f}  {status}")
                    else:
                        log.append(f"  💲 Facture: ${facture_price:.4f}  |  ⚠️  Not found in price list")
                matched += 1
            else:
                log.append(f"  {item1.item_code:<20}  →  no match found")

        # ── FINAL RESULT ──────────────────────────────────────────────────
        match_percentage = (matched / total_items * 100) if total_items > 0 else 0
        documents_match  = match_percentage >= 70 and po_match

        log.append("")
        log.append("=" * 60)
        log.append("FINAL RESULT")
        log.append("=" * 60)
        log.append(f"  {matched}/{total_items} items matched ({match_percentage:.1f}%)")
        log.append(f"  PO Match:        {'✅ YES' if po_match else '❌ NO'}")
        log.append(f"  Price Check:     {'✅ PASS' if price_check_ok else '❌ FAIL'}")
        log.append(f"  Documents match: {'✅ YES' if documents_match else '❌ NO'}")
        log.append("=" * 60)

        # ── PRICE VERIFICATION ────────────────────────────────────────────
        is_facture = getattr(doc2, 'is_facture', False)

        if is_facture:
            log.append("")
            log.append("=" * 60)
            log.append("PRICE VERIFICATION")
            log.append("=" * 60)

        for item1 in doc1.line_items:
            for item2 in doc2.line_items:
                if item1.item_code == item2.item_code or self.calculate_similarity(item1.item_code, item2.item_code) > 0.75:
                    facture_price = item2.unit_price
                    if facture_price > 0 and item2.unit:
                        suffix_match = re.search(r'-(\d+)$', item2.raw_code)
                        suffix = suffix_match.group(1) if suffix_match else ""
                        list_price = self.lookup_thermoplast_price(item1.item_code, suffix=suffix, unit=item2.unit)
                        log.append("")
                        if list_price is not None:
                            diff = abs(facture_price - list_price)
                            status = "✅ PASS" if diff <= 100 else "❌ FAIL"
                            log.append(f" {item2.item_code:<20} Facture: ${facture_price:<10.4f}  List: ${list_price:<10.4f}  Diff: ${diff:.2f}  {status}")
                        else:
                            log.append(f"  {item2.item_code:<20}  Facture: ${facture_price:.4f}  ⚠️  Not found in price list")
                    break

        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        return {
            "match": documents_match,
            "confidence": match_percentage,
            "matched_items": matched,
            "total_items": total_items,
            "po1": doc1.po_number,
            "po2": doc2.po_number,
            "price_check_ok": price_check_ok,
            "is_confirmation": 'CONFIRMATION' in
                self.extract_pdf_text(self.file2_path).upper() or
                'ENTRY' in self.extract_pdf_text(self.file2_path).upper(),
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

        po_icon = "✅" if result.get('price_check_ok') else "❌"
        stat_box(stats, "PO Numbers",    f"{po_icon}  {result['po1']} / {result['po2']}", 0)
        stat_box(stats, "Items Matched", f"{result['matched_items']} / {result['total_items']}", 1)
        stat_box(stats, "Confidence",    f"{result['confidence']:.1f}%", 2)
        stat_box(stats, "Price Match",   f"{po_icon}  {'Yes' if result.get('price_check_ok') else 'No'}", 3)

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