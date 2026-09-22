# mybiblio/papers/ — self-hosted PDF archive

Local, human-readable archive of every publication PDF.

> **Current policy — NOT linked from the site.** These PDFs are **not** wired into
> `research.html` (no `pdf` fields in `references.bib`). The full texts are deposited on
> **IRIS PoliTo**, the institutional repository the website points to, so the site links
> out to IRIS rather than self-hosting copies. Keep this in mind before adding any
> `pdf = {...}` field — that would publish a direct download button on the public site.
>
> ⚠️ Everything in this folder is still committed to the repo and served by GitHub Pages,
> so each file is publicly reachable by direct URL even without a link. If you want the
> archive kept off the public deploy until IRIS is populated, `.gitignore` this folder.

## Naming

```
<FirstAuthor>_<Year>_<short-title>[_<version>].pdf
```

- **First author** surname in PascalCase (`DiFabbio`, `Kotzlowski`, `Bres`, `Rajkumar`, …).
- **Year** of publication (4 digits).
- **short-title** — a few lowercase, hyphen-separated keywords.
- **version** (only for doubles): `_published` = publisher version of record (journal
  typeset, banner, DOI); `_shareable` = peer-reviewed author copy (all revisions, no
  publisher banner) — the green-OA-safe manuscript to deposit openly.

The BibTeX cite key (`ceas22`, `icas22`, …) is unchanged; it stays the entry key in
`../references.bib` and `../difabbio_publications.bib`. Only the filenames are readable.

## Which version may I share?

- **Open access** (`fluids24` MDPI CC BY; `ceas22` Springer CC BY): the published PDF is
  free to share.
- **Hybrid open access, CC BY** (`ast24` Elsevier; `aj23` Cambridge; `pof24` AIP;
  `ceas22` Springer): the **published** version carries a CC BY licence and may be
  redistributed freely. Verified against Unpaywall on 2026-09-21 — the publisher's
  paywall on the landing page says nothing about the licence.
- **Closed** (`aiaa26`, `aiaa-ceas26`, `scitech22` AIAA; `emw25` IEEE): only the
  `_shareable` accepted manuscript may be redistributed openly. Check embargoes on
  [Sherpa Romeo / open policy finder](https://openpolicyfinder.jisc.ac.uk/) first.

> Always re-check with Unpaywall rather than guessing from the publisher's name.
> `python3 ../sync_profiles.py --check` reports the live status per entry.

## Status (July 2026)

| Cite key | Venue | Access | File(s) present |
|---|---|---|---|
| `aiaa26` | AIAA Journal, 2026 | closed | `Kotzlowski_2026_delta-wing-gep-turbulence_shareable.pdf` · `…_published.pdf` |
| `fluids24` | Fluids (MDPI), 2024 | Gold OA | `DiFabbio_2024_gep-one-equation-strategies.pdf` |
| `pof24` | Physics of Fluids, 2024 | **hybrid OA, CC BY** | `Rajkumar_2024_vortex-shock-delta-wing_shareable.pdf` · `…_published.pdf` |
| `ast24` | Aerospace Sci. & Tech., 2024 | **hybrid OA, CC BY** | `DiFabbio_2024_vortex-breakdown-rans.pdf` *(CC BY published version — condivisibile)* |
| `aj23` | The Aeronautical Journal, 2023 | **hybrid OA, CC BY** | `DiFabbio_2023_vortex-dominated-delta-wing.pdf` *(CC BY published version — condivisibile)* |
| `ceas22` | CEAS Aeronautical J., 2022 | OA (CC BY) | `DiFabbio_2022_triple-delta-sideslip.pdf` |
| `aiaa-ceas26` | 32nd AIAA/CEAS Aeroacoustics, 2026 | closed | `Bres_2026_gpu-les-cavity-flows_shareable.pdf` · `…_published.pdf` |
| `ofw25a` | 20th OpenFOAM Workshop, 2025 | — | — **missing** → `Segalerba_2025_opensource-turbulence-model.pdf` |
| `ofw25b` | 20th OpenFOAM Workshop, 2025 | — | — **missing** → `Rossano_2025_openfoam-verification-validation.pdf` |
| `emw25` | 55th European Microwave Conf. (EuMC), 2025 | closed (IEEE) | `Zampa_2025_hypersonic-blackout-mitigation.pdf` |
| `scitech22` | AIAA SciTech Forum, 2022 | closed | `DiFabbio_2022_delta-wing-flow-pattern_shareable.pdf` · `…_published.pdf` |
| `icas22` | ICAS Congress, Stockholm, 2022 | — | `DiFabbio_2022_leading-edge-vortices-sas.pdf` |
| `tsfp22` | TSFP12, Osaka, 2022 | — | `DiFabbio_2022_reynolds-stress-vortex-breakdown.pdf` |
| `dglr20` | DGLR, Bonn, 2020 | — | `DiFabbio_2020_scale-resolving-rans-delta-wing.pdf` |
| `phd24` | PhD, UniBw München, 2024 | — | `DiFabbio_2024_phd-turbulence-vortical-swept-edges.pdf` |
| `msc19` | MSc, Politecnico di Torino, 2019 | — | `DiFabbio_2019_msc-rocket-combustor.pdf` |

**14 / 16 entries have a local PDF. Missing:** `ofw25a`, `ofw25b`
(suggested filenames in the table above).

For paywalled entries that only have the publisher typeset PDF (`ast24`, `aj23`), add a
`_shareable` accepted manuscript when available so an open version can be deposited.

> A portable BibTeX of every publication — with DOIs and `file = {...}` links for
> reference managers — is in `../difabbio_publications.bib`.
