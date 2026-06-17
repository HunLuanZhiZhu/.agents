# Zuhui PPT Story Spine（中文说明）

## 目标

把论文变成“有 claim、有证据、有边界”的中文组会 PPT 大纲。遵循 `nature-paper2ppt`：用科学论证做主线，而不是照搬论文目录。学习 `paper-ppt-agent`：先做内容稿，再做设计稿。

## AI / 系统 / 方法论文默认结构

1. 瓶颈或失败模式；
2. 系统设计假设；
3. 架构和工作流；
4. 关键证据和部署足迹；
5. 保障、验证、审计；
6. 局限和未解问题；
7. 组会讨论。

## Claim + Proof Object 规则

每个非过渡页必须有：

- claim：结论式中文标题或核心洞见；
- proof object：干净图裁剪、原生重建表格、流程图、指标或论文支持的总结；
- interpretation：观众应该相信什么；
- caveat：这个证据不能证明什么。

如果没有证据对象，除非是章节页、讨论页或局限页，否则合并或删除。

## 证据对象规则

- 截图只用于无法忠实重绘的完整图或完整流程图；
- 不要把正文段落、图注、表注或长文字块截图进 PPT；
- 表格只要数值可读，就必须用原生表格重建；
- 论文工作区已有 `images/` 文件夹时，优先把其中干净裁剪作为截图边界参考；
- 翻译 PDF 中如果图内标签已翻译，只裁剪图本体，不带周围正文和 caption；
- caption 有用时，改写成 PPT 外部的短中文解释句，不作为截图内容；
- **注意**：简单柱状图、单线图、单面板示意图等低信息量图不适合独占一页（Hero Figure Result），应与其他文字或图组合（见 `zuhui-ppt-swiss-design` 图信息量评估规则）；
- 架构图/工作流图如果原图分辨率低或有英文标注，考虑用内联 SVG 重绘，标记 `[SVG: 描述]`（见 `zuhui-ppt-swiss-design` SVG 逻辑图绘制指南）。

## 密集内容抽取

不要只看摘要和主图，要检查：

- 表格；
- 附录图；
- 工作流内部结构；
- 部署规模；
- 对比表；
- 失败模式；
- 局限段落；
- 实现细节；
- 产物名称和工作流输出。

可以学习 paper-ppt-agent 的密集中文稿，但数字和结论必须回到论文核验。

## 每页计划格式

写出 `{OUTPUT_DIR}/slide_plan_v{VERSION}.md`，每页用 `---` 分隔。格式如下：

```markdown
<!-- page_type: cover|chapter|content|ending -->
<!-- page_number: N -->

## [结论式中文标题]

**Narrative role**: Hook|Tension|Core Insight|Mechanism|Evidence|Implications|Coda
**Detail density**: light|normal|rich
**Archetype**: Hero Figure Result|Workflow/Method|Comparison/Table|Text-Led Synthesis|Cover|Chapter Transition
**Section**: [章节名]

**Core claim**: [一句话核心论点]

**Slide points**:
- [要点 1，含具体数据]
- [要点 2]
- [要点 3]

**Visual plan**:
- [CHART: 柱状图对比各方法表现]
- [DIAGRAM: 方法流程图]
- [SVG: 架构关系图]
- [TABLE: 结果对比表]
- [[FIG:fig_007_p9_page]] — 简短说明该图证明什么

**Proof object**: `assets/fig_xxx.png` — [简短说明]
**Caption**: [图注]
**Caveat**: [证据不能证明什么]
**Recommended layout**: S22|S17|S21|S09|S01|S03

**Speaker note**: [演讲要点，包括过渡语、时间提示、强调重点]
```

- `<!-- page_type: ... -->` 标记每页类型。
- `[CHART: ...]`、`[DIAGRAM: ...]`、`[SVG: ...]`、`[TABLE: ...]` 是给下游的视觉标记，不字面渲染。
- `[[FIG:fig_id]]` 必须引用 source audit 产出的真实图片 ID，独占一行并附简短说明。
- Speaker note 应包含过渡语、时间提示和强调重点。
- Detail density: light=1-2 条，normal=2-4 条，rich=4-6 条。
- slide_plan 完成后**必须先审阅确认**再进入 Phase 3 (Swiss Visual Design)。

## PPT 正文 vs 讲稿备注

- PPT 正文给听众看：论文主张、证据对象、解释和边界。
- 讲稿备注给汇报者看：为什么值得讲、这版怎么读、术语提醒、转场提示。
- 如果某页标题像“为什么这篇值得讲”“这版怎么读”或解释制作方案，应移动到讲稿。
- 可见 PPT 标题应该是论文内容相关的结论，不是内部工作流标签。

## 页数建议

详细组会 25–35 页是可以接受的。图表多时，多拆页比缩小图片更好。

## 禁止叙事

- 单独术语页；
- “如何解决英文图”的页面；
- “为什么这篇值得讲”“这版怎么读”这类自我规划页；
- 没有论文具体 claim 的背景页；
- 每栏只有一句空话的三栏页；
- “Method / Results”这种不带结论的标题；
- 没有证据支持的夸大结论。
