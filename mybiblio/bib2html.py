#!/usr/bin/env python3
"""
bib2html.py — generate the research.html publication blocks from references.bib.

The bibliography in references.bib is the single source of truth. This script
renders it into the exact .pub HTML used on research.html, so the page never has
to be hand-edited entry by entry.

USAGE
    python3 mybiblio/bib2html.py                      # print all 3 sections
    python3 mybiblio/bib2html.py --section journal    # journal | conference | theses
    python3 mybiblio/bib2html.py --write research.html  # fill marker regions in place

--write needs marker comments in research.html. Add them ONCE, inside each
<div class="section">, replacing the hand-written .pub blocks:

    <div class="section-title">Journal Articles</div>
    <!-- BIBLIO:journal:START -->
    <!-- BIBLIO:journal:END -->

...and likewise BIBLIO:conference and BIBLIO:theses. Everything between a
START/END pair is regenerated; everything else on the page is left untouched.

No third-party dependencies (pure standard library).
"""
import os
import re
import sys
import html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
BIB = os.path.join(HERE, "references.bib")


def esc(s):
    # escape only &, <, > -- these are text nodes, not attributes, so keep
    # apostrophes/quotes literal (matches the hand-written research.html)
    return _html.escape(s, quote=False)


# entry type -> page section
SECTION_OF = {
    "article": "journal",
    "inproceedings": "conference",
    "conference": "conference",
    "phdthesis": "theses",
    "mastersthesis": "theses",
    "masterthesis": "theses",       # tolerate the non-standard spelling
}
THESIS_LABEL = {
    "phdthesis": "PhD thesis",
    "mastersthesis": "Master's thesis",
    "masterthesis": "Master's thesis",
}
SECTIONS = [
    ("journal", "Journal Articles"),
    ("conference", "Conference Papers"),
    ("presentation", "Conference Presentations"),
    ("theses", "Theses"),
]


# ----------------------------------------------------------------- parsing ---
def strip_comments(text):
    # remove everything from the first '%' to end of line (no escaped % in file)
    return "\n".join(line.split("%", 1)[0] for line in text.splitlines())


def parse_bib(text):
    text = strip_comments(text)
    entries, i, n = [], 0, len(text)
    while True:
        at = text.find("@", i)
        if at < 0:
            break
        brace = text.find("{", at)
        etype = text[at + 1:brace].strip().lower()
        comma = text.find(",", brace)
        key = text[brace + 1:comma].strip()
        j, fields = comma + 1, {}
        while j < n:
            while j < n and text[j] in " \t\r\n,":
                j += 1
            if j < n and text[j] == "}":          # end of entry
                j += 1
                break
            eq = text.find("=", j)
            fname = text[j:eq].strip().lower()
            k = eq + 1
            while k < n and text[k] in " \t\r\n":
                k += 1
            if text[k] == "{":                    # brace-delimited value
                depth, start, k = 1, k + 1, k + 1
                while k < n and depth:
                    depth += (text[k] == "{") - (text[k] == "}")
                    if depth:
                        k += 1
                val, k = text[start:k], k + 1
            elif text[k] == '"':                  # quote-delimited value
                start, k = k + 1, k + 1
                while k < n and text[k] != '"':
                    k += 1
                val, k = text[start:k], k + 1
            else:                                 # bare value
                start = k
                while k < n and text[k] not in ",}":
                    k += 1
                val = text[start:k]
            fields[fname] = " ".join(val.split())
            j = k
        entries.append((etype, key, fields))
        i = j
    return entries


# --------------------------------------------------------------- rendering ---
def fmt_authors(field):
    out = []
    for nm in re.split(r"\s+and\s+", field.strip()):
        nm = nm.strip()
        if not nm:
            continue
        if "," in nm:
            last, first = (p.strip() for p in nm.split(",", 1))
            disp = f"{first} {last}".strip()
        else:
            last, disp = nm, nm
        disp = esc(disp)
        out.append(f"<strong>{disp}</strong>" if last == "Di Fabbio" else disp)
    return ", ".join(out)


