#!/usr/bin/env python3
"""Mutation suite for the documentation checker (tools/doccheck/check_constitution.py).

Documentation tooling only: no trading logic, no market or broker access, no network. Each mutation copies the
repository's docs/, tools/ and README.md into a temporary directory, injects one known defect into one Markdown
file, runs the checker there, and requires the named gate count to become non-zero. The unmodified copy must
return GATE_TOTAL = 0. Exit status 0 iff every mutation is detected and the clean copy is clean.

Usage:  python3 tools/doccheck/mutation_suite.py
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
C = "docs/constitution/"

# (name, file, anchor, replacement, gate that must fire)
MUTATIONS = [
    ("missing theorem field", C + "08-theorem-register.md",
     "**COUNTEREXAMPLE ATTEMPT.** None; any diversification", "None; any diversification",
     "THEOREMS_MISSING_FIELDS_OR_STATUS"),
    ("status outside vocabulary", C + "08-theorem-register.md",
     "**PROOF STATUS.** PROVED\n\n**PROOF.** Summation", "**PROOF STATUS.** PROVED BY CONSTRUCTION\n\n**PROOF.** Summation",
     "THEOREMS_MISSING_FIELDS_OR_STATUS"),
    ("PROVED citing a market assumption", C + "08-theorem-register.md",
     "**ASSUMPTIONS.** A-MATH-01.\n\n**PROOF STATUS.** PROVED\n\n**PROOF.** Summation",
     "**ASSUMPTIONS.** A-MATH-01; A-GAP.\n\n**PROOF STATUS.** PROVED\n\n**PROOF.** Summation",
     "THEOREM_STATUS_ASSUMPTION_INCONSISTENCIES"),
    ("conditional theorem citing no world assumption", C + "08-theorem-register.md",
     "**ASSUMPTIONS.** Those of T-10 (including case (1′)); attainability and inactive clamps (for (b) and (c) only).",
     "**ASSUMPTIONS.** A-MATH-01; attainability.",
     "THEOREM_STATUS_ASSUMPTION_INCONSISTENCIES"),
    ("unregistered symbol", C + "06-hard-safety-architecture.md",
     "## 1. What", "Extra $\\zeta^{\\mathrm{foo}}_t$ here.\n\n## 1. What", "UNREGISTERED_SYMBOLS"),
    ("dimension error (cushion)", C + "14-formula-registry.md",
     "`K == W - F`", "`K == W - m`", "DIMENSIONAL_CONFLICTS"),
    ("naive floor of shares", C + "14-formula-registry.md",
     "`Q == min(N_bar, delta_q*floor(R/(delta_q*ell)))`", "`Q == min(N_bar, floor(R/ell))`", "DIMENSIONAL_CONFLICTS"),
    ("dimension error (partial-fill charge)", C + "14-formula-registry.md",
     "+ phi_split + phi_buy - phi_paid; g_pf", "+ phi_split + phi_buy - q; g_pf", "DIMENSIONAL_CONFLICTS"),
    ("untagged display equation", C + "06-hard-safety-architecture.md",
     "$$\n[F075]", "$$\n", "UNTAGGED_EQUATIONS"),
    ("untagged := definition", C + "06-hard-safety-architecture.md",
     "**[F094]**", "", "UNTAGGED_EQUATIONS"),
    ("duplicate registry key", C + "02-symbol-registry.md",
     "| S-292 | $\\phi^{\\mathrm{split}}$", "| S-292 | $K_t$", "DUPLICATE_MEANING_SYMBOLS"),
    ("assumption without fail-closed check", C + "04-assumption-and-decision-registry.md",
     "| G9 |", "|  |", "UNRECORDED_ASSUMPTIONS"),
    ("assumption outside the seven classes", C + "04-assumption-and-decision-registry.md",
     "| A-LIQ | Future tradable volume $\\ge$ policy fraction of trailing ADV over the exit horizon | MARKET |",
     "| A-LIQ | Future tradable volume $\\ge$ policy fraction of trailing ADV over the exit horizon | MARKET/PROXY |",
     "UNRECORDED_ASSUMPTIONS"),
    ("undefined theorem reference", C + "06-hard-safety-architecture.md",
     "(T-17a, T-17b)", "(T-99)", "UNDEFINED_CROSS_REFERENCES"),
    ("undefined formula reference", C + "06-hard-safety-architecture.md",
     "**[F044]**", "**[F999]**", "UNDEFINED_CROSS_REFERENCES"),
    ("undefined over-charge reference", C + "05-wealth-dynamics.md",
     "| OC-3 |", "| OC-9 |", "UNDEFINED_CROSS_REFERENCES"),
    ("cost conservation table column renamed", C + "05-wealth-dynamics.md",
     "| Duplicate elsewhere? |", "| Duplicate? |", "COST_CONSERVATION_TABLE_MISSING"),
    ("undefined closure-review reference", C + "06-hard-safety-architecture.md",
     "(critical closure correction, CLOSURE-REV-002)", "(critical closure correction, CLOSURE-REV-099)", "UNDEFINED_CROSS_REFERENCES"),
    ("dimension error (reference wealth)", C + "14-formula-registry.md",
     "`W_R == E - Lam_floor;", "`W_R == E - nu_R;", "DIMENSIONAL_CONFLICTS"),
    ("fee-booking formula row incomplete", C + "14-formula-registry.md",
     "| entry-fee booking state: the booked part is in $W_t$, the owed part is reserved (F144, F145) |", "|  |",
     "INCOMPLETE_FORMULA_ROWS"),
    ("formula row incomplete", C + "14-formula-registry.md",
     "| exposure charge of a partially filled order: exact worst case, realised costs excluded |", "|  |",
     "INCOMPLETE_FORMULA_ROWS"),
    ("quantity-validity formula row incomplete", C + "14-formula-registry.md",
     "| quantity-state validity and fail-closed charge: held quantity, cumulative fill and order quantity are never merged, inferred or defaulted |",
     "|  |", "INCOMPLETE_FORMULA_ROWS"),
    ("dimension error (unfilled remainder)", C + "14-formula-registry.md",
     "`q <= q_fill; q_fill <= n_o; q_unf == n_o - q_fill;", "`q <= q_fill; q_fill <= n_o; q_unf == n_o - phi_paid;",
     "DIMENSIONAL_CONFLICTS"),
    ("unregistered unfilled-remainder symbol", C + "02-symbol-registry.md",
     "| S-309 | $q^{\\mathrm{unf}}_o$ |", "| S-309 | $q^{\\mathrm{zzz}}_o$ |", "UNREGISTERED_SYMBOLS"),
]


def gates(tree):
    out = subprocess.run([sys.executable, "-B", str(tree / "tools/doccheck/check_constitution.py")],
                         capture_output=True, text=True).stdout
    return {line.split(" = ")[0]: int(line.split(" = ")[1]) for line in out.splitlines()
            if re.match(r"^[A-Z_]+ = \d+$", line)}


def fresh(tmp):
    tree = tmp / "repo"
    if tree.exists():
        shutil.rmtree(tree)
    tree.mkdir()
    shutil.copytree(ROOT / "docs", tree / "docs")
    shutil.copytree(ROOT / "tools", tree / "tools", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(ROOT / "README.md", tree / "README.md")
    return tree


def main():
    failed = 0
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        clean = gates(fresh(tmp))
        print(f"clean copy: GATE_TOTAL = {clean.get('GATE_TOTAL')}")
        failed += clean.get("GATE_TOTAL", 1) != 0
        for name, rel, anchor, repl, gate in MUTATIONS:
            tree = fresh(tmp)
            path = tree / rel
            text = path.read_text(encoding="utf-8")
            if anchor not in text:
                print(f"ANCHOR MISSING: {name}")
                failed += 1
                continue
            path.write_text(text.replace(anchor, repl, 1), encoding="utf-8")
            g = gates(tree)
            ok = g.get(gate, 0) > 0 and g.get("GATE_TOTAL", 0) > 0
            failed += not ok
            print(f"{'DETECTED' if ok else 'MISSED  '}  {name}: {gate} = {g.get(gate)}")
        tree = fresh(tmp)
        (tree / "engine.py").write_text("import socket\n", encoding="utf-8")
        g = gates(tree)
        ok = g.get("NON_DOCUMENTATION_FILES", 0) > 0 and g.get("FORBIDDEN_IMPORTS", 0) > 0
        failed += not ok
        print(f"{'DETECTED' if ok else 'MISSED  '}  code file with a network import: NON_DOCUMENTATION_FILES = "
              f"{g.get('NON_DOCUMENTATION_FILES')}, FORBIDDEN_IMPORTS = {g.get('FORBIDDEN_IMPORTS')}")
    total = len(MUTATIONS) + 1
    print(f"MUTATIONS = {total}; UNDETECTED_OR_FAILED = {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
