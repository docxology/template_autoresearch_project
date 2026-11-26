# Fork guide

Fork this repository and register the checkout in the pinned template runner
using the [runbook](runbook.md). The shared runner provides the AutoResearch
planner, artifact hashing, evidence registry, rendering, and validation.

- Update [the manuscript config](manuscript/config.yaml), project metadata,
  source ledger, and human-authored research program.
- Define the new task, candidate budget, evidence requirements, and review
  decisions in the [project configuration](configuration.md).
- Run the tests and analysis on the fork's data, then render and validate.
  Link claims to the fork's generated evidence and record publication
  decisions in `human_review.yaml`.

The default run demonstrates a bounded offline loop on the shipped fixture.
Claims about other datasets or performance require evidence from those runs.
