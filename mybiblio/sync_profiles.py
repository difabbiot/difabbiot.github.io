#!/usr/bin/env python3
"""
sync_profiles.py — propagate mybiblio/references.bib to every place a
publication has to appear: the website, the sitemap, ORCID, ResearchGate,
Google Scholar, PORTO@IRIS and the MSCA blog.

references.bib stays the single source of truth. This script never invents
metadata: it validates what is in the .bib against the publisher record
(Crossref / DataCite), regenerates what can be regenerated, and produces
ready-to-paste material for the platforms that have no write API.

USAGE
    python3 mybiblio/sync_profiles.py                 # full run
    python3 mybiblio/sync_profiles.py --check         # report only, write nothing
    python3 mybiblio/sync_profiles.py --key fluids26  # focus on one new entry
    python3 mybiblio/sync_profiles.py --no-net        # skip Crossref/ORCID lookups

WHAT IS AUTOMATED, AND WHAT IS NOT
    website + sitemap : fully automated (bib2html.py --write)
    DOI verification  : fully automated (Crossref, then DataCite)
    ORCID             : coverage read automatically from the public API;
                        the missing entries are written to exports/orcid_import.bib
                        for ORCID's "Add works -> BibTeX" importer (ORCID's
                        write API needs an OAuth member token we don't have)
    ResearchGate      : no API and bot-hostile -> exports/profile_cards.md
    Google Scholar    : no write API -> exports/profile_cards.md
    PORTO@IRIS        : authenticated session required, drafts only ->
                        exports/iris_queue.md, per IRIS_DEPOSIT_PLAYBOOK.md
    MSCA blog post    : exports/blog_draft.html, paste into blog.html

Coverage that cannot be probed (ResearchGate, Scholar, IRIS) is tracked by
hand in mybiblio/profile_state.json. Update that file after you upload.

Pure standard library. No third-party dependencies.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXPORTS = os.path.join(HERE, "exports")
STATE = os.path.join(HERE, "profile_state.json")
ORCID_ID = "0000-0002-7078-3739"
UA = "linerfun-biblio-sync/1.0 (mailto:tonydifabbio@gmail.com)"

sys.path.insert(0, HERE)
import bib2html  # noqa: E402  (parser + renderer reused verbatim)

PLATFORMS = ["website", "orcid", "scholar", "researchgate", "iris"]

# Una voce con "skip" su una piattaforma e esclusa di proposito, non mancante:
# resta sul sito ma non viene mai proposta per l'upload. Usato per i talk senza
# proceedings paper, che su ORCID/RG/IRIS non hanno senso.
SKIP = "skip"


def skipped(st, key, platform):
    return st["entries"].get(key, {}).get(platform) == SKIP


# ------------------------------------------------------------------ helpers --
def get_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"Accept": "application/json",
                                               "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def load_entries():
    text = open(bib2html.BIB, encoding="utf-8").read()
    return bib2html.parse_bib(text)


def section_of(etype, fields):
    sec = bib2html.SECTION_OF.get(etype)
    if sec == "conference" and fields.get("presentation", "").lower() in (
            "true", "yes", "1"):
        sec = "presentation"
    return sec


def authors_of(fields):
    out = []
    for nm in re.split(r"\s+and\s+", fields.get("author", "").strip()):
        nm = nm.strip()
        if not nm:
            continue
        out.append(f"{nm.split(',')[1].strip()} {nm.split(',')[0].strip()}"
                   if "," in nm else nm)
    return out


def venue_of(etype, fields):
    return bib2html.venue(etype, fields)


SHARE_NOTE = {
    "aam": "l'accepted manuscript puo essere caricato apertamente",
    "vor": "la versione editoriale e liberamente ridistribuibile (OA)",
    "none": "NON caricare nulla apertamente: in archivio c'e solo il typeset "
            "editoriale di un lavoro paywalled",
}


def pdf_advice(f):
    """Which file in mybiblio/papers/ may be attached, per the archive policy."""
    share = (f.get("share") or "").lower()
    if share == "aam" and f.get("aam"):
        return f["aam"], SHARE_NOTE["aam"]
    if share == "vor" and f.get("vor"):
        return f["vor"], SHARE_NOTE["vor"]
    if share == "none":
        return None, SHARE_NOTE["none"]
    return None, "nessun PDF in archivio per questa voce"


def size_flag(rel):
    """IRIS refuses uploads over 10 MB per file — say so before Tony tries."""
    if not rel:
        return ""
    path = os.path.join(HERE, rel)
    if not os.path.exists(path):
        return " **[file assente]**"
    mb = os.path.getsize(path) / 1e6
    return (f" **[{mb:.0f} MB — oltre il limite IRIS di 10 MB: comprimi o "
            f"deposita i soli metadati]**" if mb > 10 else f" ({mb:.1f} MB)")


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


# ------------------------------------------------------- DOI verification ----
def verify_doi(doi):
    """Return (status, record) with status in ok / mismatch-source / missing."""
    for base, extract in (
        ("https://api.crossref.org/works/", _from_crossref),
        ("https://api.datacite.org/dois/", _from_datacite),
    ):
        try:
            return extract(get_json(base + doi))
        except urllib.error.HTTPError as e:
            if e.code != 404:
                return {"error": f"HTTP {e.code}"}
        except Exception as e:                      # network / parse trouble
            return {"error": str(e)}
    return None


def _from_crossref(d):
    m = d["message"]
    return {
        "source": "Crossref",
        "title": (m.get("title") or [""])[0],
        "container": (m.get("container-title") or [""])[0],
        "volume": m.get("volume"), "issue": m.get("issue"), "page": m.get("page"),
        "year": str((m.get("issued", {}).get("date-parts") or [["?"]])[0][0]),
        "authors": [f"{a.get('given','')} {a.get('family','')}".strip()
                    for a in m.get("author", [])],
    }


def _from_datacite(d):
    a = d["data"]["attributes"]
    return {
        "source": "DataCite",
        "title": (a.get("titles") or [{}])[0].get("title", ""),
        "container": a.get("publisher") if isinstance(a.get("publisher"), str)
        else (a.get("publisher") or {}).get("name", ""),
        "volume": None, "issue": None, "page": None,
        "year": str(a.get("publicationYear", "")),
        "authors": [c.get("name", "") for c in a.get("creators", [])],
    }


def doi_report(entries, enabled=True):
    rows = []
    for etype, key, f in entries:
        doi = f.get("doi")
        if not doi:
            rows.append((key, "no-doi", "nessun DOI (normale per ICAS/TSFP/talk)"))
            continue
        if not enabled:
            rows.append((key, "skipped", "verifica di rete disattivata"))
            continue
        rec = verify_doi(doi)
        if rec is None:
            rows.append((key, "MISSING", f"{doi} non trovato su Crossref ne DataCite"))
            continue
        if "error" in rec:
            rows.append((key, "error", rec["error"]))
            continue
        notes = []
        if norm(rec["title"]) != norm(f.get("title")):
            notes.append(f"titolo: bib='{f.get('title')}' vs {rec['source']}='{rec['title']}'")
        if rec.get("volume") and f.get("volume") and rec["volume"] != f["volume"]:
            notes.append(f"volume: {f['volume']} vs {rec['volume']}")
        if rec.get("issue") and f.get("number") and rec["issue"] != f["number"]:
            notes.append(f"numero: {f['number']} vs {rec['issue']}")
        if rec.get("page") and f.get("pages") and \
                norm(rec["page"]) != norm(f["pages"].replace("--", "-")):
            notes.append(f"pagine: {f['pages']} vs {rec['page']}")
        if rec["year"] != f.get("year"):
            notes.append(f"anno: {f.get('year')} vs {rec['year']}")
        if len(rec["authors"]) != len(authors_of(f)):
            notes.append(f"n. autori: {len(authors_of(f))} vs {len(rec['authors'])}")
        rows.append((key, "ok" if not notes else "DIFF",
                     f"{rec['source']} ok" if not notes else "; ".join(notes)))
    return rows


# ----------------------------------------------------------------- ORCID -----
def orcid_dois(enabled=True):
    """DOIs and normalised titles currently on the public ORCID record."""
    if not enabled:
        return None
    try:
        d = get_json(f"https://pub.orcid.org/v3.0/{ORCID_ID}/works")
    except Exception as e:
        sys.stderr.write(f"warning: ORCID non raggiungibile ({e})\n")
        return None
    dois, titles = set(), set()
    for g in d.get("group", []):
        for e in (g.get("external-ids") or {}).get("external-id", []):
            if e.get("external-id-type") == "doi":
                dois.add(e["external-id-value"].lower())
        titles.add(norm(g["work-summary"][0]["title"]["title"]["value"]))
    return dois, titles


ORCID_TYPE = {"article": "article", "inproceedings": "inproceedings",
              "conference": "inproceedings", "phdthesis": "phdthesis",
              "mastersthesis": "mastersthesis"}


def orcid_bibtex(etype, key, f):
    """A minimal, import-safe BibTeX entry (ORCID's parser dislikes extras)."""
    keep = ["author", "title", "journal", "booktitle", "school", "year",
            "volume", "number", "pages", "doi", "url", "note"]
    lines = [f"@{ORCID_TYPE.get(etype, etype)}{{{key},"]
    for k in keep:
        if f.get(k):
            lines.append(f"  {k:<9} = {{{f[k]}}},")
    lines.append("}")
    return "\n".join(lines)


# ----------------------------------------------------------------- state -----
def load_state(entries):
    st = {}
    if os.path.exists(STATE):
        st = json.load(open(STATE, encoding="utf-8"))
    st.setdefault("_comment", "Copertura per piattaforma. website/orcid sono "
                              "verificati automaticamente; scholar/researchgate/"
                              "iris vanno aggiornati a mano dopo il caricamento. "
                              "Valori: true | false | \"draft\" (solo IRIS).")
    st.setdefault("entries", {})
    for _, key, _ in entries:
        st["entries"].setdefault(key, {p: False for p in PLATFORMS})
        for p in PLATFORMS:
            st["entries"][key].setdefault(p, False)
    return st


# ---------------------------------------------------------------- exports ----
def write(path, text, dry):
    if dry:
        print(f"  [check] scriverei {os.path.relpath(path, ROOT)}")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)
    print(f"  scritto {os.path.relpath(path, ROOT)}")


