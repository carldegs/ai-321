# AI-321 Repository Notes

- Unless the user explicitly requests an edit, do not add, modify, or delete code or repository files. Act as an assistant that provides snippets, opinions, explanations, and recommendations.
- Lesson PDFs are stored in the [`notes/`](notes/) directory. Look there first when a task needs lesson material or reference notes.
- Each machine exercise lives in its own top-level folder (for example, `me-01/`).
- Each machine-exercise folder manages its own isolated Python virtual environment; do not share a virtual environment between exercises or create one at the repository root.
- Use `uv` for a machine exercise's environment and dependencies. Run `uv sync` from that exercise's directory before working on it.
- When asked to grade or review coursework PDFs, use `$coursework-grader`. It compares an assignment PDF with a submission PDF, keeps its generated checklist in `.grader/<coursework-name>/rubrics.md`, and does not execute submitted work.

## Creating a new machine exercise

- Use the root-level `create_me.py` script to create a new exercise folder and personalized notebook: run `python create_me.py` from the repository root.
- Enter the exercise number when prompted; the script creates `me-XX/` and `me-XX.ipynb`, using `machine_exercise_template.ipynb`.
- Press Enter at the title, name, and student-number prompts to keep their defaults. The script uses the ME-01 student identity defaults and sets the default title to `AI 321 Machine Exercise XX`.
- The generator copies `student_seed.py` and an exercise-specific `pyproject.toml` into the new folder. Run `uv sync` from that new folder before opening or executing the notebook.
- Do not overwrite an existing `me-XX/` folder; the generator intentionally refuses to replace it.

## Notebook math and PDF export

- Use `$...$` for inline mathematics and `$$...$$` for standalone equations. Leave a blank line before and after each display equation.
- Use `\begin{aligned}...\end{aligned}` for multi-line derivations and `\begin{cases}...\end{cases}` for piecewise definitions. Separate aligned lines with `\\`.
- Prefer LaTeX commands over text approximations: `\frac{a}{b}`, `z^{-1}`, `\sin`, `\Delta f`, and `\lvert x\rvert`.
- Keep Matplotlib title and axis-label math to simple `$...$` expressions. Put complex environments such as `aligned` and `cases` only in Markdown cells.
- When editing an `.ipynb` file as raw JSON, escape every backslash: write `\\frac` for `\frac` and `\\\\` for a LaTeX line break. In Jupyter's Markdown editor, use normal single backslashes.
- Before submission, export from the exercise folder with `uv run jupyter nbconvert --to pdf me-XX.ipynb`, then visually check the PDF for clipped equations, tables, and figures.

## Relevant documentation websites

- [Matlab Documentation](https://www.mathworks.com/help/matlab/index.html)
- [System ID Documentation Reference List](https://www.mathworks.com/help/ident/referencelist.html?type=app)
- [Statistics and Machine Learning Toolbox Documentation](https://www.mathworks.com/products/statistics.html)
