## 1. OpenSpec Deltas

- [x] 1.1 新增 change 元数据（proposal/design/tasks/.openspec.yaml）
- [x] 1.2 为 `skill-converter-agent` 增加双模式评估与同源契约要求
- [x] 1.3 为 `skill-converter-prompt-first` 增加“独立模式评估先于转换决策”的要求
- [x] 1.4 为 `skill-converter-dual-mode` 增加 execution_modes 生成规则与目录模式 zip 产物约束
- [x] 1.5 为 `skill-converter-directory-first` 增加“目录模式也产出 zip”的要求

## 2. Skill Implementation

- [x] 2.1 重写 `skill-converter-agent/SKILL.md` 为双评估驱动流程
- [x] 2.2 修正 `skill-converter-agent/assets/runner.json` prompt 文案并对齐双模式语义
- [x] 2.3 升级 `embedded_skill_package_validator.py` 到同源行为（execution_modes + engine policy + meta-schema + YAML）
- [x] 2.4 保持转换器输出字段契约不变

## 3. Reference Sync

- [x] 3.1 同步 `references/autoskill_package_guide.md` 到上游最新版
- [x] 3.2 同步 `references/file_protocol.md` 到上游最新版
- [x] 3.3 同步 `references/skill-runner_api_reference.md` 到上游最新版

## 4. Tests and Validation

- [x] 4.1 增加嵌入式 validator 与上游 validator parity 测试样例
- [x] 4.2 覆盖样例：合法双模式、缺 execution_modes、engine 非法、schema 扩展非法、身份不一致
- [x] 4.3 运行 `validate_converted_skill.py` 验证转换器自身通过校验
- [x] 4.4 运行类型检查（mypy）