def profile_card(etype, key, f):
    """Copy-paste metadata for ResearchGate / Scholar manual entry."""
    sec = section_of(etype, f)
    kind = {"journal": "Article", "conference": "Conference Paper",
            "presentation": "Presentation",
            "theses": "Thesis"}[sec]
    rg_kind = {"journal": "Article (journal article)",
               "conference": "Conference Paper",
               "presentation": "Presentation (conference presentation)",
               "theses": "Thesis"}[sec]
    L = [f"### `{key}` — {kind}", "",
         f"- **Titolo**: {f.get('title','')}",
         f"- **Autori**: {'; '.join(authors_of(f))}",
         f"- **Venue**: {venue_of(etype, f)}",
         f"- **Anno**: {f.get('year','')}"]
    if f.get("doi"):
        L.append(f"- **DOI**: {f['doi']}  → https://doi.org/{f['doi']}")
    else:
        L.append("- **DOI**: nessuno")
    if f.get("oaurl") or f.get("url"):
        L.append(f"- **Full text**: {f.get('oaurl') or f.get('url')}")
    up, why = pdf_advice(f)
    L.append(f"- **PDF da allegare**: `mybiblio/{up}` — {why}" if up
             else f"- **PDF da allegare**: nessuno — {why}")
    L += ["",
          f"**ResearchGate** → Add research → *{rg_kind}*."
          + (" Cerca prima per DOI: se RG lo trova, l'import e automatico."
             if f.get("doi") else
             " Nessun DOI: inserimento manuale con i campi sopra."),
          ("  Poi *Add full-text* con il file indicato sopra."
           if up else
           "  Non allegare full-text: vedi la nota sul PDF qui sopra."),
          "",
          "**Google Scholar** → il profilo si aggiorna da solo per tutto cio che "
          "Scholar indicizza. Aggiungi a mano (Aggiungi → Aggiungi articolo "
          "manualmente) solo se dopo ~4 settimane non compare.",
          ""]
    return "\n".join(L)


