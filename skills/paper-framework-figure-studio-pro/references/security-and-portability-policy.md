# Security And Portability Policy

- Store project paths as relative paths.
- Reject path traversal and host-specific absolute paths in state fields.
- Do not store API keys, tokens, passwords, credentials, or secret-like fields in project state.
- Do not include Python caches, temporary smoke-test output, or local runtime artifacts in release packages.
- S2/S5 target-paper outputs must be generated raster images from Image Gen, ChatGPT Create Image, or a named approved image-generation API, not code-drawn or programmatic-raster substitutes such as Python/PIL, Matplotlib, Graphviz, TikZ, screenshots, SVG-to-PNG, or PPT-rendered diagrams.
- Run the release path scanner before packaging.
