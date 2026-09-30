#!/usr/bin/env python3
"""Documentation consistency checker for the TRADING RISK LAB Phase-0 constitution.

This is a documentation linter. It contains no trading logic, no market or broker
access, no order handling and performs no network access. It reads Markdown files
under docs/ and reports:

  1. deliverable presence (01..14)
  2. cross-reference closure (T-, RQ-, D-, H, G, FM-, RT-, F###, DC-, OC-, E-, DT-, L-, S-, A-, REV-, AUD-)
  3. symbol closure: UNREGISTERED_SYMBOLS, DUPLICATE_MEANING_SYMBOLS, registry row completeness
  4. formula closure: display equations tagged with a formula ID; ":=" definitions tagged;
     formula-registry rows complete; referenced IDs exist
  5. dimensional audit: every formula-registry `dim:` expression is dimensionally consistent
     under the canonical dimension table in 03; dimension table agrees with registry units
  6. bibliography counts
  7. repository content: no files other than Markdown and this checker

Usage:  python3 tools/doccheck/check_constitution.py [--verbose]
Exit status 0 iff every gate count is zero.
"""
import ast
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CDIR = ROOT / "docs" / "constitution"
VERBOSE = "--verbose" in sys.argv

EXPECTED = {
    "01": "Mathematical Constitution", "02": "Symbol Registry", "03": "Units", "04": "Assumption",
    "05": "Wealth Dynamics", "06": "Hard-Safety Architecture", "07": "Research Questions",
    "08": "Theorem Register", "09": "Failure Modes", "10": "Alternative", "11": "Literature",
    "12": "Roadmap", "13": "Next Task", "14": "Formula Registry",
}

# ---------------------------------------------------------------- loading
def load_docs():
    docs = {}
    for p in sorted(CDIR.glob("*.md")):
        docs[p.name] = p.read_text(encoding="utf-8")
    return docs

FENCE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")

def strip_code(text):
    text = FENCE.sub(" ", text)
    return INLINE_CODE.sub(" ", text)

def math_segments(text):
    """Return list of (is_display, content). Handles escaped dollars."""
    t = strip_code(text).replace(r"\$", "\x00")
    out = []
    for m in re.finditer(r"\$\$(.+?)\$\$", t, re.S):
        out.append((True, m.group(1)))
    t2 = re.sub(r"\$\$(.+?)\$\$", " ", t, flags=re.S)
    for m in re.finditer(r"\$([^$\n]+?)\$", t2):
        out.append((False, m.group(1)))
    return out

# ---------------------------------------------------------------- tokenizer
GREEK = ("alpha beta gamma Gamma delta Delta epsilon varepsilon zeta eta theta Theta vartheta iota kappa varkappa "
         "lambda Lambda mu nu xi Xi pi Pi varpi rho varrho sigma Sigma varsigma tau upsilon Upsilon phi Phi varphi "
         "chi psi Psi omega Omega ell").split()
OPERATORS = set("""max min inf sup log exp lim arg det dim sqrt frac sum prod int partial lfloor rfloor lceil rceil
 le ge leq geq lt gt ne neq in notin subseteq subset supseteq cup cap bigcup bigcap setminus times cdot cdots dots ldots
 to mapsto rightarrow Rightarrow Leftrightarrow longrightarrow iff implies land lor wedge vee bigwedge bigvee neg
 forall exists mid lvert rvert vert lVert rVert langle rangle circ pm mp approx sim propto equiv infty emptyset varnothing
 star ast prime quad qquad text textbf mathbf mathrm operatorname boxed underbrace overbrace left right big Big bigg Bigg
 displaystyle textstyle hat bar tilde widehat widetilde check dot ddot vec overline underline sqrt
 not colon ge le gg ll uparrow downarrow top bot perp nabla oplus otimes checkmark""".split())
UNIT_NAMES = {"USD", "sh", "T", "day", "unit"}
NAMED_OK = {"sgn", "RN", "arg"}  # operator names written with \operatorname / \mathrm

class Tok:
    def __init__(self, s):
        self.s = s
        self.i = 0