def venue(etype, f):
    if etype == "article":
        v = f"{f['journal']}, {f['year']}"
        if f.get("volume"):
            v += f", {f['volume']}"
            if f.get("number"):
                v += f"({f['number']})"
        return v
    if etype in THESIS_LABEL:
        parts = [THESIS_LABEL[etype], f["school"], f["year"]]
        if f.get("note"):
            parts.append(f["note"])
        return " · ".join(parts)
    return f"{f['booktitle']}, {f['year']}"


def link_rows(f, c):
    rows = []
    if f.get("doi"):
        d = f["doi"]
        rows.append(f'{c}<div class="pub-doi"><a href="https://doi.org/{d}" '
                    f'target="_blank" rel="noopener">doi: {d}</a></div>')
    elif f.get("url"):
        u = f["url"]
        disp = esc(re.sub(r"^https?://", "", u).rstrip("/"))
        rows.append(f'{c}<div class="pub-doi"><a href="{u}" '
                    f'target="_blank" rel="noopener">{disp}</a></div>')
    href = None
    if f.get("pdf") and os.path.exists(os.path.join(HERE, f["pdf"])):
        href = "mybiblio/" + f["pdf"]            # path relative to site root
    if not href and f.get("oaurl"):
        href = f["oaurl"]
    if href:
        rows.append(f'{c}<div class="pub-links"><a class="pub-link" href="{href}" '
                    f'target="_blank" rel="noopener">PDF</a></div>')
    return rows


def entry_html(etype, key, f):
    ind, c = "    ", "      "                     # match research.html indentation
    out = [f'{ind}<div class="pub" id="pub-{key}">',
           f'{c}<div class="pub-title">{esc(f["title"])}</div>',
           f'{c}<div class="pub-authors">{fmt_authors(f["author"])}</div>',
           f'{c}<div class="pub-venue">{esc(venue(etype, f))}</div>']
    out += link_rows(f, c)
    out.append(f"{ind}</div>")
    return "\n".join(out)


def build():
    entries = parse_bib(open(BIB, encoding="utf-8").read())
    bucket = {sec: [] for sec, _ in SECTIONS}
    for etype, key, f in entries:
        sec = SECTION_OF.get(etype)
        if sec is None:
            sys.stderr.write(f"warning: unknown entry type @{etype} ({key})\n")
            continue
        # a conference entry marked as a talk-only presentation is routed to
        # the "Conference Presentations" section rather than "Conference Papers"
        if sec == "conference" and f.get("presentation", "").strip().lower() in (
            "true", "yes", "1",
        ):
            sec = "presentation"
        bucket[sec].append(entry_html(etype, key, f))
    return bucket


# -------------------------------------------------------------------- main ---
def main(argv):
    bucket = build()
    if "--write" in argv:
        path = argv[argv.index("--write") + 1]
        src = open(path, encoding="utf-8").read()
        for sec, _ in SECTIONS:
            block = "\n\n".join(bucket[sec])
            pat = re.compile(r"(<!-- BIBLIO:%s:START -->).*?(<!-- BIBLIO:%s:END -->)"
                             % (sec, sec), re.S)
            if not pat.search(src):
                sys.stderr.write(f"note: no '{sec}' markers in {path}; skipped\n")
                continue
            src = pat.sub(lambda m: f"{m.group(1)}\n{block}\n    {m.group(2)}", src)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(src)
        print(f"wrote regenerated sections into {path}")
        return
    if "--section" in argv:
        sec = argv[argv.index("--section") + 1]
        print("\n\n".join(bucket[sec]))
        return
    for sec, title in SECTIONS:
        print(f"<!-- ==== {title} ==== -->")
        print("\n\n".join(bucket[sec]))
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
