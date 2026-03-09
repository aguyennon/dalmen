"""
AI Document Matcher - GUI Version
Upload any 2 PDFs and check if they match
FIXED VERSION - Improved DECKO/Dalmen matching
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
        r'Votre\s+N[°o]\s+commande\s*[:\s]*([\d\-]+[A-Z0-9]*)',  # DECKO confirmation: "Votre N° commande 310-03328-23-1-1"
        r'Num[ée]ro?\s+de\s+bon\s*[:\s]*\n\s*([\d\-]+)',  # Dalmen order: "Numéro de bon\n310-03328-23-1"
        r'commande\s+([\d\-]{10,})',  # "commande" followed by long number (10+ chars)
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
            
            # PATTERN 0: Decko format with Code column (PPCCOR - 51817, OPTION - 50843, THER - 99715)
            # Matches lines like: "PPCCOR - 51817" or "OPTION - 50843"
            # BUT skip header lines
            if not any(x in line.upper() for x in ['CODE', 'DESCRIPTION', 'QTÉ', 'N° INTERNE']):
                decko_code_match = re.match(r'^([A-Z]+)\s*-\s*(\d+)', line)
                if decko_code_match:
                    product_code = f"{decko_code_match.group(1)}-{decko_code_match.group(2)}"
                    print(f"  Found [DECKO-CODE]: {product_code}")
                    # Don't add yet if we already have it
                    if not any(item.product_code == product_code for item in items):
                        items.append(LineItem(
                            product_code=product_code,
                            quantity=1.0,
                            unit_price=0.0,
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
                # Check if we already have this code
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
        """Detect which provider/format the document is from"""
        t = text.upper()

        has_decko = "DECKO" in t or "PORTES DECKO" in t or "PORTES DECKO" in t
        has_dalmen = "DALMEN" in t or "DA1LMEN" in t or "DALM EN" in t or "PRODUITS DALMEN" in t
        has_tamarack = "TAMARACK" in t
        has_fournisseur = "FOURNISSEUR" in t

        has_decko_codes = bool(re.search(r'(PPCCOB|PPHA2B|PPH|BL-\d+|OPTION\s*-\s*\d+|THER\s*-\s*\d+)', t))

        has_confirmation_format = "CONFIRMATION DE" in t and "COMMANDE" in t and "RENEAD DESROSIERS" in t

        # If it has both DECKO and DALMEN, it's a DECKO_DALMEN document
        if has_decko and has_dalmen:
            return "DECKO_DALMEN"
        
        # If it has DALMEN and TAMARACK (Dalmen order for DECKO)
        if has_dalmen and has_tamarack:
            return "DECKO_DALMEN"
        
        # If it has DECKO and TAMARACK (DECKO confirmation)
        if has_decko and has_tamarack:
            return "DECKO_DALMEN"
        
        # If it mentions "Fournisseur : DECKO" (Supplier: DECKO)
        if has_fournisseur and has_decko:
            return "DECKO_DALMEN"
        
        if has_fournisseur and has_dalmen and ("PATIO" in t or "DOOR" in t or "PORTE" in t):
            return "DECKO_DALMEN"
        
        if has_dalmen and has_decko_codes:
            return "DECKO_DALMEN"
         
        return "GENERIC"

    def extract_decko_header(self, text: str) -> dict:
        fields = {}

        patterns = {
            "order_number": r'(?:NUM[EÉ]RO DE BON|N[°O]\s*COMMANDE|Votre\s+N[°o]\s+commande)\s*[:#]?\s*([A-Z0-9\-]+)',
            "client": r'DALMEN',
            "supplier": r'DECKO',
            "project": r'TAMARACK',
            "lot": r'LOT\s*\d+',
            "required_date": r'REQUIS\s*[: ]\s*(\d{4}-\d{2}-\d{2})'
        }
    
        for k, p in patterns.items():
            m = re.search(p, text, re.IGNORECASE)
            if m:
                try:
                    fields[k] = m.group(1) if m.lastindex and m.lastindex >= 1 else True
                except:
                    fields[k] = True

        return fields
        
    def parse_fraction(self, value: str) -> float:
        value = value.replace('-', '').strip()

        if ' ' in value:
            whole, frac = value.split()
            num, den = frac.split('/')
            return float(whole) + float(num) / float(den)
        
        if '/' in value:
            num, den = value.split('/')
            return float(num) / float(den)
        
        return float(value)

    def extract_decko_fingerprint(self, text: str) -> ProductFingerprint:
        """Extract product fingerprint from DECKO document text"""
        t = text.upper()
        fp = ProductFingerprint(extras=set())

        print("\nDEBUG: Extracting fingerprint from text...")
        
        # Category detection
        if "PATIO" in t or "PORTE-PATIO" in t:
            fp.category = "PATIO_DOOR"
            print("  - Category: PATIO_DOOR")
        elif "DOOR" in t or "PORTE" in t:
            fp.category = "DOOR"
            print("  - Category: DOOR")
        elif "WINDOW" in t or "FENETRE" in t or "FENÊTRE" in t:
            fp.category = "WINDOW"
            print("  - Category: WINDOW")

        print(f"\nDEBUG: Searching for configuration in text...")
        print(f"  Text contains 'XO': {'XO' in t}")
        print(f"  Text contains '(XO)': {'(XO)' in t}")
        print(f"  Text contains 'X0': {'X0' in t}")
        
        # Configuration (XO, OX, etc.) - look for these patterns
        config_patterns = [
            r'\(([XO0]{2,3})\)',  # (XO), (X0), or (OX)
            r'\b([XO0]{2,3})\b\s*[\'"]?\s*6',  # "XO 6" or "X0 6"
            r'OPENING?\s+TOWARDS?\s+THE\s+(RIGHT|LEFT)',
            r'(RIGHT|LEFT)\s*\(?(XO|OX|X0|0X)\)?',
            r'CLASSIC\s+["\']?C["\']?\s+PATIO\s+DOORS?\s*\(([XO0]+)\)',  # Classic "C" Patio Doors (XO)
            r'PATIO.*?\(([XO0]{2})\)',  # Any "patio....(XO)" pattern
        ]
        
        for pattern in config_patterns:
            m = re.search(pattern, t)
            if m:
                config_text = m.group(0).upper()
                print(f"  DEBUG: Found config match: '{config_text}'")

                if 'XO' in config_text or 'X0' in config_text or 'RIGHT' in config_text:
                    fp.configuration = "XO"
                    print(f"  - Configuration: {fp.configuration}")
                    break
                elif 'OX' in config_text or '0X' in config_text or 'LEFT' in config_text:
                    fp.configuration = "OX"
                    print(f"  - Configuration: {fp.configuration}")
                    break

        if not fp.configuration:
            if re.search(r'\bXO\b', t):
                fp.configuration = "XO"
                print(f"  - Configuration: XO (detected by standalone 'XO')")
            elif re.search(r'\bOX\b', t):
                fp.configuration = "OX"
                print(f"  - Configuration: OX (detected by standalone 'OX')")

        print(f"\nDEBUG: Searching for dimensions...")
        # Look for any X pattern
        x_matches = re.findall(r'\d+[^\n]{0,20}[Xx×][^\n]{0,20}\d+', t)
        if x_matches:
            print(f"  Found potential dimension patterns: {x_matches[:3]}")
            
        desc_patterns = [
            r'CLASS[^\n]{0,100}',  # CLASS... line
            r'PATIO[^\n]{0,100}',  # PATIO... line  
            r'70[^\n]{0,100}81',   # Any line with 70...81
        ]
        for dp in desc_patterns:
            desc_match = re.search(dp, t)
            if desc_match:
                print(f"  Found description pattern match: '{desc_match.group(0)}'")
        
        # Special case: Look for "BL-141 70 5/8"" pattern (width on separate line from height)
        bl_width_match = re.search(r'BL-\d+\s+(\d+)\s+(\d+)/(\d+)\s*[\"″]', t)
        if bl_width_match:
            fp.width = float(bl_width_match.group(1)) + float(bl_width_match.group(2)) / float(bl_width_match.group(3))
            print(f"  DEBUG: Found width from BL-141 line: {fp.width:.2f}\"")
            
            # Now look for height in the product description line (usually "81"")
            height_match = re.search(r'-\s*(\d{2})\s*[\"″]\s*-', t)  # "- 81" -"
            if height_match:
                fp.height = float(height_match.group(1))
                print(f"  DEBUG: Found height from description: {fp.height:.2f}\"")
                
                if 60 <= fp.width <= 100 and 70 <= fp.height <= 96:
                    print(f"  - Dimensions: {fp.width:.2f}\" x {fp.height:.2f}\"")
        
        # Define dimension patterns
        dim_patterns = [
            # Pattern: "70 5/8 "X 81 " or "70 11/16" X 81"
            (r'(\d+)\s+(\d+)/(\d+)\s*[\"″]?\s*[Xx×]\s*(\d+)\s+(\d+)/(\d+)', 'both_fractions'),
            (r'(\d+)\s+(\d+)/(\d+)\s*[\"″]?\s*[Xx×]\s*(\d+)', 'width_fraction'),
            # Pattern: simple dimensions like "70" X 81" or 70 X 81
            (r'(\d{2,3})\s*[\"″]?\s*[Xx×]\s*(\d{2,3})\s*[\"″]?', 'simple'),
            # Pattern: "81" - 7 1/4" format (height then width)
            (r'(\d{2})\s*[\"″]\s*-\s*(\d+)\s+(\d+)/(\d+)', 'height_first'),
        ]
        
        # If dimensions not found yet, try standard patterns
        if fp.width == 0.0 or fp.height == 0.0:
            for pattern, ptype in dim_patterns:
                matches = re.finditer(pattern, t)
                for dim in matches:
                    try:
                        if ptype == 'both_fractions':  # "70 5/8 X 81 1/4"
                            fp.width = float(dim.group(1)) + float(dim.group(2)) / float(dim.group(3))
                            fp.height = float(dim.group(4)) + float(dim.group(5)) / float(dim.group(6))
                        elif ptype == 'width_fraction':  # "70 5/8 X 81"
                            fp.width = float(dim.group(1)) + float(dim.group(2)) / float(dim.group(3))
                            fp.height = float(dim.group(4))
                        elif ptype == 'height_first':  # "81" - 7 1/4" (height - width)
                            fp.height = float(dim.group(1))
                            fp.width = float(dim.group(2)) + float(dim.group(3)) / float(dim.group(4))
                        else:  # 'simple': "70 X 81"
                            fp.width = float(dim.group(1))
                            fp.height = float(dim.group(2))
                        
                        print(f"  DEBUG: Parsed {ptype}: width={fp.width}, height={fp.height}")
                        
                        # Sanity check: reasonable patio door dimensions (60-100" wide, 70-96" tall)
                        if 60 <= fp.width <= 100 and 70 <= fp.height <= 96:
                            print(f"  - Dimensions: {fp.width:.2f}\" x {fp.height:.2f}\"")
                            break
                        else:
                            print(f"  DEBUG: Rejected - outside reasonable range")
                            fp.width = 0.0
                            fp.height = 0.0
                    except Exception as e:
                        print(f"  DEBUG: Parse error: {e}")
                        continue
                
                # If we found valid dimensions, stop searching
                if fp.width > 0 and fp.height > 0:
                    break
                        
        # Frame material
        if "PVC" in t or "VINYL" in t:
            fp.frame = "PVC"
            print("  - Frame: PVC")

        # Glass configuration
        if "TRIPLE" in t:
            fp.glass_layers = 3
            print("  - Glass: TRIPLE (3 layers)")
        elif "DOUBLE" in t:
            fp.glass_layers = 2
            print("  - Glass: DOUBLE (2 layers)")
        
        # Low-E detection
        if re.search(r'LOW\s*-?\s*E', t) or "LOW-E" in t or "LOWE" in t:
            fp.low_e = True
            print("  - Low-E: Yes")
        
        # Argon
        if "ARGON" in t:
            fp.argon = True
            print("  - Argon: Yes")

        # Colors - look for interior/exterior patterns
        color_patterns = [
            (r'(?:EXTERIOR|EXT\.?|EXTERIEUR)\s+(?:COLOR|COLOUR|COULEUR)?[:\s]*([A-Z]+)', 'exterior'),
            (r'(?:INTERIOR|INT\.?|INTERIEUR)\s+(?:COLOR|COLOUR|COULEUR)?[:\s]*([A-Z]+)', 'interior'),
            (r'(?:EXT\.?\s+)?(?:PAINT|PAINTED|PEINTURE)[:\s-]*([A-Z]+)', 'exterior'),
        ]
        
        for pattern, side in color_patterns:
            m = re.search(pattern, t)
            if m:
                color = m.group(1)
                if "BLACK" in color or "NOIR" in color or "525" in color:
                    if side == 'exterior':
                        fp.exterior_color = "BLACK"
                        print(f"  - Exterior Color: BLACK")
                elif "WHITE" in color or "BLANC" in color or "141" in color:
                    if side == 'interior':
                        fp.interior_color = "WHITE"
                        print(f"  - Interior Color: WHITE")
                    elif side == 'exterior':
                        fp.exterior_color = "WHITE"

        # Extras/Options - look for common add-ons
        extras_map = {
            r'SCREEN|MOUSTIQUAIRE': 'SCREEN',
            r'HANDLE|POIGN[EÉ]E': 'HANDLE',
            r'BRICKMOULD|BRICK\s*MOULD': 'BRICKMOULD',
            r'GRILLE?|GRID': 'GRILLE',
            r'MORTISE': 'MORTISE_HANDLE',
            r'CONTEMPORARY': 'CONTEMPORARY',
            r'ALUMINUM': 'ALUMINUM_SCREEN',
        }
        
        for pattern, extra in extras_map.items():
            if re.search(pattern, t):
                fp.extras.add(extra)
                print(f"  - Extra: {extra}")

        # Look for product codes that might indicate options
        if "OPTION" in t:
            fp.extras.add("OPTION")
            print("  - Has OPTIONS")
        
        if "THER" in t or "THERMO" in t:
            fp.extras.add("THERMAL")
            print("  - Has THERMAL option")

        return fp

    def compare_fingerprints(self, f1: ProductFingerprint, f2: ProductFingerprint) -> float:
        """Compare two product fingerprints and return similarity score (0-100)"""
        score = 0
        max_score = 0

        def cmp(a, b, weight):
            nonlocal score, max_score
            if a and b:
                max_score += weight
                if a == b:
                    score += weight
        
        # Category
        cmp(f1.category, f2.category, 10)
        
        # Configuration
        cmp(f1.configuration, f2.configuration, 10)

        # Dimensions (within 0.25" tolerance)
        if f1.width and f2.width:
            max_score += 10
            if abs(f1.width - f2.width) < 0.25:
                score += 10

        if f1.height and f2.height:
            max_score += 10
            if abs(f1.height - f2.height) < 0.25:
                score += 10
        
        # Frame material
        cmp(f1.frame, f2.frame, 10)
        
        # Glass layers
        cmp(f1.glass_layers, f2.glass_layers, 10)

        # Low-E
        if f1.low_e == f2.low_e:
            score += 5
        max_score += 5

        # Argon
        if f1.argon == f2.argon:
            score += 5
        max_score += 5

        # Extras (Jaccard similarity)
        extras_union = len(f1.extras | f2.extras)
        if extras_union:
            max_score += 10
            score += 10 * (len(f1.extras & f2.extras) / extras_union)
        
        return (score / max_score) * 100 if max_score else 0

    def match_decko_documents(self, doc1, doc2):
        """Match two DECKO documents using fingerprint comparison"""
        log = []
        log.append("="*60)
        log.append("DECKO FINGERPRINT MATCHING")
        log.append("="*60)
        
        score = 0
        max_score = 100
        
        # Order number matching (50 points)
        log.append(f"\nOrder Numbers:")
        log.append(f"  Doc1: {doc1.order_number}")
        log.append(f"  Doc2: {doc2.order_number}")
        
        if doc1.order_number == doc2.order_number and doc1.order_number != "Unknown":
            score += 50
            log.append("  ✓ EXACT MATCH (+50 points)")
        elif doc1.order_number != "Unknown" and doc2.order_number != "Unknown":
            if doc1.order_number in doc2.order_number or doc2.order_number in doc1.order_number:
                score += 45
                log.append(" ~ PARTIAL MATCH (+45 points)")
            else:
                similarity = self.calculate_similarity(doc1.order_number, doc2.order_number)
                if similarity > 0.7:
                    score += 40
                    log.append(f" ~ SIMILAR ({similarity:.0%} similarity) (+40 points)")
                else:
                    log.append("  ✗ Different order numbers (0 points)")
        else:
            log.append("  ✗ Order number missing in one or both documents.")
    

        # Fingerprint comparison (50 points)
        log.append(f"\n{'='*60}")
        log.append("PRODUCT FINGERPRINT COMPARISON:")
        log.append(f"{'='*60}")
        
        fp1 = doc1.fingerprint
        fp2 = doc2.fingerprint
        
        fingerprint_score = 0
        fingerprint_max = 0
        
        # Category (5 points)
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
        
        # Configuration (10 points)
        log.append(f"\n[CONFIGURATION]")
        log.append(f"  Doc1: {fp1.configuration or 'Not specified'}")
        log.append(f"  Doc2: {fp2.configuration or 'Not specified'}")
        if fp1.configuration and fp2.configuration:
            fingerprint_max += 10
            if fp1.configuration == fp2.configuration:
                fingerprint_score += 10
                log.append(f"  ✓ Match (+10)")
            else:
                log.append(f"  ✗ Different")
        
        # Dimensions (15 points - very important)
        log.append(f"\n[DIMENSIONS]")
        log.append(f"  Doc1: {fp1.width}\" x {fp1.height}\"")
        log.append(f"  Doc2: {fp2.width}\" x {fp2.height}\"")
        if fp1.width and fp2.width and fp1.height and fp2.height:
            fingerprint_max += 15
            width_diff = abs(fp1.width - fp2.width)
            height_diff = abs(fp1.height - fp2.height)
            
            if width_diff < 0.25 and height_diff < 0.25:
                fingerprint_score += 15
                log.append(f"  ✓ Match within tolerance (+15)")
            elif width_diff < 1.0 and height_diff < 1.0:
                fingerprint_score += 10
                log.append(f"  ~ Close match (+10)")
            else:
                log.append(f"  ✗ Different (diff: {width_diff}\" x {height_diff}\")")
        
        # Frame material (5 points)
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
        
        # Glass layers (10 points)
        log.append(f"\n[GLASS CONFIGURATION]")
        log.append(f"  Doc1: {fp1.glass_layers} layers, Low-E: {fp1.low_e}, Argon: {fp1.argon}")
        log.append(f"  Doc2: {fp2.glass_layers} layers, Low-E: {fp2.low_e}, Argon: {fp2.argon}")
        if fp1.glass_layers and fp2.glass_layers:
            fingerprint_max += 10
            if (fp1.glass_layers == fp2.glass_layers and 
                fp1.low_e == fp2.low_e and 
                fp1.argon == fp2.argon):
                fingerprint_score += 10
                log.append(f"  ✓ Full match (+10)")
            elif fp1.glass_layers == fp2.glass_layers:
                fingerprint_score += 5
                log.append(f"  ~ Partial match (+5)")
            else:
                log.append(f"  ✗ Different")
        
        # Colors (5 points)
        log.append(f"\n[COLORS]")
        log.append(f"  Doc1: Interior={fp1.interior_color or 'N/A'}, Exterior={fp1.exterior_color or 'N/A'}")
        log.append(f"  Doc2: Interior={fp2.interior_color or 'N/A'}, Exterior={fp2.exterior_color or 'N/A'}")
        color_match = True
        if fp1.interior_color and fp2.interior_color and fp1.interior_color != fp2.interior_color:
            color_match = False
        if fp1.exterior_color and fp2.exterior_color and fp1.exterior_color != fp2.exterior_color:
            color_match = False
        
        if (fp1.interior_color or fp1.exterior_color) and (fp2.interior_color or fp2.exterior_color):
            fingerprint_max += 5
            if color_match:
                fingerprint_score += 5
                log.append(f"  ✓ Colors match (+5)")
            else:
                log.append(f"  ✗ Different colors")
        
        # Extras (5 points)
        log.append(f"\n[EXTRAS/OPTIONS]")
        log.append(f"  Doc1: {fp1.extras if fp1.extras else 'None'}")
        log.append(f"  Doc2: {fp2.extras if fp2.extras else 'None'}")
        
        if fp1.extras or fp2.extras:
            fingerprint_max += 5
            if fp1.extras and fp2.extras:
                extras_union = len(fp1.extras | fp2.extras)
                extras_intersect = len(fp1.extras & fp2.extras)
                if extras_union > 0:
                    extras_score = 5 * (extras_intersect / extras_union)
                    fingerprint_score += extras_score
                    log.append(f"  ~ Similarity: {extras_intersect}/{extras_union} ({extras_score:.1f} points)")
            else:
                log.append(f"  - Only one document has extras specified")
        
        # Calculate final fingerprint score as percentage of max possible
        if fingerprint_max > 0:
            fp_percentage = (fingerprint_score / fingerprint_max) * 100
            # Add to total score (out of 50 points for fingerprint)
            score += (fp_percentage / 100) * 50
            log.append(f"\nFingerprint Score: {fingerprint_score:.1f}/{fingerprint_max} = {fp_percentage:.1f}%")
            log.append(f"Contributes: {(fp_percentage / 100) * 50:.1f}/50 points to total")
        else:
            log.append(f"\n⚠ Warning: No comparable fingerprint data found")
            log.append(f"Matching based on order number only")
        
        documents_match = score >= 70
        
        log.append("\n" + "="*60)
        log.append(f"FINAL SCORE: {score:.1f}/100")
        log.append(f"Threshold: 70 points")
        log.append(f"Result: {'✓ DOCUMENTS MATCH' if documents_match else '✗ DOCUMENTS DO NOT MATCH'}")
        log.append("="*60)
        
        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        return {
            "match": documents_match,
            "confidence": score,
            "matched_items": 1,
            "total_items": 1,
            "order1": doc1.order_number,
            "order2": doc2.order_number,
            "total1": doc1.total,
            "total2": doc2.total,
            "total_diff": abs(doc1.total - doc2.total)
        }

    def needs_ocr(self, text):
        """Check if OCR is needed - look in full text instead of lines"""
        # Check if we have product codes and prices in the text
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
        """Extract text from PDF using pdfplumber"""
        all_text = ""
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
        
        return all_text


    def contains_prices(self, text):
        """Check if text contains prices - works on full text string"""
        return bool(re.search(r'\$\s*\d+\.\d{2}|\d+\.\d{2}', text))
    
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
        # Extract raw text
        text = self.extract_pdf_text(pdf_path)

        if not text or len(text.strip()) < 50:
            print("DEBUG: pdfplumber returned empty - forcing OCR")
            ocr_lines = self.ocr_pdf(pdf_path)
            text = "\n".join([self.normalize_ocr_line(l) for l in ocr_lines])
        
        # DEBUG: Print first 500 chars to see what we're working with
        print(f"DEBUG: Text preview (first 500 chars):")
        print(text[:500])
        print(f"DEBUG: Contains 'DALMEN': {'DALMEN' in text.upper()}")
        print(f"DEBUG: Contains 'DECKO': {'DECKO' in text.upper()}")
        print(f"DEBUG: Contains 'TAMARACK': {'TAMARACK' in text.upper()}")
        print(f"DEBUG: Contains 'Fournisseur': {'FOURNISSEUR' in text.upper()}")

        provider = self.detect_provider(text)
        print(f"DEBUG: Detected provider: {provider}")

        # Normalize text for price extraction
        normalized_text = self.normalize_price_text(text)

        # Only use OCR if absolutely necessary - check if we can extract meaningful content
        use_ocr = False
        if provider == "DECKO_DALMEN":
            # For DECKO docs, we don't need prices - just check if we have product codes or specs
            has_content = bool(re.search(r'[A-Z]{2,}\s*-?\s*\d+|XO|OX|\d+\s*["\']?\s*[Xx]\s*\d+', text))
            print(f"DEBUG: DECKO doc has content: {has_content}")
            if not has_content:
                use_ocr = True
                print("DEBUG: OCR required for DECKO doc - missing product specs")
        else:
            # For other docs, check for codes and prices
            if self.needs_ocr(normalized_text) or not self.contains_prices(normalized_text):
                use_ocr = True
                print("DEBUG: OCR required: missing prices or product codes...")
        
        if use_ocr:
            ocr_lines = self.ocr_pdf(pdf_path)
            text = "\n".join([self.normalize_ocr_line(l) for l in ocr_lines])
            normalized_text = self.normalize_price_text(text)
 
        header = {}
        fingerprint = None
        if provider == "DECKO_DALMEN":
            header = self.extract_decko_header(text)
            fingerprint = self.extract_decko_fingerprint(text)
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
        doc.raw_text = text  # Store raw text for debugging
        return doc

    
    def normalize_code(self, code: str) -> str:
        """Normalize product code"""
        code = code.upper()
        code = re.sub(r'\(.*?\)', '', code)  # Remove parentheses
        code = re.sub(r'\s+', '', code)  # Remove spaces
        code = re.sub(r'^CL-', '', code)  # Remove CL- prefix
        
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
        
        # If both documents are DECKO_DALMEN format, use fingerprint matching
        if (doc1.provider == "DECKO_DALMEN" and doc2.provider == "DECKO_DALMEN" and
            hasattr(doc1, 'fingerprint') and hasattr(doc2, 'fingerprint') and
            doc1.fingerprint and doc2.fingerprint):
            
            print("Using DECKO fingerprint matching...")
            return self.match_decko_documents(doc1, doc2)
        
        # Otherwise use standard line item matching
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