#!/usr/bin/env python3
"""Unit tests for the read-only review-state helper."""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import review_state


LEDGER_HEADER = """# Routing Ledger — {review_id}

Demo: yes

| Date | Round | Doc version | From stage | To stage | Status / verdict | Reason | Source artifacts | Human actor |
|---|---|---|---|---|---|---|---|---|
"""


class ReviewStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.original_root = review_state.ROOT
        review_state.ROOT = self.root
        (self.root / "reviews").mkdir()

    def tearDown(self) -> None:
        review_state.ROOT = self.original_root
        self.temp.cleanup()

    def write(self, relative: str, content: str = "") -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def ledger(self, review_id: str, row: str) -> None:
        self.write(
            f"reviews/{review_id}-routing-log.md",
            LEDGER_HEADER.format(review_id=review_id) + row + "\n",
        )

    def test_status_detects_revision_files_without_advancing(self) -> None:
        self.ledger(
            "UT-001",
            "| 2026-07-19 | 01 | v1 | 02_editor-review | 03_author-revision | Revise Before Formal Review | findings | review.md | — |",
        )
        self.write("04_revision-intake/input/UT-001/design-sdd-v2.md", "# SDD v2")
        self.write(
            "04_revision-intake/input/UT-001/UT-001-revision-response-round-01.md",
            "# Revision response",
        )
        ledger = review_state.parse_ledger("UT-001")
        status = review_state.render_status(ledger)
        self.assertIn("Revision files detected for the current round — not yet accepted", status)
        self.assertIn("submit revision UT-001", status)
        self.assertEqual(ledger.latest["to_stage"], "03_author-revision")

    def test_automated_stage_status_names_current_work(self) -> None:
        self.ledger(
            "UT-001",
            "| 2026-07-19 | 02 | v2 | 04_revision-intake | 02_editor-review | revision intake complete | complete | manifest.md | — |",
        )
        status = review_state.render_status(review_state.parse_ledger("UT-001"))
        self.assertIn("automated editor review round 02", status)
        self.assertIn("Editor review round 02 is in progress", status)
        self.assertIn("No human action is required", status)

    def test_requirement_mismatch_warns_on_absolute_to_percentage(self) -> None:
        requirements = self.write(
            "01_intake/input/UT-001/project-requirements.md",
            "| ID | Requirement |\n|---|---|\n| R-05 | All customers receive a response within two minutes |\n",
        )
        self.assertTrue(requirements.exists())
        sdd = self.write(
            "04_revision-intake/input/UT-001/project-sdd-v2.md",
            "| Req | Acceptance criterion |\n|---|---|\n| R-05 | Pass when 95% receive a response within two minutes |\n",
        )
        warnings = review_state.requirement_mismatch_warnings("UT-001", sdd)
        self.assertEqual(len(warnings), 1)
        self.assertIn("95%", warnings[0])

    def test_response_blocks_require_disposition_location_and_explanation(self) -> None:
        response = self.write(
            "response.md",
            """## Finding 1: Test

- **Disposition (mark one):** [x] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:** Section 2
- **What changed / why (your own words):** Added a bounded fallback.
""",
        )
        count, problems = review_state.response_blocks(response)
        self.assertEqual(count, 1)
        self.assertEqual(problems, [])

    def test_response_blocks_reject_unselected_checkbox_options(self) -> None:
        response = self.write(
            "response.md",
            """## Finding 1: Test

- **Disposition (mark one):** [ ] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:** Section 2
- **What changed / why (your own words):** Added a bounded fallback.
""",
        )
        count, problems = review_state.response_blocks(response)
        self.assertEqual(count, 1)
        self.assertIn("finding 1 has no selected disposition", problems)

    def test_blank_response_fields_do_not_consume_the_next_label(self) -> None:
        response = self.write(
            "response.md",
            """## Finding 1: Test

- **Disposition (mark one):**
- **Where the design changed:**
- **What changed / why (your own words):**
- **Evidence / links:**
""",
        )
        _, problems = review_state.response_blocks(response)
        self.assertIn("finding 1 has no selected disposition", problems)
        self.assertIn("finding 1 has no change location", problems)
        self.assertIn("finding 1 has no author explanation", problems)

    def test_decision_value_rejects_unselected_template_options(self) -> None:
        text = """## Decision

`Approved` / `Approved with Conditions` / `Changes Required`

## Rationale
"""
        self.assertIsNone(review_state.decision_value(text))

    def test_blank_decision_fields_do_not_consume_the_next_label(self) -> None:
        block = """### OD-01 — Choose
- **Selected option / disposition (human):**
- **Reviewer rationale (human):**
- **Required concurrence and evidence (human):**
- **Blocking? (human):** yes / no / n-a
"""
        self.assertFalse(review_state.filled_field(block, "Selected option / disposition (human)"))
        self.assertFalse(review_state.filled_field(block, "Reviewer rationale (human)"))
        self.assertFalse(review_state.filled_field(block, "Required concurrence and evidence (human)"))
        self.assertFalse(review_state.filled_field(block, "Blocking? (human)"))

    def test_placeholders_are_not_human_dispositions(self) -> None:
        block = """### OD-01 — Choose
- **Selected option / disposition (human):** <select an option>
- **Reviewer rationale (human):** [insert rationale]
- **Required concurrence and evidence (human):** n/a
- **Blocking? (human):** n-a
"""
        self.assertFalse(review_state.filled_field(block, "Selected option / disposition (human)"))
        self.assertFalse(review_state.filled_field(block, "Reviewer rationale (human)"))
        self.assertFalse(review_state.filled_field(block, "Required concurrence and evidence (human)"))
        self.assertTrue(review_state.filled_field(block, "Blocking? (human)"))

    def test_blank_signature_fields_do_not_consume_the_next_label(self) -> None:
        text = """## Signature
- **Accountable reviewer (human actor):**
- **Role:**
- **Date signed (ISO 8601):**
"""
        self.assertEqual(review_state.parse_signature(text), ("", "", ""))

    def test_preflight_decision_accepts_complete_nonblocking_conditions(self) -> None:
        self.ledger(
            "UT-001",
            "| 2026-07-19 | 02 | v2 | 02_editor-review | 05_formal-review | Ready for Formal Review | ready | review.md | — |",
        )
        self.write(
            "05_formal-review/input/UT-001/UT-001-open-decision-index-round-02.md",
            """# Index

| ID | Source | State | Authority | Evidence | Question | Link |
|---|---|---|---|---|---|---|
| OD-01 | author | ready | Architect | none | Choose | design.md |
""",
        )
        self.write(
            "05_formal-review/output/UT-001/UT-001-formal-decision-round-02.md",
            """# Decision

- **Review ID:** UT-001

## Decision
`Approved with Conditions`

## Open decision dispositions

### OD-01 — Choose
- **Selected option / disposition (human):** Option A
- **Reviewer rationale (human):** Best fit for the requirement.
- **Required concurrence and evidence (human):** None required; architecture owner decision.
- **Blocking? (human):** no

## Conditions
| # | Condition | Owner | Disposition | Blocking? |
|---|---|---|---|---|
| 1 | Verify mapping | Platform owner | Accepted before build | no |

## Signature
- **Accountable reviewer (human actor):** A. Reviewer
- **Role:** Architect
- **Date signed (ISO 8601):** 2026-07-19
""",
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = review_state.preflight_decision("UT-001")
        self.assertEqual(code, 0, output.getvalue())
        self.assertIn("all 1 condition(s)", output.getvalue())

    def test_manifest_marks_history_as_history(self) -> None:
        self.ledger(
            "UT-001",
            "| 2026-07-19 | 02 | v2 | 02_editor-review | 05_formal-review | Ready for Formal Review | ready | review.md | — |",
        )
        self.write("05_formal-review/input/UT-001/project-sdd-v2.md", "current")
        self.write("05_formal-review/input/UT-001/history/project-sdd-v1.md", "old")
        self.write("05_formal-review/input/UT-001/UT-001-current-artifacts-round-02.md", "generated")
        content = review_state.manifest_content(review_state.parse_ledger("UT-001"))
        self.assertIn("`project-sdd-v2.md` | solution design | current", content)
        self.assertIn("`history/project-sdd-v1.md` | solution design | superseded/history", content)
        self.assertNotIn("current-artifacts-round-02.md` |", content)

    def test_manifest_distinguishes_form_from_signed_decision(self) -> None:
        self.ledger(
            "UT-001",
            "| 2026-07-19 | 02 | v2 | 02_editor-review | 05_formal-review | Ready for Formal Review | ready | review.md | — |",
        )
        self.write("05_formal-review/input/UT-001/UT-001-formal-decision-round-02-FORM.md", "blank")
        self.write("05_formal-review/input/UT-001/UT-001-formal-decision-round-02.md", "signed")
        content = review_state.manifest_content(review_state.parse_ledger("UT-001"))
        self.assertIn("formal-decision-round-02-FORM.md` | required human output form", content)
        self.assertIn("formal-decision-round-02.md` | human formal decision record", content)


if __name__ == "__main__":
    unittest.main()
