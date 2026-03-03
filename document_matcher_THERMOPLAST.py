"""
AI Document Matcher - GUI Version
Upload any 2 PDFs and check if they match
THERMOPLAST - 2-Way Matching for Thermoplastics
TO BE MATCHED: ITEM CODE, QUANTITY, PO NUMBER
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import pdfplumber
import re
from typing import Dict, List
from dataclasses import dataclass
from difflib import SequenceMatcher
import threading
import os


@dataclass
class LineItem:
    item_code: str
    quantity: float = 0.0

@dataclass
class OrderDocument:
    po_number: str
    line_items: List[LineItem]
    total: float = 0.0
class DocumentMatcherGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("THERMOPLAST - 2-Way Document Matcher")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Colours
        self.bg_color = "#f0f0f0"
        self.primary_color = "#1e3a8a"
        self.success_color = "#4caf50"
        self.error_color = "#f44336"

        self.root.configure(bg=self.bg_color)
        
        self.file1_path = None
        self.file2_path = None
        self.match_log = ""
        
        self.create_widgets()

    def extract_pdf_text(self, pdf_path: str) -> str:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
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

            # ADD DEBUG: Show lines that might be products
            if re.search(r'^[A-Z]\d', line):  # Starts with letter then digit
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
                # Line looks like a product but didn't match
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
                
                # Extract base code (before underscore)
                item_code = full_code.split('_')[0]
                
                try:
                    quantity = float(quantity_str)
                except:
                    quantity = 0.0
                
                print(f"  Found: {item_code} | Qty: {quantity}")
                items.append(LineItem(item_code=item_code, quantity=quantity))
        
        print(f"DEBUG: Total items: {len(items)}\n")
        
        return OrderDocument(
            po_number=po_number,
            line_items=items,
            total=0.0
            )

            
    
    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="Thermoplast Order Matcher",
            font=("Arial", 24, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(expand=True)

        bottom_header = tk.Frame(title_frame, bg=self.primary_color)
        bottom_header.pack(fill=tk.X, padx=20)
        
        subtitle_label = tk.Label(
            bottom_header,
            text="MATCH DALMEN - THERMOPLAST ORDERS",
            font=("Arial", 10),
            bg=self.primary_color,
            fg="white"
        )
        subtitle_label.pack(side=tk.LEFT)
        
        self.log_btn = tk.Button(
            bottom_header,
            text="View Log",
            font=("Arial", 9, "bold"),
            bg="#0c2454",
            fg="white",
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
        """Browse for a PDF file"""
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
        """Run the actual comparison"""
        try:
            print("Starting comparison...")
            print(f"File 1: {self.file1_path}")
            print(f"File 2: {self.file2_path}")
            
            text1 = self.extract_pdf_text(self.file1_path)
            doc1 = self.parse_dalmen_order(text1)
            print(f"Doc1 parsed: {len(doc1.line_items)} items")
            
            text2 = self.extract_pdf_text(self.file2_path)

            if 'CONFIRMATION' in text2.upper() or 'ENTRY' in text2.upper():
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

    def display_result(self, result):
        """Display the comparison result"""
        self.progress.stop()
        self.progress.pack_forget()
        self.compare_btn.config(state=tk.NORMAL)
        self.log_btn.config(state=tk.NORMAL)
        
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        if result['match']:
            bg_color = self.success_color
            icon = "✅"
            title = "DOCUMENTS MATCH"
            message = "Orders are consistent!"
        else:
            bg_color = self.error_color
            icon = "❌"
            title = "DOCUMENTS DO NOT MATCH"
            message = "Discrepancies found."
        
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
            ("PO Numbers:", f"{result['po1']} ↔ {result['po2']}"),
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
        """Display error message"""
        self.progress.stop()
        self.progress.pack_forget()
        self.compare_btn.config(state=tk.NORMAL)
        
        messagebox.showerror(
            "Error",
            f"Failed to process documents:\n\n{error_msg}"
        )

    def show_log_window(self):
        """Show detailed log in popup window"""
        log_window = tk.Toplevel(self.root)
        log_window.title("Detailed Log")
        log_window.geometry("800x600")
        
        header = tk.Frame(log_window, bg=self.primary_color, padx=10, pady=10)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="Detailed Matching Log",
            font=("Arial", 16, "bold"),
            bg=self.primary_color,
            fg="white"
        ).pack()
        
        text_area = scrolledtext.ScrolledText(
            log_window,
            font=("Courier", 9),
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

    def calculate_similarity(self, str1: str, str2: str) -> float:
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def match_documents(self, doc1: OrderDocument, doc2: OrderDocument) -> Dict:
        log = []
        log.append("="*60)
        log.append("DALMEN MATCHER RESULTS")
        log.append("="*60)

        if len(doc1.line_items) == 0 or len(doc2.line_items) == 0:
            log.append("\n ERROR: One or both documents have no items!")
            log.append(f"Doc1 items: {len(doc1.line_items)}")
            log.append(f"Doc2 items: {len(doc2.line_items)}")

        log.append(f"\n[PO NUMBERS]")
        log.append(f" Doc1: {doc1.po_number}")
        log.append(f" Doc2: {doc2.po_number}")

        po_match = doc1.po_number == doc2.po_number
        if po_match:
            log.append(" PO NUMBER MATCH: YES")
        else:
            log.append(" PO NUMBER MATCH: NO")

        log.append(f"\n{'='*60}")
        log.append("DOC1 ITEMS:")
        log.append(f"{'='*60}")
        for item in doc1.line_items:
            log.append(f" {item.item_code} | Qty: {item.quantity}")

        log.append(f"\n{'='*60}")
        log.append("DOC2 ITEMS:")
        log.append(f"{'='*60}")
        for item in doc2.line_items:
            log.append(f" {item.item_code} | Qty: {item.quantity}")
        
        log.append(f"\n{'='*60}")
        log.append("MATCHING PROCESS:")
        log.append(f"{'='*60}")

        matched = 0
        total_items = max(len(doc1.line_items), len(doc2.line_items))

        for item1 in doc1.line_items:
            best_match = None
            best_score = 0

            for item2 in doc2.line_items:
                score = 0

                if item1.item_code == item2.item_code:
                    score += 60
                else:
                    code_sim = self.calculate_similarity(item1.item_code, item2.item_code)
                    if code_sim > 0.8:
                        score += 30 

                if item1.quantity > 0 and  item2.quantity > 0:
                    if abs(item1.quantity - item2.quantity) < 1:
                        score += 10

                if score > best_score:
                    best_score = score
                    best_match = item2
            
            log.append(f"\n{item1.item_code} | Qty: {item1.quantity}")

            if best_match:
                log.append(f"  Best Match: {best_match.item_code} | Qty: {best_match.quantity}")

                if best_match:
                    log.append(f"  → Best match: {best_match.item_code}")
                    log.append(f"     Score: {best_score}/80")
                    
                    if best_score >= 50:
                        log.append("  ✅ MATCHED")
                        matched += 1
                    else:
                        log.append("  ❌ Score too low")
                else:
                    log.append("  ❌ No match found")

        match_percentage = (matched / total_items * 100) if total_items > 0 else 0
        documents_match = match_percentage >= 70 and po_match

        log.append("\n" + "="*60)
        log.append(f"FINAL RESULT: {matched}/{total_items} items matched ({match_percentage:.1f}%)")
        log.append(f"PO numbers: {'MATCH' if po_match else 'NO MATCH'}")
        log.append(f"Documents match: {documents_match}")
        log.append("="*60)

        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        return {
            "match": documents_match,
            "confidence": match_percentage,
            "matched_items": matched,
            "total_items": total_items,
            "po1": doc1.po_number,
            "po2": doc2.po_number,
        }

  
def main():
    root = tk.Tk()
    app = DocumentMatcherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


    