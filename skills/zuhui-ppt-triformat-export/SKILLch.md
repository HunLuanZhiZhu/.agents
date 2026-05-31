# Zuhui PPT Tri-Format Export（中文说明）

## 目标

从同一份内容模型导出并保留三种产物：

- `.pptx`：方便编辑；
- `.html`：Guizang Swiss 横向网页演示；
- `.pdf`：方便审阅、打印和归档。

用户要求三种产物时，HTML/PDF 不能当作可选项。

## 构建顺序

推荐：

1. 生成内容模型和 slide specs；
2. 生成可编辑 PPTX；
3. 把 slide sections 注入 Guizang `template-swiss.html`；
4. 从 HTML 导出 PDF；
5. 生成讲稿和 QA。

三种输出必须由同一份 slide specs 驱动，避免内容漂移。

## PPTX 规则

- 16:9；
- 文字可编辑；
- 明确数值尽量用原生表格；
- 翻译 PDF 裁图只用于无法重绘的密集原图，且不能带正文、图注或表注；
- 论文表格只要数值可读，就要重建为原生表格；
- 保留 Swiss 节奏：IKB 封面、暗色 statement、白底证据页、暗色章节页；
- 图表要大，不要机械 50/50；
- 有页码和来源。

## HTML 规则

- 优先使用 `guizang-ppt-skill/assets/template-swiss.html`；
- 替换标题占位符；
- 只把真实 slide 插入 deck 区域；
- 每页必须有 `data-layout`；
- `data-animate` 要和版式匹配；
- 图片放 `assets/`；
- 为 PDF 导出注入必要 print CSS。

## PDF 规则

- 从 HTML 导出；
- 使用 16:9 页面；
- 打印时覆盖 Guizang 横向固定 deck，让每个 slide 成为一页；
- PDF 页数必须等于 slide 数。

如果浏览器打印会裁掉 Guizang 固定版式页面，可以从实时 HTML 逐页渲染 16:9 截图，再由截图组装 PDF。这个降级方案必须写进 QA 报告。

## 视觉保真降级方案

常规目标是 PPTX 文字可编辑、表格原生。但如果用户明确更重视浏览器/v1 视觉效果，且原生 PPTX 复刻会明显变丑，可以使用截图型 PPTX，条件是：

- 用户反馈已经否定前一版视觉，或明确要求视觉质量优先；
- HTML 仍然是 canonical source；
- QA 报告明确说明 PPTX 是视觉保真/截图型，不是完全逐元素可编辑；
- HTML 中表格仍然是原生表格，不能来自表格截图。

## 输出包

版本目录中保留：

- `aris_group_meeting_vX.pptx`
- `aris_group_meeting_vX.html`
- `aris_group_meeting_vX.pdf`
- `speaker_notes_vX.md`
- `qa_report_vX.md`
- `assets/`
- `contact_sheet_vX.png` 或等价渲染预览；
- 构建脚本或命令

不要覆盖旧版本，除非用户要求。

## 失败处理

如果 PDF 失败，不能说三格式完成；要报告错误并修复。HTML/PPTX 页数不一致时，也要先修。
