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

    def test_validate_state_detects_terminal_tampering(self) -> None:
        self.ledger(
            "UT-090",
            "| 2026-07-19 | 02 | v2 | 05_formal-review | 06_completed | Approved | human decision | decision.md | A. Human |",
        )
        sdd = self.write("06_completed/input/UT-090/design-sdd-v2.md", "# Approved design\n")
        digest = review_state.sha256(sdd)
        self.write(
            "06_completed/input/UT-090/UT-090-current-artifacts-round-02.md",
            "# Current Artifact Manifest — UT-090\n\n"
            "| Artifact | Role | State | Declared context | SHA-256 |\n"
            "|---|---|---|---|---|\n"
            f"| `design-sdd-v2.md` | solution design | current | v2 / round 02 | `{digest}` |\n",
        )
        sdd.write_text("# Approved design\nTAMPERED AFTER COMPLETION\n", encoding="utf-8")
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = review_state.validate_state("UT-090")
        self.assertNotEqual(code, 0)
        self.assertIn("SHA-256 mismatch", buffer.getvalue())

    def test_validate_state_passes_untampered_terminal_package(self) -> None:
        self.ledger(
            "UT-091",
            "| 2026-07-19 | 02 | v2 | 05_formal-review | 06_completed | Approved | human decision | decision.md | A. Human |",
        )
        sdd = self.write("06_completed/input/UT-091/design-sdd-v2.md", "# Approved design\n")
        digest = review_state.sha256(sdd)
        self.write(
            "06_completed/input/UT-091/UT-091-current-artifacts-round-02.md",
            "| Artifact | Role | State | Declared context | SHA-256 |\n"
            "|---|---|---|---|---|\n"
            f"| `design-sdd-v2.md` | solution design | current | v2 / round 02 | `{digest}` |\n",
        )
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            review_state.validate_state("UT-091")
        self.assertIn("terminal package integrity verified", buffer.getvalue())

    def test_preflight_start_fails_on_empty_sdd(self) -> None:
        self.write("01_intake/input/UT-092/acme-sdd-draft-v1.md", "   \n")
        self.write("01_intake/input/UT-092/acme-requirements.md", "| R-01 | req |")
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = review_state.preflight_start("UT-092")
        self.assertNotEqual(code, 0)
        self.assertIn("empty", buffer.getvalue())

    def test_preflight_start_recognizes_embedded_diagrams(self) -> None:
        body = "# Acme SDD\n" + ("Design content. " * 60) + "\n```mermaid\nflowchart TD\nA-->B\n```\n"
        self.write("01_intake/input/UT-093/acme-sdd-draft-v1.md", body)
        self.write("01_intake/input/UT-093/acme-requirements.md", "| R-01 | req |")
        self.write("01_intake/input/UT-093/acme-assumptions-open-decisions.md", "- A-01")
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            review_state.preflight_start("UT-093")
        out = buffer.getvalue()
        self.assertIn("embedded diagram blocks detected", out)
        self.assertNotIn("no diagrams detected", out)

    def _formal_setup(self, review_id: str, index_row: str) -> None:
        self.ledger(
            review_id,
            "| 2026-07-19 | 02 | v2 | 02_editor-review | 05_formal-review | Ready for Formal Review with Open Decisions | decisions | review.md | — |",
        )
        self.write(
            f"05_formal-review/input/{review_id}/{review_id}-open-decision-index-round-02.md",
            "| ID | Source | State | Required authority | Missing evidence | Question | Link |\n"
            "|---|---|---|---|---|---|---|\n" + index_row + "\n",
        )

    def _decision(self, review_id: str, disposition: str, concurrence: str) -> None:
        self.write(
            f"05_formal-review/output/{review_id}/{review_id}-formal-decision-round-02.md",
            f"# Formal Architecture Review Decision — {review_id} — Round 02\n\n"
            f"- **Review ID:** {review_id}\n\n"
            "## Decision\n\n`Changes Required`\n\n"
            "### OD-01 — Sample decision\n\n"
            f"- **Selected option / disposition (human):** {disposition}\n"
            "- **Reviewer rationale (human):** Because reasons stated by the human.\n"
            f"- **Required concurrence and evidence (human):** {concurrence}\n"
            "- **Blocking? (human):** yes\n\n"
            "## Required changes (only for Changes Required)\n\n- 1. Do the thing.\n\n"
            "## Signature\n\n"
            "- **Accountable reviewer (human actor):** A. Human\n"
            "- **Role:** Senior Architect\n"
            "- **Date signed (ISO 8601):** 2026-07-19\n",
        )

    def test_content_missing_decision_cannot_be_approved(self) -> None:
        self._formal_setup(
            "UT-094",
            "| OD-01 | register | content missing | Architect | wording draft | Approve wording? | link |",
        )
        self._decision("UT-094", "Approve the wording as drafted", "E-commerce owner confirmation")
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = review_state.preflight_decision("UT-094")
        self.assertNotEqual(code, 0)
        self.assertIn("cannot be approved", buffer.getvalue())

    def test_content_missing_accepts_required_change_disposition(self) -> None:
        self._formal_setup(
            "UT-095",
            "| OD-01 | register | content missing | Architect | wording draft | Approve wording? | link |",
        )
        self._decision("UT-095", "Returned to the author as required change 1", "E-commerce owner confirmation once drafted")
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            review_state.preflight_decision("UT-095")
        self.assertNotIn("cannot be approved", buffer.getvalue())

    def test_gated_concurrence_rejects_self_waiver(self) -> None:
        self._formal_setup(
            "UT-096",
            "| OD-01 | register | Security/Privacy concurrence needed | Architect + Security | concurrence | Approach? | link |",
        )
        self._decision("UT-096", "Returned to the author as required change 1", "None required")
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = review_state.preflight_decision("UT-096")
        self.assertNotEqual(code, 0)
        self.assertIn("self-waiver", buffer.getvalue())

    def test_round_versioned_decision_requires_index(self) -> None:
        self.ledger(
            "UT-097",
            "| 2026-07-19 | 02 | v2 | 02_editor-review | 05_formal-review | Ready for Formal Review with Open Decisions | decisions | review.md | — |",
        )
        self._decision("UT-097", "Returned to the author", "Named evidence")
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = review_state.preflight_decision("UT-097")
        self.assertNotEqual(code, 0)
        self.assertIn("requires the authoritative open-decision index", buffer.getvalue())

    def test_preflight_revision_fails_on_empty_revised_sdd(self) -> None:
        self.ledger(
            "UT-098",
            "| 2026-07-19 | 01 | v1 | 02_editor-review | 03_author-revision | Revise Before Formal Review | findings | review.md | — |",
        )
        self.write("04_revision-intake/input/UT-098/acme-sdd-draft-v2.md", "  \n")
        self.write("04_revision-intake/input/UT-098/UT-098-revision-response-round-01.md", "# log")
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = review_state.preflight_revision("UT-098")
        self.assertNotEqual(code, 0)
        self.assertIn("revised SDD file is empty", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
