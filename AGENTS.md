# 项目级 AGENTS（skill-converter-agent / `$skill-converter-agent`）

本文件仅包含 **skill-converter-agent** Skill 项目特有约定，用于补充上级/全局 `AGENTS.md`；全局通用规则不在此重复。

---

## 目标

- 本项目旨在开发名为 `skill-converter-agent` 的 Agent Skill
- `skill-converter-agent` 是一个能将满足 Open Agent Skills 规范的 Skill 包转换为可以由 Skill-Runner 项目（见 references/Skill-Runner 目录）执行的 AutoSkill 包的 Agent Skill
- 本项目目标 Skill 的发布目录是项目目录中的 `skill-converter-agent` 目录

## 非目标

- `skill-converter-agent` 不负责优化、完善输入 Skill 包的业务逻辑，对输入 Skill 包的指令文件（SKILL.md）仅做最小必要的修改
- `skill-converter-agent` 不对输入 Skill 包的可执行性负责

## 约束

- 本项目是 Agent Skill 开发项目，所以你需要转变逻辑，围绕着 SKILL.md 进行文本语义驱动的开发，而不是倾向于编写代码
- 目标 Skill 执行过程中，如果有些环节适合用代码来实现（例如确定且重复的任务），可以编写代码，放在 Skill 发布目录中的 `scripts` 文件夹下
- Skill 发布目录的组织结构需要遵守 Open Agent Skills 规范
- `skill-converter-agent` 自身也是一个 AutoSkill 包，需要包含 AutoSkill 所必需的执行资产

## 参考

- Skill-Runner 项目： `references/Skill-Runner/`
- AutoSkill 包规范： `references/Skill-Runner/docs/file_protocol.md`
- AutoSkill 包构建指南： `references/Skill-Runner/docs/developer/autoskill_package_guide.md`
- AutoSkill 包必要工件 schema: `references/Skill-Runner/server/contracts/skill/*`