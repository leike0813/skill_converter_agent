## Why

`skill-converter-agent` 当前实现基于“自动执行优先”的历史假设，尚未完整吸收 Skill-Runner 近期的双模式（`auto` / `interactive`）与契约更新。  
现状存在三类问题：

1. 转换流程中缺少对 `auto` 与 `interactive` 的独立适配性评估，难以稳定决定目标 `execution_modes`。
2. 内嵌校验器与上游 `contracts + validator + engine policy` 存在漂移，可能出现“本地校验通过、上游安装失败”。
3. skill 内置参考文档与上游主干存在差异，影响后续转换判断的一致性。

## What Changes

- 新增一次双模式升级：
  - 转换流程改为“独立评估 auto / interactive 适配性 -> 转换决策 -> 契约生成 -> 最终校验”。
  - 仅 interactive 可行时，分类映射为 `convertible_with_constraints`。
  - `execution_modes` 按评估结果生成：双可行写 `["auto","interactive"]`，单可行写单模式。
- 以 Skill-Runner 当前主干为单一真源，对齐：
  - `runner`/schema 合同约束
  - 嵌入式 validator 行为
  - engine policy 语义
- 全量同步 skill 包内置参考文档到上游最新版本：
  - `autoskill_package_guide.md`
  - `file_protocol.md`
  - `skill-runner_api_reference.md`

## Locked Decisions

- 对齐范围：以上游 `contracts + validator + engine policy` 为准。
- 评估机制：独立输出 `auto` 与 `interactive` 适配结论和依据。
- 分类映射：仅 interactive 可行时，`classification=convertible_with_constraints`。
- `execution_modes` 生成：双可行写 `["auto","interactive"]`；单可行写单模式。
- 不强制 `__SKILL_DONE__`。
- 目录模式也产出 zip。
- 转换器输出字段保持现状（`status/classification/路径字段`）。

## Impact

- 影响 specs：
  - `skill-converter-agent`
  - `skill-converter-prompt-first`
  - `skill-converter-dual-mode`
  - `skill-converter-directory-first`
- 影响实现：
  - `skill-converter-agent/SKILL.md`
  - `skill-converter-agent/assets/runner.json`
  - `skill-converter-agent/scripts/embedded_skill_package_validator.py`
  - `skill-converter-agent/references/*`
