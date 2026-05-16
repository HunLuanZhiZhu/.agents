# Learnings

经验、纠正、最佳实践、任务回顾记录。

---

## [LRN-20260516-001] correction

**Priority**: high
**Status**: resolved
**Area**: docs

### 内容

在为 skill 标注来源时，未验证就凭主观判断标注为"非官方"，导致错误。

**错误行为**：看到 lark 系列没有 author 字段，就假设是"大厂员工个人开发"，标注为 `🏢 非官方`。

**正确做法**：来源信息必须从 `.skill-lock.json` 中验证。该文件记录了每个 skill 的 `source` 字段（如 `larksuite/cli`），这才是真实来源。

**验证方法**：
```bash
# 检查 skill 来源
cat .skill-lock.json | grep -A5 "lark-im"
# 输出: "source": "larksuite/cli" → 飞书官方
```

**结论**：`larksuite` 是飞书/Lark 的官方 GitHub 组织，所有 lark 系列都是 `🏢 官方` 出品。

### 建议修复

1. 标注来源前，必须先读取 `.skill-lock.json` 验证 `source` 字段
2. 如果 source 是知名公司的官方 GitHub 组织（如 `larksuite`、`anthropics`、`openai` 等），标注为 `🏢 官方`
3. 如果 SKILL.md 中有明确的 `author` 字段指向大厂，才考虑 `🏢 非官方`
4. 无法确定时标注 `-`

### 元数据
- Source: correction
- Pattern-Key: verify-before-annotate
- See Also: LRN-20260516-002

---

## [LRN-20260516-002] correction

**Priority**: medium
**Status**: resolved
**Area**: docs

### 内容

在 README.md 和 AGENTS.md 中写了冗余的安装命令，但已有 `find-skills` skill 提供完整的安装指引。

**错误行为**：在文档中重复写 `npx skills find`、`npx skills add` 等命令。

**正确做法**：已有 skill 提供功能时，文档只需引用该 skill，不重复写命令。用户可以通过 `find-skills` skill 获取最新、最准确的安装命令。

### 建议修复

1. 文档中涉及安装/删除 skill 时，只引用 `find-skills` skill
2. 具体命令由 skill 介绍页面提供，避免文档与 skill 内容不同步

### 元数据
- Source: correction
- Pattern-Key: avoid-redundancy
- See Also: LRN-20260516-001

---

## [LRN-20260516-003] best_practice

**Priority**: high
**Status**: pending
**Area**: config

### 内容

被用户纠正或批评后，必须触发 `proactive-self-improving-agent` 的经验记录机制，将经验写入 `.learnings/LEARNINGS.md`。

**错误行为**：被批评后只修复了具体问题，没有记录经验，导致同样的错误可能再次发生。

**正确做法**：
1. 被用户纠正时 → 触发 `proactive-self-improving-agent`
2. 写入 LEARNINGS.md（category: correction）
3. 追加 CHANGELOG.md 日志
4. 如果同一问题反复出现 ≥3 次 → 晋升到 AGENTS.md

### 建议修复

在 AGENTS.md 中增加规则：被用户纠正后必须检查是否需要记录经验。

### 元数据
- Source: best_practice
- Pattern-Key: learn-from-correction
- See Also: LRN-20260516-001, LRN-20260516-002

---

## [LRN-20260516-004] correction

**Priority**: medium
**Status**: resolved
**Area**: docs

### 内容

知道某个重要信息（如 `lark-cli update` 更新命令），但没有主动写入文档。

**错误行为**：学习了 `lark-shared` skill，知道飞书 skill 的标准更新程序是 `lark-cli update`，但没有主动写入 README。

**正确做法**：P8 的 owner 意识——**还有什么没想到的？** 看到一棵树，要想到整片林子。获取重要信息后，主动检查是否应该写入相关文档，让后续使用者也能受益。

### 建议修复

1. 学习新知识后，主动思考：这个信息是否应该写入文档？
2. 如果是操作指南类信息，写入 README 的"使用说明"章节
3. 如果是规则类信息，写入 AGENTS.md

### 元数据
- Source: correction
- Pattern-Key: proactively-document
- See Also: LRN-20260516-001, LRN-20260516-002

---

## [LRN-20260516-005] correction

**Priority**: high
**Status**: resolved
**Area**: docs

### 内容

执行更新操作后，没有检查更新结果、没有对比版本变化、没有更新文档。

**错误行为**：执行 `lark-cli update` 后直接收工，没有：
1. 检查是否有新 skill
2. 检查每个 skill 的版本变化
3. 更新 README 的最后更新时间

**正确做法**：更新操作的完整闭环：
1. 执行更新命令
2. 检查 `.skill-lock.json` 的 `updatedAt` 时间戳
3. 对比 README 中列出的 skill 与实际 skill 目录
4. 检查版本号变化（读取 SKILL.md 的 version 字段）
5. 更新 README 的最后更新时间

### 建议修复

在 AGENTS.md 中增加规则：更新 skill 后必须执行完整闭环检查。

### 元数据
- Source: correction
- Pattern-Key: update-verification-loop
- See Also: LRN-20260516-004

---
