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

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@dataclass
class LineItem:
    product_code: str
    annexe_pr: str
    description: str
    quantity: int = 1

@dataclass
class OrderDocument:
    order_number: str
    line_items: List[LineItem]
    provider: str = "NOVATECH_WINDOWS"

class DocumentMatcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Novatech Windows Matcher")
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
            f.write("NOVATECH WINDOWS MATCHER - DETAILED LOG\n")
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
        title_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text=" Novatech Windows Matcher",
            font=("Arial", 24, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(expand=True)

        bottom_header = tk.Frame(title_frame, bg=self.primary_color)
        bottom_header.pack(fill=tk.X, padx=20)

        subtitle_label = tk.Label(
            bottom_header,
            text="Match Dalmen window orders with Novatech confirmations",
            font=("Arial", 10),
            bg=self.primary_color,
            fg="white"
        )
        subtitle_label.pack(side=tk.LEFT)

        self.print_btn = tk.Button(
            bottom_header,
            text="Print Log",
            font=("Arial", 9, "bold"),
            bg="#667eea",
            fg="#FFFFFF",
            cursor="hand2",
            command=self.print_log,
            relief=tk.FLAT,
            padx=10,
            pady=5,
            state=tk.DISABLED
        )
        self.print_btn.pack(side=tk.RIGHT)

        self.log_btn = tk.Button(
            bottom_header,
            text="Log",
            font=("Arial", 9, "bold"),
            bg="#667eea",
            fg="#FFFFFF",
            cursor="hand2",
            command=self.show_log_window,
            relief=tk.FLAT,
            padx=10,
            pady=5,
            state=tk.DISABLED
        )
        self.log_btn.pack(side=tk.RIGHT, padx=(0, 5))

        content_frame = tk.Frame(self.root, bg=self.bg_color, padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Document 1 - Dalmen Order
        doc1_frame = tk.LabelFrame(
            content_frame,
            text="Dalmen Window Order",
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
            activebackground="#69abd6",
            activeforeground="white",
            cursor="hand2",
            command=lambda: self.browse_file(1),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        btn1.pack()

        # Document 2 - Novatech Confirmation
        doc2_frame = tk.LabelFrame(
            content_frame,
            text="Novatech Confirmation",
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
            activebackground="#5490b8",
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
            activebackground="#667eea",
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

    def browse_file(self, file_num):
        filename = filedialog.askopenfilename(
            title=f"Select Document {file_num}",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        if filename:
            if file_num == 1:
                self.file1_path = filename
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
        return text
    
    def extract_order_number(self, text: str, doc_type: str) -> str:
        if doc_type == "DALMEN":
            # "Numéro de PO.:V-003265"
            match = re.search(r'Num[ée]ro\s+de\s+PO\.:?\s*(V-\d+)', text, re.IGNORECASE)
            if match:
                return match.group(1)
        else:  # NOVATECH
            # "#BC client V-003265" or just "V-003265"
            match = re.search(r'(V-\d+)', text)
            if match:
                return match.group(1)
        
        return "Unknown"
    
    def parse_glaze_dalmen_order(self, text: str, target_po: str) -> List[LineItem]:
        items = []
        lines = text.split('\n')

        print(f"\nDEBUG: Parsing Dalmen order...")

        for i, line in enumerate(lines):
            line = line.strip()

            match1 = re.match(r'^([\d\-]+)\s+(\d+)\s+([\d\-]+)\s+(.+)$', line)
            if match1:
                product_code = match1.group(1).strip()
                quantity = int(match1.group(2))
                annexe_pr = match1.group(3).strip()
                description = match1.group(4).strip()
                desc_clean = re.sub(r'^[\d\-]+\s*-\s*', '', description)

                print(f" Found item: {product_code} | Annexe: {annexe_pr} | DESC: {desc_clean[:50]}")

                items.append(LineItem(
                    product_code=product_code,
                    annexe_pr=annexe_pr,
                    description=desc_clean,
                    quantity=quantity
                ))
                continue

            match2 = re.match(r'^([\d\-]+)\s+(\d+)\s+([\d\-]+)$', line)
            if match2:
                product_code = match2.group(1).strip()
                quantity = int(match2.group(2))
                annexe_pr = match2.group(3).strip()

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
        
    
    def parse_glaze_novatech_confirmation(self, text: str, target_po: str) -> List[LineItem]:
        """Parse Novatech confirmation (handles multi-page)"""
        items = []
        lines = text.split('\n')
        
        print(f"\nDEBUG: Parsing Novatech confirmation...")


        for i, line in enumerate(lines):
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
            match = re.match(r'^([\d\-]+)\s+(\d+)\s+([\d\-]+)\s+(.+)$', line)

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
        lines = text.split('\n')

        print(f"\nDEBUG: Parsing Novatech SLAB confirmation... (Filtering for PO: {target_po})")

        for i, line in enumerate(lines):
            line = line.strip()

            if target_po not in line:
                continue

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
                    description = description,
                    quantity=1
                ))

        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return items
    

    def parse_document(self, pdf_path: str, doc_type: str = None) -> OrderDocument:
        
        text = self.extract_pdf_text(pdf_path)

        print(f"\nDEBUG: Text preview (first 500 chars):\n{text[:500]}\n")

        if not doc_type:
            if "Commande de vitraux" in text or "Fournisseur :" in text:
                doc_type = "DALMEN"
            elif "Confirmation de Commande" in text and "GROUPE NOVATECH" in text:
                doc_type = "NOVATECH"
            else:
                doc_type = "UNKNOWN"

        print(f"DEBUG: Detected document type: {doc_type}")

        is_slab = False
        if "Coupe-FEU" in text or "COUPE FEU" in text or "N600" in text:
            is_slab = True
            print("DEBUG: Document detected as SLAB")
        else:
            print("DEBUG: Document detected as GLAZING")

        order_number = self.extract_order_number(text, doc_type)
        print(f"DEBUG: Extracted order number: {order_number}")

        if doc_type == "DALMEN":
            if is_slab:
                line_items = self.parse_slab_dalmen_order(text, order_number)
            else:
                line_items = self.parse_glaze_dalmen_order(text, order_number)
        elif doc_type == "NOVATECH":
            if is_slab:
                line_items = self.parse_slab_novatech_confirmation(text, order_number)
            else:
                line_items = self.parse_glaze_novatech_confirmation(text, order_number)
        else:
            line_items = []

        return OrderDocument(
            order_number=order_number,
            line_items=line_items,
            provider="NOVATECH_WINDOWS"
        )
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def match_documents(self, doc1: OrderDocument, doc2: OrderDocument) -> Dict:
        log = []
        log.append("="*60)
        log.append("NOVATECH WINDOWS ORDER MATCHING")
        log.append("="*60)
        
        log.append(f"\n[\nORDER NUMBERS]")
        log.append(f" Doc1: {doc1.order_number}")
        log.append(f" Doc2: {doc2.order_number}")
        
        order_match = doc1.order_number == doc2.order_number
        if order_match:
            log.append(" ✅ Order numbers match")
        else:
            log.append(" ❌ Order numbers do NOT match")

        # Get all the unique Annexe bases from first document
        doc1_bases = set()
        for item in doc1.line_items:
            if item.annexe_pr and len(item.annexe_pr.split('-')) >= 2:
                # Extract base: "382-01135-04-1" -> "382-01135"
                base = '-'.join(item.annexe_pr.split('-')[:2])
                doc1_bases.add(base)

        # Get all the unique Annexe bases from second document
        doc2_bases = set()
        for item in doc2.line_items:
            if item.annexe_pr and len(item.annexe_pr.split('-')) >= 2:
                # Extract base: "382-01135-04-1" -> "382-01135"
                base = '-'.join(item.annexe_pr.split('-')[:2])
                doc2_bases.add(base)

        common_bases = doc1_bases & doc2_bases

        if not common_bases:
            log.append("\n⚠️ No common Annexe PR bases found between both documents.")
        else:
            log.append(f"\nCommon Annexe bases: {common_bases}")

        doc1_filtered = [item for item in doc1.line_items
                         if item.annexe_pr and '-'.join(item.annexe_pr.split('-')[:2]) in common_bases]
        doc2_filtered = [item for item in doc2.line_items
                         if item.annexe_pr and '-'.join(item.annexe_pr.split('-')[:2]) in common_bases]
        
        log.append(f"Filtered Doc1: {len(doc1.line_items)} → {len(doc1_filtered)} items")
        log.append(f"Filtered Doc2: {len(doc2.line_items)} → {len(doc2_filtered)} items\n")

        doc1.line_items = doc1_filtered
        doc2.line_items = doc2_filtered
        
        log.append(f"{'='*60}\n")
        log.append(f"DOC1 LINE ITEMS:")
        log.append(f"{'='*60}")
        for item in doc1.line_items:
            log.append(f" {item.product_code} | Annexe: {item.annexe_pr}")
            log.append(F" {item.description[:80]}")

        log.append(f"\n{'='*60}")
        log.append(f" DOC2 LINE ITEMS:")
        log.append(f"{'='*60}")
        for item in doc2.line_items:
            log.append(f" {item.product_code} | Annexe: {item.annexe_pr}")
            log.append(F" {item.description[:80]}")

        log.append(f"\n{'='*60}")
        log.append(f"MATCHING RESULTS:")
        log.append(f"\n{'='*60}")

        matched = 0
        total_items = max(len(doc1.line_items), len(doc2.line_items)) 

        for item1 in doc1.line_items:
            best_score = 0
            best_match = None

            for item2 in doc2.line_items:
                score = 0

                if item1.annexe_pr and item2.annexe_pr:
                    if item1.annexe_pr == item2.annexe_pr:
                        score += 50

                code_sim = self.calculate_similarity(item1.product_code, item2.product_code)
                if code_sim > 0.8:
                    score += 30

                desc_sim = self.calculate_similarity(item1.description, item2.description)
                if desc_sim > 0.6:
                    score += 20

                if score > best_score:
                    best_score = score
                    best_match = item2
            
            log.append(f"\n{item1.product_code} | Annexe: {item1.annexe_pr}")
            log.append(f" Description: {item1.description[:60]}")

            if best_match:
                log.append(f" → Best match: {best_match.product_code} | Annexe: {best_match.annexe_pr}")
                log.append(f"    Similarity Score: {best_score}/100")

                if best_score >= 50:
                    log.append("    ✅ MATCH")
                    matched += 1
                else:
                    log.append(" SCORE TOO LOW - NO MATCH")
            else:
                log.append("    ❌ NO MATCH ")

        match_percentage = (matched / total_items * 100) if total_items > 0 else 0
        documents_match = match_percentage >= 70 and order_match

        log.append(f"\n{'='*60}")
        log.append(f"FINAL RESULT: {matched}/{total_items} items matched ({match_percentage:.1f}%)")
        log.append(f"Order numbers: {'MATCH' if order_match else 'NO MATCH'}")
        log.append(f"Documents Match: {documents_match}")
        log.append(f"{'='*60}")

        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        return {
            "match": documents_match,
            "confidence": match_percentage,
            "matched_items": matched,
            "total_items": total_items,
            "order1": doc1.order_number,
            "order2": doc2.order_number
        }
        
    def display_result(self, result):
        self.progress.stop()
        self.progress.pack_forget()
        self.compare_btn.config(state=tk.NORMAL)
        self.log_btn.config(state=tk.NORMAL, bg=self.primary_color)
        self.print_btn.config(state=tk.NORMAL, bg=self.primary_color)

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if result['match']:
            bg_color = self.success_color
            icon = "✅"
            title = "DOCUMENTS MATCH"
            message = "Window order confirmed!"
        else:
            bg_color = self.error_color
            icon = "❌"
            title = "DOCUMENTS DO NOT MATCH"
            message = "There are discrepancies in the order."

        result_card = tk.Frame(self.result_frame, bg=bg_color, padx=20, pady=20)
        result_card.pack(fill=tk.BOTH, expand=True)

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
        
        details_frame = tk.Frame(result_card, bg="white", padx=15, pady=15)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        details = [
            ("Order Numbers:", f"{result['order1']} ↔ {result['order2']}"),
            ("Confidence:", f"{result['confidence']:.1f}%"),
            ("Matched Items:", f"{result['matched_items']} / {result['total_items']}"),
        ]

        for label, value in details:
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
        self.progress.stop()
        self.progress.pack_forget()
        self.compare_btn.config(state=tk.DISABLED)

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
