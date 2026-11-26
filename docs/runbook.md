# Runbook

The core run uses the checked-in fixture and fixed seeds. It evaluates a finite set of candidates, writes the evidence and review packet, then renders the manuscript. The default human-review state is deferred.

## Set up a pinned runner

Install Python 3.14+, uv, Pandoc 3.14, the matching `pandoc-crossref` v0.3.26b release, and XeLaTeX with the [template's TeX packages](https://github.com/docxology/template/blob/87704feae0a4490ef7dad9c931d268e8c30273c2/README.md#L565-L574). Set `AUTORESEARCH_CHECKOUT` to the absolute path of a clean checkout of this repository.

```sh
git clone https://github.com/docxology/template.git autoresearch-template-runner
cd autoresearch-template-runner
git checkout --detach 87704feae0a4490ef7dad9c931d268e8c30273c2
uv sync --locked
project=projects/working/template_autoresearch_project
mkdir -p projects/working
git -C "$AUTORESEARCH_CHECKOUT" worktree add --detach "$PWD/$project" HEAD
```

## Test, analyze, render, and validate

From the template root, run the native tests and source-ledger audit:

```sh
uv run --no-sync --with pytest --with pytest-cov pytest "$project/tests" \
  --cov="$project/src" --cov-fail-under=90
uv run python "$project/scripts/check_source_ledger.py"
```

In the detached worktree, move the tracked publication snapshot aside and start with new analysis and rendered outputs:

```sh
mv "$project/output" "$(mktemp -d)/published-output"
uv run python scripts/pipeline/stage_02_analysis.py --project working/template_autoresearch_project
uv run python scripts/pipeline/stage_03_render.py --project working/template_autoresearch_project
uv run python scripts/maintenance/refresh_artifact_manifests.py --project working/template_autoresearch_project
uv run python scripts/pipeline/stage_04_validate.py --project working/template_autoresearch_project
```

Stage 02 runs the bounded loop and hydrates the manuscript. Stage 03 produces the combined PDF under `$project/output/pdf/`, HTML at `$project/output/web/index.html`, and per-section PDFs under `$project/output/slides/`. Check the abstract's hydrated metrics, numbered sections, citations, and diagnostic figures. The rendered evidence tables name local artifacts so readers can locate them in the output tree. Stage 04 records validation and source provenance in `$project/output/reports/`. See the [output inventory](outputs.md) for evidence and review artifacts.

Check documentation navigation from the project checkout with Lychee:

```sh
git diff --check
lychee --offline README.md AGENTS.md STANDALONE.md program.md 'docs/**/*.md'
```

## Loop sequence (`src.loop.run_autoresearch_loop`)

1. Compose plan via `build_autoresearch_plan()` and merge manuscript settings
   via `build_loop_config()`.
2. Write core artifacts (plan JSON, loop markdown, stage matrix CSV, figure).
3. Write the first evidence registry snapshot from on-disk artifacts.
4. Run the bounded local MNIST neural-network task and write resolved config,
   results, candidate ledger, confusion matrix, training history, error
   examples, probability records, classification diagnostics, calibration
   report, calibration-bin intervals, candidate accuracy intervals,
   class-balance counts, robustness report, probability diagnostics, bootstrap
   intervals, paired baseline comparison, statistical summary, training
   diagnostics, candidate rank-stability diagnostics, report, benchmark score,
   candidate-selection audit, diagnostic-boundary report, candidate-score
   figure, rank-stability figure, and figure-quality report.
5. Build file-backed claims and finalize loop JSON, review packet, summary, and
   manuscript variables.
6. Write method-contract artifacts: research program, idea ledger, run ledger,
   deferred review decisions, benchmark grading report, and benchmark scores.
7. Refresh loop payloads provisionally (`readiness_valid=False`) and write the
   first local security artifacts, schema manifest, local research-object
   manifest, phase ledger, and artifact manifest.
8. Run intrinsic readiness checks, including disclosure from the hydrated
   variables, and extrinsic readiness checks (evidence registry, artifact manifest,
   required artifacts, method ledgers, review gates, benchmark outputs, and
   enabled security artifacts).
9. Write the combined intrinsic + extrinsic readiness report.
10. Rebuild claims after readiness reports exist and refresh loop payloads with
   final `readiness_valid` and output paths.
11. Regenerate final figures and figure registry captions from the final loop
   state, including candidate scores, confusion matrix, per-class accuracy,
   learning curves, complexity/accuracy, error examples, calibration,
   classification metrics, confusion pairs, generalization gaps, robustness
   matrix, probability and margin distributions, bootstrap intervals, paired
   correctness, selective accuracy, probability quality, training dynamics,
   candidate rank stability, candidate lifecycle, local class balance, local
   data contact sheet, readiness matrix, closure flow, security-control matrix,
   and integrity chain.
12. Write manuscript variables, registry-backed figure blocks, and variable
   provenance sidecars.
13. Rewrite the compact evidence-registry report, security artifacts, phase
   ledger, schema manifest, local research-object manifest, figure-quality
   report, and artifact manifest.

The evidence registry is validated in memory. By default,
`output/reports/evidence_registry.json` is a compact reviewer-facing summary
with counts and a bounded fact sample. To debug individual registry facts
locally, run the loop with `TEMPLATE_EVIDENCE_REGISTRY_FULL=1`; this additionally
writes `output/reports/evidence_registry_full.json`, which is not part of the
required artifact contract.

Targeted checks:

```bash
uv run python scripts/pipeline/stage_01_test.py --project working/template_autoresearch_project --project-only --quiet
uv run python scripts/pipeline/stage_02_analysis.py --project working/template_autoresearch_project
uv run python -m infrastructure.autoresearch.cli plan --project working/template_autoresearch_project
uv run python -m infrastructure.autoresearch.cli benchmark --project working/template_autoresearch_project
uv run python -m infrastructure.autoresearch.cli validate --project working/template_autoresearch_project --fail-on-issues
```

Review `output/reports/autoresearch_review_packet.md` before treating the
generated outputs as publication-ready. The exemplar records review readiness;
it does not approve itself.
Also review `output/reports/autoresearch_security_review.md`; it is local
artifact-integrity evidence, not an external security certification.
Use `output/data/autoresearch_schema_manifest.json` to confirm schema-versioned
JSON governance payloads and `output/data/research_object_manifest.json` to
review the local package of observed paths and checksums.

## Fixture maintenance

The default pipeline uses the checked-in `data/mnist_small.npz` fixture and does
not download MNIST. To intentionally rebuild that fixture, run the manual
maintenance utility:

```bash
uv run python $project/scripts/regenerate_mnist_fixture.py
```

Do not wire this script into project tests, analysis, rendering, validation, or
CI. The maintenance path verifies the fixed HTTPS source URL, file sizes, and
SHA-256 hashes before rewriting the fixture and provenance files.