def _group(tk):
    """Read a {...} group or a single token after ^ or _; return raw string."""
    s, i = tk.s, tk.i
    while i < len(s) and s[i] == " ":
        i += 1
    if i >= len(s):
        tk.i = i
        return ""
    if s[i] == "{":
        depth, j = 0, i
        while j < len(s):
            if s[j] == "{":
                depth += 1
            elif s[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        tk.i = j + 1
        return s[i + 1:j]
    if s[i] == "\\":
        m = re.match(r"\\[A-Za-z]+", s[i:])
        if m:
            tk.i = i + len(m.group(0))
            return m.group(0)
        tk.i = i + 2
        return s[i:i + 2]
    tk.i = i + 1
    return s[i]

def _label_of(sup):
    sup = sup.strip()
    m = re.fullmatch(r"\\mathrm\{([^}]*)\}", sup)
    if m:
        return m.group(1).replace(" ", "")
    m = re.fullmatch(r"\\mathrm\{([^}]*)\},?\s*\\mathrm\{([^}]*)\}", sup)
    if m:
        return m.group(1) + "," + m.group(2)
    if sup in ("*", r"\star", r"\ast"):
        return "*"
    if sup == r"\varnothing":
        return "∅"
    if sup == r"\log":
        return "log"
    if sup in ("\\prime", "'"):
        return "'"
    if re.fullmatch(r"[A-Za-z]", sup):
        return sup
    if re.fullmatch(r"\(\d\)", sup):
        return sup
    return None  # exponent / expression / positive part

def tokenize(math):
    """Return (principal_keys, index_keys) for a math string."""
    s = math.replace("\x00", "$")
    s = re.sub(r"\\text(?:bf|it)?\{[^{}]*\}", " ", s)
    s = re.sub(r"\\operatorname\{([^}]*)\}", lambda m: " \\OPNAME{" + m.group(1) + "} ", s)
    s = re.sub(r"\\frac\{d\}\{d", r"\\frac{}{", s)       # derivative operator d/d
    s = re.sub(r"\[\\mathrm\{[^}]*\}(?:[/^][^\]]*)?\]", " ", s)  # unit brackets like [\mathrm{USD}/...]
    s = re.sub(r"\\(?:,|;|:|!| |quad|qquad)", " ", s)
    principal, index = [], []
    tk = Tok(s)
    while tk.i < len(s):
        c = s[tk.i]
        key = None
        accent = ""
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+)", s[tk.i:])
            if not m:
                tk.i += 2
                continue
            name = m.group(1)
            tk.i += len(m.group(0))
            if name in ("hat", "bar", "tilde", "widehat", "widetilde", "overline"):
                inner = _group(tk).strip()
                sub_p, sub_i = tokenize(inner)
                if len(sub_p) == 1:
                    key = f"{name.replace('wide','').replace('overline','bar')}:{sub_p[0]}"
                else:
                    principal += sub_p
                    index += sub_i
                    continue
            elif name in ("mathcal", "mathbb", "mathfrak", "mathsf", "mathbf"):
                inner = _group(tk).strip()
                key = f"{name}:{inner}"
            elif name == "mathrm":
                inner = _group(tk).strip()
                if inner in UNIT_NAMES:
                    continue
                key = f"mathrm:{inner}"
            elif name == "OPNAME":
                inner = _group(tk).strip()
                key = f"op:{inner}"
            elif name in GREEK:
                key = name
            elif name in OPERATORS:
                continue
            else:
                key = f"macro:{name}"
        elif c.isalpha():
            key = c
            tk.i += 1
        else:
            tk.i += 1
            continue
        # scripts
        label_parts = []
        while tk.i < len(s) and s[tk.i] in "^_'":
            ch = s[tk.i]
            tk.i += 1
            if ch == "'":
                label_parts.append("'")
                continue
            grp = _group(tk)
            if ch == "^":
                lab = _label_of(grp)
                if lab is not None and not (lab in ("'",) and False):
                    label_parts.append("^" + lab)
                else:
                    p2, i2 = tokenize(grp)
                    index += p2 + i2
            else:
                mm = re.fullmatch(r"\s*\\mathrm\{([^}]*)\}\s*", grp)
                if mm:
                    label_parts.append("_" + mm.group(1))
                else:
                    p2, i2 = tokenize(grp)
                    index += p2 + i2
        if key.startswith("mathcal:A") and label_parts == [] and tk.i < len(s):
            pass
        full = key + "".join(sorted(label_parts))
        principal.append(full)
    return principal, index

def keys_in(math):
    p, i = tokenize(math)
    return p + i

# ---------------------------------------------------------------- registry
def md_tables(text):
    """Yield (section_heading, header_cells, rows) for pipe tables."""
    lines = text.splitlines()
    section = ""
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("#"):
            section = ln.strip("# ").strip()
        if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[-| :]+\|$", lines[i + 1].strip()):
            header = split_row(ln)
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            yield section, header, rows
            i = j
            continue
        i += 1

