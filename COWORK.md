# COWORK.md — content operations playbook

This file tells Cowork **how to do the recurring content jobs** on this site: add a
blog post, add a publication, add an award, then publish. It is task-oriented;
the architecture, build model and design tokens live in `CLAUDE.md` and `README.md`.
Read the **Guardrails** at the bottom before changing anything — a few elements are
legally required and must not be touched.

No build step. Edit HTML/`.bib`, commit, push — GitHub Pages redeploys in ~1 minute.

| Page | Holds | You'll edit it to… |
|---|---|---|
| `blog.html` | news / outreach feed (`.post` articles) | add a post |
| `research.html` | publications, expertise cards, awards table | regenerate pubs, add an award |
| `mybiblio/references.bib` | **master bibliography (source of truth)** | add/edit a publication |
| `mybiblio/papers/` | self-hosted PDFs | drop an accepted-manuscript PDF |
| `sitemap.xml` | SEO sitemap | bump `<lastmod>` after any change |
| `mybiblio/sync_profiles.py` | **pipeline di sincronizzazione profili** | eseguirlo dopo ogni nuova voce (§2-bis) |
| `mybiblio/profile_state.json` | copertura per piattaforma | aggiornarlo dopo ogni caricamento manuale |
| `mybiblio/exports/` | materiale generato per ORCID/RG/Scholar/IRIS/blog | leggerlo, non modificarlo a mano |

---

## 1 · Add a blog / news post

Edit `blog.html`. Insert the new `<article>` **directly below the `<!-- ── NEW POSTS ── -->`
comment** (i.e. right after the pinned post) so the newest item is at the top. Leave the
pinned article first.

```html
<article class="post">
  <div class="post-meta">
    <span class="post-tag tag-news">News</span>
    <span class="post-date">June 2026</span>
  </div>
  <h2>Post title goes here</h2>
  <div class="post-body">
    <p>Opening paragraph.</p>
    <div class="post-highlight">Optional pull-quote or key statistic.</div>
    <p>More paragraphs as needed.</p>
  </div>
  <a href="project.html" class="post-read-more">Optional read-more link →</a>
</article>
```

**Tags** — the class sets the colour, the label text is free:

| Class | Colour | Use for | Typical label |
|---|---|---|---|
| `tag-msca` | blue | fellowship / project milestones | `MSCA`, `Project update` |
| `tag-news` | amber | general news, outreach, explainers | `News`, `Outreach`, `Science explainer` |
| `tag-paper` | green | publications | `Publication` |
| `tag-talk` | purple | talks, conferences | `Conference` |
| `tag-pinned` | navy | the single pinned post only | `📌 pinned` |

**Date**: human format — `June 2026`, `May 2026`, or just `2025` / `Aug 2024` for older items.
**Cross-post rule**: if the post announces a paper or an award, also add it to the
bibliography (§2) or the awards table (§3) so the Research page stays in sync.

---

## 2 · Add or edit a publication

**Never hand-edit the `.pub` blocks in `research.html` directly.** Edit the master
bibliography and regenerate. The cite key is the anchor, so the expertise-card deep-links
keep working.

### Step 1 — add the entry to `mybiblio/references.bib`

```bibtex
@article{KEY,                              % KEY -> id="pub-KEY" on the page
  author  = {Di Fabbio, T. and Coauthor, A. B.},  % "Last, F." joined by " and "
  title   = {Full paper title},
  journal = {Journal Name},
  year    = {2026},
  volume  = {12},
  number  = {3},
  doi     = {10.xxxx/yyyy},
}
```

Conference paper — use `@inproceedings` and put the city **inside** `booktitle`:

```bibtex
@inproceedings{KEY,
  author    = {Di Fabbio, T. and ...},
  title     = {...},
  booktitle = {Conference Name, City},
  year      = {2026},
}
```

Conventions enforced by the generator: `@article` → *Journal Articles*,
`@inproceedings` → *Conference Proceedings*, `@phdthesis`/`@mastersthesis` → *Theses*.
Any author whose surname is `Di Fabbio` is auto-bolded. Order inside a section = order in
the file (newest first). Keep cite keys stable.

### Step 2 — regenerate the HTML

```bash
# preview one section and paste it into the matching block of research.html
python3 mybiblio/bib2html.py --section journal      # journal | conference | theses

# or print all three sections
python3 mybiblio/bib2html.py
```

**One-command regeneration (recommended once set up).** Add these markers to
`research.html` *one time*, replacing the hand-written `.pub` blocks inside each
`<div class="section">`:

```html
<div class="section-title">Journal Articles</div>
<!-- BIBLIO:journal:START -->
<!-- BIBLIO:journal:END -->
```

(likewise `BIBLIO:conference` and `BIBLIO:theses`). Then a single command rewrites only
the regions between the markers and leaves the rest of the page — expertise cards, awards,
EU banner — untouched:

```bash
python3 mybiblio/bib2html.py --write research.html
```

> Note: regenerating renders the **complete** citation (volume/issue included), which is
> richer than some of the current hand-written venues. That's intended.

### Step 3 — link the PDF (optional)

A **PDF** button appears automatically when the entry has either field:

- `oaurl = {https://...}` — link to a free / open-access full text (e.g. the MDPI page for
  the *Fluids* paper). Preferred for open-access papers.
