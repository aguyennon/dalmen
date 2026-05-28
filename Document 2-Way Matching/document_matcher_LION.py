"""
AI Document Matcher - GUI Version
Upload any 2 PDFs and check if they match
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import scrolledtext
from unittest import skip
import pdfplumber
import re
from typing import Dict, List
from dataclasses import dataclass
from difflib import SequenceMatcher
import threading
from collections import defaultdict
import os



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


    def parse_dalmen_confirmation(self, text_lines):
    
        items = []
    
        # If text_lines is a string, split it into lines
        if isinstance(text_lines, str):
            text_lines = text_lines.split('\n')
        
        print(f"\nDEBUG: Parsing Dalmen confirmation - {len(text_lines)} lines")
        
        for i, line in enumerate(text_lines):
            # Strip whitespace for cleaner processing
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip header/footer/summary lines
            skip_keywords = [
                'ORDER CONFIRMATION',
                'Customer #',
                'Customer name',
                'Customer PO#',
                'Confirmation date',
                'Richelieu',
                'QTY ITEM U/M',
                'DESCRIPTION',
                'COST',
                'Sous-total',
                'Freight',
                'GST',
                'PST',
                'www.lionhardware.com',
                'St-Jacques',
                '24 rue',
                'E7B',
                'PH:',
                'Fax:',
                'BO'
            ]
            
            # Check if line should be skipped
            should_skip = False
            for keyword in skip_keywords:
                if keyword in line:
                    should_skip = True
                    break
            
            if should_skip:
                continue
            
            # Skip lines that start with "Total" (but not header row)
            if line.startswith('Total'):
                continue
            
            # Pattern: QUANTITY ITEM_CODE U/M DESCRIPTION UNIT_PRICE $TOTAL
            pattern = r'^(\d+)\s+(?:\w+\s+)?(TH\d+)\s+\w+\s+(.+?)\s+([\d.]+)\s+\$?([\d,]+\.?\d*)$'
            
            match = re.match(pattern, line)
            
            if match:
                # Extract the matched groups
                qty = int(match.group(1))           # "3861"
                item_code = match.group(2)          # "TH2390593"
                description = match.group(3)        # "KEEPER MP NON-HANDED"
                unit_price = float(match.group(4))  # "0.7200"
                total = float(match.group(5).replace(',', ''))  # "2779.92"
                
                print(f"  ✓ Found [Dalmen]: {item_code} qty={qty} total=${total:.2f}")
                
                # Create LineItem object
                items.append(LineItem(
                    product_code=item_code,
                    quantity=float(qty),
                    unit_price=unit_price,
                    total=total
                ))
            else:
                # Only log if line has TH code (potential item that didnt match)
                if 'TH' in line and len(line) > 20:
                    print(f"  ✗ Dalmen line didn't match: {line[:50]}...")
        
        print(f"DEBUG: Total Dalmen items extracted: {len(items)}")
        
        return items


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

        tk.Label(header, text="LION Matcher", font=("Arial", 22, "bold"),
                bg=self.primary_color, fg="white").pack(side=tk.LEFT, padx=24, pady=16)

        self.log_btn = tk.Button(header, text="📋  View Log", font=("Arial", 10, "bold"),
                                bg="#5568d3", fg="white", cursor="hand2",
                                command=self.show_log_window, relief=tk.FLAT,
                                padx=14, pady=8, state=tk.DISABLED)
        self.log_btn.pack(side=tk.RIGHT, padx=20, pady=14)

        tk.Label(header, text="Match Dalmen orders with Lion invoices",
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
        tk.Label(inner2, text="Lion Invoice", font=("Arial", 8),
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

    def normalize_lion_code(self, code: str) -> str:
        code = code.replace('-', '')
        if not code.startswith('TH'):
            code = 'TH' + code
        return code

    
    def lion_codes_match(self, code1: str, code2: str) -> bool:
        c1 = self.normalize_lion_code(code1)
        c2 = self.normalize_lion_code(code2)

        return c1.startswith(c2) or c2.startswith(c1)

    
    def extract_order_number(self, text: str) -> str:
        print(f"DEBUG order number text:\n{text[:500]}") 
        """Extract order number"""
        patterns = [
            r'N[°o]\s*COMMANDE\s+DU\s+CLIENT\s*[\n\r]+\s*(\d+)',
            r'CUSTOMER\s*ORDER\s*NO\.?\s*[\n\r]+\s*(\d+)',
            r'CUSTOMERORDERNO\.?\s*(\d+)',
            r'K0C\s+2B0\s+(\d{4})',
            r'CUSTOMERORDERNO\.?\s*[\n\r]+\s*(\d+)',
            r'PO\s+number\s*[\n\r]+\s*(\d+)',
            r'N°?\s*COMMANDE\s+DU\s+CLIENT\s*[\n\r]+\s*(\d+)',
            r'CUSTOMER\s*ORDER\s*NO\.?\s*[\n\r]+\s*(\d+)',
            r'PO\s+number\s*[:\s]+(\d+)',
            r'Commande\s+n°\s*(\w+)',
            r'Numéro de PO\s+(\d+)',
            r'(?:Order|PO)\s*[#:]*\s*(\d+)',
            r'commande\s+(\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return "Undetected"
    
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
        
        for line in cleaned_lines:
            line = line.strip()
            
            # PATTERN 1: Same format as FIT 
            m1 = re.match(r'^(\d+\s+)?\[([A-Z0-9\-\s\(\)]+)\]', line)
            if m1:
                product_code = m1.group(2).strip()
                total = None
                
                # Look in the NEXT 10 lines only (not all cleaned_lines)
                line_idx = cleaned_lines.index(line)
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
            
            # PATTERN 2: Dalmen format - everything on one line
            # Look for: CODE (anything with dashes) then description with prices
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
                # Debug: Show lines that look like they should match but dont
                print(f"  DEBUG: Dalmen line didn't match: {line[:60]}...")
        
        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items

    def parse_lion_facture(self, text_lines) -> List[LineItem]:
        items = []
        if isinstance(text_lines, str):
            text_lines = text_lines.split('\n')

        print(f"\nDEBUG: Parsing Lion facture - {len(text_lines)} lines")

        for line in text_lines:
            line = line.strip()
            if not line:
                continue

            match = re.match(r'^(\d+)\s+(TH\d+)\s+.+?\s+EA\s+([\d\.]+)\s+([\d\.]+)\s*$', line)
            if match:
                qty = float(match.group(1))
                code = match.group(2)
                unit_price = float(match.group(3))
                total = float(match.group(4))
                print(f"  ✓ Found [Lion Facture]: {code} qty={qty} unit=${unit_price} total=${total}")
                items.append(LineItem(
                    product_code=code,
                    quantity=qty,
                    unit_price=unit_price,
                    total=total
                ))
            elif 'TH' in line and len(line) > 20:
                print(f" Lion facture line didn't match: {line[:60]}")

        print(f"DEBUG: Total Lion facture items: {len(items)}")
        return items
    
    def parse_document(self, pdf_path: str) -> OrderDocument:
    
        # Extract text from PDF
        full_text = self.extract_text_from_pdf(pdf_path)
        text_lines = full_text.split('\n')
        
        # Extract order number and total
        order_number = self.extract_order_number(full_text)
        total = self.extract_total(full_text)
        
        # Detect document type - BE MORE LENIENT**
        full_text_upper = full_text.upper()
        

        print(f"DEBUG: Checking document type...")
        print(f"  Contains 'DALMEN': {'DALMEN' in full_text_upper}")
        print(f"  Contains 'ORDER CONFIRMATION': {'ORDER CONFIRMATION' in full_text_upper}")
        print(f"  Contains 'QUINCAILLERIE LION': {'QUINCAILLERIE LION' in full_text_upper}")

        is_lion_confirmation = ('ORDER CONFIRMATION' in full_text_upper and 
                        ('LION' in full_text_upper or 'RICHELIEU' in full_text_upper or 
                         'TH' in full_text_upper))

        is_dalmen_confirmation = ('DALMEN' in full_text_upper and 
                                'CONFIRMATION' in full_text_upper and
                                not is_lion_confirmation)

        is_lion_facture = ('INVOICE' in full_text_upper or 'FACTURE' in full_text_upper or
                        'N° PRODUIT' in full_text_upper or 'PRIX UNITAIRE' in full_text_upper)

        is_lion_order = ('QUINCAILLERIE LION' in full_text_upper or 
                        'LION' in full_text_upper) and not is_lion_facture and not is_lion_confirmation

        if is_lion_confirmation:
            print("✓ Detected: LION CONFIRMATION")
            line_items = self.parse_dalmen_confirmation(text_lines)
        elif is_dalmen_confirmation:
            print("✓ Detected: DALMEN CONFIRMATION")
            line_items = self.parse_dalmen_confirmation(text_lines)
        elif is_lion_facture:
            print("✓ Detected: LION FACTURE")
            line_items = self.parse_lion_facture(text_lines)
        elif is_lion_order:
            print("✓ Detected: LION ORDER")
            line_items = self.extract_line_items(full_text)
        else:
            print("⚠ WARNING: Unknown document type, using standard parser")
            line_items = self.extract_line_items(full_text)
        
        # ALWAYS return OrderDocument, never return dict
        doc = OrderDocument(
            order_number=order_number,
            line_items=line_items,
            total=total
        )
        doc.is_facture = is_lion_facture
        return doc

    
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

        agg1 = self.aggregate(doc1.line_items)
        agg2 = self.aggregate(doc2.line_items)

        # ── SUMMARY ───────────────────────────────────────────────────────
        log.append("=" * 60)
        log.append("SUMMARY")
        log.append("=" * 60)

        col_width = 38
        header = f"{'Doc1 — ' + str(len(agg1)) + ' items':<{col_width}}  {'Doc2 — ' + str(len(agg2)) + ' items'}"
        log.append(header)
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
        scored  = 0

        for key1, data1 in agg1.items():
            total1 = data1["total"]
            label1 = data1["label"]
            best_match       = None
            best_match_total = 0.0
            best_diff        = float("inf")
            best_sim         = 0

            for key2, data2 in agg2.items():
                total2 = data2["total"]
                label2 = data2["label"]

                if self.lion_codes_match(label1, label2):
                    sim = 1.0
                else:
                    sim = self.calculate_similarity(
                        self.normalize_code(label1),
                        self.normalize_code(label2))
                    if sim < 0.85:
                        sim = 0.0

                diff = abs(total1 - total2)
                if sim > 0.60 and diff < best_diff:
                    best_match       = label2
                    best_match_total = total2
                    best_diff        = diff
                    best_sim         = sim

            log.append("")

            if not best_match:
                log.append(f"  {label1:<20}  →  not found on facture — skipped")
                continue

            scored += 1
            threshold    = max(5.0, total1 * 0.15)
            matched_this = best_diff < threshold

            is_facture = hasattr(doc2, 'is_facture') and doc2.is_facture
            if is_facture and total1 > 0:
                price_diff_pct = abs(total1 - best_match_total) / total1 * 100
                price_ok = price_diff_pct <= 15
                if not price_ok:
                    matched_this = False
            else:
                price_diff_pct = 0.0
                price_ok = True

            result_str = "✅ MATCH" if matched_this else "❌ NO MATCH"
            sim_str    = f"(Similarity: {best_sim:.0%})"

            log.append(f"  {label1:<20}  →  {best_match:<20}  {sim_str:<20}  {result_str}")
            if is_facture:
                log.append(f"  💲 Price:  PO ${total1:<10.2f}  |  Facture ${best_match_total:<10.2f}  |  Diff: {price_diff_pct:.1f}%  →  {'✅' if price_ok else '❌'}")

            if matched_this:
                matched += 1

        # ── FINAL RESULT ──────────────────────────────────────────────────
        match_percentage = (matched / scored * 100) if scored > 0 else 0
        documents_match  = match_percentage >= 70

        log.append("")
        log.append("=" * 60)
        log.append("FINAL RESULT")
        log.append("=" * 60)
        log.append(f"  {matched}/{scored} items matched ({match_percentage:.1f}%)")
        log.append(f"  Documents match: {'✅ YES' if documents_match else '❌ NO'}")
        log.append("=" * 60)

        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        return {
            "match": documents_match,
            "confidence": match_percentage,
            "matched_items": matched,
            "total_items": scored,
            "order1": doc1.order_number,
            "order2": doc2.order_number,
            "total1": doc1.total,
            "total2": doc2.total,
            "total_diff": abs(doc1.total - doc2.total),
            "price_check_ok": documents_match,
            "is_confirmation": not (hasattr(doc2, 'is_facture') and doc2.is_facture),
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

        order_icon = "✅" if result['order1'] == result['order2'] else "❌"
        stat_box(stats, "PO Numbers", f"{order_icon}  {result['order1']} / {result['order2']}", 0)
        stat_box(stats, "Items Matched", f"{result['matched_items']} / {result['total_items']}", 1)
        stat_box(stats, "Confidence", f"{result['confidence']:.1f}%", 2)
        price_ok = result['confidence'] >= 70 
        stat_box(stats, "Price Check", "✅" if price_ok else "❌", 3)

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
    