def split_row(line):
    line = line.strip()
    cells, cur, depth, in_math = [], "", 0, False
    k = 0
    body = line[1:-1] if line.endswith("|") else line[1:]
    while k < len(body):
        ch = body[k]
        if ch == "\\" and k + 1 < len(body) and body[k + 1] == "|":
            cur += "|"
            k += 2
            continue
        if ch == "|" and not in_math:
            cells.append(cur.strip())
            cur = ""
        else:
            if ch == "$":
                in_math = not in_math
            cur += ch
        k += 1
    cells.append(cur.strip())
    return cells

REG_COLS = ["ID", "Symbol", "Meaning", "Type", "Domain", "Codomain", "Units", "Sign", "Valid range", "Source", "Class"]

def load_registry(reg_text):
    rows = []  # (id, section, cells-dict, keys, scope)
    for section, header, trs in md_tables(reg_text):
        if len(header) < 2 or header[0] != "ID" or header[1] not in ("Symbol",):
            if not (header and header[0] == "Scope"):
                continue
        for r in trs:
            d = dict(zip(header, r))
            sid = d.get("ID", "")
            if not re.match(r"S-\d+", sid):
                continue
            sym = d.get("Symbol", "")
            ks = []
            for disp, seg in math_segments(sym):
                p, _ = tokenize(seg)
                ks += p
            rows.append({"id": sid, "section": section, "cells": d, "keys": ks, "scope": d.get("Scope", "").strip()})
    return rows

# ---------------------------------------------------------------- scopes
def scopes_of(docname, text):
    """Split a doc into (scope_name, text). 08 is split per theorem block."""
    short = docname[:2]
    if short == "08":
        parts = re.split(r"(?m)^(### (?:T-\d+|OPEN-\d+)[^\n]*)$", text)
        out = [("08", parts[0])]
        for k in range(1, len(parts), 2):
            tid = re.match(r"### ((?:T-\d+|OPEN-\d+))", parts[k]).group(1)
            out.append((f"08:{tid}", parts[k] + parts[k + 1]))
        return out
    return [(short, text)]

# ---------------------------------------------------------------- dimensions
BASES = ("USD", "sh", "day", "T", "unit")

def parse_dim(s):
    s = s.strip()
    if s in ("1", "[1]"):
        return {}
    s = s.strip("[]")
    dims = collections.Counter()
    num, den = (s.split("/", 1) + [""])[:2] if "/" in s else (s, "")
    for part, sign in ((num, 1), (den, -1)):
        for f in re.findall(r"([A-Za-z]+)(?:\^\(?(-?\d+(?:/\d+)?)\)?)?", part):
            base, exp = f
            if base == "1":
                continue
            if base not in BASES:
                raise ValueError(f"unknown base {base} in {s}")
            e = eval(exp) if exp else 1
            dims[base] += sign * e
    return {k: v for k, v in dims.items() if v}

def registry_units_dim(u):
    u = u.replace("$", "").replace("_i", "").replace("^{", "^(").replace("}", ")").replace(" ", "")
    m = re.fullmatch(r"\[([^\]]*)\]", u)
    if not m:
        return None
    return parse_dim(m.group(1))

class DimError(Exception):
    pass

