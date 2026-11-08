"""Mark the held-out questions in the workbook's `split` column (all others stay `development`).

Run once:  python evaluation/set_split.py
The selection is documented in evaluation/heldout_selection.md.
"""
from pathlib import Path

import openpyxl

XLSX = Path(__file__).parent / "text_evaluation_candidates.xlsx"
HELD_OUT = ["Q05", "Q10", "Q19", "Q41",          # text-only: factual, conceptual, insufficient-evidence, cross-paper
            "Q22", "Q26", "Q28",                 # table-only
            "Q33", "Q36", "Q38"]                 # text+table

wb = openpyxl.load_workbook(XLSX)
ws = wb["Questions"]
col = [c.value for c in ws[1]].index("split") + 1
for r in range(2, ws.max_row + 1):
    qid = ws.cell(r, 1).value
    ws.cell(r, col).value = "held-out" if qid in HELD_OUT else "development"
wb.save(XLSX)
print(f"{len(HELD_OUT)} held-out, {ws.max_row - 1 - len(HELD_OUT)} development")
