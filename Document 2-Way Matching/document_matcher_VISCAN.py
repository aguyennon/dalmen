"""
AI Document Matcher - GUI Version
Upload any 2 PDFs and check if they match
"""

from email.mime import text
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
            text="🤖 AI Document Matcher",
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
                    print(f"  Found [VISCAN-PO]: {product_code} (no total)")
                    items.append(LineItem(
                        product_code=product_code,
                        quantity=1.0,
                        unit_price=0.0,
                        total=0.0
                    ))
                    continue
        
        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items
    
    def needs_ocr(self, lines):
        has_code = any(re.search(r'[A-Z]{2}\d{2}\.\d+', l) for l in lines)
        has_price = any(re.search(r'\d+\.\d{2}', l) for l in lines)
        return not (has_code and has_price)
        
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
        code = re.sub(r'^CL-', '', code)  # Remove CL- prefix
        
        # Remove VISCAN suffixes like CA, TF, CATW at the end
        # Keep the base code: VA26.0615CA -> VA26.0615
        code = re.sub(r'([A-Z]{2}\d{2}\.\d{4,})([A-Z]+)$', r'\1', code)
        
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
            if i.total > 0:
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

                # If either document has no prices ($0), match ONLY by code similarity
                if total1 == 0 or total2 == 0:
                    if sim > 0.80 and sim > best_sim:  # Higher threshold for code-only matching
                        best_match = label2
                        best_diff = 0
                        best_sim = sim
                else:
                    # Both have prices, match by similarity AND price
                    if sim > 0.60 and diff < best_diff:
                        best_match = label2
                        best_diff = diff
                        best_sim = sim
            
            # When matching by code only, accept any good similarity
            if total1 == 0 or (best_match and data2.get("total", 0) == 0):
                threshold = 0  # No price check needed
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
    