def dim_eval(node, table):
    if isinstance(node, ast.Expression):
        return dim_eval(node.body, table)
    if isinstance(node, ast.Constant):
        return {}
    if isinstance(node, ast.Name):
        if node.id not in table:
            raise DimError(f"unknown name {node.id}")
        return dict(table[node.id])
    if isinstance(node, ast.UnaryOp):
        return dim_eval(node.operand, table)
    if isinstance(node, ast.BinOp):
        a, b = dim_eval(node.left, table), dim_eval(node.right, table)
        if isinstance(node.op, (ast.Add, ast.Sub)):
            if a != b:
                raise DimError(f"add/sub mismatch {a} vs {b} at {ast.unparse(node)}")
            return a
        if isinstance(node.op, ast.Mult):
            c = collections.Counter(a); c.update(b)
            return {k: v for k, v in c.items() if v}
        if isinstance(node.op, ast.Div):
            c = collections.Counter(a); c.subtract(b)
            return {k: v for k, v in c.items() if v}
        if isinstance(node.op, ast.Pow):
            if not isinstance(node.right, ast.Constant):
                if b:
                    raise DimError("non-constant exponent with dimension")
                if a:
                    raise DimError(f"dimensioned base with symbolic exponent at {ast.unparse(node)}")
                return {}
            from fractions import Fraction
            e = Fraction(str(node.right.value))
            return {k: v * e for k, v in a.items() if v * e}
    if isinstance(node, ast.Compare):
        d0 = dim_eval(node.left, table)
        for comp in node.comparators:
            d1 = dim_eval(comp, table)
            if d0 != d1:
                raise DimError(f"comparison mismatch {d0} vs {d1} at {ast.unparse(node)}")
        return {}
    if isinstance(node, ast.Call):
        fn = node.func.id if isinstance(node.func, ast.Name) else "?"
        args = [dim_eval(a, table) for a in node.args]
        if fn in ("min", "max", "floor", "ceil", "pos", "abs", "E", "ES", "VaR", "inf", "sup", "argmax", "sum_t", "sum_j", "sum_k", "lattice_floor"):
            for a in args[1:]:
                if a != args[0]:
                    raise DimError(f"{fn} arguments differ {args}")
            return args[0] if args else {}
        if fn == "sum_i":   # sum across instruments: shares of different instruments are incommensurable
            if any(k == "sh" for k in args[0]):
                raise DimError(f"sum over instruments of a share-dimensioned term at {ast.unparse(node)}")
            return args[0]
        if fn in ("log", "exp", "P", "ind"):
            if fn in ("log", "exp") and args[0]:
                raise DimError(f"{fn} of dimensioned argument {args[0]} at {ast.unparse(node)}")
            return {}
        if fn == "sqrt":
            from fractions import Fraction
            return {k: v * Fraction(1, 2) for k, v in args[0].items()}
        raise DimError(f"unknown function {fn}")
    raise DimError(f"unsupported syntax {ast.dump(node)[:60]}")

def load_dimtable(units_text):
    m = re.search(r"```dimtable\n(.*?)```", units_text, re.S)
    table, sids = {}, {}
    if not m:
        return None, None
    for ln in m.group(1).splitlines():
        ln = ln.split("#")[0].strip()
        if not ln:
            continue
        name, sid, dim = ln.split(None, 2)
        table[name] = parse_dim(dim)
        sids[name] = sid
    return table, sids

