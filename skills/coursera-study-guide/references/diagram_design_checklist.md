# Diagram Design Checklist (`matplotlib` / `Pillow`)

Every module study guide should include **1 Module Roadmap visual** plus **1 dedicated diagram per subsection**, rendered at `300 DPI`.

## 1. Visual Styling Standards
- **Cohesive Palette**: Stick to 1 primary dark (`#0F2942`), 1–2 accents (`#0F62FE`, `#007D79`), muted text (`#393939` / `#6F6F6F`), soft card backgrounds (`#F8FAFC` / `#EDF5FF`), and semantic highlights (`#198038` green, `#B25000` amber, `#DA1E28` red, `#6929C4` purple).
- **Resolution & Sizing**: Aspect ratios around `10.8–11.4 in` wide by `4.5–6.0 in` tall (`dpi=300`, `bbox_inches="tight"`, white `#FFFFFF` background). Embed in `.docx` at `6.0–6.85 in` width.

## 2. Diagram Types by Content
- **Module Overview**: Horizontal phase roadmap showing numbered item badges color-coded by type (Video, Reading, Lab, Practice Quiz, Graded Quiz).
- **Curriculum / Concept Arcs**: Stage-by-stage progression cards with prerequisite pillars and tool chips.
- **Image / Matrix Concepts**: Side-by-side human perception vs. numeric pixel/channel grid (`imshow` with printed cell values `0–255` and high-contrast text).
- **Image Processing / Pipelines**: Multi-panel step visualizations (e.g., raw image → grid slicing / filter kernel → intermediate mask → heatmap / transformed output).
- **Code / Lab Data Flow**: Visual pipeline showing tensor/array shapes (`(H, W, 3)` → grayscale `(H, W)` → kernel convolution / histogram) paired with Python API calls (`cv2`, `PIL.Image`, `numpy`).
- **Quiz Reviews**: Scenario decision cards highlighting why right architectures succeed and why common traps fail, or traceability tables mapping Qs back to source lectures.

## 3. Common Layout Bugs to Prevent
1. **Use `ax.inset_axes(..., transform=ax.transData)` — NEVER `fig.add_axes(...)`**: `fig.add_axes` uses figure fractions that drift over headers when `bbox_inches="tight"` crops the canvas. `ax.inset_axes(..., transform=ax.transData)` locks sub-plots strictly inside box coordinates.
2. **Explicit `zorder`**: Rounded container boxes (`zorder=2`) will hide shapes drawn inside them unless inner artwork sets `zorder >= 3` and labels set `zorder >= 5`.
3. **Title/Subtitle Clearance**: Keep at least `0.35`–`0.45` data units between the subtitle and the top border of the first row of cards.
4. **Badge & Pill Overflow**: Never place long titles and right-aligned badges on the same tight single line—stack them vertically or use multi-line labels inside boxes.
5. **Visual QA Gate**: Always open every generated `.png` with your file/image-reading tool before building the `.docx`. Fix any clipped characters, overlapping pills, or low-contrast text on dark fills immediately.
