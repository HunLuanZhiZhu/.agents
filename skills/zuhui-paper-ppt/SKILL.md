---
name: zuhui-paper-ppt
description: Legacy alias for the newer zuhui-ppt-master workflow. Use when older prompts mention zuhui-paper-ppt; immediately switch to zuhui-ppt-master and its subskills for advanced Chinese group-meeting paper PPTX/HTML/PDF generation with Swiss International style and evidence-first paper extraction. All project-specific hardcodes have been removed; output paths use PROJECT_SLUG and VERSION parameters.
---

# Zuhui Paper PPT

This legacy skill is superseded by `zuhui-ppt-master`.

When this skill triggers:

1. Load `zuhui-ppt-master`.
2. Follow its subskill chain:
   - `zuhui-ppt-source-audit`
   - `zuhui-ppt-story-spine`
   - `zuhui-ppt-swiss-design`
   - `zuhui-ppt-triformat-export`
   - `zuhui-ppt-qa`
   - `zuhui-ppt-visual-score`
3. Preserve PPTX, HTML, and PDF.
4. Use Swiss International style and evidence-first paper extraction.
5. All output paths use project parameters (`PROJECT_SLUG`, `VERSION`, `OUTPUT_DIR`, `VISUAL_REF`) — no hardcoded project names or version numbers.

Do not continue using the older short workflow except as a compatibility alias.

