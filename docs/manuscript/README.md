# Manuscript

The manuscript uses `{{TOKEN}}` placeholders that are hydrated by
`scripts/z_generate_manuscript_variables.py` into `output/manuscript/` before
rendering.

`source_ledger.yaml` is the offline citation-source ledger for the
current-trends survey section. It uses schema
`template-autoresearch-source-ledger-v1`; each row declares `citekey`,
`canonical_url`, `source_tier`, and `checked_as_of`. Project tests validate
shape, HTTPS canonical URLs, non-future ISO dates, allowed source tiers,
BibTeX coverage, and numbered manuscript citation coverage without making
network calls.

## Read the manuscript

- [Abstract](00_abstract.md) and [introduction](01_introduction.md)
- [Methodology](02_methodology.md), [results](03_results.md), and [conclusion](04_conclusion.md)
- [References](99_references.md), [bibliography](references.bib), and [source ledger](source_ledger.yaml)
- [Configuration](config.yaml) and [runbook](../runbook.md)
