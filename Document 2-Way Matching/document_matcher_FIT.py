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
import pandas as pd


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


class DocumentMatcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FIT Document Matcher")
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
            text="FIT Document Matcher",
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
        tk.Label(inner1, text="Dalmen Order or FIT Confirmation",
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
        tk.Label(inner2, text="Dalmen Order or FIT Confirmation",
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
            
            print("Parsing second doc...")
            doc2 = self.parse_document(self.file2_path)
            print(f"Doc2 parsed: {len(doc2.line_items)} items found")

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
        """Extract all text from PDF"""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def extract_order_number(self, text: str) -> str:
        
        print(f"\nDEBUG: First 500 chars of text:")
        print(text[:500])
        print("\nDEBUG: Searching for order number...")

        patterns = [
            r'Référence\s*:\s*commande\s+(\d{4})',              
            r'commande\s+(\d{4})\b',                         
            r'K0C\s+2B0\s+(\d{4})',                              
            r'Numéro\s+de\s+PO.*?(\d{4})(?!\d)',  
        ]
        for i, pattern in enumerate(patterns, 1):
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                order_num = match.group(1).strip()
                print(f"✓ Pattern {i} matched: {order_num}")
                return order_num
            else:
                print(f"  ✗ Pattern {i} failed")

        print(f"  ❌ No pattern matched - returning 'Unknown'")  
        return "Unknown"
    
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
        
        # Join lines that are continuations (like "CL-PB-350187-" + "BK")
        cleaned_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # If line ends with hyphen and next line exists
            if line.endswith('-') and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # If next line is short (< 20 chars) and alphanumeric, join them
                if len(next_line) < 20 and next_line and not re.search(r'[\$,\.]', next_line):
                    print(f"  DEBUG: Joining '{line}' + '{next_line}'")
                    line = line + next_line
                    i += 1  # Skip next line
            cleaned_lines.append(line)
            i += 1
        
        print(f"DEBUG: After line joining, have {len(cleaned_lines)} lines")
        
        for i, line in enumerate(cleaned_lines):
            line = line.strip()

            # PATTERN 1: FIT format 
            m1 = re.match(r'^(\d+\s+)?\[([A-Z0-9\-\s\(\)]+)\]', line)
            if m1:
                product_code = m1.group(2).strip()
                total = None
   
                for j in range(i, min(i+ 20, len(cleaned_lines))):
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
            
            # PATTERN 2: Dalmen format - everything on one line
            # Pattern: starts with LETTERS-NUMBERS and has two $ signs
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
            elif re.match(r'^[A-Z]', line) and '$' in line:
                # Debug: Show lines that look like they should match but don't
                print(f"  DEBUG: Dalmen line didn't match: {line[:60]}...")
        
        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items

    def extract_line_items_receipt(self, text: str) -> List[LineItem]:
        items = []
        lines = text.split('\n')

        print(f"\nDEBUG: Parsing FIT receipt - {len(lines)} lines")

        for i, line in enumerate(lines):
            line = line.strip()

            match = re.match(r'^\[([A-Z0-9\-\s]+)\]', line)
            if match:
                product_code = match.group(1).strip()

                unit_price = 0.0
                total = 0.0

                # Look for pattern: QTY UNIT_PRICE HST... TOTAL CAD
                for j in range(i, min(i + 20, len(lines))):
                    # Pattern: number  number  HST...  number CAD
                    price_line = re.search(
                        r'(\d+)\s+([\d,]+)\s+HST\S*\s+([\d\s,]+)\s+CAD',
                        lines[j]
                    )
                    if price_line:
                        try:
                            unit_price = float(price_line.group(2).replace(',', '.'))
                            total_str  = price_line.group(3).replace(' ', '').replace(',', '.')
                            total      = float(total_str)
                            break
                        except:
                            pass

                    # Fallback: just grab CAD amount
                    if not total:
                        cad_match = re.search(r'([\d\s,\.]+)\s+CAD', lines[j])
                        if cad_match:
                            try:
                                val = float(cad_match.group(1).replace(' ', '').replace(',', '.'))
                                if val > 1:
                                    total = val
                            except:
                                pass

                print(f"  Found [Receipt]: {product_code}, Unit: ${unit_price:.3f}, Total: ${total:.2f}")
                items.append(LineItem(
                    product_code=product_code,
                    quantity=1.0,
                    unit_price=unit_price,
                    total=total,
                ))

        print(f"DEBUG: Total items extracted from receipt: {len(items)}\n")
        return items

    def extract_line_items_dalmen(self, text: str) -> List[LineItem]:
        items = []
        lines = text.split('\n')

        print(f"\nDEBUG: Parsing Dalmen PO - {len(lines)} lines")

        in_table = False
        for line in lines:
            line = line.strip()

            if 'Description' in line and 'QTY' in line:
                in_table = True
                continue

            if in_table and (not line or 'Exterior Color' in line):
                break

            if in_table and line:
                if re.match(r'^[A-Z0-9\-]+', line):
                    product_code = line.strip()
                    print(f" Found [Dalmen PO]: {product_code}")
                    items.append(LineItem(
                        product_code=product_code,
                        quantity=1.0,
                        unit_price=0.0,
                        total=0.0
                    ))
    
    def parse_document(self, pdf_path: str) -> OrderDocument:
        """Parse a PDF document"""
        text = self.extract_text_from_pdf(pdf_path)
        order_number = self.extract_order_number(text)
        
        is_receipt = 'Facture' in text or 'FACTURE' in text
        is_dalmen = "DALMEN" in text.upper() and 'Purchase Order' in text

        if is_receipt:
            print(" Detected: FIT Receipt")
            line_items = self.extract_line_items_receipt(text)
        elif is_dalmen:
            print(" Detected: Dalmen PO")
            line_items = self.extract_line_items_dalmen(text)
        else:
            print(" Detected: FIT Confirmation")
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
        code = re.sub(r'^CL-', '', code)  # Remove CL- prefix
        return code.strip()
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    

    def base_code(self, code: str) -> str:
        """Get base product code (first part before space)"""
        return code.split()[0] if code else code
    

    def aggregate(self, items):
        """Aggregate items by base code"""
        agg = defaultdict(lambda: {"total": 0.0, "label": ""})
        for i in items:
            key = self.base_code(i.product_code)
            agg[key]["total"] += i.total
            if not agg[key]["label"]:  # Keep first label seen
                agg[key]["label"] = i.product_code
        return agg


    def match_documents(self, doc1: OrderDocument, doc2: OrderDocument) -> Dict:
        log = []

        order_match = doc1.order_number == doc2.order_number
        if not order_match:
            self.match_log = f"❌ Order numbers do not match ({doc1.order_number} vs {doc2.order_number}) — documents rejected."
            return {
                "match": False, "confidence": 0,
                "matched_items": 0, "total_items": 0,
                "order1": doc1.order_number, "order2": doc2.order_number,
                "total1": doc1.total, "total2": doc2.total,
                "total_diff": 0, "price_check_ok": None,
            }

        agg1 = self.aggregate(doc1.line_items)
        agg2 = self.aggregate(doc2.line_items)

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

        matched = 0

        for key1, data1 in agg1.items():
            total1 = data1["total"]
            label1 = data1["label"]
            best_match = None
            best_diff  = float("inf")
            best_sim   = 0

            for key2, data2 in agg2.items():
                label2 = data2["label"]
                sim = self.calculate_similarity(
                    self.normalize_code(label1),
                    self.normalize_code(label2))
                if sim > best_sim:
                    best_match = label2
                    best_diff  = 0
                    best_sim   = sim

            log.append("")
            matched_this = best_match and best_sim > 0.60
            result_str   = "✅ MATCH" if matched_this else "❌ NO MATCH"
            sim_str      = f"(Similarity: {best_sim:.0%})"

            if best_match:
                log.append(f"  {label1:<20}  →  {best_match:<20}  {sim_str:<20}  {result_str}")
            else:
                log.append(f"  {label1:<20}  →  no match found")

            if matched_this:
                matched += 1

        # ── FINAL RESULT ──────────────────────────────────────────────────
        total_items      = max(len(agg1), len(agg2))
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
        is_facture = 'Facture' in self.extract_text_from_pdf(self.file2_path) or \
                    'FACTURE' in self.extract_text_from_pdf(self.file2_path)
        catalog = self.load_price_catalog() if is_facture else {}
        price_discrepancies = []

        if catalog:
            log.append("")
            log.append("=" * 60)
            log.append("PRICE VERIFICATION")
            log.append("=" * 60)

            for item in doc2.line_items:
                full_code  = item.product_code
                base_code  = full_code.split()[0]
                facture_price = item.unit_price

                catalog_price = None
                if full_code in catalog:
                    catalog_price = catalog[full_code]
                elif base_code in catalog:
                    catalog_price = catalog[base_code]
                else:
                    for cat_code, price in catalog.items():
                        if cat_code.startswith(base_code):
                            catalog_price = price
                            break

                log.append("")
                if catalog_price is not None:
                    diff = abs(facture_price - catalog_price)
                    tol = catalog_price * 0.05
                    status = "✅ PRICE OK" if diff <= tol else "❌ PRICE MISMATCH"
                    log.append(f"  {full_code:<20}  Facture: ${facture_price:<10.3f}  Catalog: ${catalog_price:<10.3f}  Diff: ${diff:.3f}  {status}")
                    if diff > 0.5:
                        price_discrepancies.append({
                            'code': full_code, 'facture': facture_price,
                            'catalog': catalog_price, 'diff': diff})
                else:
                    log.append(f"  {full_code:<20}  ❌ Not found in catalog")

            log.append("")
            if price_discrepancies:
                log.append(f"  ⚠️  {len(price_discrepancies)} price discrepancy(s) found")
            else:
                log.append("  ✅ All prices verified!")

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
            "price_check_ok": len(price_discrepancies) == 0 if catalog else None,
        }


    # ── FUNCTIONALITY FOR PRICING ───────────────────────────────────────────────────────
    def load_price_catalog(self) -> Dict[str, float]:
        try:
            excel_path = r"\\10.0.7.2\Group\Taxi\2026 PRICE LIST\FIT  2026-03-13.xls"
            df = pd.read_excel(excel_path, sheet_name='SO08469', header=0)

            catalog = {}

            for _, row in df.iterrows():
                code = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else None
                price_val = row.iloc[5] if pd.notna(row.iloc[5]) else None

                if code and price_val:
                    try:
                        catalog[code] = float(price_val)
                    except:
                        pass

            print(f"DEBUG: Loaded {len(catalog)} prices from catalog")
            print(f"DEBUG: Sample codes: {list(catalog.keys())[:10]}")
            return catalog

        except Exception as e:
            print(f"WARNING: Could not load price catalog: {e}")
            return {}



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

        order_icon = "✅" if result['order1'] == result['order2'] else "❌"
        stat_box(stats, "Order Numbers",  f"{order_icon}  {result['order1']} / {result['order2']}", 0)
        stat_box(stats, "Items Matched",  f"{result['matched_items']} / {result['total_items']}", 1)
        stat_box(stats, "Doc 1 Total",    f"${result['total1']:.2f}", 2)
        stat_box(stats, "Doc 2 Total",    f"${result['total2']:.2f}", 3)

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