## MODIFIED Requirements

### Requirement: zip 模式仅作为包装层
在 Skill-Runner 自动执行场景中，zip 输入 MUST 通过解包/打包包装实现，且转换逻辑与目录模式一致。目录模式成功后同样 MUST 产出可安装 zip 包。

#### Scenario: directory 模式也产出 zip
- **WHEN** 输入为目录并转换成功
- **THEN** 输出中包含转换后目录与 install-ready zip artifact
- **AND** zip 的合同语义与 zip 输入路径下的结果一致