def iris_card(etype, key, f):
    doi = f.get("doi")
    L = [f"### `{key}` — {f.get('title','')}", ""]
    L.append(f"1. **Import**: Ricerca per identificativo → DOI `{doi}`"
             if doi else
             "1. **Import**: nessun DOI → inserimento manuale dei metadati.")
    L += [
        f"2. **Tipologia**: {'Articolo su rivista' if etype == 'article' else 'Contributo in atti di convegno' if etype in ('inproceedings','conference') else 'Tesi di dottorato' if etype == 'phdthesis' else 'Tesi di laurea'}",
        "3. **SDG**: `Not applicable` (sempre)",
        "4. **Referee**: `Sì, ma tipo non specificato`",
        "5. **File in archivio**: "
        + (f"`mybiblio/{pdf_advice(f)[0]}` (condivisibile)"
           + size_flag(pdf_advice(f)[0]) + " " if pdf_advice(f)[0]
           else "nessun file condivisibile ")
        + (f"· VoR `mybiblio/{f['vor']}` (riservato)" + size_flag(f["vor"])
           if f.get("vor") and f["vor"] != pdf_advice(f)[0] else ""),
        "6. **Accesso**: controlla il pannello Unpaywall live nella scheda IRIS —"
        " se risulta open access, deposita il Version of Record in `accesso"
        " aperto` con la licenza reale; altrimenti post-print/AAM in `accesso"
        " aperto` CC BY-NC-ND **più** il published VoR in `accesso riservato`"
        " / `Non Pubblico`. Limite di upload: **10 MB per file**.",
        "7. **Salva come Bozza** (`Annulla/Salva` → `Salva in temporaneo`)."
        " **Mai** cliccare Invia: rivedi e invia tu.",
        "",
    ]
    return "\n".join(L)


