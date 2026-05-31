# Zuhui PPT Master（中文说明）

## 用途

用于制作高级感中文组会论文汇报 PPT。默认同时保留三种产物：

1. 可编辑 `.pptx`
2. Guizang 瑞士风横向翻页 `.html`
3. 从 HTML 导出的 `.pdf`
4. 讲稿备注和 QA 报告

它不是替代 `guizang-ppt-skill` 或 `nature-paper2ppt`，而是把它们组合起来：

- 用 `nature-paper2ppt` 做论文理解、图表选择、证据优先的 PPTX 结构；
- 用 `guizang-ppt-skill` 做瑞士风、IKB 蓝、网格、章节页、大图页和 HTML；
- 学习 `paper-ppt-agent` 的“内容稿 / 设计稿 / 生成 / 批评 / 修复”流程，让内容更密、更像论文汇报。

## 子 Skill 调用顺序

主 skill 必须按顺序使用这些子 skill：

1. `zuhui-ppt-source-audit`：检查论文、翻译 PDF、旧版本、参考项目。
2. `zuhui-ppt-story-spine`：建立论文主线和证据地图。
3. `zuhui-ppt-swiss-design`：选择 Guizang Swiss 注册版式和视觉节奏。
4. `zuhui-ppt-triformat-export`：同步生成 PPTX、HTML、PDF。
5. `zuhui-ppt-qa`：做结构、密度、图片、禁用内容和渲染检查。

## 必须做到

- 最终保留 PPTX / HTML / PDF 三种产物。
- HTML 必须继承 Guizang Swiss 风格，优先用 `template-swiss.html`。
- 如果旧版本视觉更好，要把旧版本当作视觉金标准。本工作流优先继承 v1 的 Guizang Swiss `aris-*` 风格：IKB 蓝封面、黑底 statement、细网格、大标题、干净图页。
- PPTX 默认要可编辑，并尽量接近 HTML 的视觉层级。若用户已经否定可编辑 PPTX 的视觉效果、并明确更重视 v1/浏览器视觉保真，可以使用截图型 PPTX，但必须在 QA 报告里说明可编辑性限制。
- 大图页图片要足够大；论文图表是证据，不是装饰。
- 生成脚本、讲稿和 QA 报告要保留，方便后续迭代。
- PPT 页面必须给听众看，不要把给 agent 自己看的阅读地图、制作思路、选题理由放进正文页；这类内容放讲稿或构建备注。
- 可见文字以中文为主。必须保留英文专业词时，写成 `中文解释（English term）`，不能让英文单独出现在标题、卡片、caption、页脚或章节标签里。

## 禁止事项

- 不要做很多空泛三栏页。
- 不要把密集论文图缩得很小。
- 不要把论文大段正文、图注、表注截进截图。
- 能重写的表格必须自己写成原生表格，不要用表格截图。
- 翻译 PDF 裁图只裁图/流程图本体，不要连周围段落一起裁。
- 不要做单独术语记忆页，除非用户明确要求。
- 不要做“这版如何解决英文图”这种过程型废页。
- 不要做“为什么这篇文章值得讲”“这版汇报怎么读”这类自我规划页；应转成讲稿或内部 slide plan。
- 不要让 `controlled evaluation`、`autonomous research harness`、`components`、`claim`、`workflow` 等英文裸露在 PPT 上；翻译或写成 `中文（English）`。
- 不要为了填满页面编造数字或结论。
- 不要抛开 Guizang 和 Nature 两个基础 skill 从头发明新风格。

## 工作流

### 1. 源文件审计

使用 `zuhui-ppt-source-audit`。

输出：

- 源文件清单；
- 论文元数据；
- 页码 / 图 / 表地图；
- 从翻译 PDF 中裁出的中文图表；
- 资产 manifest；
- 旧版本问题和用户硬约束。

如果翻译 PDF 里已经有翻译后的图表，就渲染 PDF 页面并裁图，不要因为没有独立图片文件就放弃。

### 2. 论文主线

使用 `zuhui-ppt-story-spine`。

每一页都要回答：

- 本页 claim 是什么？
- 证据对象是什么？
- 为什么重要？
- 边界或局限是什么？

### 3. 瑞士风视觉计划

使用 `zuhui-ppt-swiss-design`。

优先使用 Guizang Swiss IKB 蓝、暗色章节页、白底证据页和 `S01–S22` 注册版式。大图证据页优先使用 `S22 Image Hero` 或近似的大图结构。

### 4. 三格式导出

使用 `zuhui-ppt-triformat-export`。

从同一份内容模型生成：

- PPTX；
- 注入 Guizang `template-swiss.html` 的 HTML；
- 从 HTML 打印出的 PDF；
- 讲稿和 QA。

如果浏览器 HTML 明显比原生 PPTX 复刻更接近 v1 金标准，优先保留视觉系统，并在 QA 中披露截图型 PPTX 降级。

### 5. QA 和迭代

使用 `zuhui-ppt-qa`。

必须检查：

- PPTX 页数 = HTML slide 数 = PDF 页数；
- 每个 HTML slide 都有 `data-layout`；
- 图片足够大；
- 没有禁用词；
- 所有素材存在；
- 有渲染器就做预览，没有就明确说明。

## 推荐输出目录

- `ppt_v4/`：修正后的第一版三格式瑞士风；
- `ppt_v5/`：写完新 skill 后，用新 skill 流程重新生成的版本。
- `ppt_v6/`：如果 v4/v5 视觉被否定，则回到 v1 风格并修正截图/表格策略后的版本。

## 最终回复

最终回复要说明：

- PPTX / HTML / PDF 路径；
- 相比被批评版本改了什么；
- 用了哪些基础 skill 和子 skill；
- QA 结果；
- 未完成的渲染限制。
