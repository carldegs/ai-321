# AI-321

Course materials and machine exercises for AI-321.

## Lesson notes

Lesson PDFs are organized in [`notes/`](notes/), including the [complementary notes](notes/AI321_ComplementaryNotes.pdf).

## Machine exercises

Each machine exercise has its own top-level directory (for example, [`me-01/`](me-01/)) and an independent Python environment.

From an exercise directory, install its locked dependencies with:

```sh
uv sync
```

Run commands for that exercise through `uv`, for example:

```sh
uv run python student_seed.py
```
