# AI Response Evaluation System

A practical portfolio project for structured human evaluation of AI-generated text.

## Project purpose

This Streamlit application helps an evaluator compare two AI responses to the same user prompt using a consistent six-dimension rubric:

- Accuracy
- Relevance
- Instruction Following
- Clarity
- Completeness
- Safety

The evaluator can add evidence-based notes, choose an overall preference, review saved evaluations, and export results as CSV or JSON.

## Features

- Side-by-side response comparison
- Six evaluation dimensions, each scored from 1 to 5
- Live average-score summary
- Overall preference selection (Response A, Response B, or Tie)
- Evaluator notes and evidence
- Four fictional practice cases
- Session history with CSV and JSON export
- English-language interface and documentation

## Run locally

### 1. Install Python

Use Python 3.10 or newer.

### 2. Download or clone this repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-response-evaluation-system.git
cd ai-response-evaluation-system
```

### 3. Create and activate a virtual environment (recommended)

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Launch the app

```bash
streamlit run app.py
```

The application will open in your browser. If it does not, use the local URL printed in the terminal (usually `http://localhost:8501`).

## How to use

1. Open **Evaluate responses**.
2. Optionally load a fictional practice case.
3. Enter the user prompt and both AI responses.
4. Score Response A and Response B on all six dimensions.
5. Select the better response (or a tie).
6. Add evidence-based notes.
7. Save the evaluation.
8. Open **Evaluation history** to review or export your work.

## Repository structure

```text
ai-response-evaluation-system/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── sample_cases.json
├── docs/
│   └── evaluation_rubric.md
└── tests/
    └── test_scoring.py
```

## Methodology

Both responses are evaluated independently against the same rubric. Scores range from 1 (Poor) to 5 (Excellent). The arithmetic mean is shown as a descriptive summary only; it is not a calibrated probability or an official quality score.

Specific evidence should be recorded in the evaluator notes. A serious factual or safety failure may outweigh a small numerical advantage.

## Limitations and responsible use

- This is an educational portfolio demonstration, not an official annotation platform.
- The application does not call an AI model or automatically determine which answer is correct; the human evaluator makes the judgment.
- Saved evaluations are held in Streamlit session memory. Export CSV or JSON files to preserve them.
- Use fictional or public examples. Do not enter confidential, personal, or customer data.
- Always follow task-specific instructions from the organization being evaluated for.

## Portfolio skills demonstrated

- Structured evaluation and quality assurance
- Analytical comparison and evidence-based judgment
- Instruction-following assessment
- Clear written documentation
- Basic Python application development
- Data organization and export

## Suggested future improvements

- Persistent database storage
- Customizable rubric weights
- Batch evaluation and analytics dashboard
- Blind evaluation mode
- Authentication and reviewer roles

## Author

Portfolio project created for learning and demonstration purposes.
