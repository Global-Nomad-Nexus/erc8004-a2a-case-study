# Checked vector figures

These four SVG files render directly on GitHub. Text, lines, markers, and bars are native SVG elements and remain sharp at any display resolution. They contain no embedded bitmap, remote font, external stylesheet, third-party icon, or SDG logo.

| File | Role and evidence class | Input |
|---|---|---|
| [`hero.svg`](hero.svg) | Conceptual navigation through governance structures and the evidence pipeline; no quantitative effect is drawn. | Schematic based on the primary standards charters and the repository workflow. |
| [`participation-inequality.svg`](participation-inequality.svg) | R1 degree-Gini comparison; descriptive. | [`analysis/metrics/r1/network_metrics_table.csv`](../analysis/metrics/r1/network_metrics_table.csv) |
| [`scope-connectivity.svg`](scope-connectivity.svg) | R1 and R2 giant-component ratios shown in distinct panels; descriptive, not causal. | R1 and R2 network metric CSVs. |
| [`argument-bootstrap.svg`](argument-bootstrap.svg) | Five A2A-minus-ERC estimates and 95% resampling intervals; descriptive. | [`analysis/metrics/neurips26/bootstrap_argument_differences.csv`](../analysis/metrics/neurips26/bootstrap_argument_differences.csv) |

Regenerate and check without a model service or a Python package installation:

```bash
python3 scripts/visualise/build_release_figures.py
python3 scripts/visualise/build_release_figures.py --check
python3 scripts/verify_release_assets.py
```

Run these commands from the repository root. [`manifest.json`](manifest.json) records the source-code path, input SHA-256 values, output SHA-256 values, alt text, and the limitation of each display. Colors distinguish ERC (cyan), A2A (green), and interpretation boundaries (amber); all quantitative marks have text labels. The SVG `<title>` and `<desc>` provide alternatives for assistive technologies.

The gallery is a new visualization of **existing released tables**, not a substitute for the historic analysis figures. The older image inventory is in [`analysis/`](../analysis/README.md). To redraw with another palette or typography, edit [`build_release_figures.py`](../scripts/visualise/build_release_figures.py); the data values and caveats should still be checked against the linked tables.
