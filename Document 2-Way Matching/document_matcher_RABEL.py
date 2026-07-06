"""
AI Document Matcher - GUI Version
Upload any 2 PDFs and check if they match
RABEL - 2-Way Matching for RABEL Provider

*UNFINISHED* --> Waiting on more examples to text
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import pdfplumber
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from difflib import SequenceMatcher
import threading
import os
import sys
import pytesseract


def get_tesseract_path():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
        bundled = os.path.join(base, '_internal', 'tesseract', 'tesseract.exe')
        if os.path.exists(bundled):
            os.eviron['TESSDATA_PREFIX'] = os.path.join(base, '_internal', 'tessdata')
            return bundled
    
    return r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

@dataclass
class LineItem:
    product_code : str
    description : str
    quantity : float = 0.0
    unit_price : float = 0.0
    total : float = 0.0
    raw_code : str = ""

class OrderDocument:
    order_number : str
    line_items : List[LineItem] = field(default_factory=list)
    doc_type : str = "UNKNOWN"
    total : float = 0.0

class DocumentMatcherGUI:
    BG      = "#f4f5f7"   
    SURFACE = "#ffffff"   
    PRIMARY = "#1b2a4a"  
    ACCENT  = "#e8601c"  
    SUCCESS = "#2e7d32"   
    ERROR   = "#c62828"   
    MUTED   = "#6b7280"   
    BORDER  = "#dde1e7"   


    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("RABEL Matcher")
        self.root.geometry("840x700")   
        self.root.resizable(False, False) 
        self.root.configure(bg=self.BG)
 
        self.file1_path: Optional[str] = None   
        self.file2_path: Optional[str] = None   
        self.match_log: str = ""                

        self._build_ui()


    def _build_ui(self):
        bar = tk.Frame(self.root, bg=self.PRIMARY, height=64)
        bar.pack(fill=tk.X)          
        bar.pack_propagate(False)

        tk.Label(bar, text="RABEL", font=("Courier New", 20, "bold"),
            bg=self.PRIMARY, fg=self.ACCENT).pack(side=tk.LEFT, padx=22, pady=16)
 
        tk.Label(bar, text="Document Matcher",
            font=("Segoe UI", 11), bg=self.PRIMARY, fg="#9ba8be"
            ).pack(side=tk.LEFT, pady=16)
        self.log_btn = tk.Button(
            bar, text="📋  View Log", font=("Segoe UI", 9, "bold"),
            bg="#2e3f60", fg="white", cursor="hand2",
            relief=tk.FLAT, padx=14, pady=8,
            state=tk.DISABLED, command=self._show_log)
        self.log_btn.pack(side=tk.RIGHT, padx=16, pady=14)
 
        body = tk.Frame(self.root, bg=self.BG, padx=26, pady=22)
        body.pack(fill=tk.BOTH, expand=True)

        cards = tk.Frame(body, bg=self.BG)
        cards.pack(fill=tk.X)

        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)
 
        self.lbl1 = self._upload_card(cards, 0, "DOC 1", "Dalmen Purchase Order", 1)
        self.lbl2 = self._upload_card(cards, 1, "DOC 2", "Rabel Confirmation de Commande", 2)
 
        self.match_btn = tk.Button(
            body, text="⚡  Compare Documents",
            font=("Segoe UI", 12, "bold"),
            bg=self.PRIMARY, fg="white",
            activebackground=self.ACCENT, activeforeground="white",
                                              
            cursor="hand2",           
            relief=tk.FLAT,               
            padx=24, pady=14,
            state=tk.DISABLED,           
            command=self._run)            
        self.match_btn.pack(fill=tk.X, pady=(18, 0))
 
        style = ttk.Style()
        style.theme_use("default")
        style.configure("R.Horizontal.TProgressbar",
                        troughcolor=self.BORDER,
                        background=self.ACCENT, thickness=5)
        self.progress = ttk.Progressbar(body, mode="indeterminate",
                                        style="R.Horizontal.TProgressbar")

        self.result_frame = tk.Frame(body, bg=self.BG)
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=(18, 0))
 
 
    def _upload_card(self, parent, col, title, subtitle, file_num) -> tk.Label:
        card = tk.Frame(parent, bg=self.SURFACE, bd=1, relief=tk.SOLID)
        card.grid(row=0, column=col,
                  padx=(0, 10) if col == 0 else (10, 0),
                  sticky="nsew",              # stretch in all directions to fill cell
                  pady=(0, 16))
 

        tk.Frame(card, bg=self.ACCENT, height=3).pack(fill=tk.X)
 
        inner = tk.Frame(card, bg=self.SURFACE, padx=18, pady=16)
        inner.pack(fill=tk.BOTH, expand=True)
 
        tk.Label(inner, text=title, font=("Segoe UI", 9, "bold"),
                 bg=self.SURFACE, fg=self.PRIMARY).pack(anchor="w")
 
        tk.Label(inner, text=subtitle, font=("Segoe UI", 8),
                 bg=self.SURFACE, fg=self.MUTED).pack(anchor="w", pady=(2, 10))
 
        lbl = tk.Label(inner, text="No file selected",
                       font=("Segoe UI", 9), bg=self.SURFACE, fg="#aaa",
                       anchor="w", wraplength=270, justify="left")
        lbl.pack(fill=tk.X, pady=(0, 12))

        tk.Button(inner, text="📁  Browse PDF",
                  font=("Segoe UI", 10, "bold"),
                  bg=self.PRIMARY, fg="white",
                  activebackground=self.ACCENT, activeforeground="white",
                  cursor="hand2", relief=tk.FLAT, padx=14, pady=9,
                  command=lambda n=file_num: self._browse(n)).pack(fill=tk.X)
        return lbl

    def _browse(self, file_num: int):
        path = filedialog.askopenfilename(filetypes=[("PDF files," "*.pdf"), ("All files", "*.*")])
        if not path:
            return

        name = path.replace("\\", "/").split("/")[-1]

        if file_num == 1:
            self.file1_path = path
            self.lbl1.config(text=f"✓ {name}", fg=self.SUCCESS)
        else:
            self.file2_path = path
            self.lbl2.config(text=f"✓ {name}", fg=self.SUCCESS)

        if self.file1_path and self.file2_path:
            self.match_btn.config(state=tk.NORMAL)

    
    def _run(self):
        for w in self.resukt_frame.winfo_children():
            w.destroy()

        self.progress.pack(fill=tk.X, pady=(8, 0))
        self.progress.start(10)
        self.match_btn.config(state=tk.DISABLED)

        threading.Thread(target=self._do_match, daemon=True).start()

    
    def _do_match(self):
        try:
            doc1 = self.parse_document(self.file1_path)
            doc2 = self.parse_document(self.file2_path)
            result = self.match_documents(doc1, doc2)
            self.root.after(0, self._display_result, result)
        except Exception:
            import traceback
            tb = traceback.format_exc()
            print(tb)
            self.root.after(0, self._display_error, tb)

    
    def extract_pdf_text(self, pdf_path: str) -> str:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"

        # backup
        if len(text.strip()) > 100:
            print("DEBUG: PDF appears image-based - running OCR...")
            text = self._ocr_pdf(pdf_path)

        return text


    def _ocr_pdf(self, pdf_path: str) -> str:
        from pdf2image import convert_from_path
        poppler_path = r'C:\poppler\Library\bin'
        text = ""
        images = convert_from_path(pdf_path, dpi=400, poppler_path=poppler_path)
        for i, img in enumerate(images):
            print(f"DEBUG: OCR page {i+1}/{len(images)}...")
            text += pytesseract.image_to_string(img, config='--psm 1') + "\n"
        return text


    def parse_document(self, pdf_path: str) -> str:
        text = self.extract_pdf_text(pdf_path)
        upper = text.upper()

        print(f"\nDEBUG: Text preview:\n{text[:400]}\n")

        if "CONFIRMATION DE COMMANDE" in upper and ("RABEL" in upper or "QUINCAILLERIE" in upper):
            doc_type = "RABEL_CONF"
        elif "PURCHASE ORDER" in upper and "RABEL" in upper:
            doc_type = "DALMEN_PO"
        elif "RAPPORT DE COMMANDE" in upper or "NUMÉRO DE PO" in upper or "NUMERO DE PO" in upper:
            doc_type = "DALMEN_RAPPORT"
        elif "PURCHASE ORDER" in upper and "DALMEN" in upper:
            doc_type = "DALMEN_PO"
        else:
            doc_type = "DALMEN_RAPPORT"

        print(f"DEBUG: Detected type: {doc_type}")

        if doc_type == "DALMEN_RAPPORT":
            return self._parse_dalmen_rapport(text)
        if doc_type == "DALMEN_PO":
            return self._parse_dalmen_po(text)
        else:
            return self._parse_rabel_confirmation(text)

        
    def _parse_dalmen_rapport(self, text: str) -> OrderDocument:
        print("DEBUG: Parsing Dalmen Rapport de commande...")
        po = self._extract_po_number_rapport(text)
        print(f"DEBUG: PO number = {po}")

        items = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()

            m = re.match(r'^([A-Z0-9]{2,}[\-][A-Z0-9\-]+)\s+(.+?)\s+(\d+)\s+/\s*\w+\s+([\d\s,\.]+)\s*\$\s+([\d\s,\.]+)\s*\$$', line, re.IGNORECASE)
            if m:
                raw_code = m.group(1).strip()
                description = m.group(2).strip()
                quantity = float(m.group(3))

                unit_price = float(m.group(4).replace(' ', '').replace(',', '.'))
                total = float(m.group(5).replace(' ','').replace(',', '.'))
                norm_code = self._normalize_code(raw_code)

                print(f" Found: {raw_code} (norm: {norm_code}) | Qty: {quantity} | Total: ${total}")
                items.append(LineItem(
                    product_code=norm_code,
                    description=description,
                    quantity=quantity,
                    unit_price=unit_price,
                    total=total,
                    raw_code=raw_code
                ))

        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return OrderDocument(order_number=po, line_items=items, doc_type="DALMEN_RAPPORT")


    def _extract_po_number_rapport(self, text: str) -> str:
        patterns = [
             r'Num[eé]ro\s+de\s+PO\s*\n?\s*(\d+)',
             r'Num[eé]ro\s+de\s+PO[^\d]*(\d+)',
        ]

        for p in patterns:
            m = re.search(p, text, re.IGNORECASE)
            if m:
                return m.group(1).strip()
        return "Unknown"


    def _parse_dalmen_po(self, text: str) -> OrderDocument:
        print("DEBUG: Parsing Dalmen Purchase Order (English)...")

        po = "Unknown"
        m = re.search(r'PO\s*#\s*(?:PO[-\s])?(\d+)', text, re.IGNORECASE)
        if m:
            po = m.group(1).strip()
        print(f"DEBUG: PO number = {po}")

        items = []
        lines = text.split('\n')
        in_table = False # serves as a detector to tell if the table header has been passed or not

        for line in lines:
            line = line.strip()
            # start capturing if this is caught
            if 'PART #' in line.upper() and 'DESCRIPTION' in line.upper():
                in_table = True
                continue

            if not in_table or not line:
                continue

            if any(kw in line.upper() for kw in ['TOTAL QUANTITY', 'AUTHORIZED', 'GENERATED']):
                break # stop when footer is met/exits loop

            m = re.match(r'^\d+\s+([A-Z0-9][\w\-]+)\s+(.+?)\s+(\d+)\s*$', line, re.IGNORECASE)
            if m:
                raw_code = m.group(1).strip()
                description = m.group(2).strip()
                quantity = float(m.group(3))
                norm_code = self._normalize_code(raw_code)

                print(f"  Found: {raw_code} (norm: {norm_code}) | Qty: {quantity}")
                items.append(LineItem(
                    product_code=norm_code,
                    description=description,
                    quantity=quantity,
                    raw_code=raw_code
                ))
 
        print(f"DEBUG: Total items extracted: {len(items)}\n")
        return OrderDocument(order_number=po, line_items=items, doc_type="DALMEN_PO")
 
 
    def _parse_rabel_confirmation(self, text: str) -> OrderDocument:
        po = "Unknown"
        m = re.search(r'P\.O\.\s*No\.?\s*[\n\r\s]+(\d+)', text, re.IGNORECASE)
        if not m:
            m = re.search(r'P\.O\.\s*No\.?\s*[:\s]+(\d+)', text, re.IGNORECASE)
        if m:
            po - m.group(1).strip()
        print(f"DEBUG: PO number = {po}")

        items = []
        lines = text.split('\n')
        in_table = False

        for line in lines:
            line = line.strip()

            if 'CODE DE PRODUIT' in line.upper():
                in_table = True
                continue

            if not in_table or not line:
                continue

            if 'SOUS-TOTAL' in line.upper() or line.upper().startswith('TOTAL'):
                break

            if any (kw in line.upper() for kw in ['TRANSPORT', 'TAXE', 'TAX']):
                continue

            m = re.match(r'^([A-Z0-9][\w\-]+)\s+(.+?)\s+([\d,\.]+)\s+\w+\s+([\d,\.]+)\s+[\d,\.]*\s+([\d,\.]+)\s+([\d,\.]+)\s*$', line, re.IGNORECASE)

            if m:
                raw_code = m.group(1).strip()
                description = m.group(2).strip()
                qty_bte = float(m.group(4)).replace(',', '')
                unit_price = float(m.group(5).replace(',', ''))
                total = float(m.group(6).replace(',', ''))
                norm_code = self._normalize_code(raw_code)

                print(f" Found: {raw_code} (norm: {norm_code}) | Q/Bte: {qty_bte} | Total: ${total}")
                items.append(LineItem(
                    product_code=norm_code,
                    description=description,
                    quantity=qty_bte,
                    unit_price=unit_price,
                    total=total,
                    raw_code=raw_code

                ))

            print(f"DEBUG: Total items extracted: {len(items)}\n")
            return OrderDocument(order_number=po, line_items=items, doc_type="RABEL_CONF")


    # to validate a code match in any format
    def _normalize_code(self, code: str) -> str:
        code = code.upper().strip()
        code = re.sub(r'\s+', '', code)
        code = re.sub(r'-{2,}', '-', code)
        return code

    # returns true if codes match
    def _codes_match(self, c1: str, c2: str) -> bool:
        n1 = self._normalize_code(c1)
        n2 = self._normalize_code(c2)
        return n1 == n2 or n1.startswith(n2) or n2.startswith(n1)

    
    def match_documents(self, doc1: OrderDocument, doc2: OrderDocument) -> Dict:
        log = []
        order_match = doc1.order_number == doc2.order_number

        log.append("=" * 60)
        log.append("SUMMARY")
        log.append("=" * 60)

        col_width = 36
        log.append((
            f"{'Doc1 (' + doc1.doc_type + ') - ' + str(len(doc1.line_items)) + ' items':<{col_width}}"
            f"{'Doc2 (' + doc2.doc_type + ') - ' + str(len(doc2.line_items)) + ' items':<{col_width}}"))
        
        log.append("-" * 60)

        for i in range(max(len(doc1.line_items), len(doc2.line_items))):
            left = f" {doc1.line_items[i].product_code} | Qty: {doc1.line_items[i].quantity}" if i < len(doc1.line_items) else ""
            right = f" {doc2.line_items[i].product_code} | Qty: {doc2.line_items[i].quantity}" if i < len(doc2.line_items) else ""
            log.append(f"{left:<{col_width}} {right}")

        log.append("")
        po_str = "✅ MATCH" if order_match else "❌ NO MATCH"
        log.append(f" Order Numbers - Doc1: {doc1.order_number} | Doc2: {doc2.order_number} -> {po_str}")

        log.append("")
        log.append("=" * 60)
        log.append("MATCHING PROCESS")
        log.append("=" * 60)

        matched = 0
        total_items = len(doc1.line_items)

        for item1 in doc1.line_items:
            best_match = None
        
        for item2 in doc2.line_items:
            if self._codes_match(item1.product_code, item2.product_code):
                best_match = item2
                break

            log.append("")
            if best_match:
                matched += 1
                log.append(f" {item1.product_code:<22} -> {best_match.product_code:<22} ✅ MATCH")
                log.append(f" PO qty: {item1.quantity} | Confirmed Q/Bte: {best_match.total:.2f}")
            else:
                log.append(f" {item1.product_code:<22} -> ❌ NOT FOUND in confirmation")

        match_pct = (matched / total_items * 100) if total_items > 0 else 0
        documents_match = match_pct >= 70 and order_match

        log.append("")
        log.append("=" * 60)
        log.append("FINAL RESULT")
        log.append("=" * 60)
        log.append(f" {matched}/{total_items} items matched ({match_pct:.1f}%)")

        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        return{
            "match": documents_match,
            "confidence": match_pct,
            "matched_items": matched,
            "total_items":   total_items,
            "order1":        doc1.order_number,
            "order2":        doc2.order_number,
            "order_match":   order_match,
            "is_confirmation": True,
        }

    
    def _display_results(self, result: dict):
        self.progress.stop()
        self.progress.pack_forget()
        self.match_btn.config(state=tk.NORMAL)
        self.log_btn.config(state=tk.NORMAL)

        for w in self.result_frame.winfo_children():
            w.destroy()

        is_match = result["match"]
        accent = self.SUCCESS if is_match else self.ERROR

        card = tk.Frame(self.result_frame, bg=self.SURFACE, bd=1, relief=tk.SOLID)
        card.pack(fill=tk.X)
        tk.Frame(card, bg=accent, height=4).pack(fill=tk.X)
 
        inner = tk.Frame(card, bg=self.SURFACE, padx=24, pady=18)
        inner.pack(fill=tk.BOTH, expand=True)
 
        top = tk.Frame(inner, bg=self.SURFACE)
        top.pack(fill=tk.X)
 
        icon    = "✅" if is_match else "❌"
        verdict = "DOCUMENTS MATCH" if is_match else "DOCUMENTS DO NOT MATCH"
        tk.Label(top, text=icon, font=("Arial", 26), bg=self.SURFACE).pack(side=tk.LEFT)
        tk.Label(top, text=verdict, font=("Courier New", 14, "bold"),
                 bg=self.SURFACE, fg=accent).pack(side=tk.LEFT, padx=12)
        tk.Label(top, text=f"{result['confidence']:.0f}% confidence",
                 font=("Segoe UI", 10), bg=self.SURFACE, fg=self.MUTED).pack(side=tk.RIGHT)
 
        tk.Frame(inner, bg=self.BORDER, height=1).pack(fill=tk.X, pady=(14, 14))
 
        stats = tk.Frame(inner, bg=self.SURFACE)
        stats.pack(fill=tk.X, pady=(0, 14))
 
        o_icon = "✅" if result.get("order_match") else "❌"

        def statbox(label, value, col):
            box = tk.Frame(stats, bg='#f8f9fb', padx=14, pady=10, bd=1, relief=tk.SOLID)
            box.grid(row=0, column=col, padx=(0 if col == 0 else 6, 0), sticky="ew")
            stats.columnconfigure(col, weight=1)
            tk.Label(box, text=value, font=("Courier New", 13, "bold"),
                    bg="#f8f9fb", fg=self.PRIMARY).pack()
            tk.Label(box, text=label, font=("Segoe UI", 8),
                    bg="#f8f9fb", fg=self.MUTED).pack()

            statbox("Order Numbers", f"{o_icon} {result['order1']} / {result['order2']}", 0)
            statbox("Items Matched",  f"{result['matched_items']} / {result['total_items']}", 1)
            statbox("Confidence",     f"{result['confidence']:.1f}%", 2)
            statbox("Order Match",    f"{o_icon}  {'Yes' if result.get('order_match') else 'No'}", 3)

            tk.Button(inner, text="📋  View Detailed Log",
                  font=("Segoe UI", 10, "bold"),
                  bg=self.PRIMARY, fg="white",
                  activebackground=self.ACCENT, activeforeground="white",
                  cursor="hand2", relief=tk.FLAT, padx=18, pady=9,
                  command=self._show_log).pack(fill=tk.X)


    def _display_error(self, msg: str):
        self.progress.stop()
        self.progress.pack_forget()
        self.match_btn.config(state=tk.NORMAL)
        messagebox.showerror("Error", f"Failed to process \n\n{msg}")


    def _show_log(self):
        if not self.match_log:
            return
        win = tk.Toplevel(self.root)
        win.title("Detailed Matching Log")
        win.geometry("800x600")
        win.configure(bg=self.BG)

        hdr = tk.Frame(win, bg=self.PRIMARY, padx=10, pady=10)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="Detailed Matching Log", font=("Courier New", 13, "bold"), bg=self.PRIMARY, fg="white").pack

        ta = scrolledtext.ScrolledText(win, font=("Courier", 9), wrap=tk.WORD, padx=10, pady=10, bg='1e2433', fg='#e8eaf6')
        ta.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ta.insert(1.0, self.match_log)
        ta.config(state=tk.DISABLED)

        tk.Button(win, text="Close", font=("Segoe UI", 10, "bold"), bg=self.PRIMARY, fg="white", cursor="hand2", command=win.destroy,
            relief=tk.FLAT, padx=20, pady=10).pack(pady=10)


def main():
    root = tk.Tk()
    DocumentMatcherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()










 