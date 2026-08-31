# AI-321 Repository Notes

- Unless the user explicitly requests an edit, do not add, modify, or delete code or repository files. Act as an assistant that provides snippets, opinions, explanations, and recommendations.
- Lesson PDFs are stored in the [`notes/`](notes/) directory. Look there first when a task needs lesson material or reference notes.
- Each machine exercise lives in its own top-level folder (for example, `me-01/`).
- Each machine-exercise folder manages its own isolated Python virtual environment; do not share a virtual environment between exercises or create one at the repository root.
- Use `uv` for a machine exercise's environment and dependencies. Run `uv sync` from that exercise's directory before working on it.
