"""Create a personalized AI 321 machine-exercise folder and notebook."""

from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path
from typing import Any


DEFAULT_STUDENT_NAME = "DE GUIA, CARL JUSTIN"
DEFAULT_STUDENT_NUMBER = "2011-06521"
TEMPLATE_FILENAME = "machine_exercise_template.ipynb"
SEED_FILENAME = "student_seed.py"
PROJECT_FILENAME = "pyproject.toml"


def normalize_exercise_number(exercise_number: str) -> str:
    """Return a two-digit machine-exercise number."""
    value = str(exercise_number).strip()
    if not value.isdigit() or not 1 <= int(value) <= 99:
        raise ValueError("Exercise number must be a whole number from 1 to 99.")
    return f"{int(value):02d}"


def _replace_placeholders(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, str):
        for placeholder, replacement in replacements.items():
            value = value.replace(placeholder, replacement)
        return value
    if isinstance(value, list):
        return [_replace_placeholders(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key: _replace_placeholders(item, replacements) for key, item in value.items()}
    return value


def create_machine_exercise(
    root: Path | str,
    exercise_number: str,
    *,
    title: str | None = None,
    student_name: str = DEFAULT_STUDENT_NAME,
    student_number: str = DEFAULT_STUDENT_NUMBER,
    template_path: Path | str | None = None,
    seed_path: Path | str | None = None,
    project_path: Path | str | None = None,
) -> Path:
    """Create and return ``me-XX`` without replacing an existing exercise."""
    root = Path(root)
    number = normalize_exercise_number(exercise_number)
    student_name = student_name.strip()
    student_number = student_number.strip()
    if not student_name or not student_number:
        raise ValueError("Student name and student number cannot be empty.")

    title = (title or f"AI 321 Machine Exercise {number}").strip()
    if not title:
        raise ValueError("Notebook title cannot be empty.")

    template_path = Path(template_path) if template_path else root / TEMPLATE_FILENAME
    seed_path = Path(seed_path) if seed_path else root / "me-01" / SEED_FILENAME
    project_path = Path(project_path) if project_path else root / "me-01" / PROJECT_FILENAME
    exercise_dir = root / f"me-{number}"
    notebook_path = exercise_dir / f"me-{number}.ipynb"

    if exercise_dir.exists():
        raise FileExistsError(f"{exercise_dir.name} already exists; refusing to overwrite it.")
    if not template_path.is_file():
        raise FileNotFoundError(f"Notebook template not found: {template_path}")
    if not seed_path.is_file():
        raise FileNotFoundError(f"Student seed helper not found: {seed_path}")
    if not project_path.is_file():
        raise FileNotFoundError(f"Exercise dependency manifest not found: {project_path}")

    with template_path.open(encoding="utf-8") as template_file:
        notebook = json.load(template_file)
    replacements = {
        "{{TITLE}}": title,
        "{{STUDENT_NAME}}": student_name,
        "{{STUDENT_NUMBER}}": student_number,
    }
    notebook = _replace_placeholders(copy.deepcopy(notebook), replacements)
    project_text = project_path.read_text(encoding="utf-8").replace(
        'name = "me-01"', f'name = "me-{number}"', 1
    )

    exercise_dir.mkdir()
    with notebook_path.open("w", encoding="utf-8") as notebook_file:
        json.dump(notebook, notebook_file, indent=1, ensure_ascii=False)
        notebook_file.write("\n")
    shutil.copy2(seed_path, exercise_dir / SEED_FILENAME)
    (exercise_dir / PROJECT_FILENAME).write_text(project_text, encoding="utf-8")
    return exercise_dir


def main() -> None:
    """Run the interactive machine-exercise creator."""
    root = Path(__file__).resolve().parent
    try:
        number = input("Machine exercise number (e.g. 02): ").strip()
        normalized_number = normalize_exercise_number(number)
        default_title = f"AI 321 Machine Exercise {normalized_number}"
        title = input(f"Notebook title [{default_title}]: ").strip() or default_title
        name = input(f"Student name [{DEFAULT_STUDENT_NAME}]: ").strip() or DEFAULT_STUDENT_NAME
        student_number = (
            input(f"Student number [{DEFAULT_STUDENT_NUMBER}]: ").strip()
            or DEFAULT_STUDENT_NUMBER
        )
        exercise_dir = create_machine_exercise(
            root,
            normalized_number,
            title=title,
            student_name=name,
            student_number=student_number,
        )
    except (FileExistsError, FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        print(f"Could not create the machine exercise: {error}")
        return

    print(f"Created {exercise_dir.name}/{exercise_dir.name}.ipynb")


if __name__ == "__main__":
    main()
