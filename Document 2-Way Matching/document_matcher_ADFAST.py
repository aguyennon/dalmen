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

        self.progress = ttk.Progressbar(body, mode='indeterminate')

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
            self.display_result(result)

        except Exception as e:
            import traceback
            err = traceback.format_exc()
            print(err)
            self.root.after(0, self.display_error, f"{str(e)}\n\n{err}")


    def parse_document(self, pdf_path: str):
        text = self.extract_pdf_text(pdf_path)
        is_dalmen = "Rapport de commande" in text or "Dalmen Portes" in text
        is_confirmation = "CONFIRMATION DE COMMANDE" in text.upper()
        
        if is_dalmen:
            doc = self.parse_dalmen_order(text)
        else:
            doc = self.parse_adfast_confirmation(text)
        
        doc.is_confirmation = is_confirmation
        return doc


    def extract_pdf_text(self, pdf_path: str) -> str:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def normalize_code(self, code: str) -> str:
        code = code.upper().strip()
        code = re.sub(r'\s*-\s*', '-', code)
        code = re.sub(r'\s+ML', 'ML', code)
        code = re.sub(r'ML\s+', 'ML/', code)
        code = re.sub(r'/ADSEAL$', '', code, flags=re.IGNORECASE)
        return code.strip()

    def extract_color_from_text(self, text: str) -> str:
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

        m = re.search(r'Num[ée]ro de PO[\s\S]{0,60}?(\b\d{3,6}\b)', text, re.IGNORECASE)
        if m:
            candidate = m.group(1).strip()
            if candidate not in ('5630', '2268', '3070', '514', '613'):
                return candidate

        section = re.search(r'Num[ée]ro de PO([\s\S]{0,200})', text, re.IGNORECASE)
        if section:
            numbers = re.findall(r'\b(\d{3,6})\b', section.group(1))
            blacklist = {'5630', '2268', '3070', '514', '613', '524'}
            for num in numbers:
                if num not in blacklist:
                    return num

        return "Unknown"

    def load_adfast_price_list(self) -> Dict[str, float]:
        catalog = {}
        price_list_path = r"\\10.0.7.2\Group\2026 PRICE LIST\ADFAST - Les Produits Dalmen Ltd.pdf"
        try:
            with pdfplumber.open(price_list_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            if not row or len(row) < 2:
                                continue
                            code_cell = str(row[0] or "").strip()
                            price_cell = str(row[-1] or "").strip()
                            if not code_cell or not price_cell:
                                continue
                            if not re.search(r'\d+\s*ml', code_cell, re.IGNORECASE):
                                continue
                            price_str = re.sub(r'[^\d\.]', '', price_cell.replace(',', '.'))
                            try:
                                price = float(price_str)
                                if price <= 0:
                                    continue
                                normalized = self.normalize_adfast_catalog_code(code_cell)
                                catalog[normalized] = price
                            except ValueError:
                                continue
            print(f"Loaded {len(catalog)} ADFAST price list entries")
        except Exception as e:
            print(f"WARNING: Could not load ADFAST price list: {e}")
        return catalog

    def normalize_adfast_catalog_code(self, code: str) -> str:
        code = code.upper().strip()
        code = re.sub(r'\s*-\s*', '-', code)
        code = re.sub(r'\s+', '', code)
        code = re.sub(r'^455[1-9]', '4550', code)
        code = re.sub(r'-?ALL/', '-', code, flags=re.IGNORECASE)
        code = re.sub(r'/ADSEAL$', '', code, flags=re.IGNORECASE)
        code = re.sub(r'\s*ML', 'ML', code)
        return code

    def parse_dalmen_order(self, text: str) -> OrderDocument:
        po_number = self.extract_po_number(text)
        items: List[LineItem] = []
        total = 0.0
        raw_lines = text.split('\n')

        merged_lines = []
        i = 0
        while i < len(raw_lines):
            line = raw_lines[i].strip()

            partial_match = re.match(r'^(\d{4})-\s', line)
            if partial_match and i + 1 < len(raw_lines):
                next_line = raw_lines[i + 1].strip()
                ml_match = re.match(r'^(\d+\s*ml)', next_line, re.IGNORECASE)
                if ml_match:
                    ml_part = ml_match.group(1).replace(' ', '')
                    line = line.replace(
                        partial_match.group(0),
                        f"{partial_match.group(1)}-{ml_part} ",
                        1
                    )
                    i += 2
                    merged_lines.append(line)
                    continue

            if re.match(r'^\d{4}-$', line) and i + 1 < len(raw_lines):
                merged_lines.append(line + raw_lines[i + 1].strip())
                i += 2
                continue

            merged_lines.append(line)
            i += 1

        for line in merged_lines:
            line = line.strip()
            if not line:
                continue

            if re.match(r'^(Code|Pi[eè]ce|Total|Livr[eé]|Command[eé]|Date|Notes|ADFAST)', line, re.IGNORECASE):
                continue

            code_match = re.match(r'^(\d{4}-\d+\s*ml[\w/,]*)', line, re.IGNORECASE)
            if not code_match:
                continue

            raw_code = code_match.group(1)
            product_code = self.normalize_code(raw_code)

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
            items.append(LineItem(product_code=product_code, color=color, price=price, unit_price=unit_price))

        total_match = re.search(r'Total\s*:\s*([\d\s,\.]+)\s*\$', text)
        if total_match:
            ts = total_match.group(1).replace(' ', '').replace(',', '.')
            try:
                total = float(ts)
            except ValueError:
                pass

        return OrderDocument(po_number=po_number, line_items=items, total=total)

    def parse_adfast_confirmation(self, text: str) -> OrderDocument:
        po_number = self.extract_po_number(text)
        items: List[LineItem] = []
        total = 0.0
        lines = text.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            code_match = re.match(r'^(\d{4}-\d+\s*ml[/\w]*)', line, re.IGNORECASE)
            if code_match:
                raw_code = code_match.group(1)
                product_code = self.normalize_code(raw_code)

                block_lines = [line]
                for j in range(i + 1, min(i + 9, len(lines))):
                    next_line = lines[j].strip()
                    if re.match(r'^\d{4}-\d+', next_line):
                        break
                    if re.match(r'^(SOUS-TOTAL|TRANSPORT|HST|TOTAL|Paiement|Conditions)', next_line):
                        break
                    block_lines.append(next_line)

                block = ' '.join(block_lines)
                color = self.extract_color_from_text(block)

                price = 0.0
                unit_price = 0.0

                all_nums = re.findall(r'\b(\d{1,3}(?:,\d{3})*\.\d{2})\b', block)
                float_nums = []
                for n in all_nums:
                    try:
                        float_nums.append(float(n.replace(',', '')))
                    except ValueError:
                        pass

                non_qty = [n for n in float_nums if not (n == round(n) and n > 50)]

                if len(non_qty) >= 2:
                    unit_price = non_qty[-2]
                    price = non_qty[-1]
                elif len(non_qty) == 1:
                    unit_price = non_qty[0]
                    price = non_qty[0]
                elif float_nums:
                    unit_price = float_nums[-2] if len(float_nums) >= 2 else float_nums[-1]
                    price = float_nums[-1]

                items.append(LineItem(product_code=product_code, color=color, price=price, unit_price=unit_price))

            i += 1

        st_match = re.search(r'SOUS-TOTAL\s*:\s*\$([\d,]+\.\d{2})', text)
        if st_match:
            try:
                total = float(st_match.group(1).replace(',', ''))
            except ValueError:
                pass

        if total == 0.0:
            total_match = re.search(r'TOTAL\s+\$([\d,]+\.\d{2})\s*CAD', text)
            if total_match:
                try:
                    total = float(total_match.group(1).replace(',', ''))
                except ValueError:
                    pass

        return OrderDocument(po_number=po_number, line_items=items, total=total)

    def codes_match(self, c1: str, c2: str) -> bool:
        c1, c2 = self.normalize_code(c1), self.normalize_code(c2)
        if c1 == c2:
            return True
        ratio = SequenceMatcher(None, c1, c2).ratio()
        return ratio >= 0.90


    def match_documents(self, doc1, doc2) -> Dict:
        dalmen = doc1
        adfast = doc2

        print(f" DEBUG is_confirmation: {getattr(adfast, 'is_confirmation', 'NOT SET')}")

        log = []

        if not hasattr(self, '_adfast_catalog'):
            self._adfast_catalog = self.load_adfast_price_list()

        po_match = (dalmen.po_number != "Unknown" and
                    adfast.po_number != "Unknown" and
                    dalmen.po_number == adfast.po_number)

        # ── SUMMARY ───────────────────────────────────────────────────────
        log.append("=" * 60)
        log.append("SUMMARY")
        log.append("=" * 60)

        col_width = 38
        log.append(f"{'Doc1 (Dalmen) - ' + str(len(dalmen.line_items)) + ' items':<{col_width}} {'Doc2 (ADFAST) - ' + str(len(adfast.line_items)) + ' items'}")
        log.append("=" * 60)

        for i in range(max(len(dalmen.line_items), len(adfast.line_items))):
            left  = f" {dalmen.line_items[i].product_code} | {dalmen.line_items[i].color}" if i < len(dalmen.line_items) else ""
            right = f"{adfast.line_items[i].product_code} | {adfast.line_items[i].color}" if i < len(adfast.line_items) else ""
            log.append(f"{left:<{col_width}} {right}")

        log.append("")
        po_str = "✅ MATCH" if po_match else "❌ NO MATCH"
        log.append(f" PO Number - Dalmen: {dalmen.po_number} | ADFAST: {adfast.po_number} -> {po_str}")

        # ── MATCHING PROCESS ──────────────────────────────────────────────
        log.append("")
        log.append("=" * 60)
        log.append("MATCHING PROCESS  (need 3 of 4 criteria: PO / Code / Color / Price)")
        log.append("=" * 60)

        matched_items   = 0
        unmatched_dalmen = []
        used_adfast     = set()
        all_color_ok    = []
        all_price_ok    = []

        for d_item in dalmen.line_items:
            best_adfast = None
            best_score  = -1
            best_detail = {}

            for idx, a_item in enumerate(adfast.line_items):
                if idx in used_adfast:
                    continue

                detail   = {}
                code_ok  = self.codes_match(d_item.product_code, a_item.product_code)
                detail['code'] = ('✅', d_item.product_code, a_item.product_code) if code_ok else ('❌', d_item.product_code, a_item.product_code)

                if d_item.color and a_item.color:
                    color_ok = d_item.color.upper() == a_item.color.upper()
                elif not d_item.color and not a_item.color:
                    color_ok = True
                else:
                    color_ok = False
                detail['color'] = ('✅', d_item.color, a_item.color) if color_ok else ('❌', d_item.color, a_item.color)

                d_norm        = self.normalize_adfast_catalog_code(d_item.product_code)
                a_norm        = self.normalize_adfast_catalog_code(a_item.product_code)
                catalog_price = self._adfast_catalog.get(a_norm) or self._adfast_catalog.get(d_norm)

                is_confirmation = getattr(adfast, 'is_confirmation', False)
                if not is_confirmation and catalog_price and a_item.unit_price > 0:
                    tol = catalog_price * 0.03
                    price_ok = abs(a_item.unit_price - catalog_price) <= tol
                    detail['price'] = ('✅', a_item.unit_price, catalog_price) if price_ok else ('❌', a_item.unit_price, catalog_price)
                else:
                    price_ok = True
                    detail['price'] = ('-', 0.0, 0.0)

                score = sum([code_ok, color_ok, price_ok])
                if score > best_score:
                    best_score  = score
                    best_adfast = (idx, a_item)
                    best_detail = detail

            criteria_met = (1 if po_match else 0) + best_score
            item_passes  = criteria_met >= 3

            a_code  = best_adfast[1].product_code if best_adfast else "—"
            a_unit  = best_adfast[1].price if best_adfast else 0.0
            d_unit  = d_item.price

            code_icon  = best_detail.get('code',  ('❌',))[0]
            color_icon = best_detail.get('color', ('❌',))[0]
            price_icon = best_detail.get('price', ('❌',))[0]
            po_icon    = '✅' if po_match else '❌'
            result_str = "✅ PASS" if item_passes else "❌ FAIL"

            log.append("")
            log.append(f" {d_item.product_code:<20} -> {a_code:<20} {result_str}")
            is_confirmation = getattr(adfast, 'is_confirmation', False)
            price_display = f"Price {price_icon}" if not is_confirmation else "Price -"
            log.append(f" PO {po_icon} Code {code_icon} Color {color_icon} {price_display} ({criteria_met}/4 criterias met)")
            if not is_confirmation:
                log.append(f" Dalmen: ${d_unit:<10.2f} ADFAST: ${a_unit:.2f}")

            if item_passes and best_adfast:
                matched_items += 1
                used_adfast.add(best_adfast[0])
                all_color_ok.append(color_icon == '✅')
                all_price_ok.append(price_icon == '✅')
            else:
                unmatched_dalmen.append(d_item)
                all_color_ok.append(False)
                all_price_ok.append(False)

        # ── FINAL RESULT ──────────────────────────────────────────────────
        total_items   = len(dalmen.line_items)
        match_pct     = (matched_items / total_items * 100) if total_items > 0 else 0
        overall_match = matched_items == total_items

        log.append("")
        log.append("=" * 60)
        log.append("FINAL RESULT")
        log.append("=" * 60)
        log.append(f" {matched_items}/{total_items} items passed ({match_pct:.1f}%)")
        log.append(f" Documents match: {'✅ YES' if overall_match else '❌ NO'}")

        if unmatched_dalmen:
            log.append("")
            log.append(" Unmatched Dalmen items:")
            for it in unmatched_dalmen:
                log.append(f" • {it.product_code} | {it.color} | {it.price:.2f}")
        log.append("=" * 60)

        # ── PRICE VERIFICATION ────────────────────────────────────────────
        is_confirmation = getattr(adfast, 'is_confirmation', False)
        print(f"DEBUG price verification gate: is_confirmation={is_confirmation}")
        if not is_confirmation:
            log.append("")
            log.append("=" * 60)
            log.append("PRICE VERIFICATION")
            log.append("=" * 60)

            for d_item in dalmen.line_items:
                d_norm        = self.normalize_adfast_catalog_code(d_item.product_code)
                catalog_price = self._adfast_catalog.get(d_norm)

                adfast_unit = None
                for a_item in adfast.line_items:
                    if self.codes_match(d_item.product_code, a_item.product_code):
                        adfast_unit = a_item.unit_price
                        break

                log.append("")
                if catalog_price and adfast_unit is not None:
                    diff     = abs(adfast_unit - catalog_price)
                    tol      = catalog_price * 0.03
                    price_ok = diff <= tol
                    status   = "✅ PASS" if price_ok else "❌ FAIL"
                    log.append(f"  {d_item.product_code:<20}  PRICE LIST: ${catalog_price:<8.2f}  FACTURE: ${adfast_unit:<8.2f}  Diff: ${diff:.2f}  {status}")
                elif catalog_price:
                    log.append(f"  {d_item.product_code:<20}  PRICE LIST: ${catalog_price:.2f}  — ADFAST price not found")
                else:
                    log.append(f"  {d_item.product_code:<20}  ❌ Not in price list")

        self.match_log = "\n".join(log)
        print("\n" + self.match_log)

        return {
            "match": overall_match,
            "confidence": match_pct,
            "matched_items": matched_items,
            "total_items": total_items,
            "order1": dalmen.po_number,
            "order2": adfast.po_number,
            "po1": dalmen.po_number,
            "po2": adfast.po_number,
            "total1": dalmen.total,
            "total2": adfast.total,
            "color_match": all(all_color_ok) if all_color_ok else False,
            "price_match": all(all_price_ok) if all_price_ok else False,
            "is_confirmation": is_confirmation,
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

        tk.Label(top_row, text=icon, font=("Arial", 28),
                 bg="white").pack(side=tk.LEFT)

        tk.Label(top_row, text=verdict,
                 font=("Arial", 16, "bold"), bg="white", fg=accent
                 ).pack(side=tk.LEFT, padx=12)

        tk.Label(top_row,
                 text=f"{result['confidence']:.0f}% confidence",
                 font=("Arial", 11), bg="white", fg="#666"
                 ).pack(side=tk.RIGHT)

        tk.Frame(inner, bg="#e0e0e0", height=1).pack(fill=tk.X, pady=(14, 14))

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