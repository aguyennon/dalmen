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
        self.root.title("DECKO Document Matcher")
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
        self.decko_prices = {}
        self.decko_options = {}
        self.load_decko_price_list()

        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg=self.primary_color)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="DECKO Document Matcher",
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
        tk.Label(inner1, text="Dalmen Order or DECKO Confirmation",
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
        tk.Label(inner2, text="Dalmen Order or DECKO Confirmation",
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
            print(f"Doc1 provider: {doc1.provider}")
            print(f"Doc1 order: {doc1.order_number}")
            
            print("Parsing second doc...")
            doc2 = self.parse_document(self.file2_path, dalmen_po=doc1.order_number)
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

    
    def load_decko_price_list(self):
        import pandas as pd
        try:
            df = pd.read_excel(
                r"G:\2026 PRICE LIST\DECKO - PRODUITS DALMEN LTÉE.xlsx",
                sheet_name="Liste de prix",
                header=None
            )

            size_cols = {}
            for col_idx in range(7, 17):
                val = str(df.iloc[5, col_idx]).strip()
                if val and val != 'nan':
                    size_cols[col_idx] = val

            print(f" DEBUG DECKO price list: size columns = {size_cols}")

            model_rows = {
                "LÉGENDE 'S'": 6,
                "CLASSIQUE 'S'": 7,
                "CLASSIQUE 'C'": 8,
                "JARDIN-PVC": 9,
                "COMBO-PVC": 10,
                "COMBO-PVC-PEINTURE": 12,
                "COMBO-ALU": 14,
                "HYBRIDE": 16,
                "JARDIN-HYBRIDE": 18,
            }

            for model, row_idx in model_rows.items():
                self.decko_prices[model] = {}
                for col_idx, size_label in size_cols.items():
                    val = df.iloc[row_idx, col_idx]
                    try:
                        self.decko_prices[model][size_label] = float(val)
                    except:
                        self.decko_prices[model][size_label] = 0.0

            option_rows = range(21, 52)
            for row_idx in option_rows:
                option_name = str(df.iloc[row_idx, 1]).strip()
                if option_name and option_name != 'nan':
                    self.decko_options[option_name] = {}
                    for col_idx, size_label in size_cols.items():
                        val = df.iloc[row_idx, col_idx]
                        try:
                            self.decko_options[option_name][size_label] = float(val)
                        except:
                            self.decko_options[option_name][size_label] = 0.0

            print(f"Loaded {len(self.decko_prices)} DECKO models")
            print(f"Loaded {len(self.decko_options)} DECKO options")
            print(f"DEBUG all energetique keys: {[k for k in self.decko_options if 'NERG' in k.upper()]}")

        except Exception as e:
            print(f"Failed to load DECKO price list: {e}")

    
    def get_decko_size_col(self, text: str) -> str:
        t = text.upper()

        sash_match = re.search(r'(\d)\s*SASH|(\d)\s*VOLETS?|MODELE\s*(\d)\s*VOLETS?', t)
        if sash_match:
            sash_count = int(next(g for g in sash_match.groups() if g))
        else:
            sash_count = 2

        footage_match = re.search(r'(?:SASH\s+MODEL|MODELE\s+\d\s+VOLETS?)[^\']*?(\d+)\'', t)
        if not footage_match:
            footage_match = re.search(r'(?:PATIO|PORTE)[^\']{0,60}\)\s*(\d+)\s*(?:\'|$)', t)
        if not footage_match:
            footage_match = re.search(r'\b([5-9]|10|12)\'', t)
        
        
        footage = int(footage_match.group(1)) if footage_match else 6
        size_col = f"{footage}' {sash_count}L"

        print(f"DEBUG DECKO size: footage={footage}', sash={sash_count} -> column='{size_col}'")
        return size_col


    def strip_accents(self, text: str) -> str:
        import unicodedata
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )

    def calculate_decko_expected_price(self, text: str, include_moustiquaire: bool = False) -> tuple:
        t = text.upper()
        breakdown = []
        if re.search(r'V01R\s*S0UMISS10N|VOIR\s*SOUMISSION', t):
            breakdown.append("⚠️ Custom package — voir soumission de Decko")
            breakdown.append("Cannot verifty against standard price list")
            breakdown.append("Manual review required")
            return 0.0, breakdown

        total = 0.0

        print(f"DEBUG calc_price: text length={len(text)}")
        exterior_match = re.search(r'.{0,30}(EXTERIOR|PAINTED|PEINTUR).{0,30}', t)
        print(f"DEBUG calc_price: exterior area = '{exterior_match.group(0) if exterior_match else 'NOT FOUND'}'")
        print(f"DEBUG calc_price: first 300 chars of text:\n{t[:300]}")

        model_map = {
            r"CLASSIQUE\s*['\"]?C['\"]?|CLASSIC\s*['\"]?C['\"]?": "CLASSIQUE 'C'",
            r"L[EÉ]GENDE\s*['\"]?S['\"]?|LEGENDE\s*['\"]?S['\"]?": "LÉGENDE 'S'",
            r"CLASSIQUE\s*['\"]?S['\"]?|CLASSIC\s*['\"]?S['\"]?": "CLASSIQUE 'S'",
            r"JARDIN-HYBRIDE": "JARDIN-HYBRIDE",
            r"JARDIN-PVC": "JARDIN-PVC",
            r"COMBO-PVC-PEINTURE|COMBO\s*PVC\s*PEINTURE": "COMBO-PVC-PEINTURE",
            r"COMBO-ALU|COMBO\s*ALU": "COMBO-ALU",
            r"COMBO-PVC|COMBO\s*PVC": "COMBO-PVC",
            r"HYBRIDE": "HYBRIDE",
        }

        model = None
        for pattern, model_name in model_map.items():
            if re.search(pattern, t):
                model = model_name
                break

        if not model:
            breakdown.append("⚠️ Could not detect model from PO")
            return 0.0, breakdown

        breakdown.append(f"Model: {model}")

        size_col = self.get_decko_size_col(text)
        breakdown.append(f"Size: {size_col}")

        # Base price lookup
        if model in self.decko_prices and size_col in self.decko_prices[model]:
            base = self.decko_prices[model][size_col]
            total += base
            breakdown.append(f"Base price ({model} × {size_col}): ${base:.2f}")
        else:
            breakdown.append(f"⚠️ Base price not found for {model} × {size_col}")
            return 0.0, breakdown

        # Triple glass — each size is independent of the others
        # so this block is at top level, not nested inside anything
        if re.search(r'TRIPLE\s*GLASS|TRIPLE\s*VERRE|VERRE\s*TRIPLE', t):
            if size_col == "6' 2L":
                option_price = 223.0
            else:
                option_key = next(
                    (k for k in self.decko_options if 'TRIPLE' in k.upper()),
                    None
                )
                option_price = (
                    self.decko_options[option_key][size_col]
                    if option_key and size_col in self.decko_options[option_key]
                    else 0.0
                )
            total += option_price
            breakdown.append(f"Triple verre: +${option_price:.2f}")
        elif re.search(r'LOW[\s\-]*E\s*\+?\s*ARGON|VERRE\s*[EÉ]NERG|ENERGETIQUE', t):
            option_key = next(
                (k for k in self.decko_options
                if self.strip_accents(k).upper().startswith('VERRE')
                and 'NERG' in self.strip_accents(k).upper()),
                None
            )
            if option_key and size_col in self.decko_options[option_key]:
                option_price = self.decko_options[option_key][size_col]
                total += option_price
                breakdown.append(f"Verre énergétique: +${option_price:.2f}")
                print(f"DEBUG verre energetique: option_key='{option_key}, price={self.decko_options.get(option_key, {}).get(size_col, 'NOT FOUND')}")

        if re.search(r'9\s*1/4|9\.25', t) and re.search(r'FRAME|CADRE', t):
            option_key = next(
                (k for k in self.decko_options
                if 'EXTENSION DE CADRE' in k.upper() and 'REV' in k.upper()),
                None
            )
            if option_key and size_col in self.decko_options[option_key]:
                option_price = self.decko_options[option_key][size_col]
                total += option_price
                breakdown.append(f"Extension cadre 9¼\" + revêtement: +${option_price:.2f}")

        # 7 1/4" frame — check if soufflage/extension present
        elif re.search(r'7\s*1/4|7\.25', t) and re.search(r'FRAME|CADRE', t):
            # Soufflage/Extension present → use the extension cadre option ($83)
            # No soufflage → use plain revêtement intérieur ($46)
            has_soufflage = bool(re.search(
                r'SOUFFLAGE|EXTENSION\s*DE\s*CADRE|EXTENS10N\s*DE\s*CADRE', t
            ))
            if has_soufflage:
                option_key = next(
                    (k for k in self.decko_options
                    if 'EXTENSION DE CADRE' in k.upper() and 'REV' in k.upper()),
                    None
                )
            else:
                option_key = next(
                    (k for k in self.decko_options
                    if self.strip_accents(k).upper().startswith('REV')
                    and '7' in k),
                    None
                )
            if option_key and size_col in self.decko_options[option_key]:
                option_price = self.decko_options[option_key][size_col]
                total += option_price
                breakdown.append(f"{'Extension cadre' if has_soufflage else 'Revêtement intérieur'} 7¼\": +${option_price:.2f}")

        # Exterior paint — also at top level, independent of frame size
        if re.search(r'EXTER1?0?R\s*PA1?NTED|EXTERIOR\s*PAINTED|PEINTUR[EÉ].*NOIR|EXT.*PEINTUR', t):
            print(f"DEBUG: paint check: searching in text snippet:")
            paint_area = re.search(r'.{0,50}(PAINT|PEINTUR|EXT).{0,50}', t)
            if paint_area:
                print(f" FOund: '{paint_area.group(0)}'")
            print(f"DEBUG: paint regex match: {bool(re.search(r'EXTERIOR PAINTED|PEINTURE.*EXT|EXT.*PEINTUR', t))}")
            option_key = next(
                (k for k in self.decko_options
                if 'PEINTURE' in k.upper()
                and '1' in k
                and 'EXT' in k.upper()
                and 'HYBRIDE' not in k.upper()
                and 'CARRELAGE' not in k.upper()
                and 'POIGN' not in k.upper()),
                None
            )
            print(f"DEBUG paint option key found: {option_key}")

            if option_key and size_col in self.decko_options[option_key]:
                option_price = self.decko_options[option_key][size_col]
                total += option_price
                breakdown.append(f"Peinture 1 côté ext: +${option_price:.2f}")
        
        if re.search(r'BARRE\s*DE\s*SECUR|BARRE\s*DE\s*S[EÉ]CUR1T[EÉ]|SECURITY\s*BAR', t):
            option_key = next(
                (k for k in self.decko_options
                if self.strip_accents(k).upper().startswith('BARRE')),
                None
            )
            if option_key:
                option_price = 23.0
                total += option_price
                breakdown.append(f"Barre de sécurité: +${option_price:.2f}")

            print(f"DEBUG barre: option_key='{option_key}', all_barre_keys={[k for k in self.decko_options if 'BARRE' 
                in k.upper()]}, price={self.decko_options.get(option_key, {}).get(size_col, 'NOT FOUND')}")

        if include_moustiquaire:
            total += 9.0
            breakdown.append(f"Moustiquaire (screen in bag): +$9.00")

        # Explicitly $0 items — documented so the log is transparent
        breakdown.append(f"Aluminum screen: $0.00 (standard)")
        breakdown.append(f"Contemporary handle: $0.00")
        breakdown.append(f"COMM:ADJUSTMENT: ignored")
        breakdown.append(f"─────────────────────")
        breakdown.append(f"Expected Total: ${total:.2f}")

        return total, breakdown


    def extract_facture_sous_total(self, text: str) -> float:
        match = re.search(r'Sous-total\s*:\s*([\d\s,\.]+)', text, re.IGNORECASE)
        if match:
            raw = match.group(1).strip()
            raw = raw.replace(' ', '').replace(',', '.')
            try:
                val = float(raw)
                print(f"DEBUG: Facture Sous-total extracted: ${val:.2f}")
                return val
            except:
                pass
        print("DEBUG: Could not extract Sous-total from facture")
        return 0.0

    
    def match_decko_documents(self, doc1, doc2):
        log = []
        log.append("="*60)
        log.append("DECKO MATCHING")
        log.append("="*60)

        score = 0

        # --- Order number matching ---
        log.append(f"\nOrder Numbers:")
        log.append(f"  Doc1: {doc1.order_number}")
        log.append(f"  Doc2: {doc2.order_number}")

        order_match = (doc1.order_number == doc2.order_number and
                    doc1.order_number != "Unknown")
        if order_match:
            score += 50
            log.append("  ✓ EXACT MATCH (+50 points)")
        elif doc1.order_number != "Unknown" and doc2.order_number != "Unknown":
            if doc1.order_number in doc2.order_number or doc2.order_number in doc1.order_number:
                score += 45
                log.append(" ~ PARTIAL MATCH (+45 points)")
            else:
                log.append("  ✗ Different order numbers (0 points)")
        else:
            log.append("  ✗ Order number missing in one or both documents.")

        doc2_is_facture = (
            "FACTURE" in doc2.raw_text.upper() and
            "SOUS-TOTAL" in doc2.raw_text.upper()
        )
        print(f"DEBUG is_facture check: 'FACTURE' in text = {'FACTURE' in doc2.raw_text.upper()}")
        print(f"DEBUG is_facture check: 'SOUS-TOTAL' in text = {'SOUS-TOTAL' in doc2.raw_text.upper()}")
        print(f"DEBUG doc2 raw text preview: {doc2.raw_text[:300]}")

        if doc2_is_facture:
        # ── PRICE CHECK PATH (PO vs Facture) ─────────────────────────
            log.append(f"\n{'='*60}")
            log.append("PRICE VERIFICATION (PO vs Facture)")
            log.append(f"{'='*60}")

            facture_has_moustiquaire = bool(re.search(
                r'MOUSTIQUAIRE|DIVERS-50892', doc2.raw_text.upper()
            ))
            expected_price, breakdown = self.calculate_decko_expected_price(
                doc1.raw_text, include_moustiquaire=facture_has_moustiquaire
            )
            facture_total = self.extract_facture_sous_total(doc2.raw_text)

            # Write the price breakdown into the log so the user can see each component
            for line in breakdown:
                log.append(f"  {line}")

            log.append(f"\n  Facture Sous-total: ${facture_total:.2f}")

            price_ok = False
            if expected_price > 0 and facture_total > 0:
                diff = abs(expected_price - facture_total)
                price_ok = diff <= 5.0
                log.append(f"  Difference: ${diff:.2f} (threshold: $5.00)")
                log.append(f"  Price Check: {'✅ PASS' if price_ok else '❌ FAIL'}")
                if price_ok:
                    score += 50  # Price check passes = full second half of score
            elif expected_price == 0.0:
                log.append("  ⚠️ Price verification skipped — manual review required")
                price_ok = True
                score += 25
            else:
                log.append("  ⚠️ Could not complete price check — missing data")

            documents_match = order_match and price_ok

            log.append(f"\n{'='*60}")
            log.append(f"ORDER MATCH: {'✅ YES' if order_match else '❌ NO'}")
            log.append(f"PRICE CHECK: {'✅ PASS' if price_ok else '❌ FAIL'}")
            log.append(f"RESULT: {'✅ DOCUMENTS MATCH' if documents_match else '❌ DO NOT MATCH'}")
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
                "total1": expected_price,   # What we calculated from the PO + price list
                "total2": facture_total,    # What the facture says
                "total_diff": abs(expected_price - facture_total),
                "configuration": doc1.fingerprint.configuration if doc1.fingerprint else "N/A",
                "config_match": order_match,
                "frame": doc1.fingerprint.frame if doc1.fingerprint else "N/A",
                "frame_match": price_ok,
                "is_facture": True,   # Tells display_result which set of stat boxes to show
                "price_ok": price_ok,
            }

        else:
            # ── FINGERPRINT PATH (PO vs Confirmation) ────────────────────
            # This is the original logic — unchanged so existing PO→confirmation
            # matching continues to work exactly as before
            log.append(f"\n{'='*60}")
            log.append("PRODUCT FINGERPRINT COMPARISON (PO vs Confirmation):")
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
                    log.append("  ✓ Match (+5)")
                elif 'DOOR' in fp1.category and 'DOOR' in fp2.category:
                    fingerprint_score += 2.5
                    log.append(" - Partial match (+2.5)")
                else:
                    log.append("  ✗ Different")

            # Configuration (10 points)
            log.append(f"\n[CONFIGURATION]")
            log.append(f"  Doc1: {fp1.configuration or 'Not specified'}")
            log.append(f"  Doc2: {fp2.configuration or 'Not specified'}")
            if fp1.configuration and fp2.configuration:
                fingerprint_max += 10
                if fp1.configuration == fp2.configuration:
                    fingerprint_score += 10
                    log.append("  ✓ Match (+10)")
                else:
                    log.append("  ✗ Different")

            # Dimensions (15 points)
            log.append(f"\n[DIMENSIONS]")
            log.append(f"  Doc1: {fp1.width}\" x {fp1.height}\"")
            log.append(f"  Doc2: {fp2.width}\" x {fp2.height}\"")
            if fp1.width and fp2.width and fp1.height and fp2.height:
                fingerprint_max += 15
                if abs(fp1.width - fp2.width) < 0.25 and abs(fp1.height - fp2.height) < 0.25:
                    fingerprint_score += 15
                    log.append("  ✓ Match (+15)")
                elif abs(fp1.width - fp2.width) < 1.0 and abs(fp1.height - fp2.height) < 1.0:
                    fingerprint_score += 10
                    log.append("  ~ Close match (+10)")
                else:
                    log.append(f"  ✗ Different")

            # Frame (5 points)
            log.append(f"\n[FRAME MATERIAL]")
            log.append(f"  Doc1: {fp1.frame or 'Not specified'}")
            log.append(f"  Doc2: {fp2.frame or 'Not specified'}")
            if fp1.frame and fp2.frame:
                fingerprint_max += 5
                if fp1.frame == fp2.frame:
                    fingerprint_score += 5
                    log.append("  ✓ Match (+5)")
                else:
                    log.append("  ✗ Different")

            # Glass (10 points)
            log.append(f"\n[GLASS CONFIGURATION]")
            log.append(f"  Doc1: {fp1.glass_layers} layers, Low-E: {fp1.low_e}, Argon: {fp1.argon}")
            log.append(f"  Doc2: {fp2.glass_layers} layers, Low-E: {fp2.low_e}, Argon: {fp2.argon}")
            if fp1.glass_layers and fp2.glass_layers:
                fingerprint_max += 10
                if (fp1.glass_layers == fp2.glass_layers and 
                    fp1.low_e == fp2.low_e and 
                    fp1.argon == fp2.argon):
                    fingerprint_score += 10
                    log.append("  ✓ Full match (+10)")
                elif fp1.glass_layers == fp2.glass_layers:
                    fingerprint_score += 5
                    log.append("  ~ Partial match (+5)")
                else:
                    log.append("  ✗ Different")

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
                    log.append("  ✓ Colors match (+5)")
                else:
                    log.append("  ✗ Different colors")

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

            if fingerprint_max > 0:
                fp_pct = (fingerprint_score / fingerprint_max) * 100
                score += (fp_pct / 100) * 50
                log.append(f"\nFingerprint Score: {fingerprint_score:.1f}/{fingerprint_max} = {fp_pct:.1f}%")
                log.append(f"Contributes: {(fp_pct / 100) * 50:.1f}/50 points to total")

            documents_match = score >= 70

            log.append(f"\n{'='*60}")
            log.append(f"FINAL SCORE: {score:.1f}/100")
            log.append(f"Threshold: 70 points")
            log.append(f"Result: {'✅ DOCUMENTS MATCH' if documents_match else '❌ DO NOT MATCH'}")
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
                "total_diff": abs(doc1.total - doc2.total),
                "configuration": fp1.configuration or fp2.configuration or "N/A",
                "config_match": bool(fp1.configuration and fp2.configuration 
                                    and fp1.configuration == fp2.configuration),
                "frame": fp1.frame or fp2.frame or "N/A",
                "frame_match": bool(fp1.frame and fp2.frame 
                                    and fp1.frame == fp2.frame),
                "is_facture": False,  # Tells display_result to show fingerprint stat boxes
                "price_ok": None,
            }
    
    def extract_order_number(self, text: str) -> str:
        """Extract order number"""
        text = re.sub(r'(\d{3}-\d{5}-\d)\s+(\d-\d-\d)', r'\1\2', text)
        patterns = [
            r'Votre\s+n[°o]\.?\s*commande\s*[:\s]*\n?\s*Remarque\s*\n\s*([\d\-]+)',
            r'Votre\s+n[°o]\.?\s*commande\s*[:\s]*([\d\-]+)',
            r'Num[ée]ro?\s+de\s+bon\s*[:\s]*\n?\s*(\d{3}-\d{5}-\d{2}-\d-\d)',  
            r'Votre\s+N[°o]\.?\s+commande\s*[:\s]*([\d\-]+)',
            r'(\d{3}-\d{5}-\d{2}-\d-\d)', 
            ]

        print(f"DEBUG: Searching for order number in text...")

        for i, pattern in enumerate(patterns):
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                order_num = match.group(1).strip()
                print(f" Pattern {i+1} matched: '{order_num}'")
                return order_num

        print(f" No pattern matched. Text preview around 'commande':")
        commande_idx = text.lower().find('commande')
        if commande_idx != -1:
            snippet = text[max(0, commande_idx-20):commande_idx+100]
            print(f" '{snippet}'")

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

        is_facture = "FACTURE" in t or "N° CLIENT" in t or "DATE FACTURÉE" in t

        if is_facture:
            print(" DEBUG: FACTURE detected - will skip dimension extraction")
        
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

        if not is_facture:
            print(f"\nDEBUG: Searching for dimensions...")
            x_matches = re.findall(r'\d+[^\n]{0,20}[Xx×][^\n]{0,20}\d+', t)
            if x_matches:
                print(f"  Found potential dimension patterns: {x_matches[:3]}")
        else:
            print(f" Skipping dimension extraction (facture document)")
            
        desc_patterns = [
            r'CLASS[^\n]{0,100}',  # CLASS... line
            r'PATIO[^\n]{0,100}',  # PATIO... line  
            r'70[^\n]{0,100}81',   # Any line with 70...81
        ]
        for dp in desc_patterns:
            desc_match = re.search(dp, t)
            if desc_match:
                print(f"  Found description pattern match: '{desc_match.group(0)}'")
        
        hybrid_match = re.search(r'HYBRIDE\s*[-:]\s*(\d+)\s+(\d+)/(\d+)\s*[\"″]?\s*-\s*[A-Z]+', t)

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

    def extract_pdf_text_by_page(self, pdf_path: str) -> List[str]:
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    pages.append(page_text)
                else:
                    pages.append("")
        return pages

    def filter_pages_by_po(self, pages: List[str], target_po: str) -> str:
        matching_text = []

        print(f"\nDEBUG: Filtering {len(pages)} pages for PO: {target_po}")

        for i, page_text in enumerate(pages, 1):
            if target_po in page_text:
                print(f" Page {i} DOES contain PO {target_po}")
                matching_text.append(page_text)
            else:
                po_base = '-'.join(target_po.split('-')[:3])
                if po_base in page_text and len(po_base) >= 10:
                    print(f" Page {i} DOES contain PO base {po_base}")
                    matching_text.append(page_text)
        
        if not matching_text:
            print(f"   WARNING: No pages found with PO {target_po}")
            print(f"  Will process all pages (fallback mode)")
            return '\n'.join(pages)

        print(f"  Found {len(matching_text)} matching page(s)\n")
        return '\n'.join(matching_text)


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


    def parse_document(self, pdf_path: str, dalmen_po: str = None) -> OrderDocument:
        quick_scan_text = self.extract_pdf_text(pdf_path)
        provider = self.detect_provider(quick_scan_text)
        quick_scan_text = re.sub(r'(\d{3}-\d{5}-\d)\s+(\d-\d-\d)', r'\1\2', quick_scan_text)
        temp_order_number = self.extract_order_number(quick_scan_text)

        if dalmen_po and provider == "DECKO_DALMEN" and "FACTURE" in quick_scan_text.upper():
            print(f"DEBUG: Using Dalmen PO {dalmen_po} to filter facture pages")
            temp_order_number = dalmen_po

        print(f"DEBUG: Quick scan - Provider: {provider}, PO: {temp_order_number}")

        if provider == "DECKO_DALMEN" and temp_order_number != "Unknown" and dalmen_po:
            print(f"DEBUG: DECKO document detected - filtering pages by PO")
            pages = self.extract_pdf_text_by_page(pdf_path)
            text = self.filter_pages_by_po(pages, temp_order_number)
            print(f"DEBUG: Diltered text length: {len(text)} chars")
        else:
            text = quick_scan_text

        if not text or len(text.strip()) < 50:
            print("DEBUG: pdfplumber returned empty - forcing OCR")
            ocr_lines = self.ocr_pdf(pdf_path)
            text = "\n".join([self.normalize_ocr_line(l) for l in ocr_lines])
            full_text = text
            print(f"DEBUG FULL PO TEXT:\n{full_text}")

        print(f"DEBUG: Text preview (first 500 chars):")
        print(text[:500])
        print(f"DEBUG: Contains 'DALMEN': {'DALMEN' in text.upper()}")
        print(f"DEBUG: Contains 'DECKO': {'DECKO' in text.upper()}")
        print(f"DEBUG: Contains 'TAMARACK': {'TAMARACK' in text.upper()}")
        print(f"DEBUG: Contains 'Fournisseur': {'FOURNISSEUR' in text.upper()}")

        provider = self.detect_provider(text)
        print(f"DEBUG: Detected provider: {provider}")

        normalized_text = self.normalize_price_text(text)

        use_ocr = False
        if provider == "DECKO_DALMEN":
            has_content = bool(re.search(r'[A-Z]{2,}\s*-?\s*\d+|XO|OX|\d+\s*["\']?\s*[Xx]\s*\d+', text))
            print(f"DEBUG: DECKO doc has content: {has_content}")
            if not has_content:
                use_ocr = True
                print("DEBUG: OCR required for DECKO doc - missing product specs")
        else:
            if self.needs_ocr(normalized_text) or not self.contains_prices(normalized_text):
                use_ocr = True
                print("DEBUG: OCR required: missing prices or product codes...")

        if use_ocr:
            ocr_lines = self.ocr_pdf(pdf_path)
            text = "\n".join([self.normalize_ocr_line(l) for l in ocr_lines])
            normalized_text = self.normalize_price_text(text)

        # Store full text now before anything else touches it
        # This is used by calculate_decko_expected_price to read all PO option lines
        full_text = text
        print(f"DEBUG: full_text length = {len(full_text)}")

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
        # Facture uses filtered page text (right page only for Sous-total extraction)
        # PO uses full_text so all option lines like EXTERIOR PAINTED are available
        doc.raw_text = full_text

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

            if not agg[key]["label"]:
                agg[key]["label"] = i.product_code
        return agg

    def match_documents(self, doc1: OrderDocument, doc2: OrderDocument) -> Dict:
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

                if total1 == 0 or total2 == 0:
                    if sim > 0.80 and sim > best_sim:
                        best_match = label2
                        best_diff = 0
                        best_sim = sim
                else:
                    if sim > 0.60 and diff < best_diff:
                        best_match = label2
                        best_diff = diff
                        best_sim = sim
            
            if total1 == 0 or (best_match and data2.get("total", 0) == 0):
                threshold = 0
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
            "total_diff": abs(doc1.total - doc2.total)
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

        order_icon = "✅" if result['order1'] == result['order2'] else "❌"

        if result.get('is_facture'):
            price_icon = "✅" if result.get('price_ok') else "❌"
            stat_box(stats, "Order Numbers",  f"{order_icon}  {result['order1']} / {result['order2']}", 0)
            stat_box(stats, "Expected Price", f"${result['total1']:.2f}", 1)
            stat_box(stats, "Facture Total",  f"${result['total2']:.2f}", 2)
            stat_box(stats, "Price Check",    f"{price_icon}  {'Pass' if result.get('price_ok') else 'Fail'}", 3)
        else:
            config_icon = "✅" if result.get('config_match') else "❌"
            frame_icon  = "✅" if result.get('frame_match')  else "❌"
            stat_box(stats, "Order Numbers",   f"{order_icon}  {result['order1']} / {result['order2']}", 0)
            stat_box(stats, "Items Matched",   f"{result['matched_items']} / {result['total_items']}", 1)
            stat_box(stats, "Configuration",   f"{config_icon}  {result.get('configuration', 'N/A')}", 2)
            stat_box(stats, "Frame Material",  f"{frame_icon}  {result.get('frame', 'N/A')}", 3)

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