# IRIS PoliTo — deposit playbook (PORTO@IRIS)

Repeatable procedure to deposit a paper on **PORTO@IRIS** (`iris.polito.it`, DSpace6/Cineca),
attaching the shareable + published PDFs from `mybiblio/papers/`. Everything is left as a
**Bozza** (draft) for Tony to review and submit — this playbook never clicks the final "Invia".

> Not an unattended bot: IRIS needs Tony's personal login, so a session must be open and
> authenticated. With this playbook each deposit is ~2 minutes of guided browser steps.

## Prerequisites
- Logged in to `iris.polito.it` as Tony (he authenticates; credentials are never entered by the agent).
- PDFs present in `mybiblio/papers/` named `<FirstAuthor>_<Year>_<short-title>[_shareable/_published].pdf`.

## Procedure (per paper)
1. **Skip-if-present.** Search the title in the top "Search IRIS" box (scope *Tutto PORTO@Iris*).
   If a record already exists, stop (don't duplicate). *(aiaa26 is already on IRIS — done by Tony.)*
2. **New record.** Desktop prodotti → green **Nuova pubblicazione** → **Ricerca per identificativo** →
   paste the **DOI** → *Cerca* → tick **Importa** on the result → set **Tipologia** (see table) →
   **Importa i record selezionati**. *(No DOI → use Inserimento manuale with that Tipologia.)*
3. **Wizard steps 1–4 (Descrivere).** Most fields auto-fill from the DOI. Fill only the required (*)
   ones still empty:
   - **SDG - Sustainable Development Goals** → always `Not applicable`.
   - **Referee / Con Referee** → `Sì, ma tipo non specificato` (peer-reviewed).
   - **Numero di pagine** (required for `1.1 Articolo in rivista`) → real page count if empty.
   - Publisher / Titolo volume / Titolo convegno / identifiers usually import automatically.
   - Skip every optional field. No EU project for pre-LINERFUN papers.
   - **Check the author disambiguation** on step 3: Di Fabbio should be green (internal). If the DOI
     source mis-parsed the name (e.g. `Fabbio, T. Di`), he stays grey/external → disambiguate.
4. **Step 5 (Carica) — one row per file. Trust the live Unpaywall/Open-Policy panel on the right:**
   - **`Con licenza: cc-by` + `publishedVersion`** ⇒ the VoR is genuinely OA → deposit the published
     file **`accesso aperto` · VoR · Creative commons → commercial *Sì*, modification *Sì* (= CC BY)**.
   - **`OA: closed`** (paywalled, e.g. AIAA) ⇒ **shareable** → `2. Post-print / AAM`, `accesso aperto`,
     Licenza `Creative commons` → **NC = No, ND = No (= CC BY-NC-ND)**, Publisher copyright statement =
     the matching publisher; **published** → `Version of Record`, `accesso riservato`, `Non Pubblico`.
   - ⚠️ **File-upload limit: 10 MB per file** (browser tool). Larger PDFs cannot be attached this way —
     create the metadata-only draft and attach the PDF manually, or compress the PDF below 10 MB first.
5. **Save as draft.** Bottom bar → **Annulla/Salva** → green **"Salva in temporaneo. Continuerò il
   lavoro dopo"**. (Never the red *Elimina l'inserimento*.) The item lands in *bozze* with Status **Bozza**.

## Status (2026-07-03) — 6 deposited as Bozza, 7 remaining

| Cite key | DOI | Status / how to deposit |
|---|---|---|
| `scitech22` | 10.2514/6.2022-1204 | ✅ **Bozza** — shareable open CC BY-NC-ND + published private |
| `fluids24` | 10.3390/fluids9080191 | ✅ **Bozza** — open · VoR · CC BY |
| `ceas22` | 10.1007/s13272-022-00571-9 | ✅ **Bozza** — open · VoR · CC BY |
| `ast24` | 10.1016/j.ast.2024.108973 | ✅ **Bozza** — open · VoR · **CC BY** (Unpaywall says hybrid OA, *not* private) |
| `aj23` | 10.1017/aer.2023.30 | ✅ **Bozza** — open · VoR · **CC BY** (Unpaywall says hybrid OA, *not* private) |
| `pof24` | 10.1063/5.0213122 | ✅ **Bozza** — open · VoR · CC BY. ⚠️ name mis-parsed `Fabbio, T. Di` → **disambiguate author**; 73 MB shareable skipped (>10 MB, redundant) |
| `emw25` | 10.23919/EuMC65286.2025.11235288 | ⏳ has DOI now — import; single file (4 MB, uploadable) |
| `icas22` | — (url only) | ⏳ manual entry; file 6 MB uploadable |
| `tsfp22` | — | ⏳ manual entry; file 4 MB uploadable |
| `dglr20` | — | ⏳ manual entry; file 2.5 MB uploadable |
| `aiaa-ceas26` | 10.2514/6.2026-3359 | ⏳ import metadata; **files ~22 MB each > 10 MB** → attach manually (shareable open CC BY-NC-ND / published private) |
| `phd24` | — | ⏳ manual (PhD thesis); **file 56 MB > 10 MB** → attach manually |
| `msc19` | webthesis 12809 | ⏳ manual (PoliTo MSc thesis); **file 18 MB > 10 MB** → attach manually |

**Already on IRIS:** `aiaa26` (in approval, by Tony). **No PDF yet:** `ofw25a`, `ofw25b`.

> Key finding: several papers assumed paywalled (`ast24`, `aj23`, `pof24`) are actually **CC BY hybrid
> OA** per the live Unpaywall panel — always trust that panel over the static guess. AIAA papers
> (`scitech22`, `aiaa26`, `aiaa-ceas26`) are the genuinely paywalled ones (shareable open / VoR private).
