#!/usr/bin/env python3
"""Read-only workflow inspection and preflight helper.

This tool makes the markdown workflow observable without replacing the agent or
changing authoritative state. It never appends a routing-ledger row, moves a
package, critiques a design, or creates a formal decision.

Examples:
    python3 tools/review_state.py status UX-003
    python3 tools/review_state.py status UX-003 --write
    python3 tools/review_state.py preflight start UX-004
    python3 tools/review_state.py preflight revision UX-003
    python3 tools/review_state.py preflight decision UX-003
    python3 tools/review_state.py validate-state UX-003
    python3 tools/review_state.py manifest UX-003 --write
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACCEPTED_INPUT_SUFFIXES = {".md", ".txt", ".pdf", ".docx"}
LEDGER_FIELDS = (
    "date",
    "round",
    "doc_version",
    "from_stage",
    "to_stage",
    "status",
    "reason",
    "source_artifacts",
    "human_actor",
)
ABSOLUTE_REQUIREMENT_TERMS = re.compile(
    r"\b(all|every|must|never|always|within|no more than|at least)\b", re.I
)
QUALIFIER_TERMS = re.compile(r"\b(average|target|percentile|eligible)\b|\d+(?:\.\d+)?\s*%", re.I)


@dataclass
class Ledger:
    review_id: str
    demo: str
    rows: list[dict[str, str]]
    path: Path

    @property
    def latest(self) -> dict[str, str]:
        return self.rows[-1]


@dataclass
class CheckResult:
    failures: list[str]
    warnings: list[str]
    passes: list[str]

    def emit(self, heading: str) -> int:
        print(f"# {heading}")
        for item in self.passes:
            print(f"PASS: {item}")
        for item in self.warnings:
            print(f"WARN: {item}")
        for item in self.failures:
            print(f"FAIL: {item}")
        print(
            f"\nResult: {len(self.failures)} failure(s), "
            f"{len(self.warnings)} warning(s), {len(self.passes)} pass(es)"
        )
        return 1 if self.failures else 0


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_ledger(review_id: str) -> Ledger:
    path = ROOT / "reviews" / f"{review_id}-routing-log.md"
    if not path.exists():
        raise FileNotFoundError(f"No routing ledger found: {path.relative_to(ROOT)}")

    text = path.read_text(encoding="utf-8")
    demo_match = re.search(r"^Demo:\s*(yes|no)\b", text, re.M | re.I)
    demo = demo_match.group(1).lower() if demo_match else "unknown"
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = split_table_row(line)
        if len(cells) != len(LEDGER_FIELDS):
            continue
        if cells[0] in {"Date", "---"} or set(cells[0]) == {"-"}:
            continue
        rows.append(dict(zip(LEDGER_FIELDS, cells)))
    if not rows:
        raise ValueError(f"Routing ledger has no state rows: {path.relative_to(ROOT)}")
    return Ledger(review_id=review_id, demo=demo, rows=rows, path=path)


def numeric_round(value: str) -> int:
    match = re.search(r"\d+", value)
    return int(match.group()) if match else 0


def numeric_version(value: str) -> int:
    match = re.search(r"\d+", value)
    return int(match.group()) if match else 0


def relative(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def package_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted(
        p for p in path.rglob("*") if p.is_file() and p.name != "README.md" and not p.name.startswith(".")
    )


def find_sdd_files(path: Path) -> list[Path]:
    candidates = []
    for item in package_files(path):
        lowered = item.name.lower()
        if item.suffix.lower() not in ACCEPTED_INPUT_SUFFIXES:
            continue
        if "sdd" in lowered or "solution-design" in lowered or "solution_design" in lowered:
            candidates.append(item)
    return candidates


def version_from_path(path: Path) -> int:
    match = re.search(r"(?:^|[-_])v(\d+)(?:\D|$)", path.stem, re.I)
    return int(match.group(1)) if match else 0


def newest_versioned(paths: list[Path]) -> Path | None:
    if not paths:
        return None
    return max(paths, key=lambda path: (version_from_path(path), path.stat().st_mtime_ns, path.name))


def markdown_links(path: Path) -> list[Path]:
    if not path.exists() or path.suffix.lower() != ".md":
        return []
    text = path.read_text(encoding="utf-8")
    targets: list[Path] = []
    for raw in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
        target = raw.strip().split("#", 1)[0]
        if not target or re.match(r"^[a-z]+://", target, re.I) or target.startswith("mailto:"):
            continue
        targets.append((path.parent / target).resolve())
    return targets


def meaningful_value(value: str) -> bool:
    normalized = value.strip()
    if not normalized or normalized == "—":
        return False
    if re.fullmatch(r"<[^>]+>", normalized) or re.fullmatch(r"\[[^]]*(?:insert|enter|fill)[^]]*]", normalized, re.I):
        return False
    return True


def response_blocks(path: Path) -> tuple[int, list[str]]:
    if not path.exists():
        return 0, ["response log is missing"]
    text = path.read_text(encoding="utf-8")
    headings = list(re.finditer(r"^## Finding\s+(\d+):", text, re.M))
    problems: list[str] = []
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        block = text[match.start():end]
        number = match.group(1)
        disposition = re.search(
            r"^[ \t]*-[ \t]*\*\*Disposition(?: \(mark one\))?:\*\*[ \t]*([^\n]*)$",
            block,
            re.M | re.I,
        )
        disposition_text = disposition.group(1).strip() if disposition else ""
        checkboxes = re.findall(
            r"\[([ xX])\]\s*(resolved|partially resolved|disagree)",
            disposition_text,
            re.I,
        )
        if checkboxes:
            marked = sum(1 for mark, _ in checkboxes if mark.strip().lower() == "x") == 1
        else:
            marked = bool(
                re.fullmatch(
                    r"`?(resolved|partially resolved|disagree)`?",
                    disposition_text,
                    re.I,
                )
            )
        location = re.search(
            r"Where (?:the design )?changed:\*\*[ \t]*([^\n]*)",
            block,
            re.I,
        )
        rationale = re.search(
            r"What changed / why(?: \(your own words\))?:\*\*[ \t]*([^\n]*)",
            block,
            re.I,
        )
        if not marked:
            problems.append(f"finding {number} has no selected disposition")
        if not location or not meaningful_value(location.group(1)):
            problems.append(f"finding {number} has no change location")
        if not rationale or not meaningful_value(rationale.group(1)):
            problems.append(f"finding {number} has no author explanation")
    if not headings:
        problems.append("no finding blocks were detected")
    return len(headings), problems


def expected_finding_count(review_id: str, round_number: int) -> int:
    name = f"{review_id}-review-round-{round_number:02d}.md"
    candidates = [
        ROOT / "02_editor-review" / "output" / review_id / name,
        ROOT / "03_author-revision" / "input" / review_id / name,
    ]
    for path in candidates:
        if path.exists():
            text = path.read_text(encoding="utf-8")
            return len(re.findall(r"^###\s+\d+\.\s+", text, re.M))
    return 0


def parse_requirements(path: Path) -> dict[str, str]:
    requirements: dict[str, str] = {}
    if not path.exists() or path.suffix.lower() != ".md":
        return requirements
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = split_table_row(line) if line.startswith("|") else []
        if len(cells) >= 2 and re.fullmatch(r"R-\d+", cells[0], re.I):
            requirements[cells[0].upper()] = cells[1]
    return requirements


def latest_named_file(review_id: str, term: str, roots: list[Path]) -> Path | None:
    candidates: list[Path] = []
    for root in roots:
        candidates.extend(p for p in package_files(root) if term in p.name.lower())
    return newest_versioned(candidates) or (sorted(candidates)[-1] if candidates else None)


def requirement_mismatch_warnings(review_id: str, sdd: Path) -> list[str]:
    roots = [
        ROOT / "04_revision-intake" / "input" / review_id,
        ROOT / "02_editor-review" / "input" / review_id,
        ROOT / "01_intake" / "input" / review_id,
        sdd.parent,
    ]
    requirements_file = latest_named_file(review_id, "requirement", roots)
    if not requirements_file or not sdd.exists() or sdd.suffix.lower() != ".md":
        return []
    requirements = parse_requirements(requirements_file)
    sdd_lines = sdd.read_text(encoding="utf-8").splitlines()
    warnings: list[str] = []
    for req_id, wording in requirements.items():
        if not ABSOLUTE_REQUIREMENT_TERMS.search(wording):
            continue
        relevant = [line.strip() for line in sdd_lines if req_id in line]
        qualified = [
            line for line in relevant
            if QUALIFIER_TERMS.search(line)
            and re.search(r"accept|criterion|pass|success|sla|target|measure|test", line, re.I)
        ]
        percentages = []
        for line in qualified:
            percentages.extend(float(value) for value in re.findall(r"(\d+(?:\.\d+)?)\s*%", line))
        percentage_mismatch = [
            line for line in qualified
            if any(float(value) < 100 for value in re.findall(r"(\d+(?:\.\d+)?)\s*%", line))
        ]
        if percentage_mismatch or qualified:
            sample = (percentage_mismatch or qualified)[0][:180]
            warnings.append(
                f"{req_id} uses absolute wording ({wording!r}) but the SDD introduces a "
                f"qualified acceptance statement ({sample!r}); accountable reconciliation may be required"
            )
    return warnings


def preflight_start(review_id: str) -> int:
    result = CheckResult([], [], [])
    ledger_path = ROOT / "reviews" / f"{review_id}-routing-log.md"
    package = ROOT / "01_intake" / "input" / review_id
    if ledger_path.exists():
        result.failures.append(f"review ID is already assigned: {relative(ledger_path)}")
    else:
        result.passes.append("review ID is not present in the ledger registry")
    files = package_files(package)
    if not files:
        result.failures.append(f"no candidate submission files found in {relative(package)}")
        return result.emit(f"Preflight start — {review_id}")
    result.passes.append(f"detected {len(files)} candidate file(s) in {relative(package)}")
    sdds = find_sdd_files(package)
    sdd_text = ""
    if len(sdds) == 1:
        sdd = sdds[0]
        result.passes.append(f"one candidate SDD: {sdd.name}")
        if sdd.suffix.lower() in {".md", ".txt"}:
            sdd_text = sdd.read_text(encoding="utf-8", errors="ignore")
            stripped = len(sdd_text.strip())
            if stripped == 0:
                result.failures.append(f"SDD file is empty: {sdd.name}")
            elif stripped < 500:
                result.warnings.append(
                    f"SDD content is unusually small ({stripped} characters); confirm this is the real draft"
                )
        elif sdd.stat().st_size == 0:
            result.failures.append(f"SDD file is empty: {sdd.name}")
    elif not sdds:
        result.failures.append("no SDD-like filename detected")
    else:
        result.failures.append(f"multiple candidate SDDs detected: {', '.join(p.name for p in sdds)}")
    requirements = [p for p in files if "requirement" in p.name.lower()]
    if requirements:
        result.passes.append(f"requirements source detected: {requirements[-1].name}")
    else:
        result.warnings.append("no requirements-named file detected; intake must confirm whether requirements are embedded")
    assumptions = [p for p in files if "assumption" in p.name.lower() or "decision" in p.name.lower()]
    if assumptions:
        result.passes.append(f"assumptions/open-decisions source detected: {assumptions[-1].name}")
    else:
        result.warnings.append("no assumptions/open-decisions file detected; acceptable only when not applicable or embedded")
    diagrams = [p for p in files if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".drawio"}]
    if diagrams:
        result.passes.append(f"detected {len(diagrams)} separate diagram file(s)")
    elif re.search(r"```\s*(mermaid|plantuml)|\b(flowchart|sequenceDiagram|erDiagram|stateDiagram)\b", sdd_text):
        result.passes.append("embedded diagram blocks detected in the SDD (no separate diagram files)")
    else:
        result.warnings.append(
            "no diagrams detected (separate files or embedded blocks); missing author-produced diagrams pass through for critique"
        )
    return result.emit(f"Preflight start — {review_id}")


def preflight_revision(review_id: str) -> int:
    result = CheckResult([], [], [])
    try:
        ledger = parse_ledger(review_id)
    except (FileNotFoundError, ValueError) as error:
        result.failures.append(str(error))
        return result.emit(f"Preflight revision — {review_id}")
    latest = ledger.latest
    if latest["to_stage"] != "03_author-revision":
        result.failures.append(f"ledger is at {latest['to_stage']}, not the author-revision human stop")
    else:
        result.passes.append("ledger is waiting at author revision")
    package = ROOT / "04_revision-intake" / "input" / review_id
    files = package_files(package)
    if not files:
        result.failures.append(f"no revision files detected in {relative(package)}")
        return result.emit(f"Preflight revision — {review_id}")
    result.passes.append(f"detected {len(files)} submitted revision file(s)")
    current_version = numeric_version(latest["doc_version"])
    sdds = find_sdd_files(package)
    new_sdds = [path for path in sdds if version_from_path(path) > current_version]
    if len(new_sdds) == 1:
        result.passes.append(f"new SDD version detected: {new_sdds[0].name}")
    elif not new_sdds:
        result.failures.append(f"no SDD version newer than {latest['doc_version']} detected")
    else:
        result.failures.append(f"multiple new SDD candidates detected: {', '.join(p.name for p in new_sdds)}")
    round_number = numeric_round(latest["round"])
    response = package / f"{review_id}-revision-response-round-{round_number:02d}.md"
    count, problems = response_blocks(response)
    if response.exists():
        result.passes.append(f"response log detected for round {round_number:02d}")
    else:
        result.failures.append(f"missing response log: {response.name}")
    expected = expected_finding_count(review_id, round_number)
    if expected and count != expected:
        result.failures.append(f"response contains {count} finding block(s); prior review contains {expected}")
    elif expected:
        result.passes.append(f"all {expected} prior finding blocks are represented")
    result.failures.extend(problems)
    if not problems and count:
        result.passes.append("every response block has a disposition, location, and author explanation")
    chosen_sdd = new_sdds[0] if len(new_sdds) == 1 else newest_versioned(sdds)
    if chosen_sdd:
        result.warnings.extend(requirement_mismatch_warnings(review_id, chosen_sdd))
    return result.emit(f"Preflight revision — {review_id}")


def decision_value(text: str) -> str | None:
    section = re.search(r"^## Decision\s*(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not section:
        return None
    for line in section.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("<!--"):
            continue
        matches = re.findall(r"`(Approved with Conditions|Approved|Changes Required)`", stripped)
        if len(matches) == 1 and "/" not in stripped:
            return matches[0]
        return None
    return None


def parse_signature(text: str) -> tuple[str, str, str]:
    actor = re.search(
        r"Accountable reviewer \(human actor\):\*\*[ \t]*([^\n]*)",
        text,
        re.I,
    )
    role = re.search(
        r"^[ \t]*-[ \t]*\*\*Role:\*\*[ \t]*([^\n]*)",
        text,
        re.I | re.M,
    )
    signed = re.search(
        r"Date signed \(ISO 8601\):\*\*[ \t]*(\d{4}-\d{2}-\d{2})",
        text,
        re.I,
    )
    return (
        actor.group(1).strip() if actor else "",
        role.group(1).strip() if role else "",
        signed.group(1) if signed else "",
    )


def condition_rows(text: str) -> list[list[str]]:
    section = re.search(r"^## Conditions.*?(?=^## |\Z)", text, re.M | re.S)
    if not section:
        return []
    rows = []
    for line in section.group(0).splitlines():
        if not line.startswith("|"):
            continue
        cells = split_table_row(line)
        if len(cells) == 5 and cells[0] not in {"#", "---"} and set(cells[0]) != {"-"}:
            rows.append(cells)
    return rows


def formal_artifact(review_id: str, round_number: int, kind: str, output: bool = False) -> tuple[Path, Path]:
    root = ROOT / "05_formal-review" / ("output" if output else "input") / review_id
    names = {
        "packet": (f"{review_id}-formal-review-packet-round-{round_number:02d}.md", f"{review_id}-formal-review-packet.md"),
        "index": (f"{review_id}-open-decision-index-round-{round_number:02d}.md", f"{review_id}-open-decision-index.md"),
        "form": (f"{review_id}-formal-decision-round-{round_number:02d}-FORM.md", f"{review_id}-formal-decision-FORM.md"),
        "decision": (f"{review_id}-formal-decision-round-{round_number:02d}.md", f"{review_id}-formal-decision.md"),
        "manifest": (f"{review_id}-current-artifacts-round-{round_number:02d}.md", f"{review_id}-current-artifacts.md"),
    }
    current, legacy = names[kind]
    return root / current, root / legacy


def existing_formal_artifact(review_id: str, round_number: int, kind: str, output: bool = False) -> Path | None:
    current, legacy = formal_artifact(review_id, round_number, kind, output)
    if current.exists():
        return current
    if legacy.exists():
        return legacy
    return None


def decision_index_ids(review_id: str, round_number: int) -> list[str]:
    path = existing_formal_artifact(review_id, round_number, "index")
    if not path:
        return []
    if not path.exists():
        return []
    ids = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = split_table_row(line) if line.startswith("|") else []
        if cells and re.fullmatch(r"OD-(?:E)?\d+", cells[0], re.I):
            ids.append(cells[0].upper())
    return ids


def disposition_block(text: str, decision_id: str) -> str:
    pattern = rf"^###\s+{re.escape(decision_id)}\b.*?(?=^###\s+OD-|^##\s+|\Z)"
    match = re.search(pattern, text, re.M | re.S | re.I)
    return match.group(0) if match else ""


def filled_field(block: str, label: str) -> bool:
    match = re.search(
        rf"\*\*{re.escape(label)}[^*]*:\*\*[ \t]*([^\n]*)",
        block,
        re.I,
    )
    if not match:
        return False
    value = match.group(1).strip()
    if not meaningful_value(value) or value.lower() == "yes / no / n-a":
        return False
    if "concurrence" in label.lower() and value.lower() in {"n/a", "n-a", "na"}:
        return False
    return True


def preflight_decision(review_id: str) -> int:
    result = CheckResult([], [], [])
    try:
        ledger = parse_ledger(review_id)
    except (FileNotFoundError, ValueError) as error:
        result.failures.append(str(error))
        return result.emit(f"Preflight decision — {review_id}")
    latest = ledger.latest
    if latest["to_stage"] != "05_formal-review":
        result.failures.append(f"ledger is at {latest['to_stage']}, not formal review")
    else:
        result.passes.append("ledger is waiting at formal review")
    round_number = numeric_round(latest["round"])
    expected, legacy = formal_artifact(review_id, round_number, "decision", output=True)
    path = existing_formal_artifact(review_id, round_number, "decision", output=True)
    if not path:
        result.failures.append(f"no decision file detected at {relative(expected)}")
        return result.emit(f"Preflight decision — {review_id}")
    text = path.read_text(encoding="utf-8")
    result.passes.append("candidate formal decision file detected")
    value = decision_value(text)
    if not value:
        result.failures.append("Decision section has no single selected decision token")
    else:
        result.passes.append(f"selected decision: {value}")
    actor, role, signed_date = parse_signature(text)
    if meaningful_value(actor):
        result.passes.append(f"named human actor: {actor}")
    else:
        result.failures.append("signature has no named accountable human actor")
    if meaningful_value(role):
        result.passes.append(f"accountable reviewer role: {role}")
    else:
        result.failures.append("signature has no accountable reviewer role")
    try:
        date.fromisoformat(signed_date)
        result.passes.append(f"signature date: {signed_date}")
    except ValueError:
        result.failures.append("signature has no valid ISO date")
    metadata_id = re.search(
        r"^[ \t]*-[ \t]*\*\*Review ID:\*\*[ \t]*([^\s]+)",
        text,
        re.I | re.M,
    )
    if metadata_id and metadata_id.group(1) == review_id:
        result.passes.append("decision metadata matches the review ID")
    else:
        result.failures.append("decision metadata is missing the exact review ID")
    if path == legacy:
        result.warnings.append("legacy unversioned decision filename detected; new formal rounds use round-versioned records")
    index_ids = decision_index_ids(review_id, round_number)
    if index_ids:
        result.passes.append(f"authoritative decision index contains {len(index_ids)} ID(s)")
        for item in index_ids:
            block = disposition_block(text, item)
            if not block:
                result.failures.append(f"decision record has no disposition block for {item}")
                continue
            if not filled_field(block, "Selected option / disposition (human)"):
                result.failures.append(f"{item} has no human-selected disposition")
            if not filled_field(block, "Reviewer rationale (human)"):
                result.failures.append(f"{item} has no human reviewer rationale")
            if not filled_field(block, "Required concurrence and evidence (human)"):
                result.failures.append(f"{item} has no concurrence/evidence disposition (use an explicit 'none required' when applicable)")
            if not filled_field(block, "Blocking? (human)"):
                result.failures.append(f"{item} has no blocking-status disposition")
        if not any(any(item in failure for item in index_ids) for failure in result.failures):
            result.passes.append("every authoritative decision ID has a structured human disposition")
    else:
        result.warnings.append("no authoritative open-decision index found; legacy decision validation is less complete")
    if value == "Approved with Conditions":
        rows = condition_rows(text)
        if not rows:
            result.failures.append("Approved with Conditions has no condition rows")
        for row in rows:
            number, condition, owner, disposition, blocking = row
            if not all((number, condition, owner, disposition)):
                result.failures.append(f"condition row is incomplete: {row}")
            if blocking.strip().lower() != "no":
                result.failures.append(f"condition {number} is not explicitly non-blocking")
        if rows and not any("condition row" in item or "condition " in item for item in result.failures):
            result.passes.append(f"all {len(rows)} condition(s) are owned, dispositioned, and non-blocking")
    if value == "Changes Required":
        section = re.search(r"^## Required changes.*?(?=^## |\Z)", text, re.M | re.S | re.I)
        bullets = re.findall(r"^-\s+\S.+", section.group(0), re.M) if section else []
        if bullets:
            result.passes.append(f"{len(bullets)} required-change item(s) recorded")
        else:
            result.failures.append("Changes Required has no specific required-change bullets")
    return result.emit(f"Preflight decision — {review_id}")


def latest_verdict(ledger: Ledger) -> str:
    known = (
        "Approved with Conditions",
        "Changes Required",
        "Approved",
        "Ready for Formal Review with Open Decisions",
        "Ready for Formal Review",
        "Revise Before Formal Review",
        "Insufficient Context",
    )
    for row in reversed(ledger.rows):
        for value in known:
            if row["status"].lower() == value.lower():
                return row["status"]
    return ledger.latest["status"]


def revision_probe(ledger: Ledger) -> tuple[str, str]:
    review_id = ledger.review_id
    path = ROOT / "04_revision-intake" / "input" / review_id
    files = package_files(path)
    if not files:
        return "none", relative(path)
    current_round = numeric_round(ledger.latest["round"])
    current_version = numeric_version(ledger.latest["doc_version"])
    response = path / f"{review_id}-revision-response-round-{current_round:02d}.md"
    new_sdd = any(version_from_path(item) > current_version for item in find_sdd_files(path))
    if response.exists() and new_sdd:
        return "candidate", relative(path)
    return "stale", relative(path)


def decision_probe(ledger: Ledger) -> tuple[bool, str]:
    round_number = numeric_round(ledger.latest["round"])
    expected, _ = formal_artifact(ledger.review_id, round_number, "decision", output=True)
    found = existing_formal_artifact(ledger.review_id, round_number, "decision", output=True)
    return bool(found), relative(found or expected)


def render_status(ledger: Ledger) -> str:
    row = ledger.latest
    review_id = ledger.review_id
    stage = row["to_stage"]
    round_value = f"{numeric_round(row['round']):02d}"
    version = row["doc_version"]
    verdict = latest_verdict(ledger)
    lines = [
        f"# Status — {review_id}                      <!-- regenerated; ledger is authoritative -->",
        "",
        f"- **Where:** {stage} (round {round_value}, SDD {version}) — Demo: {ledger.demo}",
        f"- **Last verdict:** {verdict}",
    ]
    if stage == "03_author-revision":
        probe, location = revision_probe(ledger)
        probe_text = {
            "candidate": "Revision files detected for the current round — not yet accepted",
            "stale": "Only stale/prior revision files detected; no complete candidate for the current round",
            "none": "No revision files detected yet",
        }[probe]
        lines.extend(
            [
                "- **Waiting on:** the author",
                f"- **Submission check:** {probe_text} in `{location}/`",
                "",
                "## Your next action",
                "",
                f"1. Open [03_author-revision/input/{review_id}/{review_id}-author-packet.md](../03_author-revision/input/{review_id}/{review_id}-author-packet.md)",
                "2. Revise the SDD as a new version, complete the response form, and submit every changed artifact",
                f"3. Say `submit revision {review_id}` — the agent runs the revision preflight first",
                "",
                "## Rounds and versions",
                "",
                "- SDD version bumps when design content changes",
                "- Response-log round is the review round being answered",
                "- The next editor round starts only after revision intake passes",
                "- Supporting artifacts receive a new version only when their content changes",
            ]
        )
    elif stage == "05_formal-review":
        found, location = decision_probe(ledger)
        round_number = numeric_round(row["round"])
        packet = existing_formal_artifact(review_id, round_number, "packet") or formal_artifact(review_id, round_number, "packet")[0]
        decision_index = existing_formal_artifact(review_id, round_number, "index")
        lines.extend(
            [
                "- **Waiting on:** the accountable senior architect",
                f"- **Submission check:** {'Decision file detected — not yet validated' if found else 'No signed decision detected yet'} at `{location}`",
                "",
                "## Your next action",
                "",
                f"1. Open [{relative(packet)}](../05_formal-review/input/{review_id}/{packet.name})",
            ]
        )
        if decision_index:
            lines.append(f"2. Disposition every item in [{decision_index.name}](../05_formal-review/input/{review_id}/{decision_index.name})")
            lines.append(f"3. Say `continue {review_id}` — the agent validates the decision before advancing")
        else:
            lines.append("2. Review the current design, open decisions, and residual risks")
            lines.append(f"3. Complete the human decision form, then say `continue {review_id}` — the agent validates it before advancing")
    elif stage == "06_completed":
        manifest = ROOT / "06_completed" / "output" / review_id / f"{review_id}-completion-manifest.md"
        lines.extend(
            [
                "- **Waiting on:** no one — package is terminal",
                "- **Submission check:** Completed and read-only",
                "",
                "## Your next action",
                "",
                "Completed — new design changes require a new review ID referencing this one.",
                "",
                f"- [Completion manifest](../06_completed/output/{review_id}/{manifest.name})",
                f"- [Immutable package](../06_completed/input/{review_id}/)",
            ]
        )
    else:
        automated = {
            "01_intake": (
                "automated intake validation",
                "Intake validation is in progress",
            ),
            "02_editor-review": (
                f"automated editor review round {round_value}",
                f"Editor review round {round_value} is in progress",
            ),
            "04_revision-intake": (
                "automated revision-intake validation",
                "Revision submitted; revision-intake validation is in progress",
            ),
        }
        waiting, progress = automated.get(
            stage,
            ("workflow processing", "The invoked workflow is in progress"),
        )
        lines.extend(
            [
                f"- **Waiting on:** {waiting}",
                f"- **Submission check:** {progress}",
                "",
                "## Your next action",
                "",
                f"No human action is required. Run `validate-state {review_id}`, then continue from the latest ledger row.",
            ]
        )
    lines.extend(
        [
            "",
            "## Latest transition receipt",
            "",
            f"- **Transition:** {row['from_stage']} → {row['to_stage']}",
            f"- **Status:** {row['status']}",
            f"- **Reason:** {row['reason']}",
            f"- **Source artifacts:** {row['source_artifacts']}",
            "",
            "---",
            "Operator verbs: `start` · `continue <ID>` · `status <ID>` · `submit revision <ID>` · `preflight <start|revision|decision> <ID>` · `validate state <ID>`",
            "",
        ]
    )
    return "\n".join(lines)


def status_command(review_id: str, write: bool) -> int:
    try:
        ledger = parse_ledger(review_id)
    except (FileNotFoundError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    content = render_status(ledger)
    if write:
        path = ROOT / "reviews" / f"{review_id}-status.md"
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {relative(path)}")
    else:
        print(content, end="")
    return 0


def validate_links(paths: list[Path]) -> list[str]:
    failures = []
    for path in paths:
        for target in markdown_links(path):
            if not target.exists():
                failures.append(f"broken link in {relative(path)}: {target}")
    return failures


def validate_state(review_id: str) -> int:
    result = CheckResult([], [], [])
    try:
        ledger = parse_ledger(review_id)
    except (FileNotFoundError, ValueError) as error:
        result.failures.append(str(error))
        return result.emit(f"Validate state — {review_id}")
    row = ledger.latest
    result.passes.append(f"ledger parsed; latest stage is {row['to_stage']}")
    status_path = ROOT / "reviews" / f"{review_id}-status.md"
    if not status_path.exists():
        result.failures.append(f"missing derived status card: {relative(status_path)}")
    else:
        status_text = status_path.read_text(encoding="utf-8")
        expected = f"**Where:** {row['to_stage']} (round {numeric_round(row['round']):02d}, SDD {row['doc_version']})"
        if expected in status_text:
            result.passes.append("status stage, round, and version match the latest ledger row")
        else:
            result.failures.append("status stage/round/version does not match the latest ledger row")
        if f"Demo: {ledger.demo}" in status_text:
            result.passes.append("status demo flag matches the ledger")
        else:
            result.failures.append("status demo flag does not match the ledger")
    registry = sorted((ROOT / "reviews").glob(f"{review_id}-*"))
    allowed = {
        ROOT / "reviews" / f"{review_id}-routing-log.md",
        ROOT / "reviews" / f"{review_id}-status.md",
    }
    unexpected = [path for path in registry if path not in allowed]
    if unexpected:
        result.failures.append(f"unexpected registry files: {', '.join(relative(p) for p in unexpected)}")
    else:
        result.passes.append("review registry contains only the ledger and status card")
    stage_input = ROOT / row["to_stage"] / "input" / review_id
    if row["to_stage"] == "01_intake":
        stage_input = ROOT / "01_intake" / "input" / review_id
    if stage_input.exists() or row["to_stage"] == "06_completed":
        result.passes.append(f"current-stage package location exists: {relative(stage_input)}")
    else:
        result.failures.append(f"current-stage package location is missing: {relative(stage_input)}")
    # Validate navigation at the active human stop. Formal packet covers that
    # have already been flattened into a terminal archive are historical
    # evidence; their pre-completion relative links are intentionally not live
    # navigation and the completion manifest provides the terminal index.
    link_sources = [status_path] if status_path.exists() else []
    if row["to_stage"] == "03_author-revision":
        link_sources.append(
            ROOT / "03_author-revision" / "input" / review_id / f"{review_id}-author-packet.md"
        )
    elif row["to_stage"] == "05_formal-review":
        formal_root = ROOT / "05_formal-review" / "input" / review_id
        link_sources.extend(formal_root.glob(f"{review_id}-formal-review-packet*.md"))
        link_sources.extend(formal_root.glob(f"{review_id}-open-decision-index*.md"))
    link_sources = [path for path in link_sources if path.exists()]
    link_failures = validate_links(sorted(set(link_sources)))
    if link_failures:
        result.failures.extend(link_failures)
    elif link_sources:
        result.passes.append(f"validated relative links in {len(set(link_sources))} status/packet file(s)")
    if row["to_stage"] == "03_author-revision":
        packet = ROOT / "03_author-revision" / "input" / review_id / f"{review_id}-author-packet.md"
        if packet.exists():
            result.passes.append("author packet exists")
        else:
            result.failures.append("author-revision state has no author packet")
    if row["to_stage"] == "05_formal-review":
        packet_root = ROOT / "05_formal-review" / "input" / review_id
        round_number = numeric_round(row["round"])
        required = [
            ("packet", "formal packet cover"),
            ("form", "formal decision form"),
        ]
        for kind, label in required:
            path = existing_formal_artifact(review_id, round_number, kind)
            if path:
                result.passes.append(f"{label} exists: {path.name}")
            else:
                result.failures.append(f"{label} is missing: {formal_artifact(review_id, round_number, kind)[0].name}")
        decision_index = existing_formal_artifact(review_id, round_number, "index")
        if decision_index:
            result.passes.append(f"authoritative open-decision index exists: {decision_index.name}")
        else:
            result.warnings.append("legacy formal packet has no generated open-decision index")
    if row["to_stage"] != "06_completed":
        completed = ROOT / "06_completed" / "input" / review_id
        if completed.exists() and package_files(completed):
            result.failures.append("non-terminal ledger state has files in 06_completed")
        else:
            result.passes.append("no premature completed package detected")
    else:
        verify_terminal_package(review_id, result)
    return result.emit(f"Validate state — {review_id}")


MANIFEST_ROW_RE = re.compile(
    r"^\|\s*`([^`]+)`\s*\|([^|]*)\|([^|]*)\|[^|]*\|\s*`([0-9a-f]{64})`\s*\|"
)


def verify_terminal_package(review_id: str, result: "CheckResult") -> None:
    """Recompute checksums for the immutable terminal package against its stored manifest."""
    package = ROOT / "06_completed" / "input" / review_id
    manifests = sorted(package.rglob(f"{review_id}-current-artifacts*.md"))
    if not manifests:
        result.warnings.append(
            "terminal package has no checksummed artifact manifest; tampering cannot be verified (legacy run)"
        )
        return
    manifest = manifests[-1]
    checked = 0
    clean = True
    for line in manifest.read_text(encoding="utf-8").splitlines():
        match = MANIFEST_ROW_RE.match(line)
        if not match:
            continue
        rel, role, state, digest = (
            match.group(1),
            match.group(2).strip(),
            match.group(3).strip(),
            match.group(4),
        )
        target = package / rel
        if not target.exists():
            # Superseded/history rows and the pre-signature FORM are legitimately
            # absent from the terminal package; only a missing current design is fatal.
            if state == "current" and role == "solution design":
                result.failures.append(
                    f"terminal integrity: current solution design missing from terminal package: `{rel}`"
                )
                clean = False
            elif state == "current" and "form" not in role:
                result.warnings.append(
                    f"terminal integrity: manifest lists current `{rel}` but it is absent from the terminal package"
                )
            continue
        checked += 1
        if sha256(target) != digest:
            result.failures.append(
                f"terminal integrity: SHA-256 mismatch for `{rel}` against {manifest.name} — terminal package was modified after completion"
            )
            clean = False
    if checked and clean:
        result.passes.append(
            f"terminal package integrity verified: {checked} artifact checksum(s) match {manifest.name}"
        )
    elif not checked:
        result.warnings.append(f"terminal manifest {manifest.name} lists no verifiable rows")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_content(ledger: Ledger) -> str:
    row = ledger.latest
    review_id = ledger.review_id
    stage = row["to_stage"]
    package = ROOT / stage / "input" / review_id
    files = package_files(package)
    current_version = numeric_version(row["doc_version"])
    current_round = numeric_round(row["round"])
    rows = []
    for path in files:
        name = path.name.lower()
        # Generated manifests are verification outputs, not inputs to their own
        # checksum inventory. Excluding them keeps repeated generation stable.
        if re.fullmatch(rf"{re.escape(review_id.lower())}-current-artifacts(?:-round-\d+)?\.md", name):
            continue
        role = "supporting artifact"
        state = "current"
        if "history" in path.relative_to(package).parts:
            state = "history"
        if "sdd" in name:
            role = "solution design"
            state = "current" if state != "history" and version_from_path(path) == current_version else "superseded/history"
        elif "review-round" in name:
            role = "editor review"
            round_match = re.search(r"round-(\d+)", name)
            state = "current" if round_match and int(round_match.group(1)) == current_round else "superseded/history"
        elif "response-round" in name:
            role = "author response"
            state = "history"
        elif "template" in name:
            role = "legacy copied template"
            state = "superseded/history"
        elif "requirement" in name:
            role = "requirements"
        elif "formal-review-packet" in name:
            role = "packet cover"
        elif re.search(r"formal-decision.*-form\.md$", name):
            role = "required human output form"
        elif "formal-decision" in name and "template" not in name:
            role = "human formal decision record"
        elif "open-decision-index" in name:
            role = "authoritative decision index"
        elif "assumption" in name or "decision" in name:
            role = "decision/support register"
        rows.append(
            f"| `{path.relative_to(package).as_posix()}` | {role} | {state} | "
            f"{row['doc_version']} / round {current_round:02d} | `{sha256(path)}` |"
        )
    return "\n".join(
        [
            f"# Current Artifact Manifest — {review_id}",
            "",
            f"- **Authoritative stage:** `{stage}`",
            f"- **Document version:** `{row['doc_version']}`",
            f"- **Review round:** `{current_round:02d}`",
            "- **Purpose:** generated inventory for verification; the routing ledger remains authoritative workflow state.",
            "",
            "| Artifact | Role | State | Declared context | SHA-256 |",
            "|---|---|---|---|---|",
            *rows,
            "",
        ]
    )


def manifest_command(review_id: str, write: bool) -> int:
    try:
        ledger = parse_ledger(review_id)
    except (FileNotFoundError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    content = manifest_content(ledger)
    if write:
        stage = ledger.latest["to_stage"]
        round_number = numeric_round(ledger.latest["round"])
        if stage == "05_formal-review":
            path = formal_artifact(review_id, round_number, "manifest")[0]
        else:
            path = ROOT / stage / "input" / review_id / f"{review_id}-current-artifacts-round-{round_number:02d}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {relative(path)}")
    else:
        print(content, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    status = subparsers.add_parser("status", help="render the derived status card")
    status.add_argument("review_id")
    status.add_argument("--write", action="store_true", help="write reviews/<ID>-status.md")
    validate = subparsers.add_parser("validate-state", aliases=["validate"], help="check ledger/status/package consistency")
    validate.add_argument("review_id")
    preflight = subparsers.add_parser("preflight", help="inspect a human submission without changing state")
    preflight_sub = preflight.add_subparsers(dest="preflight_kind", required=True)
    for name in ("start", "revision", "decision"):
        command = preflight_sub.add_parser(name)
        command.add_argument("review_id")
    manifest = subparsers.add_parser("manifest", help="render a checksummed current-artifact manifest")
    manifest.add_argument("review_id")
    manifest.add_argument("--write", action="store_true", help="write the manifest into the current stage input package")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    review_id = getattr(args, "review_id", "").upper()
    if not re.fullmatch(r"[A-Z]+-\d{3}", review_id):
        print("ERROR: review ID must match PREFIX-000 (for example UX-003)", file=sys.stderr)
        return 2
    if args.command == "status":
        return status_command(review_id, args.write)
    if args.command in {"validate-state", "validate"}:
        return validate_state(review_id)
    if args.command == "manifest":
        return manifest_command(review_id, args.write)
    if args.command == "preflight":
        return {
            "start": preflight_start,
            "revision": preflight_revision,
            "decision": preflight_decision,
        }[args.preflight_kind](review_id)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