# ---------------------------------------------------------------- main
def main():
    docs = load_docs()
    report = collections.OrderedDict()
    # 1. deliverables
    missing = []
    for num, word in EXPECTED.items():
        f = [n for n in docs if n.startswith(num + "-")]
        if not f or word.lower().split()[0] not in docs[f[0]].splitlines()[0].lower():
            missing.append(f"{num} ({word})")
    report["MISSING_DELIVERABLES"] = missing

    # 2. cross references
    allt = "\n".join(docs.values()) + (ROOT / "README.md").read_text(encoding="utf-8")
    review_dir = ROOT / "docs" / "review" / "phase0"
    review_text = "\n".join(p.read_text(encoding="utf-8") for p in sorted(review_dir.glob("*.md"))) if review_dir.exists() else ""
    d = lambda n: docs.get(next((k for k in docs if k.startswith(n)), ""), "")
    defs = {
        "T": set(re.findall(r"### (T-\d+[a-z]?)\b", d("08"))),
        "RQ": set(re.findall(r"\| (RQ-\d+) \|", d("07"))),
        "D": set(re.findall(r"\| (D-\d+) \|", d("04"))),
        "H": set(re.findall(r"\| (H\d+) \|", d("06"))),
        "G": set(re.findall(r"\b(G\d+)\b", d("06"))),
        "FM": set(re.findall(r"\| (FM-[A-Z]+-\d+) \|", d("09"))),
        "RT": set(re.findall(r"\| (RT-\d+) \|", d("09"))),
        "F": set(re.findall(r"\| (F\d{3}) \|", d("14"))),
        "DC": set(re.findall(r"\| (DC-\d+)(?: \(revised\))? \|", d("05"))),
        "OC": set(re.findall(r"\| (OC-\d+) \|", d("05"))),
        "E": set(re.findall(r"\| (E-\d+) \|", d("03"))),
        "DT": set(re.findall(r"\| (DT-\d+) \|", d("03"))),
        "L": set(re.findall(r"\| (L-\d+) \|", d("11"))),
        "S": set(re.findall(r"\| (S-\d+) \|", d("02"))),
        "A": set(re.findall(r"\| (A-[A-Z]+(?:-\d+)?) \|", d("04"))),
        "REV": set(re.findall(r"^### (REV-\d{3})", review_text, re.M)),
        "AUD": set(re.findall(r"^### (AUD-\d{3})", review_text, re.M)),
    }
    pats = {"T": r"\bT-\d+[a-z]?\b", "RQ": r"\bRQ-\d+", "D": r"\bD-\d+\b", "H": r"\bH\d+\b", "G": r"\bG\d+\b",
            "FM": r"\bFM-[A-Z]+-\d+", "RT": r"\bRT-\d+", "F": r"\bF\d{3}\b", "DC": r"\bDC-\d+", "OC": r"\bOC-\d+",
            "E": r"(?<![A-Z-])E-\d+\b", "DT": r"\bDT-\d+", "L": r"(?<![A-Z-])L-\d+\b", "S": r"\bS-\d+",
            "A": r"\bA-(?:SCOPE|ACC|AUTH|MKT|STOPLIVE|STOP|TRIG|GAP|LIQ|EXE|STAT|NLA|NUM|TIME|SET|FLOW|MATH)(?:-\d+)?\b",
            "REV": r"\bREV-\d{3}\b", "AUD": r"\bAUD-\d{3}\b"}
    xref = []
    for k, pat in pats.items():
        used = set(re.findall(pat, allt + review_text))
        if k in ("REV", "AUD") and not review_text:
            continue
        miss = sorted(u for u in used if u not in defs[k])
        if k == "F" and not defs["F"]:
            miss = []  # no formula registry yet
        xref += [f"{k}:{m}" for m in miss]
    report["UNDEFINED_CROSS_REFERENCES"] = xref

    # 3. symbols
    reg_rows = load_registry(d("02"))
    glob, local = collections.defaultdict(list), collections.defaultdict(list)
    for r in reg_rows:
        for kk in r["keys"]:
            (local if r["scope"] else glob)[kk].append(r)
    dup = sorted(f"{k} -> {', '.join(x['id'] for x in v)}" for k, v in glob.items() if len({x['id'] for x in v}) > 1)
    report["DUPLICATE_MEANING_SYMBOLS"] = dup
    incomplete = []
    for r in reg_rows:
        need = [c for c in REG_COLS if c not in r["cells"] or not r["cells"][c].strip()]
        if r["scope"] == "" and need:
            incomplete.append(f"{r['id']}: missing {need}")
        if r["scope"] and [c for c in REG_COLS[1:] if c not in r["cells"] or not r["cells"][c].strip()]:
            incomplete.append(f"{r['id']}: missing columns")
    report["INCOMPLETE_REGISTRY_ROWS"] = incomplete
    unreg = collections.defaultdict(set)
    for name, text in docs.items():
        for scope, body in scopes_of(name, text):
            for disp, seg in math_segments(body):
                for kk in keys_in(seg):
                    if kk.startswith("op:") and kk[3:] in NAMED_OK:
                        continue
                    if kk in glob:
                        continue
                    if any(scope == r["scope"] or scope.startswith(r["scope"] + ":") or r["scope"] == scope.split(":")[0] and ":" not in r["scope"]
                           for r in local.get(kk, [])):
                        continue
                    unreg[kk].add(scope)
    report["UNREGISTERED_SYMBOLS"] = sorted(f"{k} [{', '.join(sorted(v))}]" for k, v in unreg.items())
    shadows = sorted(f"{k} (local {', '.join(sorted({r['scope'] for r in v}))})" for k, v in local.items() if k in glob)
    report["_SHADOWED_LOCAL_SYMBOLS (explicitly namespaced)"] = shadows

    # 4. formula closure
    fdoc = d("14")
    untagged = []
    for name, text in docs.items():
        if name.startswith("14") or name.startswith("02"):
            continue
        t = strip_code(text)
        for m in re.finditer(r"\$\$(.+?)\$\$", t, re.S):
            after = t[m.end():m.end() + 160]
            if not re.search(r"\[F\d{3}(?:[–,-]F?\d{3})*\]", after):
                untagged.append(f"{name}: {m.group(1).strip()[:50]}...")
        for dispflag, seg in math_segments(text):
            if ":=" in seg and not dispflag:
                pos = t.find(seg)
                ctx = t[pos:pos + len(seg) + 200] if pos >= 0 else ""
                if not re.search(r"\[F\d{3}\]", ctx):
                    untagged.append(f"{name}: inline definition {seg[:50]}")
    report["UNTAGGED_EQUATIONS"] = untagged if fdoc else ["formula registry 14 missing"]
    frows = []
    if fdoc:
        for section, header, rows in md_tables(fdoc):
            if header and header[0] == "ID":
                for r in rows:
                    frows.append(dict(zip(header, r)))
    fbad = []
    FCOLS = ["ID", "Formula", "Purpose", "Variables", "Units", "Assumptions", "Dependencies", "Proof status",
             "Counterexample status", "Research status", "Location", "dim"]
    for r in frows:
        miss = [c for c in FCOLS if not r.get(c, "").strip()]
        if miss:
            fbad.append(f"{r.get('ID')}: missing {miss}")
    report["INCOMPLETE_FORMULA_ROWS"] = fbad
    # formula ids used in docs but never located
    unlocated = []
    for r in frows:
        fid = r["ID"]
        if not any(fid in text for n, text in docs.items() if not n.startswith("14")):
            unlocated.append(fid)
    report["FORMULAS_NOT_REFERENCED_IN_ANY_DOCUMENT"] = unlocated

    # 5. dimensions
    table, sids = load_dimtable(d("03"))
    dimerr = []
    if table is None:
        dimerr.append("no dimtable in 03")
    else:
        regmap = {r["id"]: r for r in reg_rows}
        for name, sid in sids.items():
            if sid == "-":
                continue
            if sid not in regmap:
                dimerr.append(f"dimtable {name}: {sid} not in registry")
                continue
            ru = registry_units_dim(regmap[sid]["cells"].get("Units", ""))
            if ru is not None and ru != table[name]:
                dimerr.append(f"dimtable {name} {table[name]} != registry {sid} units {regmap[sid]['cells'].get('Units')}")
        for r in frows:
            expr = r.get("dim", "").strip().strip("`").strip()
            if not expr or expr.startswith("n/a"):
                if not expr.startswith("n/a"):
                    dimerr.append(f"{r['ID']}: no dim expression")
                continue
            for part in expr.split(";"):
                part = part.strip()
                if not part:
                    continue
                try:
                    dim_eval(ast.parse(part, mode="eval"), table)
                except (DimError, SyntaxError) as e:
                    dimerr.append(f"{r['ID']}: {e}")
    report["DIMENSIONAL_CONFLICTS"] = dimerr

    # 6. bibliography
    lit = d("11")
    sec = lit[lit.find("## 1."):lit.find("## 2.")]
    entries = []
    for p in sec.split("\n\n"):
        if p.startswith("**"):
            body = re.sub(r"^\*\*.+?\*\*\s*", "", p).replace("\n", " ")
            entries += [x.strip() for x in body.split(" · ") if x.strip()]
    titles = collections.Counter((re.search(r"\*(.+?)\*", e).group(1).lower() if re.search(r"\*(.+?)\*", e) else e) for e in entries)
    report["_BIBLIOGRAPHY_TOTAL"] = [str(len(entries))]
    report["BIBLIOGRAPHY_DUPLICATES"] = [t for t, c in titles.items() if c > 1]

    # 7. repository content
    other = []
    for p in ROOT.rglob("*"):
        if ".git" in p.parts or p.is_dir():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel.endswith(".md") or rel == "tools/doccheck/check_constitution.py":
            continue
        other.append(rel)
    report["NON_DOCUMENTATION_FILES"] = other
    bad_imports = []
    for p in ROOT.rglob("*.py"):
        src = p.read_text(encoding="utf-8")
        for kw in ("alpaca", "requests", "urllib", "socket", "http.client", "websocket", "broker"):
            if re.search(rf"^\s*(import|from)\s+{re.escape(kw)}", src, re.M):
                bad_imports.append(f"{p.name}: {kw}")
    report["FORBIDDEN_IMPORTS"] = bad_imports

    # print
    total = 0
    for k, v in report.items():
        gate = not k.startswith("_")
        n = len(v) if gate else v[0] if k == "_BIBLIOGRAPHY_TOTAL" else len(v)
        if gate:
            total += len(v)
        print(f"{k} = {n}")
        if v and (VERBOSE or gate):
            for x in (v if VERBOSE else v[:400]):
                if k != "_BIBLIOGRAPHY_TOTAL":
                    print(f"    {x}")
    print(f"GATE_TOTAL = {total}")
    return 0 if total == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
