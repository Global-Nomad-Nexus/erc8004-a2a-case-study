.PHONY: verify manifest robustness reproduce all figures figures-check

verify:
	uv run python scripts/verify_repository.py
	uv run python scripts/verify_neurips26.py
	python3 scripts/verify_release_assets.py

figures:
	python3 scripts/visualise/build_release_figures.py

figures-check:
	python3 scripts/verify_release_assets.py

manifest:
	uv run python scripts/process/build_r1_paper_manifest.py

robustness:
	uv run python scripts/analyse/run_neurips26_robustness.py

reproduce:
	uv run python scripts/reproduce_release.py

all: reproduce
