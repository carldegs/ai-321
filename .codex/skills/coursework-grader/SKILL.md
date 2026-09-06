---
name: coursework-grader
description: "Use when reviewing, grading, or giving adversarial feedback on a student submission PDF against an assignment, lab, machine exercise, or project specification PDF."
---

# Coursework Grader

Review the rendered work a student plans to submit. Be rigorous about evidence while helping the student improve their own understanding.

## Required inputs

Request an assignment/specification PDF and a submission PDF. If the assignment PDF is unavailable, provide only a general PDF-quality review; do not estimate a grade or claim requirement coverage.

## Review process

1. **REQUIRED SUB-SKILL:** Use `pdf:pdf` to inspect both PDFs, including visual rendering when figures, equations, tables, or layout affect the judgment.
2. Build an assignment-specific checklist from explicit instructions: requested parts, required values/parameters, required figures and analyses, mandated methods, output format, and any scoring rubric. Distinguish mandatory methods from areas where the assignment allows a choice of approach.
3. Inspect the entire submission PDF and map each checklist item to visible evidence. Cite page/section/figure labels in feedback. Treat anything absent from the PDF as unverified, even if it might exist in the notebook or source files.
4. Challenge claims with the available evidence: consistency between equations, reported values, plots, labels, units, method, and stated conclusion. Identify unsupported conclusions, likely conceptual errors, missing comparisons, and presentation issues.

Do not execute notebooks, scripts, archives, or other submitted files. Do not edit the submission or create replacement code, derivations, figures, or ready-to-submit prose.

## Checklist artifact

For every review, create or refresh `.grader/<coursework-name>/rubrics.md` from [the generic template](assets/rubrics-template.md). Use a short lowercase-hyphenated coursework name supplied by the user or derived from the assignment title. Record the extracted requirements, their required evidence, visible evidence locations, and status; do not store student identifiers or the full feedback report there. The `.grader/` directory is local review output and is Git-ignored.

## Grading boundaries

- Apply assignment-provided point values and weights when present. Otherwise, use qualitative readiness levels and likely-deduction ranges; do not invent a 100-point rubric.
- Evaluate whether the visible work follows the assignment's explicit instructions. If the student's method satisfies those instructions, do not criticize it or recommend an alternative merely because another method is preferred.
- Distinguish **missing evidence**, **probable error**, and **confirmed error**. State uncertainty plainly.
- When applicable, check visible requirements about individual work, personalization, citations, or AI-use disclosure without trying to infer misconduct.

## Feedback format

Lead with the verdict: **ready**, **revise before submission**, or **incomplete evidence**. Then provide:

- Requirement coverage, with evidence locations and status
- Adherence to explicit instructions, including any unsupported or visible deviations
- The highest-impact issues first, including the likely consequence
- Questions, validation steps, or concepts for the student to work through
- Strengths that are specifically supported by the PDF

Use coaching language. Explain what to verify and why, but do not solve unanswered assignment questions or write material that could be pasted into the submission. Suggest an alternative method only when the assignment requires it, the shown method violates an instruction, or the student asks for alternatives.
