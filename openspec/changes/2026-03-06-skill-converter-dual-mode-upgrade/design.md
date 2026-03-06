## Context

本升级的设计目标是：在不改变转换器对外输出字段契约的前提下，完成双模式转换决策与上游契约同源对齐。  
实现需保持 prompt-first 主体架构（`SKILL.md` 驱动），脚本仅承担包装与最终校验职责。

## Design

### 1) 双模式评估驱动的转换决策

转换流程按固定阶段执行：

1. 输入解析（目录或 zip）。
2. 独立评估 `auto_suitability`。
3. 独立评估 `interactive_suitability`。
4. 根据双评估结果确定：
   - `classification`
   - 目标 `runner.execution_modes`
   - 是否需要约束化改造（constraints）
5. 生成/更新 `SKILL.md` 与 `assets/*`，再执行最终 validator。

映射规则：

- auto=false 且 interactive=false -> `not_convertible`
- auto=false 且 interactive=true -> `convertible_with_constraints`
- auto=true 且 interactive=false -> `ready_for_auto`
- auto=true 且 interactive=true -> `ready_for_auto`

`execution_modes` 规则：

- auto=true 且 interactive=true -> `["auto","interactive"]`
- auto=true 且 interactive=false -> `["auto"]`
- auto=false 且 interactive=true -> `["interactive"]`

### 2) 嵌入式 validator 同源对齐

嵌入式 validator 与上游语义保持一致（不引入 server 运行时依赖）：

- 使用与上游一致的 runner/schema 校验规则（含 meta-schema 扩展字段）。
- 使用与上游一致的 engine policy：
  - `engines` 可选
  - `unsupported_engines` 可选
  - 两者合法性、去重、冲突与 `effective_engines` 非空约束
- 强制 `execution_modes` 非空，且仅允许 `auto|interactive`。
- frontmatter 解析与上游一致（YAML）。

### 3) 契约与文档同步策略

- 转换器输出字段保持不变，不新增外部结果字段。
- 内置 references 采用“全量覆盖同步”策略，避免规则漂移。
- `runner.json` prompt 文案修正为双模式语义且语法有效。

## Risks and Mitigations

- 风险：双评估结论不稳定。  
  - 对策：在 `SKILL.md` 固定评估依据模板，要求输出可追溯理由。
- 风险：嵌入式 validator 再次漂移。  
  - 对策：增加 parity 测试，按样例对照上游 validator 结论。
- 风险：文档同步后与旧转换提示冲突。  
  - 对策：以 `SKILL.md` 显式流程为准，references 作为规范依据而非执行分支。
