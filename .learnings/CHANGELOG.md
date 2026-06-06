# Changelog

<!-- SCHEMA: {"ts":"ISO-8601","action":"add|promote|extract|resolve","type":"learning|error|feature","id":"entry ID","summary":"≤100字","target":"晋升目标(可选)"} -->

```jsonl
{"ts":"2026-05-16T15:30:00+08:00","action":"add","type":"learning","id":"LRN-20260516-001","summary":"标注来源前必须从 .skill-lock.json 验证 source 字段，不能凭主观判断"}
{"ts":"2026-05-16T15:30:00+08:00","action":"add","type":"learning","id":"LRN-20260516-002","summary":"已有 skill 提供功能时，文档只引用 skill，不重复写命令"}
{"ts":"2026-05-16T15:30:00+08:00","action":"add","type":"learning","id":"LRN-20260516-003","summary":"被用户纠正后必须触发经验记录机制，写入 .learnings/LEARNINGS.md"}
{"ts":"2026-05-16T16:00:00+08:00","action":"add","type":"learning","id":"LRN-20260516-004","summary":"知道重要信息后要主动写入文档，P8 的 owner 意识"}
{"ts":"2026-05-16T16:30:00+08:00","action":"add","type":"learning","id":"LRN-20260516-005","summary":"更新 skill 后必须检查新 skill、版本变化、更新 README，完整闭环"}
{"ts":"2026-05-16T17:00:00+08:00","action":"add","type":"learning","id":"LRN-20260516-006","summary":"执行命令后必须向用户汇报结果（状态、位置、错误原因），闭环意识"}
{"ts":"2026-05-16T17:00:00+08:00","action":"add","type":"learning","id":"LRN-20260516-007","summary":"主要任务完成后必须执行复盘四步法，沉淀规律到 LEARNINGS.md"}
{"ts":"2026-05-16T18:21:00+08:00","action":"add","type":"learning","id":"LRN-20260516-008","summary":"新增分类时须同步更新 AGENTS.md 和 README.md 的分类说明表"}
{"ts":"2026-05-16T18:30:00+08:00","action":"add","type":"learning","id":"LRN-20260516-009","summary":"搜索 skill 需多角度关键词搜索，区分用户用和项目内部用的 skill"}
{"ts":"2026-05-16T18:35:00+08:00","action":"add","type":"learning","id":"LRN-20260516-010","summary":"用户提供 GitHub URL 时可直接安装，无需先搜索"}
{"ts":"2026-05-16T18:45:00+08:00","action":"add","type":"learning","id":"LRN-20260516-011","summary":"Anthropic/OpenAI 官方 skill 仓库信息及文档处理分类新增决策"}
{"ts":"2026-05-16T19:00:00+08:00","action":"audit","type":"learning","id":"LRN-20260516-012","summary":"全量校验发现25个遗漏skill，新增组会PPT分类，教训：定期全量校验"}
```
