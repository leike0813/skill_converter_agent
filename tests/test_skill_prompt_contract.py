from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "skill-converter-agent" / "SKILL.md"


def test_skill_md_contains_dual_mode_assessment_sections() -> None:
    content = SKILL_MD.read_text(encoding="utf-8")
    assert "auto_suitability" in content
    assert "interactive_suitability" in content
    assert "双模式独立适配性评估" in content


def test_skill_md_contains_classification_mapping_for_interactive_only() -> None:
    content = SKILL_MD.read_text(encoding="utf-8")
    assert "auto=unsuitable 且 interactive=suitable -> `convertible_with_constraints`" in content


def test_skill_md_requires_zip_output_for_directory_and_zip_modes() -> None:
    content = SKILL_MD.read_text(encoding="utf-8")
    assert "目录/zip 模式都执行" in content
    assert "converted_skill.zip" in content
