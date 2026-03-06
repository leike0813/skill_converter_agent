from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "references" / "Skill-Runner"))
sys.path.append(str(ROOT / "skill-converter-agent" / "scripts"))

from embedded_skill_package_validator import EmbeddedSkillPackageValidator  # noqa: E402
from server.services.skill.skill_package_validator import SkillPackageValidator  # type: ignore[import-not-found]  # noqa: E402


def _write_skill_package(tmp_path: Path, *, skill_id: str, runner: dict[str, Any], skill_name: str) -> Path:
    skill_dir = tmp_path / skill_id
    assets_dir = skill_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {skill_name}\ndescription: test\n---\n\n# Test Skill\n",
        encoding="utf-8",
    )
    (assets_dir / "runner.json").write_text(
        json.dumps(runner, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    (assets_dir / "input.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "properties": {
                    "source": {"type": "string", "x-input-source": "inline"},
                },
                "required": ["source"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (assets_dir / "parameter.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "properties": {"strict": {"type": "boolean"}},
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (assets_dir / "output.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "properties": {"out": {"type": "string"}},
                "required": ["out"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return skill_dir


def _run_embedded(skill_dir: Path) -> tuple[bool, str]:
    validator = EmbeddedSkillPackageValidator()
    try:
        validator.validate_skill_dir(skill_dir, top_level_dir=skill_dir.name, require_version=True)
    except Exception as exc:  # pragma: no cover - parity assertion target
        return False, str(exc)
    return True, ""


def _run_upstream(skill_dir: Path) -> tuple[bool, str]:
    validator = SkillPackageValidator()
    try:
        validator.validate_skill_dir(skill_dir, top_level_dir=skill_dir.name, require_version=True)
    except Exception as exc:  # pragma: no cover - parity assertion target
        return False, str(exc)
    return True, ""


def _error_category(message: str) -> str:
    if "Invalid runner.json manifest" in message:
        return "runner_manifest"
    if "execution_modes" in message:
        return "execution_modes"
    if "engines/unsupported_engines" in message or "effective engines" in message:
        return "engine_policy"
    if "Invalid input schema" in message:
        return "schema_meta"
    if "Skill identity mismatch" in message:
        return "identity"
    return "other"


def _base_runner(skill_id: str) -> dict[str, Any]:
    return {
        "id": skill_id,
        "version": "1.0.0",
        "execution_modes": ["auto", "interactive"],
        "schemas": {
            "input": "assets/input.schema.json",
            "parameter": "assets/parameter.schema.json",
            "output": "assets/output.schema.json",
        },
    }


@pytest.mark.parametrize(
    "scenario,mutator,expected_ok,expected_category",
    [
        ("valid_dual_mode", lambda skill_dir, runner: None, True, "other"),
        (
            "missing_execution_modes",
            lambda skill_dir, runner: runner.pop("execution_modes", None),
            False,
            "runner_manifest",
        ),
        (
            "invalid_engine_name",
            lambda skill_dir, runner: runner.update({"engines": ["unknown-engine"]}),
            False,
            "runner_manifest",
        ),
        (
            "invalid_input_extension_field",
            lambda skill_dir, runner: (skill_dir / "assets" / "input.schema.json").write_text(
                json.dumps(
                    {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string", "x-input-source": "path"},
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            ),
            False,
            "schema_meta",
        ),
        (
            "identity_mismatch",
            lambda skill_dir, runner: (skill_dir / "SKILL.md").write_text(
                "---\nname: another-name\ndescription: test\n---\n\n# Test Skill\n",
                encoding="utf-8",
            ),
            False,
            "identity",
        ),
    ],
)
def test_embedded_validator_parity(
    tmp_path: Path,
    scenario: str,
    mutator: Any,
    expected_ok: bool,
    expected_category: str,
) -> None:
    _ = scenario
    skill_id = "demo-skill"
    runner = _base_runner(skill_id)
    skill_dir = _write_skill_package(tmp_path, skill_id=skill_id, runner=runner, skill_name=skill_id)

    mutator(skill_dir, runner)
    (skill_dir / "assets" / "runner.json").write_text(
        json.dumps(runner, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    embedded_ok, embedded_error = _run_embedded(skill_dir)
    upstream_ok, upstream_error = _run_upstream(skill_dir)

    assert embedded_ok == upstream_ok == expected_ok
    if not expected_ok:
        assert _error_category(embedded_error) == _error_category(upstream_error) == expected_category
