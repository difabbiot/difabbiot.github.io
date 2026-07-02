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
   - **Referee** → `Sì, ma tipo non specificato` (peer-reviewed).
   - Publisher / Titolo volume / Titolo convegno / identifiers usually import automatically.
   - Skip every optional field. No EU project for pre-LINERFUN papers.
4. **Step 5 (Carica) — one row per file:**
   - **shareable** → Tipologia `2. Post-print / Author's Accepted Manuscript`;
     Impostazioni di accesso `accesso aperto`; Licenza `Creative commons` → **NC = No**, **ND = No**
     (⇒ **CC BY-NC-ND 4.0**); Publisher's copyright statement = the publisher entry
     (e.g. `AIAA preprint/submitted version e/o postprint/Author's Accepted Manuscript`).
   - **published** → Tipologia `2a Post-print versione editoriale / Version of Record`;
     Impostazioni di accesso `accesso riservato`; Licenza `Non Pubblico - Accesso privato/ristretto`.
   - **Open-access papers** (single file, CC BY): Tipologia `Version of Record`, `accesso aperto`,
     Licenza `Creative commons` → **CC BY** (the real publisher licence).
   - **Paywalled, publisher PDF only** (no shareable): deposit that file as `accesso riservato` (private).
5. **Save as draft.** Bottom bar → **Annulla/Salva** → green **"Salva in temporaneo. Continuerò il
   lavoro dopo"**. (Never the red *Elimina l'inserimento*.) The item lands in *bozze* with Status **Bozza**.

## Per-paper plan (missing → deposit as draft)

| Cite key | DOI | Files | Deposit |
|---|---|---|---|
| `scitech22` | 10.2514/6.2022-1204 | shareable + published | **DONE — draft** (open CC BY-NC-ND / private) |
| `fluids24` | 10.3390/fluids9080191 | 1 (MDPI Gold OA) | open · VoR · **CC BY** |
| `pof24` | 10.1063/5.0213122 | shareable + published | open CC BY-NC-ND / private |
| `ast24` | 10.1016/j.ast.2024.108973 | 1 (Elsevier, paywalled) | **private** (no shareable yet) |
| `aj23` | 10.1017/aer.2023.30 | 1 (Cambridge, paywalled) | **private** (no shareable yet) |
| `ceas22` | 10.1007/s13272-022-00571-9 | 1 (Springer OA) | open · VoR · **CC BY** |
| `aiaa-ceas26` | 10.2514/6.2026-3359 | shareable + published | open CC BY-NC-ND / private |
| `emw25` | — (manual) | 1 | conference; open postprint CC BY-NC-ND |
| `icas22` | — (manual) | 1 | conference; open postprint CC BY-NC-ND |
| `tsfp22` | — (manual) | 1 | conference; open postprint CC BY-NC-ND |
| `dglr20` | — (manual) | 1 | conference; open postprint CC BY-NC-ND |
| `phd24` | — (manual) | 1 | PhD thesis; open |
| `msc19` | webthesis 12809 | 1 | PoliTo master's thesis; open |

**Already on IRIS:** `aiaa26` (in approval, by Tony). **Missing PDFs (not depositable yet):**
`ofw25a`, `ofw25b`, `dglr25`.

> Affiliation note: 2019–2024 works are from the UniBw München era; only deposit on PORTO@IRIS
> per Tony's instruction (he confirmed depositing his back-catalogue). VoR of paywalled papers is
> kept *private*; the green-OA `_shareable` is the openly-accessible copy.
