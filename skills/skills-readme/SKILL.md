---
name: skills-readme
description: Read and search the local skill catalog from README.md to help users find installed skills by name, category, or keyword. Invoke when user asks "what skills do I have", "find skill", "list skills", "search skill", or any query about discovering available skills in the workspace.
---

# Skills README Reader

This skill reads the local skill catalog from `README.md` (relative to the skill directory) to help users discover installed skills.

## When to Use

Invoke this skill when the user:
- Asks "what skills do I have" or "list my skills"
- Asks to "find a skill" or "search for skill"
- Wants to know if a specific skill is installed
- Needs to browse skills by category

## How It Works

1. The skill reads `../../README.md` (relative path from `skills/skills-readme/`)
2. Parses the skill catalog tables
3. Returns matching skills with name, version, category, and description

## Search Behavior

- **Exact match**: If user provides a skill name, search for exact or partial match
- **Category filter**: If user mentions a category (e.g., "framework figure skills"), filter by category
- **Keyword search**: If user provides keywords, search across name and description
- **List all**: If user asks for all skills, return the full catalog summary

## Output Format

Return results as a markdown table:

| Skill | Category | Version | Description |
|-------|----------|---------|-------------|
| ... | ... | ... | ... |

## Example

User: "Do I have any Visio-related skills?"

Response: Search README.md for "visio" keyword, then return:

| Skill | Category | Version | Description |
|-------|----------|---------|-------------|
| visiomaster | 🏗️ 框架图绘制 | - | Visio 图形重建：将流程图/架构图/论文模块图重建为可编辑 Visio 图纸(.vsdx) |
