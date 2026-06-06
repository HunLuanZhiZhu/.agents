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

## [LRN-20260516-006] correction

**Priority**: high
**Status**: resolved
**Area**: communication

### 内容

执行命令后没有向用户汇报结果，缺少沟通和汇报意识。

**错误行为**：执行 `lark-cli docs +create` 创建飞书文档后，没有向用户汇报：
- 是否创建成功
- 创建在哪里（URL）
- 文档标题是什么

**正确做法**：P8 的闭环意识——**对结果负责**。执行操作后必须：
1. 检查命令输出（成功/失败）
2. 向用户汇报关键信息（状态、结果、位置）
3. 如果失败，说明错误原因和下一步操作
4. 如果成功，提供可访问的链接或位置

### 建议修复

在 AGENTS.md 中增加规则：执行任何操作后，必须向用户汇报结果。

### 元数据
- Source: correction
- Pattern-Key: report-after-action
- See Also: LRN-20260516-005

---

## [LRN-20260516-007] best_practice

**Priority**: high
**Status**: pending
**Area**: self-evolution

### 内容

完成任务后没有主动进行复盘沉淀，缺乏自我进化意识。

**错误行为**：成功创建飞书文档后，没有：
1. 回顾目标（用户要什么）
2. 评估结果（实际交付了什么）
3. 分析原因（弯路的根因）
4. 沉淀规律（可复用的经验）

**正确做法**：P9 的复盘四步法——每次主要任务完成后执行：
1. **回顾目标**：用户要的是什么？验收标准是什么？
2. **评估结果**：实际交付了什么？有差距吗？有超预期吗？
3. **分析原因**：弯路的根因——信息不足、方案选错、还是执行偏差？
4. **沉淀规律**：可复用的经验是什么？好的复盘产出 SOP，不是"下次注意"

**本次复盘**：
- 目标：创建飞书云文档
- 结果：成功创建，URL: https://ncnohlox1lcz.feishu.cn/docx/AZ2NdX6wWo0Zo4x8It2cqgDknPc
- 弯路：lark-cli 未配置 → 需要先执行 `lark-cli config init --new`
- 规律：使用飞书 skill 前，先检查配置状态（`lark-cli config list`）

### 建议修复

在 AGENTS.md 中增加规则：主要任务完成后，必须执行复盘四步法，并将经验写入 LEARNINGS.md。

### 元数据
- Source: best_practice
- Pattern-Key: retrospective-after-task
- See Also: LRN-20260516-003, LRN-20260516-006

---

## [LRN-20260516-008] best_practice

**Priority**: medium
**Status**: pending
**Area**: docs

### 内容

安装新分类的 skill 时，如果现有分类无法覆盖，应新增分类并同步更新 AGENTS.md 和 README.md 的分类说明表。

**操作流程**：
1. 搜索并筛选 skill
2. 安装 skill
3. 读取每个 SKILL.md 的 frontmatter（版本、描述、来源）
4. 读取 `.skill-lock.json` 验证来源信息
5. 判断是否需要新增分类
6. 更新 README.md 的 skill 目录（添加条目 + 更新计数 + 更新时间戳）
7. 更新 README.md 的分类说明表
8. 更新 AGENTS.md 的分类说明表

**来源判断规则**：
- `apollographql/skills` → Apollo GraphQL 是知名公司 → 🏢 官方
- `github/awesome-copilot` → GitHub 是知名公司 → 🏢 官方
- `wshobson/agents`、`affaan-m/everything-claude-code`、`zhanghandong/rust-skills` → 个人/社区 → 🌐 社区

### 元数据
- Source: best_practice
- Pattern-Key: new-category-sync
- See Also: LRN-20260516-001, LRN-20260516-005

---

## [LRN-20260516-009] best_practice

**Priority**: medium
**Status**: pending
**Area**: search

### 内容

搜索 skill 时，同一领域的 skill 可能分散在不同关键词下，需要多角度搜索才能全面覆盖。

