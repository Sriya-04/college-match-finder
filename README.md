# College Match Finder 🎓

A beginner-friendly Python and Streamlit project that compares a student's profile with historical U.S. college admissions statistics.

## Purpose

This project was designed as a simple freshman-level programming project. The goal is to demonstrate:

- Python basics
- Functions and conditional logic
- Reading CSV data with pandas
- Working with a DataFrame
- Building a small user interface with Streamlit
- Separating program logic from the user interface

It is **not** an admissions guarantee or a machine-learning prediction.

## How it works

1. The student enters an SAT score, GPA, intended major, and a few profile details.
2. pandas loads college information from `data/colleges.csv`.
3. `matcher.py` compares the SAT score with each college's historical SAT range.
4. Very selective colleges are kept in the Reach category as a simple guardrail.
5. The application displays colleges as **Likely**, **Target**, or **Reach**.

The extracurricular/profile score is displayed as supporting context. It does not pretend to represent an official admissions formula.

## Project structure

```text
college-match/
├── app.py
├── matcher.py
├── data/
│   └── colleges.csv
├── requirements.txt
├── README.md
└── .gitignore
```

## Run locally

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Matching rules

The first version intentionally uses transparent rules rather than machine learning:

- Admission rate below 15% → Reach
- SAT at or above the college's 75th percentile → Likely
- SAT within the 25th–75th percentile range → Target
- SAT below the 25th percentile → Reach

These categories are educational profile matches, not predictions of admission.

## Data note

The starter CSV contains a small set of U.S. colleges and representative historical admissions fields so the application is easy to understand and demonstrate. Before using the project for real admissions research, refresh and verify each institution's statistics against authoritative sources such as the U.S. Department of Education College Scorecard and each college's published Common Data Set.

## Possible future improvements

- Refresh the dataset from authoritative sources
- Add ACT support
- Add state and region filters
- Add college cost information
- Add more intended majors
- Explain each match in more detail
- Explore machine learning only if reliable applicant-level training data becomes available

## Disclaimer

College admissions decisions depend on many factors including academic record, course rigor, essays, recommendations, activities, institutional priorities, residency, intended program, and other considerations. This application is for educational purposes only.