- `pdf = {papers/KEY.pdf}` — link a self-hosted copy. Drop the file in `mybiblio/papers/`
  named after the cite key. For **paywalled** journals host the **accepted manuscript**
  (your final version, no publisher banner/typesetting), never the publisher PDF. See
  `mybiblio/papers/README.md` for the per-paper open-access status.

### Step 4 — cross-link from an expertise card (optional)

The four cards in the *Areas of expertise* section list related papers by anchor. To
feature a new paper, add a line inside the relevant card's `.exp-pubs`:

```html
<a href="#pub-KEY">Short title — <em>Venue</em>, Year</a>
```

---

## 2-bis · Propagare una pubblicazione su TUTTI i profili

Dopo aver aggiunto la voce a `references.bib` (§2 step 1), un solo comando
allinea sito, sitemap e tutti i profili esterni:

```bash
python3 mybiblio/sync_profiles.py --key NUOVAKEY
```

Cosa fa, in ordine:

| # | Passo | Automatico? |
|---|---|---|
| 1 | Verifica il DOI contro Crossref, poi DataCite: titolo, autori, volume, numero, pagine, anno | sì |
| 2 | Rigenera `research.html` (tutte e 4 le sezioni) e aggiorna `sitemap.xml` | sì |
| 3 | Legge l'API pubblica ORCID e scrive le voci mancanti in `exports/orcid_import.bib` | lettura sì, scrittura no |
| 4 | Genera `exports/profile_cards.md` — metadati pronti per ResearchGate e Scholar | no (niente API di scrittura) |
| 5 | Genera `exports/iris_queue.md` — checklist di deposito per PORTO@IRIS | no (sessione autenticata) |
| 6 | Genera `exports/blog_draft.html` — il `.post` per la disseminazione MSCA | testo da completare |
| 7 | Aggiorna `profile_state.json` e `exports/SYNC_STATUS.md` (matrice di copertura) | sì |

Opzioni: `--check` (dry run), `--no-net` (salta Crossref/ORCID), `--key` ripetibile.

### I passi manuali, nell'ordine giusto

1. **ORCID** → Works → Add → *Add BibTeX* → `mybiblio/exports/orcid_import.bib`.
2. **ResearchGate** → Add research, seguendo `exports/profile_cards.md`.
   Profilo canonico: `researchgate.net/profile/Tony-Di-Fabbio-4`.
3. **Google Scholar** → non fare nulla: si aggiorna da solo. Inserimento
   manuale solo se dopo ~4 settimane la voce non compare.
4. **IRIS PoliTo** → `exports/iris_queue.md` + `IRIS_DEPOSIT_PLAYBOOK.md`.
   Accedi tu; ogni voce si ferma alla **Bozza**, l'invio lo fai tu.
5. Aggiorna `mybiblio/profile_state.json` con quello che hai caricato, così la
   matrice di copertura resta veritiera.

### Quale PDF si può caricare dove

`references.bib` porta tre campi non renderizzati che codificano la policy di
`mybiblio/papers/README.md`:

- `aam = {papers/...}` — accepted manuscript / copia autore
- `vor = {papers/...}` — versione editoriale (version of record)
- `share = {aam|vor|none}` — **quale delle due può essere diffusa apertamente**

`share = none` significa che in archivio c'è solo il typeset editoriale di un
lavoro paywalled: non va caricato da nessuna parte. `bib2html.py` ignora questi
campi, quindi non compare nessun pulsante di download sul sito pubblico — resta
valida la policy "i full text stanno su IRIS" (vedi Guardrails).


---

## 3 · Add an award / funding

Edit the awards table in `research.html` (`.award-table`). Add a `<tr>`, newest near the top:

```html
<tr>
  <td>2026</td>
  <td>Award name</td>
  <td>One sentence on what it funds and where.</td>
  <td><span class="award-amount">€10,000</span></td>
</tr>
```

---

## 4 · Publish (git + deploy)

```bash
git add -A
git commit -m "blog: add post on aircraft noise"   # or "pubs: add fluids25", "awards: add X"
git push                                            # Pages redeploys in ~1 min
```

After changing any page, bump its `<lastmod>` in `sitemap.xml` to today (`YYYY-MM-DD`).
If you're unsure whether a change is ready to go live, **ask before pushing**.

**New page?** carry the standard `<head>`: name-first `<title>`, meta description, canonical
URL, Open Graph/Twitter tags (`og:image` = absolute `img/tony.jpg`), favicon, theme-color;
add it to the `<nav>` and to `sitemap.xml`; add JSON-LD only if it's a Person/Project/Profile page.

---

## Guardrails — do not break

- **EU banner & footer attribution** (`.eu-banner` on every page, the EU/MSCA line in every
  footer) are **required by the MSCA grant**. Never remove or substantially alter them.
- **Logos**: only **MSCA** (`img/logoMSCA.png`) and **DIMEAS — Politecnico di Torino**
  (`img/logoDIMEAS.jpg`) may be shown. University of Melbourne and ONERA have **no logo
  permission** — keep them as plain text links (`.inst-partners`). Never add their logos.
- **`.nojekyll`** must stay (it disables Jekyll on GitHub Pages).
- **`news.html`** is a legacy redirect to `blog.html` — don't link to it or add content there.
- Keep the **660 px** content width and the design tokens in `:root`; page-specific CSS goes
  in a `<style>` block in that page's `<head>`.
