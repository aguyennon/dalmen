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
            pattern = r'^(\d+)\s+(TH\d+)\s+\w+\s+(.+?)\s+([\d.]+)\s+\$?([\d,]+\.?\d*)$'
            
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

    def parse_document(self, pdf_path: str) -> OrderDocument:
        """
        Parse PDF document and return OrderDocument object
        """
        # Extract text from PDF
        full_text = self.extract_text_from_pdf(pdf_path)
        text_lines = full_text.split('\n')
        
        # Extract order number and total
        order_number = self.extract_order_number(full_text)
        total = self.extract_total(full_text)
        
        # Detect document type
        full_text_upper = full_text.upper()
        
        # Check if it's a Dalmen confirmation
        is_dalmen_confirmation = 'DALMEN' in full_text_upper and 'ORDER CONFIRMATION' in full_text_upper
        
        # Parse based on document type
        if is_dalmen_confirmation:
            print("Detected: DALMEN CONFIRMATION")
            line_items = self.parse_dalmen_confirmation(text_lines)
        else:
            print("Detected: STANDARD FORMAT (using extract_line_items)")
            line_items = self.extract_line_items(full_text)
        
        # Create and return OrderDocument
        return OrderDocument(
            order_number=order_number,
            line_items=line_items,
            total=total
        )

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
        # Title
        title_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Document Matcher",
            font=("Arial", 24, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        
        title_label.pack(expand=True)
        
        # Container for subtitle and log button
        bottom_header = tk.Frame(title_frame, bg=self.primary_color)
        bottom_header.pack(fill=tk.X, padx=20)
        
        subtitle_label = tk.Label(
            bottom_header,
            text="Upload two PDF documents to compare",
            font=("Arial", 10),
            bg=self.primary_color,
            fg="white"
        )
        subtitle_label.pack(side=tk.LEFT)

        self.print_btn = tk.Button(
            bottom_header,
            text="Print Log",
            font=("Arial", 9, "bold"),
            bg="#5568d3",
            fg="#FFFFFF",
            cursor="hand2",
            command=self.print_log,
            relief=tk.FLAT,
            padx=10,
            pady=5,
            state=tk.DISABLED
        )
        self.print_btn.pack(side=tk.RIGHT)
        
        # Small log button in header
        self.log_btn = tk.Button(
            bottom_header,
            text="Log",
            font=("Arial", 9, "bold"),
            bg="#5568d3",
            fg="#FFFFFF",
            cursor="hand2",
            command=self.show_log_window,
            relief=tk.FLAT,
            padx=10,
            pady=5,
            state=tk.DISABLED
        )
        self.log_btn.pack(side=tk.RIGHT)
        
        # Main content
        content_frame = tk.Frame(self.root, bg=self.bg_color, padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Document 1
        doc1_frame = tk.LabelFrame(
            content_frame,
            text="Document 1",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.primary_color,
            padx=20,
            pady=15
        )
        doc1_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.file1_label = tk.Label(
            doc1_frame,
            text="No file selected",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#666",
            anchor="w"
        )
        self.file1_label.pack(fill=tk.X, pady=(0, 10))
        
        btn1 = tk.Button(
            doc1_frame,
            text="📁 Browse for PDF",
            font=("Arial", 11, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground="#5568d3",
            activeforeground="white",
            cursor="hand2",
            command=lambda: self.browse_file(1),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        btn1.pack()
 
        # Document 2
        doc2_frame = tk.LabelFrame(
            content_frame,
            text="Document 2",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.primary_color,
            padx=20,
            pady=15
        )
        doc2_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.file2_label = tk.Label(
            doc2_frame,
            text="No file selected",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#666",
            anchor="w"
        )
        self.file2_label.pack(fill=tk.X, pady=(0, 10))
        
        btn2 = tk.Button(
            doc2_frame,
            text="📁 Browse for PDF",
            font=("Arial", 11, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground="#5568d3",
            activeforeground="white",
            cursor="hand2",
            command=lambda: self.browse_file(2),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        btn2.pack()
        
        # Compare button
        self.compare_btn = tk.Button(
            content_frame,
            text="⚡ Compare Documents",
            font=("Arial", 14, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground="#5568d3",
            activeforeground="white",
            cursor="hand2",
            command=self.compare_documents,
            relief=tk.FLAT,
            padx=30,
            pady=15,
            state=tk.DISABLED
        )
        self.compare_btn.pack(fill=tk.X, pady=(0, 20))
        
        
        # Progress bar
        self.progress = ttk.Progressbar(
            content_frame,
            mode='indeterminate',
            length=300
        )
        
        # Result frame
        self.result_frame = tk.Frame(content_frame, bg=self.bg_color)
        self.result_frame.pack(fill=tk.BOTH, expand=True)

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
        """Extract order number"""
        patterns = [
            r'Commande\s+n°\s*(\w+)',
            r'Numéro de PO\s+(\d+)',
            r'(?:Order|PO)\s*[#:]*\s*(\d+)',
            r'commande\s+(\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
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
        
        # Check if it's a Dalmen confirmation
        is_dalmen_confirmation = 'DALMEN' in full_text_upper and 'CONFIRMATION' in full_text_upper
        
        # Check if it's a LION order
        is_lion_order = 'QUINCAILLERIE LION' in full_text_upper or 'LION' in full_text_upper
        
        # Parse based on document type
        if is_dalmen_confirmation:
            print("✓ Detected: DALMEN CONFIRMATION")
            line_items = self.parse_dalmen_confirmation(text_lines)
        elif is_lion_order:
            print("✓ Detected: LION ORDER")
            line_items = self.extract_line_items(full_text)
        else:
            print("⚠ WARNING: Unknown document type, using standard parser")
            line_items = self.extract_line_items(full_text)
        
        # ALWAYS return OrderDocument, never return dict
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
        """Match two documents"""
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

                if sim > 0.60 and diff < best_diff:
                    best_match = label2
                    best_diff = diff
                    best_sim = sim
            
            threshold = max(5.0, total1 * 0.10)
            matched_this = best_match and best_diff < threshold
            
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
        
        # Store log
        self.match_log = "\n".join(log)
        
        # Also print to console
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
            "total_diff": abs(doc1.total - doc2.total)
        }
    
    def display_result(self, result):
        """Display comparison result"""
        self.progress.stop()
        self.progress.pack_forget()
        self.compare_btn.config(state=tk.NORMAL)
        self.log_btn.config(state=tk.NORMAL, bg=self.primary_color)
        self.print_btn.config(state=tk.NORMAL, bg=self.primary_color)
        
        # Clear result frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Result color
        if result['match']:
            bg_color = self.success_color
            icon = "✅"
            title = "DOCUMENTS MATCH"
            message = "The documents are consistent!"
        else:
            bg_color = self.error_color
            icon = "❌"
            title = "DOCUMENTS DO NOT MATCH"
            message = "Discrepancies found."
        
        # Result card
        result_card = tk.Frame(self.result_frame, bg=bg_color, padx=20, pady=20)
        result_card.pack(fill=tk.BOTH, expand=True)
        
        # Icon and title
        icon_label = tk.Label(
            result_card,
            text=icon,
            font=("Arial", 48),
            bg=bg_color,
            fg="white"
        )
        icon_label.pack()
        
        title_label = tk.Label(
            result_card,
            text=title,
            font=("Arial", 18, "bold"),
            bg=bg_color,
            fg="white"
        )
        title_label.pack(pady=(10, 5))
        
        message_label = tk.Label(
            result_card,
            text=message,
            font=("Arial", 11),
            bg=bg_color,
            fg="white"
        )
        message_label.pack(pady=(0, 20))
        
        # Details frame
        details_frame = tk.Frame(result_card, bg="white", padx=15, pady=15)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        details = [
            ("Order Numbers:", f"{result['order1']} ↔ {result['order2']}"),
            ("Confidence:", f"{result['confidence']:.1f}%"),
            ("Matched Items:", f"{result['matched_items']} / {result['total_items']}"),
            ("Document Totals:", f"${result['total1']:.2f} ↔ ${result['total2']:.2f}"),
            ("Difference:", f"${result['total_diff']:.2f}")
        ]
        
        for i, (label, value) in enumerate(details):
            row_frame = tk.Frame(details_frame, bg="white")
            row_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                row_frame,
                text=label,
                font=("Arial", 10, "bold"),
                bg="white",
                anchor="w"
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row_frame,
                text=value,
                font=("Arial", 10),
                bg="white",
                anchor="e"
            ).pack(side=tk.RIGHT)
            
            # View Details button
        tk.Button(
            details_frame,
            text="📋 View Detailed Log",
            font=("Arial", 10, "bold"),
            bg=self.primary_color,
            fg="white",
            cursor="hand2",
            command=self.show_log_window,
            relief=tk.FLAT,
            padx=15,
            pady=8
        ).pack(pady=(15, 0))
        

    
    
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
    