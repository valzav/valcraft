#!/usr/bin/env python3
"""Check static consistency of Valcraft's coordination contracts.

This is drift insurance for declarations. Behavioral evals remain the proof that the
skills and delivery loop behave as specified.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = Path("plugins/valcraft/skills/foreman/references/contracts.md")
BACKENDS = Path("plugins/valcraft/skills/foreman/references/backends/README.md")
BACKEND_DIRECTORY = BACKENDS.parent
FOREMAN_EVALS = Path("plugins/valcraft/skills/foreman/evals/evals.json")

BACKEND_RETURNS = {
    "report_available": ("terminal", "ReportValidation"),
    "permission_blocked": (
        "wait for an allowed answer or escalation",
        "BlockedPrompt",
    ),
    "idle_without_report": ("terminal", "WorkerRecovery"),
    "dispatch_error": ("terminal", "DispatchRecovery"),
    "dead": ("terminal", "DeadWorkerRecovery"),
    "wait_timeout": (
        "nonterminal; foreground only",
        "remain in the current named state and re-arm await",
    ),
}

LAND_EXECUTION_FIELDS = {
    "Execution capability",
    "Permission signal",
    "Permission return",
    "Producer failure",
}

# These fingerprints name only the producer-owned report headings and their order. The
# linked producer file remains authoritative for fields, meaning, status, and behavior.
REPORT_HEADINGS = {
    "plugins/valcraft/skills/cast/SKILL.md#report": (
        "## Cast report",
        "### Project frame",
        "### Scaffold baseline",
        "### Tracker",
        "### Spec handoff",
        "### Outward mutations",
        "### Blockers",
    ),
    "plugins/valcraft/skills/draft/references/plan-contract.md#report": (
        "## Draft report",
        "### Task",
        "### Plan",
        "### MSW",
        "### Review target",
        "### Finding resolutions",
        "### Outward mutations",
        "### Open questions",
    ),
    "plugins/valcraft/skills/forge/references/verification-and-handoff.md#forge-report": (
        "## Forge report",
        "### Task",
        "### Plan and plan review",
        "### Workspace",
        "### Changed (IDs)",
        "### Verification evidence",
        "### Finding resolutions",
        "### Outward mutations",
        "### Open questions",
        "### Review target",
    ),
    "plugins/valcraft/skills/review/SKILL.md#reports": (
        "## Review report",
        "### Mode and change class",
        "### Verdict",
        "### Findings",
        "### Reproductions",
        "### Checks performed",
        "### Not examined",
    ),
    "plugins/valcraft/skills/review/references/evidence-mode.md#evidence-sufficiency-report": (
        "## Evidence-sufficiency report",
        "### Target and sources",
        "### Criterion verdicts",
        "### Overall verdict",
        "### Not independently verified",
    ),
    "plugins/valcraft/skills/land/SKILL.md#report": (
        "## Land report",
        "### Target",
        "### Authoritative state",
        "### Review or evidence coverage",
        "### Applicable checks",
        "### Prepared operations",
        "### Authority and capability",
        "### Completed operations",
        "### Remaining operations",
        "### Handoffs",
    ),
    "plugins/valcraft/skills/spec/references/delivery.md#spec-report": (
        "## Spec report",
        "### Source",
        "### Artifact",
        "### Readiness",
        "### Workspace",
        "### Projection",
        "### Outward mutations",
        "### Finding resolutions",
        "### Review target",
        "### Land target",
        "### Open questions",
    ),
    "plugins/valcraft/skills/temper/SKILL.md#report": (
        "## Temper report",
        "### Corpus and mode",
        "### Retrospective artifact",
        "### Evidence coverage",
        "### Proposal summary",
        "### Operator selection",
        "### Review target",
        "### Blockers",
    ),
}

MESSAGE_REGISTRY = {
    "Project frame": (
        "Cast",
        "plugins/valcraft/skills/cast/SKILL.md#report",
    ),
    "Feature or quick contract": (
        "Spec",
        "plugins/valcraft/skills/spec/references/delivery.md#spec-report",
    ),
    "Task plan": (
        "Draft",
        "plugins/valcraft/skills/draft/references/plan-contract.md#report",
    ),
    "Plan verdict": (
        "Review",
        "plugins/valcraft/skills/review/SKILL.md#reports",
    ),
    "Task implementation and PR": (
        "Forge",
        "plugins/valcraft/skills/forge/references/verification-and-handoff.md#forge-report",
    ),
    "Code verdict": (
        "Review",
        "plugins/valcraft/skills/review/SKILL.md#reports",
    ),
    "Finalization or evidence record": (
        "Land",
        "plugins/valcraft/skills/land/SKILL.md#report",
    ),
    "Evidence-sufficiency verdict": (
        "Review",
        "plugins/valcraft/skills/review/references/evidence-mode.md#evidence-sufficiency-report",
    ),
    "Retrospective report": (
        "Temper",
        "plugins/valcraft/skills/temper/SKILL.md#report",
    ),
    "Retrospective verdict": (
        "Review",
        "plugins/valcraft/skills/review/SKILL.md#reports",
    ),
}


def section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return ""
    end = text.find("\n## ", start + len(marker))
    return text[start:] if end < 0 else text[start:end]


def table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and not all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            rows.append(cells)
    return rows


def github_anchor(title: str) -> str:
    title = re.sub(r"[`*_]", "", title.lower())
    title = re.sub(r"[^a-z0-9\- ]", "", title)
    return re.sub(r" +", "-", title.strip())


def heading_index(text: str, anchor: str) -> int | None:
    for match in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", text, re.MULTILINE):
        if github_anchor(match.group(2)) == anchor:
            return match.start()
    return None


def report_headings(text: str, start: int) -> tuple[str, ...]:
    fence = re.search(r"^```markdown\s*$", text[start:], re.MULTILINE)
    if not fence:
        return ()
    block_start = start + fence.end()
    block_end = text.find("\n```", block_start)
    if block_end < 0:
        return ()
    return tuple(
        match.group(0).strip()
        for match in re.finditer(r"^#{2,3}\s+.+$", text[block_start:block_end], re.MULTILINE)
    )


def declared_codes(text: str) -> set[str]:
    codes = set(
        re.findall(r"Status:\s*(?:blocked|question):\s*([a-z][a-z0-9_]*)", text)
    )
    in_code_list = False
    for line in text.splitlines():
        if re.match(r"^##\s+Routing codes\s*$", line, re.IGNORECASE):
            in_code_list = True
            continue
        if re.search(r"\bUse (?:only )?these .*codes:\s*$", line, re.IGNORECASE):
            in_code_list = True
            continue
        if in_code_list and line.startswith("## "):
            in_code_list = False
        if not in_code_list or not line.startswith("- "):
            continue
        codes.update(
            token
            for token in re.findall(r"`([a-z][a-z0-9_]*)`", line)
            if token not in BACKEND_RETURNS
        )
    return codes


def parse_message_registry(
    root: Path, text: str, errors: list[str]
) -> dict[str, set[str]]:
    registry_path = root / CONTRACTS
    rows = table_rows(section(text, "Message registry"))
    producer_codes: dict[str, set[str]] = {}
    observed_messages: dict[str, tuple[str, str]] = {}
    for row in rows[1:]:
        if len(row) != 6:
            errors.append(f"message registry row has {len(row)} columns: {' | '.join(row)}")
            continue
        message = row[0]
        producer = row[1]
        if message in observed_messages:
            errors.append(f"duplicate message registry entry: {message}")
        link = re.search(r"\[[^]]+\]\(([^)#]+)(?:#([^)]*))?\)", row[3])
        if not link:
            errors.append(f"{producer}: authoritative contract is not a Markdown link")
            continue
        relative, anchor = link.group(1), link.group(2)
        contract_path = (registry_path.parent / relative).resolve()
        try:
            contract_relative = contract_path.relative_to(root.resolve()).as_posix()
        except ValueError:
            errors.append(f"{producer}: contract link escapes repository root: {relative}")
            continue
        try:
            contract_text = contract_path.read_text()
        except (FileNotFoundError, IsADirectoryError):
            errors.append(f"{producer}: contract link does not resolve: {relative}")
            continue
        anchor_start = heading_index(contract_text, anchor) if anchor else None
        if anchor_start is None:
            errors.append(
                f"{producer}: contract anchor does not resolve: {relative}#{anchor or ''}"
            )
            continue
        key = f"{contract_relative}#{anchor}"
        observed_messages[message] = (producer, key)
        expected = REPORT_HEADINGS.get(key)
        if expected is None:
            errors.append(f"{producer}: report heading fingerprint is missing: {key}")
        else:
            observed = report_headings(contract_text, anchor_start)
            if observed != expected:
                errors.append(
                    f"{producer}: report heading order drift in {key}; "
                    f"expected {expected}, observed {observed}"
                )
        producer_codes.setdefault(producer, set()).update(declared_codes(contract_text))

    if observed_messages != MESSAGE_REGISTRY:
        missing = sorted(set(MESSAGE_REGISTRY) - set(observed_messages))
        unexpected = sorted(set(observed_messages) - set(MESSAGE_REGISTRY))
        changed = sorted(
            message
            for message in set(observed_messages) & set(MESSAGE_REGISTRY)
            if observed_messages[message] != MESSAGE_REGISTRY[message]
        )
        errors.append(
            "message registry entries differ from the exact contract; "
            f"missing={missing}, unexpected={unexpected}, changed={changed}"
        )
    return producer_codes


def parse_routing_registry(text: str, errors: list[str]) -> dict[str, dict[str, str]]:
    routing = section(text, "Declared outcome routing")
    producers: dict[str, dict[str, str]] = {}
    producer = ""
    for line in routing.splitlines():
        match = re.match(r"^###\s+(.+?)\s*$", line)
        if match:
            producer = match.group(1)
            producers.setdefault(producer, {})
            continue
        if not producer or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 2 or cells[0] == "Outcome" or re.fullmatch(r":?-+:?", cells[0]):
            continue
        codes = re.findall(r"`([a-z][a-z0-9_]*)`", cells[0])
        transition = cells[1].strip("` ")
        if codes and not transition:
            errors.append(
                f"{producer}: routing codes have no transition: {', '.join(codes)}"
            )
            continue
        for code in codes:
            prior = producers[producer].get(code)
            if prior and prior != transition:
                errors.append(
                    f"{producer}: routing code {code} maps to both {prior} and {transition}"
                )
            producers[producer][code] = transition
    return producers


def check_routing_codes(
    producer_codes: dict[str, set[str]],
    registry: dict[str, dict[str, str]],
    errors: list[str],
) -> None:
    for producer in sorted(set(producer_codes) | set(registry)):
        produced = producer_codes.get(producer, set())
        routed = set(registry.get(producer, {}))
        missing_registry = produced - routed
        missing_producer = routed - produced
        if missing_registry:
            errors.append(
                f"{producer}: producer codes absent from registry: "
                f"{', '.join(sorted(missing_registry))}"
            )
        if missing_producer:
            errors.append(
                f"{producer}: registry codes absent from producer: "
                f"{', '.join(sorted(missing_producer))}"
            )


def check_backend_returns(text: str, errors: list[str]) -> None:
    rows = table_rows(section(text, "Backend returns"))
    observed: dict[str, tuple[str, str]] = {}
    for row in rows[1:]:
        if len(row) != 3:
            errors.append(f"backend return row has {len(row)} columns: {' | '.join(row)}")
            continue
        codes = re.findall(r"`([a-z][a-z0-9_]*)`", row[0])
        if len(codes) != 1:
            errors.append(f"backend return row has no unique code: {' | '.join(row)}")
            continue
        code = codes[0]
        record = (row[1], row[2].strip("` "))
        if code in observed:
            errors.append(f"duplicate backend return: {code}")
            continue
        observed[code] = record

    missing = sorted(set(BACKEND_RETURNS) - set(observed))
    unexpected = sorted(set(observed) - set(BACKEND_RETURNS))
    if missing or unexpected:
        errors.append(
            "backend returns differ from the exact contract; "
            f"missing={missing}, unexpected={unexpected}"
        )
    for code in sorted(set(BACKEND_RETURNS) & set(observed)):
        if observed[code] != BACKEND_RETURNS[code]:
            errors.append(
                f"backend return {code} differs from the exact contract; "
                f"expected={BACKEND_RETURNS[code]}, observed={observed[code]}"
            )


def check_transport_deviations(root: Path, errors: list[str]) -> None:
    backend_text = (root / BACKENDS).read_text()
    rows = table_rows(section(backend_text, "Active transport deviations"))
    eval_data = json.loads((root / FOREMAN_EVALS).read_text())
    evals = {entry["id"]: entry for entry in eval_data["evals"]}
    registry_keys: dict[str, int] = {}
    registry_evals: dict[int, str] = {}
    for row in rows[1:]:
        if len(row) != 5:
            errors.append(
                f"active transport deviation row has {len(row)} columns: {' | '.join(row)}"
            )
            continue
        keys = re.findall(r"`(transport:[a-z0-9-]+)`", row[3])
        if len(keys) != 1:
            errors.append(
                f"active transport deviation has no unique coverage key: {row[0]} — {row[1]}"
            )
            continue
        key = keys[0]
        if key in registry_keys:
            errors.append(f"duplicate active transport coverage key: {key}")
            continue
        reference = re.fullmatch(r"Foreman eval (\d+)", row[4])
        if not reference:
            errors.append(
                f"active transport deviation has no named eval: {row[0]} — {row[1]}"
            )
            continue
        eval_id = int(reference.group(1))
        if eval_id not in evals:
            errors.append(
                f"active transport deviation names missing eval {eval_id}: "
                f"{row[0]} — {row[1]}"
            )
            continue
        if eval_id in registry_evals:
            errors.append(
                f"active transport deviations reuse eval {eval_id}: "
                f"{registry_evals[eval_id]}, {key}"
            )
            continue
        registry_keys[key] = eval_id
        registry_evals[eval_id] = key
        if evals[eval_id].get("coordination_coverage") != key:
            errors.append(
                f"Foreman eval {eval_id} does not reciprocally name coverage key {key}"
            )

    eval_coverage: dict[str, int] = {}
    for eval_id, entry in evals.items():
        key = entry.get("coordination_coverage")
        if not key:
            continue
        if not isinstance(key, str) or not key.startswith("transport:"):
            errors.append(f"Foreman eval {eval_id} has invalid coordination coverage")
            continue
        if key in eval_coverage:
            errors.append(
                f"transport coverage key {key} is named by evals "
                f"{eval_coverage[key]} and {eval_id}"
            )
            continue
        eval_coverage[key] = eval_id
        if key not in registry_keys:
            errors.append(
                f"Foreman eval {eval_id} coverage has no active deviation: {key}"
            )


def check_backend_conformance(root: Path, errors: list[str]) -> None:
    backend_text = (root / BACKENDS).read_text()
    rows = table_rows(section(backend_text, "Backend conformance"))
    eval_data = json.loads((root / FOREMAN_EVALS).read_text())
    evals = {entry["id"]: entry for entry in eval_data["evals"]}
    observed: dict[str, Path] = {}
    conformance_evals: dict[int, str] = {}

    for row in rows[1:]:
        if len(row) != 3:
            errors.append(
                f"backend conformance row has {len(row)} columns: {' | '.join(row)}"
            )
            continue
        names = re.findall(r"`([a-z][a-z0-9_-]*)`", row[0])
        links = re.findall(r"\[[^]]+\]\(([^)]+)\)", row[1])
        reference = re.fullmatch(r"Foreman eval (\d+)", row[2])
        if len(names) != 1 or len(links) != 1 or reference is None:
            errors.append(f"invalid backend conformance row: {' | '.join(row)}")
            continue
        name = names[0]
        relative = Path(links[0])
        path = BACKEND_DIRECTORY / relative
        if name in observed:
            errors.append(f"duplicate backend conformance entry: {name}")
            continue
        observed[name] = path
        if not (root / path).is_file():
            errors.append(f"backend conformance reference does not resolve: {path}")
            continue
        if name != path.stem:
            errors.append(
                f"backend conformance name differs from reference stem: {name}, {path}"
            )
        concrete_text = (root / path).read_text()
        if f"# Backend: `{name}`" not in concrete_text:
            errors.append(f"backend heading does not name registered backend: {path}")
        land_section = section(concrete_text, "Land execution")
        if not land_section:
            errors.append(f"backend lacks Land execution contract: {path}")
        else:
            land_rows = table_rows(land_section)
            mappings = {
                mapping[0]: mapping[1]
                for mapping in land_rows[1:]
                if len(mapping) == 2
            }
            if set(mappings) != LAND_EXECUTION_FIELDS:
                errors.append(
                    f"backend Land execution fields differ: {path}; "
                    f"expected={sorted(LAND_EXECUTION_FIELDS)}, "
                    f"observed={sorted(mappings)}"
                )
            if mappings.get("Execution capability") != "`shared backend permission`":
                errors.append(f"backend execution capability is invalid: {path}")
            permission_signal = mappings.get("Permission signal", "").strip().lower()
            if permission_signal in {"", "none", "n/a"}:
                errors.append(f"backend permission signal is incomplete: {path}")
            if mappings.get("Permission return") != "`permission_blocked`":
                errors.append(f"backend permission mapping is incomplete: {path}")
            if mappings.get("Producer failure") != "`Land report`":
                errors.append(f"backend producer-failure mapping is incomplete: {path}")
        eval_id = int(reference.group(1))
        if eval_id not in evals:
            errors.append(f"backend conformance names missing eval {eval_id}: {name}")
            continue
        if eval_id in conformance_evals:
            errors.append(
                f"backend conformance reuses Foreman eval {eval_id}: "
                f"{conformance_evals[eval_id]}, {name}"
            )
            continue
        conformance_evals[eval_id] = name
        eval_path = str(path.relative_to(Path("plugins/valcraft/skills/foreman")))
        if eval_path not in evals[eval_id].get("files", []):
            errors.append(
                f"Foreman eval {eval_id} does not load backend conformance reference: "
                f"{eval_path}"
            )
        conformance = evals[eval_id].get("backend_conformance", [])
        if conformance != [name]:
            errors.append(
                f"Foreman eval {eval_id} does not reciprocally name backend: {name}"
            )

    concrete = {
        path.name
        for path in (root / BACKEND_DIRECTORY).glob("*.md")
        if path.name != "README.md"
    }
    registered = {path.name for path in observed.values()}
    if concrete != registered:
        errors.append(
            "backend conformance registry differs from concrete backends; "
            f"missing={sorted(concrete - registered)}, "
            f"unexpected={sorted(registered - concrete)}"
        )

    eval_backends = {
        name
        for entry in evals.values()
        for name in entry.get("backend_conformance", [])
    }
    unexpected_eval_backends = sorted(eval_backends - set(observed))
    if unexpected_eval_backends:
        errors.append(
            "Foreman eval backend conformance has no registry entry: "
            f"{unexpected_eval_backends}"
        )


def check(root: Path) -> list[str]:
    errors: list[str] = []
    contracts_text = (root / CONTRACTS).read_text()
    producer_codes = parse_message_registry(root, contracts_text, errors)
    routing = parse_routing_registry(contracts_text, errors)
    check_routing_codes(producer_codes, routing, errors)
    check_backend_returns(contracts_text, errors)
    check_backend_conformance(root, errors)
    check_transport_deviations(root, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        print("usage: check-coordination-contracts.py [repository-root]", file=sys.stderr)
        return 2
    root = Path(argv[0]).resolve() if argv else DEFAULT_ROOT
    try:
        errors = check(root)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"coordination contract check could not run: {error}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"coordination contract error: {error}", file=sys.stderr)
        return 1
    print(
        "static coordination contracts are consistent; "
        "this check does not prove runtime behavior"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
