# Reproducing the released computational package

## Two ways to rerun the study

| Route | Inputs | Output and verification | Expected identity |
|---|---|---|---|
| Frozen release | Pinned Hugging Face revision, tracked result tables, locked dependencies | R1 row manifest, Croissant data, five robustness tables, four SVGs, checks | The builders verify committed counts and digests; SVGs must be byte-identical. |
| Live collection and model annotation | Current public APIs and hosted LLMs | New source and label snapshots for exploratory use | Public records, model behavior, and platform APIs can change; this is **not** an exact replay of the release. |

The pinned dataset is hosted by the original data publisher at [`kl41r3/erc8004-vs-a2a-governance`](https://huggingface.co/datasets/kl41r3/erc8004-vs-a2a-governance), revision `987913bacae1a169bb39587b22dd002f74293177`. Its license is CC BY-NC 4.0. No `.env`, API key, paid model invocation, or GPU is needed for the frozen path.

## From a fresh clone

Install Python 3.14 or newer, `uv`, and roughly 2 GB of free space for dependencies and data. The analysis environment is relatively large because the historical pipeline includes topic-model dependencies.

```bash
git clone https://github.com/sunshineluyao/erc8004-a2a-case-study.git
cd erc8004-a2a-case-study
uv sync --frozen
make verify
make figures-check
make reproduce
```

`make verify` and `make figures-check` are offline after dependencies have been installed; `make figures-check` can also run with system Python 3.14 or another recent Python 3 without installing any third-party library. `make reproduce` reaches Hugging Face. In an environment with a SOCKS proxy, `huggingface_hub` may require the optional `socksio` transport; this is an environment prerequisite, not a dataset key.

For an isolated visual-only check, run:

```bash
python3 scripts/visualise/build_release_figures.py --check
```

To rebuild the checked SVGs after changing a source table, use `make figures`; the provenance manifest updates with the source and output digests. Check the semantic interpretation of any changed number before publishing.

## Evidence path

| Stage | Query / processing code | Data location | Check or scope |
|---|---|---|---|
| Public source records | [`scripts/scrape/`](scripts/scrape/) | `data/raw/` (downloaded, ignored by Git) | Original platform identifiers and URLs remain in the archive. Live scraping is a provenance rerun. |
| Historical annotations | [`scripts/process/`](scripts/process/) | `data/annotated/` (downloaded) | MiniMax R1 and three-model R2 layers are separate, not one denominator. |
| Frozen R1 membership | [`build_r1_paper_manifest.py`](scripts/process/build_r1_paper_manifest.py) | `data/manifests/r1_paper_v1.jsonl` (downloaded and rebuilt) | 142 ERC and 4,181 A2A retained records; input SHA-256 and row identity are checked. |
| Structured dataset | [`build_croissant_release.py`](scripts/process/build_croissant_release.py) | `data/croissant/v1/` | Five versioned dataset tables, schema, manifest, and checksums; vote tables are not extra records. |
| Historical R1/R2 results | [`scripts/analyse/`](scripts/analyse/) and [`scripts/visualise/`](scripts/visualise/) | [`analysis/metrics/r1/`](analysis/metrics/r1/), [`r2/`](analysis/metrics/r2/) | Existing network and discourse artifacts are checked as frozen tables. Historical network generation is a separate pipeline and may emit additional local files. |
| Robustness results | [`run_neurips26_robustness.py`](scripts/analyse/run_neurips26_robustness.py) | [`analysis/metrics/neurips26/`](analysis/metrics/neurips26/) | Seed 20260826; 2,000 bootstrap resamples; stage, channel, quarter, and tie-threshold tables. |
| Figure release | [`build_release_figures.py`](scripts/visualise/build_release_figures.py) | [`figures/`](figures/README.md) | Standard-library SVG generation, manifest SHA-256, XML and text/vector checks. |

The `make reproduce` workflow **rebuilds** the manifest, Croissant tables, and robustness summaries. It **verifies the tracked historical R1/R2 network and topic artifacts**, but does not rerun every hosted annotation or every historical network and topic visualization in one command. See [RESULTS.md](RESULTS.md) for the exact mapping and the distinction between the two scopes. This matters when interpreting “reproducible”: the frozen input and result lineage is available, while a live hosted-model call cannot promise identical labels.

The [historical pipeline command reference](WORKFLOW.md) preserves the individual collection, annotation, topic, and network commands from the previous release for readers who need to explore those stages separately.

## Integrity and interpretation

`make verify` runs [`verify_repository.py`](scripts/verify_repository.py) and [`verify_neurips26.py`](scripts/verify_neurips26.py), including checks for missing assets, expected table counts and hashes, Croissant metadata, and forbidden tracked payloads. `make figures-check` compares regenerated SVG bytes and provenance digests and rejects embedded bitmaps and external SVG resources. [ASSET_LICENSES.md](ASSET_LICENSES.md) distinguishes software, derived assets, source platform records, and the externally hosted dataset.

The corpus consists of public records; private decisions are unobserved. Formal access does not measure social inclusion. R1 and R2 differ in corpus scope and network construction. Cross-model agreement does not establish human-label accuracy. The findings identify governance capacities relevant to sustainable development but do not measure SDG outcomes or energy footprints of these protocols.