def blog_draft(etype, key, f):
    months = ["", "January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    when = f"{months[date.today().month]} {f.get('year', date.today().year)}"
    link = (f"https://doi.org/{f['doi']}" if f.get("doi")
            else f.get("oaurl") or f.get("url") or "research.html")
    tag = "tag-talk" if section_of(etype, f) == "presentation" else "tag-paper"
    label = "Conference" if tag == "tag-talk" else "Publication"
    return f"""<!-- paste directly under the  <!-- ── NEW POSTS ── -->  comment in blog.html -->
<article class="post">
  <div class="post-meta">
    <span class="post-tag {tag}">{label}</span>
    <span class="post-date">{when}</span>
  </div>
  <h2>{bib2html.esc(f.get('title',''))}</h2>
  <div class="post-body">
    <p>TODO: una o due frasi in linguaggio divulgativo su cosa mostra il
       lavoro e perché conta per LINERFUN.</p>
    <div class="post-highlight">TODO: il risultato chiave in una riga.</div>
    <p>Pubblicato su <em>{bib2html.esc(venue_of(etype, f))}</em> con
       {bib2html.esc(', '.join(a for a in authors_of(f) if 'Di Fabbio' not in a))}.</p>
  </div>
  <a href="{link}" class="post-read-more">Read the paper →</a>
</article>"""


# ------------------------------------------------------------------- main ----
def bump_sitemap(dry):
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        return
    src = open(path, encoding="utf-8").read()
    today = date.today().isoformat()
    new = re.sub(r"(<loc>[^<]*?(?:research|blog)\.html</loc>\s*<lastmod>)[^<]+",
                 lambda m: m.group(1) + today, src)
    if new == src:
        new = re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{today}</lastmod>", src, count=1)
    if new != src:
        write(path, new, dry)
    else:
        print("  sitemap.xml gia aggiornato")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="non scrivere nulla")
    ap.add_argument("--key", action="append", default=[],
                    help="limita gli export a questa cite key (ripetibile)")
    ap.add_argument("--no-net", action="store_true", help="salta Crossref/ORCID")
    a = ap.parse_args(argv)
    net = not a.no_net
    dry = a.check

    entries = load_entries()
    by_key = {k: (t, f) for t, k, f in entries}
    focus = a.key or [k for _, k, _ in entries]
    unknown = [k for k in focus if k not in by_key]
    if unknown:
        sys.exit(f"cite key inesistenti in references.bib: {', '.join(unknown)}")

    print(f"references.bib: {len(entries)} voci\n")

    # 1 — verifica DOI -------------------------------------------------------
    print("1. Verifica DOI contro il record editoriale")
    rows = doi_report(entries, net)
    for key, status, note in rows:
        mark = {"ok": "  ok  ", "DIFF": " DIFF ", "MISSING": " !!!! ",
                "no-doi": "  --  ", "error": " err  ", "skipped": "  ..  "}[status]
        print(f"  [{mark}] {key:<14} {note}")
    problems = [r for r in rows if r[1] in ("DIFF", "MISSING", "error")]

    # 2 — sito + sitemap -----------------------------------------------------
    print("\n2. Sito")
    if dry:
        print("  [check] rigenererei research.html e sitemap.xml")
    else:
        bib2html.main(["--write", os.path.join(ROOT, "research.html")])
    bump_sitemap(dry)

    # 3 — ORCID --------------------------------------------------------------
    print("\n3. ORCID")
    oc = orcid_dois(net)
    st = load_state(entries)
    missing_orcid = []
    for etype, key, f in entries:
        if oc is None:
            break
        if skipped(st, key, "orcid"):
            continue
        on = (f.get("doi", "").lower() in oc[0]) or (norm(f.get("title")) in oc[1])
        if not on:
            missing_orcid.append((etype, key, f))
    if oc is None:
        print("  copertura non verificata (rete disattivata o API irraggiungibile)")
    elif missing_orcid:
        print(f"  mancano {len(missing_orcid)}: {', '.join(k for _, k, _ in missing_orcid)}")
        body = ("% Generato da sync_profiles.py — import su ORCID:\n"
                "%   orcid.org → Works → Add → Add BibTeX → scegli questo file,\n"
                "%   poi spunta le voci da importare.\n\n"
                + "\n\n".join(orcid_bibtex(t, k, f) for t, k, f in missing_orcid) + "\n")
        write(os.path.join(EXPORTS, "orcid_import.bib"), body, dry)
    else:
        print("  allineato")

    # 4 — schede RG / Scholar ------------------------------------------------
    print("\n4. ResearchGate / Google Scholar")
    sel = [(t, k, f) for t, k, f in entries if k in focus
           and not (skipped(st, k, "researchgate") and skipped(st, k, "scholar"))]
    cards = ("# Schede profilo — da incollare a mano\n\n"
             "ResearchGate e Google Scholar non hanno API di scrittura.\n"
             "Profilo RG canonico: https://www.researchgate.net/profile/Tony-Di-Fabbio-4\n"
             f"Profilo Scholar: https://scholar.google.com/citations?user=FGbgU2UAAAAJ\n"
             f"Generato il {date.today().isoformat()}.\n\n"
             + "\n".join(profile_card(t, k, f) for t, k, f in sel))
    write(os.path.join(EXPORTS, "profile_cards.md"), cards, dry)

    # 5 — coda IRIS ----------------------------------------------------------
    print("\n5. PORTO@IRIS")
    todo = [(t, k, f) for t, k, f in entries
            if k in focus and st["entries"][k]["iris"] is False]
    iris = ("# Coda deposito PORTO@IRIS\n\n"
            "Regole complete: `mybiblio/IRIS_DEPOSIT_PLAYBOOK.md`.\n"
            "Accedi tu a iris.polito.it — le credenziali non vanno mai a Claude.\n"
            "Ogni voce si ferma alla **Bozza**: la revisione e l'invio li fai tu.\n"
            f"Generato il {date.today().isoformat()}. Da depositare: {len(todo)}.\n\n"
            + ("\n".join(iris_card(t, k, f) for t, k, f in todo) if todo
               else "Nulla in coda.\n"))
    write(os.path.join(EXPORTS, "iris_queue.md"), iris, dry)
    print(f"  in coda: {len(todo)}")

    # 6 — bozza post blog ----------------------------------------------------
    print("\n6. Post blog MSCA")
    if a.key:
        drafts = "\n\n".join(blog_draft(*(by_key[k][0], k, by_key[k][1])) for k in a.key)
        write(os.path.join(EXPORTS, "blog_draft.html"), drafts + "\n", dry)
    else:
        print("  salta (passa --key KEY per generare il post di un nuovo lavoro)")

    # 7 — stato --------------------------------------------------------------
    print("\n7. Stato di copertura")
    if oc is not None:
        miss = {k for _, k, _ in missing_orcid}
        for _, key, _ in entries:
            if not skipped(st, key, "orcid"):
                st["entries"][key]["orcid"] = key not in miss
            st["entries"][key]["website"] = True
    st["last_sync"] = date.today().isoformat()
    write(STATE, json.dumps(st, indent=2, ensure_ascii=False) + "\n", dry)

    hdr = "| cite key | " + " | ".join(PLATFORMS) + " |"
    tbl = [hdr, "|" + "---|" * (len(PLATFORMS) + 1)]
    for _, key, _ in entries:
        cells = []
        for p in PLATFORMS:
            v = st["entries"][key][p]
            cells.append({True: "si", False: "NO", "draft": "draft",
                          SKIP: "&mdash;"}.get(v, str(v)))
        tbl.append(f"| `{key}` | " + " | ".join(cells) + " |")
    status = ("# Stato di sincronizzazione\n\n"
              f"Ultimo run: {date.today().isoformat()}\n\n" + "\n".join(tbl)
              + "\n\n## DOI da controllare\n\n"
              + ("\n".join(f"- `{k}` — {n}" for k, _, n in problems) if problems
                 else "Nessuno: tutti i DOI combaciano col record editoriale.\n")
              + "\n\n## Cosa resta manuale\n\n"
              "- ORCID: importa `exports/orcid_import.bib` (Works → Add → Add BibTeX).\n"
              "- ResearchGate: `exports/profile_cards.md`, Add research.\n"
              "- Scholar: si aggiorna da solo; inserimento manuale solo se dopo "
              "~4 settimane la voce non compare.\n"
              "- IRIS: `exports/iris_queue.md`, solo bozze.\n"
              "- Dopo ogni caricamento aggiorna `profile_state.json`.\n"
              "- `&mdash;` = voce esclusa di proposito da quella piattaforma "
              "(`\"skip\"` in `profile_state.json`), non mancante.\n")
    write(os.path.join(EXPORTS, "SYNC_STATUS.md"), status, dry)

    print("\nFatto." + (" (dry run)" if dry else ""))
    return 1 if [r for r in rows if r[1] == "MISSING"] else 0


if __name__ == "__main__":
    sys.exit(main())
