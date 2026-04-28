# 🧑‍🏫 Adaptive SQL Tutor

An intelligent tutoring system for SQL that adapts to each student's knowledge using **Bayesian Knowledge Tracing (BKT)** and provides two kinds of hints: **rule-based** (fast, deterministic) and **AI-powered** (contextual, via local LLM).

## ✨ Features

- 📚 **Adaptive problem selection** – after each answer, the system picks the next problem targeting your weakest SQL skill
- 🧠 **Bayesian Knowledge Tracing** – probabilistic model of your mastery of `WHERE`, `JOIN`, `GROUP BY`, `NULL` handling, and more
- 💡 **Rule-based hints** – instant hints for common mistakes (`= NULL`, missing `GROUP BY`, missing quotes, etc.)
- 🤖 **AI hints (Ollama)** – free, local, offline-capable LLM (Meta's Llama 3.2) that generates contextual hints without sending data to the cloud
- 📊 **Skill mastery dashboard** – see your progress for each SQL concept in the sidebar
- 🧪 **Pre-/post-test ready** – easily extendable for user studies and research

## 📋 Prerequisites

- **Python 3.8 or higher**
- **Git** (to clone the repository)
- **Ollama** (for AI hints – free, local, offline-capable)

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/kmanche4675/SQL_Tutor_CSC4444.git
cd SQL_Tutor_CSC4444
```

### 2. Create and activate a virtual environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- `streamlit` – web UI framework
- `pandas` – data manipulation
- `sqlglot` – SQL parsing and validation
- `ollama` – local LLM client

### 4. Set up the SQLite database

```bash
python database/init_db.py
```

This creates `database/tutor.db` with sample `employees` and `departments` tables for practice problems.

### 5. Install and run Ollama (for AI hints)

Ollama runs a local LLM on your machine – completely free, no API key required, and fully offline-capable.

1. **Download and install Ollama** from [ollama.com](https://ollama.com/)
2. **Pull the model** (one-time download, ~2GB):

```bash
ollama pull llama3.2
```

3. **Verify Ollama is running:**

```bash
ollama list
```

You should see `llama3.2` in the list. Ollama typically starts automatically after installation; if you encounter connection errors, manually run:

```bash
ollama serve
```

### 6. Run the SQL Tutor

```bash
streamlit run app.py
```

Your browser will automatically open at `http://localhost:8501`.

## 🎮 How to Use

1. **Select a problem** from the sidebar
2. **Write an SQL query** in the text area
3. **Click Submit** – the system executes your query and compares results to the expected output
4. **Get help:**
   - 💡 **Rule Hint** – instant, deterministic hint based on common mistake patterns
   - 🤖 **AI Hint (Ollama)** – waits 2–5 seconds, then gives a smart, contextual hint from the local LLM
5. **After a correct answer**, click 🎯 **Adaptive Next Problem** – the tutor selects the next problem targeting your weakest skill
6. **Track progress** in the skill mastery bars in the sidebar

## 📁 Project Structure

```
SQL_Tutor_CSC4444/
├── app.py                    # Streamlit web UI
├── evaluator.py              # SQL execution, result comparison, hint generation
├── problems.py               # Problem definitions & metadata
├── student_model.py          # Bayesian Knowledge Tracing & adaptive selection
├── database/
│   ├── init_db.py            # Creates SQLite database with sample data
│   └── tutor.db              # Generated SQLite database (created by init_db.py)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔧 Extending the Tutor

### Add More SQL Problems

Edit `problems.py` and follow the existing structure. Each problem needs:

```python
{
    "id": "problem_unique_id",
    "title": "Problem Title",
    "description": "Clear problem description with context",
    "expected_sql": "SELECT ... FROM ... WHERE ...",
    "compare_columns": ["col1", "col2"],  # or None for all columns
    "skills": ["basic_where", "join"]     # must match skills in student_model.py
}
```

### Add a New SQL Skill for BKT

1. Add the skill name to `SKILLS` in `student_model.py`
2. Add default BKT parameters to `PARAMS`:
   ```python
   "new_skill": {
       "p_mastered": 0.0,  # Prior probability of mastery
       "p_learn": 0.25,    # Probability of learning from one problem
       "p_guess": 0.1,     # Probability of guessing correctly
       "p_slip": 0.05      # Probability of mistake when mastered
   }
   ```
3. Tag problems with the new skill in `problems.py`

### Use a Different Local LLM

In `evaluator.py`, modify the `ollama.chat()` call to use any model you've pulled:

```python
response = ollama.chat(
    model="mistral",  # or "phi4", "llama3.3", etc.
    messages=[...],
    stream=False
)
```

Available models can be browsed at [ollama.com/library](https://ollama.com/library).

## 📝 CSC4444 Final Project Submission

This project fulfills all requirements for an intelligent agent:

✅ **Probabilistic reasoning** – Bayesian Knowledge Tracing for adaptive learning  
✅ **Rule-based expert system** – Misconception detection & hint generation  
✅ **Generative AI** – Local LLM hints via Ollama (privacy-preserving, offline)

### Submission Checklist

- [ ] Push final code to GitHub
- [ ] Provide repository link in LaTeX report (NeurIPS template)
- [ ] Include short demo video (≤5 minutes) showing:
  - Adaptive problem selection
  - Rule-based hints
  - AI hints from Ollama
  - Skill mastery dashboard updates

## 🧠 How It Works Under the Hood

**Bayesian Knowledge Tracing** models whether you've "learned" each skill. After each problem:
- **Correct answer** → increases probability you've mastered the skill
- **Incorrect answer** → decreases probability
- **Next problem** → selected from your weakest skill (lowest mastery probability)

**Rule-based hints** check for common SQL mistakes:
- Using `= NULL` instead of `IS NULL`
- Missing `GROUP BY` when aggregating
- Missing quotes around strings
- Incorrect `JOIN` syntax

**AI hints** via Ollama generate contextual, natural-language feedback without uploading your code to external servers.

## 🙏 Acknowledgements

- Corbett & Anderson (1995) – Bayesian Knowledge Tracing
- Ahadi et al. (2016) – Common SQL mistakes in education
- [Ollama](https://ollama.com) – Local LLM runner
- [Streamlit](https://streamlit.io) – Web UI framework

## 📄 License

This project is for educational use in CSC4444 at the University of Lousiana State University.

---

**Need help?** Check the setup instructions above or run `streamlit run app.py` and explore the UI. The system is designed to be intuitive and self-explanatory.
