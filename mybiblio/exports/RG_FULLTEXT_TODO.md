# ResearchGate — full-text da caricare a mano

L'estensione Chrome non può leggere file dal disco locale, quindi gli upload
dei PDF su ResearchGate restano l'unico passo che devi fare tu. Tutto il resto
del profilo (intro, qualifica, discipline, formazione, competenze, lingue,
tesi di dottorato) è già stato aggiornato.

Su ogni voce: **Add full-text** → scegli il file indicato.
Policy verificata su Unpaywall il 2026-09-21 — vedi `mybiblio/papers/README.md`.

| voce | file da caricare | perché è lecito |
|---|---|---|
| `aiaa26` | `papers/Kotzlowski_2026_delta-wing-gep-turbulence_shareable.pdf` | AIAA closed → solo accepted manuscript |
| `emw25` | `papers/Zampa_2025_hypersonic-blackout-mitigation_shareable.pdf` | IEEE closed → solo accepted manuscript |
| `scitech22` | `papers/DiFabbio_2022_delta-wing-flow-pattern_shareable.pdf` | AIAA closed → solo accepted manuscript |
| `icas22` | `papers/DiFabbio_2022_leading-edge-vortices-sas.pdf` | atti ICAS aperti |
| `tsfp22` | `papers/DiFabbio_2022_reynolds-stress-vortex-breakdown.pdf` | atti TSFP aperti |
| `dglr20` | `papers/DiFabbio_2020_scale-resolving-rans-delta-wing.pdf` | atti DGLR aperti |
| `msc19` | `papers/DiFabbio_2019_msc-rocket-combustor.pdf` | tesi, deposito aperto PoliTo |
| `phd24` | `papers/DiFabbio_2024_phd-turbulence-vortical-swept-edges.pdf` | tesi, deposito aperto UniBw |
| `ast24` | `papers/DiFabbio_2024_vortex-breakdown-rans.pdf` | **hybrid OA CC BY** → la versione editoriale si può caricare |
| `aj23` | `papers/DiFabbio_2023_vortex-dominated-delta-wing.pdf` | **hybrid OA CC BY** → la versione editoriale si può caricare |

Già a posto (full-text presente): `aiaa-ceas26`, `fluids24`, `pof24`, `ceas22`.

Dopo il caricamento, segna `researchgate: true` in `mybiblio/profile_state.json`.
