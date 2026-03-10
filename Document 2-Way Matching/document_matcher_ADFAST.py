import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import pdfplumber
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from difflib import SequenceMatcher
import threading

@dataclass
class LineItem:
    product_code: str
    color: str = ""
    price: float = 0.0       # line total (qty * unit)
    unit_price: float = 0.0  # unit price for comparison

@dataclass
class OrderDocument:
    po_number: str
    line_items: List[LineItem] = field(default_factory=list)
    total: float = 0.0


class DocumentMatcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADFAST Order Matcher")
        self.root.geometry("820x680")
        self.root.resizable(False, False)

        self.bg_color = "#f0f0f0"
        self.primary_color = "#c8102e"
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
            text="ADFAST Order Matcher",
            font=("Arial", 22, "bold"),
            bg=self.primary_color, fg="white"
        ).pack(side=tk.LEFT, padx=24, pady=16)

        self.log_btn = tk.Button(
            header,
            text="📋  View Log",
            font=("Arial", 10, "bold"),
            bg="#9a0824", fg="white",
            cursor="hand2",
            command=self.show_log_window,
            relief=tk.FLAT, padx=14, pady=8,
            state=tk.DISABLED
        )
        self.log_btn.pack(side=tk.RIGHT, padx=20, pady=14)

        tk.Label(
            header,
            text="Match DALMEN orders with ADFAST confirmations",
            font=("Arial", 10),
            bg=self.primary_color, fg="#ffcccc"
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
        tk.Label(inner1, text="Dalmen Order or ADFAST Confirmation",
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
        tk.Label(inner2, text="Dalmen Order or ADFAST Confirmation",
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
            text1 = self.extract_pdf_text(self.file1_path)
            text2 = self.extract_pdf_text(self.file2_path)

            is_file1_dalmen = "Rapport de commande" in text1 or "Dalmen Portes" in text1
            is_file1_adfast = "CONFIRMATION DE COMMANDE" in text1 or "Adfast Canada" in text1
            is_file2_dalmen = "Rapport de commande" in text2 or "Dalmen Portes" in text2
            is_file2_adfast = "CONFIRMATION DE COMMANDE" in text2 or "Adfast Canada" in text2

            if is_file1_dalmen and is_file2_adfast:
                dalmen_text, adfast_text = text1, text2
            elif is_file1_adfast and is_file2_dalmen:
                dalmen_text, adfast_text = text2, text1
            else:
                dalmen_text, adfast_text = text1, text2

            dalmen_doc = self.parse_dalmen_order(dalmen_text)
            adfast_doc = self.parse_adfast_confirmation(adfast_text)

            result = self.match_documents(dalmen_doc, adfast_doc)
            self.root.after(0, self.display_result, result)

        except Exception as e:
            import traceback
            err = traceback.format_exc()
            print(err)
            self.root.after(0, self.display_error, f"{str(e)}\n\n{err}")

    def extract_pdf_text(self, pdf_path: str) -> str:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    # HELPERS
    def normalize_code(self, code: str) -> str:
        """Normalize product code: uppercase, strip spaces, unify separators."""
        code = code.upper().strip()
        # Remove spaces around dashes
        code = re.sub(r'\s*-\s*', '-', code)
        # Remove spaces between digits/letters and 'ML'
        code = re.sub(r'\s+ML', 'ML', code)
        code = re.sub(r'ML\s+', 'ML/', code)
        # Strip trailing /Adseal or /ADSEAL
        code = re.sub(r'/ADSEAL$', '', code, flags=re.IGNORECASE)
        return code.strip()

    def extract_color_from_text(self, text: str) -> str:
        """Return normalized English color name from French or English text."""
        mapping = {
            'NOIR': 'BLACK',
            'BLACK': 'BLACK',
            'BLANC': 'WHITE',
            'WHITE': 'WHITE',
            'TRANSLUCIDE': 'TRANSLUCIDE',
            'TRANSLUCID': 'TRANSLUCIDE',
            'CLAIR': 'TRANSLUCIDE',
            'GRIS': 'GRAY',
            'GRAY': 'GRAY',
            'ROUGE': 'RED',
            'RED': 'RED',
            'BLEU': 'BLUE',
            'BLUE': 'BLUE',
        }
        upper = text.upper()
        for key, val in mapping.items():
            if key in upper:
                return val
        return ""

    def extract_po_number(self, text: str) -> str:
        m = re.search(r'R[ée]f[ée]rence du client\s*\(PO\)[:\s]+(\d+)', text, re.IGNORECASE)
        if m:
            return m.group(1).strip()

        # search for the label and then grab the first standalone number after it
        m = re.search(
            r'Num[ée]ro de PO[\s\S]{0,60}?(\b\d{3,6}\b)',
            text, re.IGNORECASE
        )
        if m:
            candidate = m.group(1).strip()
            # Reject numbers that are clearly phone/address fragments
            if candidate not in ('5630', '2268', '3070', '514', '613'):
                return candidate

        # Broader fallback 
        section = re.search(r'Num[ée]ro de PO([\s\S]{0,200})', text, re.IGNORECASE)
        if section:
            numbers = re.findall(r'\b(\d{3,6})\b', section.group(1))
            blacklist = {'5630', '2268', '3070', '514', '613', '524'}
            for num in numbers:
                if num not in blacklist:
                    return num

        return "Unknown"


    def parse_dalmen_order(self, text: str) -> OrderDocument:
        print("\nDEBUG: Parsing Dalmen order...")
        po_number = self.extract_po_number(text)
        print(f"  PO: {po_number}")

        items: List[LineItem] = []
        total = 0.0

        raw_lines = text.split('\n')

        # Step 1: merge wrapped product-code lines 
        merged_lines = []
        i = 0
        while i < len(raw_lines):
            line = raw_lines[i].strip()

            partial_match = re.match(r'^(\d{4})-\s', line)
            if partial_match and i + 1 < len(raw_lines):
                next_line = raw_lines[i + 1].strip()
                ml_match = re.match(r'^(\d+\s*ml)', next_line, re.IGNORECASE)
                if ml_match:
                    # Inject the ml code right after the dash
                    ml_part = ml_match.group(1).replace(' ', '')
                    line = line.replace(
                        partial_match.group(0),
                        f"{partial_match.group(1)}-{ml_part} ",
                        1
                    )
                    i += 2
                    merged_lines.append(line)
                    continue

            # Case 2: line is ONLY a bare code prefix 
            if re.match(r'^\d{4}-$', line) and i + 1 < len(raw_lines):
                merged_lines.append(line + raw_lines[i + 1].strip())
                i += 2
                continue

            merged_lines.append(line)
            i += 1

        # Step 2: parse each line 
        for line in merged_lines:
            line = line.strip()
            if not line:
                continue

            # Skip header / footer / total lines
            if re.match(r'^(Code|Pi[eè]ce|Total|Livr[eé]|Command[eé]|Date|Notes|ADFAST)', line, re.IGNORECASE):
                continue

            # Product lines start with a code: digits + dash + digits + 'ml'
            code_match = re.match(r'^(\d{4}-\d+\s*ml[\w/,]*)', line, re.IGNORECASE)
            if not code_match:
                continue

            raw_code = code_match.group(1)
            product_code = self.normalize_code(raw_code)

            # Dollar amounts on this line
            amounts = re.findall(r'([\d][\d\s]*[,\.][\d]{2,3})\s*\$', line)
            price = 0.0
            unit_price = 0.0
            if len(amounts) >= 2:
                unit_str = amounts[-2].replace(' ', '').replace(',', '.')
                price_str = amounts[-1].replace(' ', '').replace(',', '.')
                try:
                    unit_price = float(unit_str)
                    price = float(price_str)
                except ValueError:
                    pass
            elif len(amounts) == 1:
                price_str = amounts[0].replace(' ', '').replace(',', '.')
                try:
                    price = float(price_str)
                except ValueError:
                    pass

            color = self.extract_color_from_text(line)

            print(f"  Found: {product_code} | {color} | unit=${unit_price:.2f} | total=${price:.2f}")
            items.append(LineItem(product_code=product_code, color=color, price=price, unit_price=unit_price))

        # Total line
        total_match = re.search(r'Total\s*:\s*([\d\s,\.]+)\s*\$', text)
        if total_match:
            ts = total_match.group(1).replace(' ', '').replace(',', '.')
            try:
                total = float(ts)
            except ValueError:
                pass

        print(f"  Items: {len(items)}, Total: ${total:.2f}\n")
        return OrderDocument(po_number=po_number, line_items=items, total=total)


    # ADFAST PARSER  — uses table extraction
    def parse_adfast_confirmation(self, text: str) -> OrderDocument:
        print("\nDEBUG: Parsing ADFAST confirmation...")
        po_number = self.extract_po_number(text)
        print(f"  PO: {po_number}")

        items: List[LineItem] = []
        total = 0.0

        lines = text.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Match ADFAST product code
            code_match = re.match(r'^(\d{4}-\d+\s*ml[/\w]*)', line, re.IGNORECASE)
            if code_match:
                raw_code = code_match.group(1)
                product_code = self.normalize_code(raw_code)

                # Gather the next ~8 lines into a block to find color, qty, price
                block_lines = [line]
                for j in range(i + 1, min(i + 9, len(lines))):
                    next_line = lines[j].strip()
                    # Stop at next product code or summary section
                    if re.match(r'^\d{4}-\d+', next_line):
                        break
                    if re.match(r'^(SOUS-TOTAL|TRANSPORT|HST|TOTAL|Paiement|Conditions)', next_line):
                        break
                    block_lines.append(next_line)

                block = ' '.join(block_lines)

                # Color
                color = self.extract_color_from_text(block)

                price = 0.0
                unit_price = 0.0

                # Find all decimal numbers in the block
                all_nums = re.findall(r'\b(\d{1,3}(?:,\d{3})*\.\d{2})\b', block)
                # Convert to floats, stripping commas
                float_nums = []
                for n in all_nums:
                    try:
                        float_nums.append(float(n.replace(',', '')))
                    except ValueError:
                        pass

                non_qty = [n for n in float_nums if not (n == round(n) and n > 50)]

                if len(non_qty) >= 2:
                    unit_price = non_qty[-2]  # Prix column = second to last
                    price = non_qty[-1]        # Total column = last
                elif len(non_qty) == 1:
                    unit_price = non_qty[0]
                    price = non_qty[0]
                elif float_nums:
                    # All numbers were qty-like — take last two as fallback
                    unit_price = float_nums[-2] if len(float_nums) >= 2 else float_nums[-1]
                    price = float_nums[-1]

                print(f"  Found: {product_code} | {color} | unit=${unit_price:.2f} | total=${price:.2f}")
                items.append(LineItem(product_code=product_code, color=color, price=price, unit_price=unit_price))

            i += 1

        # Total — SOUS-TOTAL 
        st_match = re.search(r'SOUS-TOTAL\s*:\s*\$([\d,]+\.\d{2})', text)
        if st_match:
            try:
                total = float(st_match.group(1).replace(',', ''))
            except ValueError:
                pass

        # Fallback
        if total == 0.0:
            total_match = re.search(r'TOTAL\s+\$([\d,]+\.\d{2})\s*CAD', text)
            if total_match:
                try:
                    total = float(total_match.group(1).replace(',', ''))
                except ValueError:
                    pass

        print(f"  Items: {len(items)}, Total: ${total:.2f}\n")
        return OrderDocument(po_number=po_number, line_items=items, total=total)


    # MATCHING  — 4 criteria, need 3/4 to pass
    def codes_match(self, c1: str, c2: str) -> bool:
        c1, c2 = self.normalize_code(c1), self.normalize_code(c2)
        if c1 == c2:
            return True
        # Allow fuzzy: e.g. "4553-600ML" vs "4553-600ML"
        ratio = SequenceMatcher(None, c1, c2).ratio()
        return ratio >= 0.90

    def match_documents(self, dalmen: OrderDocument, adfast: OrderDocument) -> Dict:
        log = []
        log.append("=" * 60)
        log.append("ADFAST ORDER MATCHING REPORT")
        log.append("=" * 60)

        # Criteria 1: PO Number 
        po_match = (dalmen.po_number != "Unknown" and
                    adfast.po_number != "Unknown" and
                    dalmen.po_number == adfast.po_number)
        log.append(f"\n[1] PO NUMBER")
        log.append(f"    Dalmen : {dalmen.po_number}")
        log.append(f"    ADFAST : {adfast.po_number}")
        log.append(f"    Result : {'✅ MATCH' if po_match else '❌ NO MATCH'}")

        log.append(f"\n[2/3/4] LINE ITEM MATCHING  (need 3 of 4 criteria per item)")
        log.append("-" * 60)

        matched_items = 0
        unmatched_dalmen = []
        used_adfast = set()
        all_color_ok = []
        all_price_ok = []

        # For each Dalmen item, find the best ADFAST item
        for d_item in dalmen.line_items:
            best_adfast = None
            best_score = -1
            best_detail = {}

            for idx, a_item in enumerate(adfast.line_items):
                if idx in used_adfast:
                    continue

                detail = {}

                # Code
                code_ok = self.codes_match(d_item.product_code, a_item.product_code)
                detail['code'] = ('✅', d_item.product_code, a_item.product_code) if code_ok else ('❌', d_item.product_code, a_item.product_code)

                # Color
                if d_item.color and a_item.color:
                    color_ok = d_item.color.upper() == a_item.color.upper()
                elif not d_item.color and not a_item.color:
                    color_ok = True   # both missing means not penalized
                else:
                    color_ok = False  # one has color, other doesn't
                detail['color'] = ('✅', d_item.color, a_item.color) if color_ok else ('❌', d_item.color, a_item.color)

                # Price — compare line totals
                d_unit = d_item.price
                a_unit = a_item.price
                if d_unit > 0 and a_unit > 0:
                    tol = max(d_unit, a_unit) * 0.02
                    price_ok = abs(d_unit - a_unit) <= tol
                elif d_unit == 0 and a_unit == 0:
                    price_ok = True
                else:
                    price_ok = False
                detail['price'] = ('✅', d_unit, a_unit) if price_ok else ('❌', d_unit, a_unit)

                score = sum([code_ok, color_ok, price_ok])
                if score > best_score:
                    best_score = score
                    best_adfast = (idx, a_item)
                    best_detail = detail

            # Criterion counts: PO (shared) + code + color + price = 4 total
            # For this item: code + color + price can contribute up to 3.
            criteria_met = (1 if po_match else 0) + best_score
            item_passes = criteria_met >= 3

            a_code = best_adfast[1].product_code if best_adfast else "—"
            a_color = best_adfast[1].color if best_adfast else "—"
            a_unit = best_adfast[1].price if best_adfast else 0.0
            d_unit = d_item.price

            log.append(f"\n  Dalmen: {d_item.product_code} | {d_item.color} | total=${d_unit:.2f}")
            log.append(f"  ADFAST: {a_code} | {a_color} | total=${a_unit:.2f}")
            log.append(f"  Criteria met: {criteria_met}/4  (PO={'✅' if po_match else '❌'}  "
                       f"Code={best_detail.get('code',('?','',''))[0]}  "
                       f"Color={best_detail.get('color',('?','',''))[0]}  "
                       f"Price={best_detail.get('price',('?','',''))[0]})")
            log.append(f"  → {'✅ PASS' if item_passes else '❌ FAIL'}")

            if item_passes and best_adfast:
                matched_items += 1
                used_adfast.add(best_adfast[0])
                all_color_ok.append(best_detail.get('color', ('❌',))[0] == '✅')
                all_price_ok.append(best_detail.get('price', ('❌',))[0] == '✅')
            else:
                unmatched_dalmen.append(d_item)
                all_color_ok.append(False)
                all_price_ok.append(False)

        total_items = len(dalmen.line_items)
        match_pct = (matched_items / total_items * 100) if total_items > 0 else 0
        overall_match = matched_items == total_items  # all items have to pass

        log.append("\n" + "=" * 60)
        log.append("SUMMARY")
        log.append("=" * 60)
        log.append(f"  PO Match   : {'YES' if po_match else 'NO'}")
        log.append(f"  Items      : {matched_items} / {total_items} passed")
        log.append(f"  Confidence : {match_pct:.1f}%")
        log.append(f"  DOCUMENTS  : {'✅ MATCH' if overall_match else '❌ DO NOT MATCH'}")

        if unmatched_dalmen:
            log.append("\nUnmatched Dalmen items:")
            for it in unmatched_dalmen:
                log.append(f"  • {it.product_code} | {it.color} | ${it.price:.2f}")

        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        return {
            "match": overall_match,
            "confidence": match_pct,
            "matched_items": matched_items,
            "total_items": total_items,
            "po1": dalmen.po_number,
            "po2": adfast.po_number,
            "total1": dalmen.total,
            "total2": adfast.total,
            "color_match": all(all_color_ok) if all_color_ok else False,
            "price_match": all(all_price_ok) if all_price_ok else False,
        }


    # UI DISPLAY

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

        # icon + verdict + confidence
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

        po_icon = "✅" if result['po1'] == result['po2'] else "❌"
        color_icon = "✅" if result.get('color_match') else "❌"
        price_icon = "✅" if result.get('price_match') else "❌"
        stat_box(stats, "PO Number",     f"{po_icon}  {result['po1']} / {result['po2']}", 0)
        stat_box(stats, "Items Matched", f"{result['matched_items']} / {result['total_items']}", 1)
        stat_box(stats, "Color",         f"{color_icon}  {'Match' if result.get('color_match') else 'No Match'}", 2)
        stat_box(stats, "Price",         f"{price_icon}  {'Match' if result.get('price_match') else 'No Match'}", 3)

        # ── View Log button ──────────────────────────────────────────
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