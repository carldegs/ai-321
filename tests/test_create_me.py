import json
import tempfile
import unittest
from pathlib import Path

from create_me import (
    DEFAULT_STUDENT_NAME,
    DEFAULT_STUDENT_NUMBER,
    create_machine_exercise,
)


class CreateMachineExerciseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.template_path = self.root / "machine_exercise_template.ipynb"
        self.seed_path = self.root / "student_seed.py"
        self.project_path = self.root / "pyproject.toml"
        self.seed_path.write_text("def get_my_params(student_number):\n    return {}\n")
        self.project_path.write_text(
            "[project]\nname = \"me-01\"\nversion = \"0.1.0\"\ndependencies = []\n"
        )
        self.template_path.write_text(
            json.dumps(
                {
                    "nbformat": 4,
                    "nbformat_minor": 5,
                    "metadata": {
                        "title": "{{TITLE}}",
                        "name": "{{STUDENT_NAME}}",
                        "student_number": "{{STUDENT_NUMBER}}",
                        "authors": [{"name": "{{STUDENT_NAME}} — {{STUDENT_NUMBER}}"}],
                    },
                    "cells": [
                        {
                            "cell_type": "code",
                            "metadata": {},
                            "execution_count": None,
                            "outputs": [],
                            "source": [
                                "from student_seed import get_my_params\n",
                                'params = get_my_params("{{STUDENT_NUMBER}}")\n',
                            ],
                        }
                    ],
                }
            )
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_creates_numbered_folder_notebook_and_seed_file(self):
        """Would fail if the generator omitted a runnable notebook dependency."""
        exercise_dir = create_machine_exercise(
            self.root,
            "7",
            template_path=self.template_path,
            seed_path=self.seed_path,
            project_path=self.project_path,
        )

        self.assertEqual(exercise_dir, self.root / "me-07")
        self.assertEqual((exercise_dir / "student_seed.py").read_text(), self.seed_path.read_text())
        self.assertIn('name = "me-07"', (exercise_dir / "pyproject.toml").read_text())
        with (exercise_dir / "me-07.ipynb").open() as notebook_file:
            notebook = json.load(notebook_file)
        self.assertEqual(notebook["metadata"]["title"], "AI 321 Machine Exercise 07")
        self.assertEqual(notebook["metadata"]["name"], DEFAULT_STUDENT_NAME)
        self.assertEqual(notebook["metadata"]["student_number"], DEFAULT_STUDENT_NUMBER)
        self.assertEqual(
            notebook["cells"][0]["source"][1],
            'params = get_my_params("2011-06521")\n',
        )

    def test_applies_title_and_identity_overrides(self):
        """Would fail if optional prompts did not propagate to notebook metadata and code."""
        exercise_dir = create_machine_exercise(
            self.root,
            "12",
            title="Custom exercise title",
            student_name="Ada Lovelace",
            student_number="2026-12345",
            template_path=self.template_path,
            seed_path=self.seed_path,
            project_path=self.project_path,
        )

        with (exercise_dir / "me-12.ipynb").open() as notebook_file:
            notebook = json.load(notebook_file)
        self.assertEqual(notebook["metadata"]["title"], "Custom exercise title")
        self.assertEqual(notebook["metadata"]["name"], "Ada Lovelace")
        self.assertEqual(notebook["metadata"]["student_number"], "2026-12345")
        self.assertEqual(notebook["metadata"]["authors"][0]["name"], "Ada Lovelace — 2026-12345")

    def test_refuses_to_overwrite_an_existing_exercise_folder(self):
        """Would fail if rerunning the generator could overwrite submitted work."""
        (self.root / "me-03").mkdir()

        with self.assertRaises(FileExistsError):
            create_machine_exercise(
                self.root,
                "03",
                template_path=self.template_path,
                seed_path=self.seed_path,
                project_path=self.project_path,
            )


if __name__ == "__main__":
    unittest.main()