**操作流程**：
1. 用核心关键词搜索（如 `pytorch`）
2. 用领域关键词搜索（如 `deep learning`）
3. 用具体任务关键词搜索（如 `neural network training`）
4. 合并去重后，根据安装量和来源质量筛选
5. 区分"用户用"和"项目内部用"的 skill（如 PyTorch 官方的 docstring/pr-review 是项目内部用的，不是写深度学习代码用的）

### 元数据
- Source: best_practice
- Pattern-Key: multi-angle-search
- See Also: LRN-20260516-008

---

## [LRN-20260516-010] best_practice

**Priority**: low
**Status**: pending
**Area**: install

### 内容

用户提供了明确的 GitHub 仓库 URL 时，可以直接使用 `npx skills add <url> --skill <skill-name>` 安装，无需先搜索。

**安装命令格式**：
```bash
npx skills add https://github.com/owner/repo --skill skill-name -g -y
```

**来源判断**：
- 个人 GitHub 账号（如 `op7418`）→ 👤 个人
- 知名公司官方账号（如 `anthropics`、`github`）→ 🏢 官方
- 社区组织账号 → 🌐 社区

### 元数据
- Source: best_practice
- Pattern-Key: direct-url-install
- See Also: LRN-20260516-009

---

## [LRN-20260516-011] best_practice

**Priority**: medium
**Status**: pending
**Area**: install

### 内容

Anthropic 和 OpenAI 都在 `anthropics/skills` 和 `openai/skills` 仓库中维护了多个官方 skill。安装方式为 `npx skills add <owner/repo@skill-name> -g -y`。

**知名官方仓库**：
| 仓库 | 包含 skill | 安装量 |
|------|-----------|--------|
| `anthropics/skills` | docx, pptx, xlsx, codex 等 18 个 | 100K+ |
| `openai/skills` | pdf, codex 等 43 个 | 6K+ |

**安全评估注意**：
- Anthropic 官方 skill 安全评估通常为 Safe/Low Risk
- OpenAI 的 pdf skill 评估为 High Risk (Gen) / Med Risk (Snyk)，安装前应告知用户

**分类决策**：当同类 skill 数量 ≥ 4 且有独立业务价值（如 Office 文档处理），应新增独立分类。

### 元数据
- Source: best_practice
- Pattern-Key: official-skills-repos
- See Also: LRN-20260516-008, LRN-20260516-010

---

## [LRN-20260516-012] best_practice

**Priority**: high
**Status**: pending
**Area**: install

### 内容

**全量校验发现大量遗漏 skill**：实际 skills/ 目录有 79 个 skill，但 README 只记录了 54 个，遗漏 25 个。

**遗漏原因分析**：
1. 批量安装时（如 `npx skills add owner/repo@skill -g -y`），如果仓库包含多个 skill，可能只记录了主 skill
2. 依赖自动安装的子 skill 未被记录
3. 早期安装时未执行完整的闭环检查

**遗漏 skill 清单**：
- 学术科研：nature-reader, nature-response, nature-reviewer, nature-writing（4 个）
- 组会 PPT：zuhui-paper-ppt, zuhui-ppt-master, zuhui-ppt-qa, zuhui-ppt-source-audit, zuhui-ppt-story-spine, zuhui-ppt-swiss-design, zuhui-ppt-triformat-export, zuhui-ppt-visual-score（8 个）
- 浏览器与前端：web-search（1 个）
- 深度学习：pytorch-patterns（已在 README 中）

**新增分类决策**：zuhui-ppt-* 系列共 8 个 skill，功能聚焦（学术组会 PPT 制作），且有独立业务价值，新增「📊 组会 PPT」分类。

**教训**：
- 每次安装 skill 后必须立即执行闭环检查
- 定期全量校验（建议每月一次）
- 使用 `Get-ChildItem -Path skills -Directory` 快速扫描目录

### 元数据
- Source: best_practice
- Pattern-Key: full-audit-missing-skills
- See Also: LRN-20260516-008
---
