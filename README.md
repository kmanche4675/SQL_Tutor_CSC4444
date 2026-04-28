# 🧑‍🏫 Adaptive SQL Tutor

An intelligent tutoring system for SQL that adapts to each student's knowledge using Bayesian Knowledge Tracing (BKT) and provides two kinds of hints: **rule‑based** (fast, deterministic) and **generative AI** (smart, contextual, powered by a local LLM).

## ✨ Features

- 📚 **Adaptive problem selection** – after each answer, the system picks the next problem targeting your weakest SQL skill.
- 🧠 **Bayesian Knowledge Tracing** – a probabilistic model of your mastery of `WHERE`, `JOIN`, `GROUP BY`, `NULL` handling, and more.
- 💡 **Rule‑based hints** – instant hints for common mistakes (`= NULL`, missing `GROUP BY`, missing quotes, etc.).
- 🤖 **AI hints (Ollama)** – free, local, offline‑capable LLM (Meta’s Llama 3.2) that generates contextual hints without sending your data to the cloud.
- 📊 **Skill mastery dashboard** – see your progress for each SQL concept in the sidebar.
- 🧪 **Pre‑/post‑test ready** – easily extendable for user studies.

## 📋 Prerequisites

- **Python 3.8 or higher**
- **Git** (to clone the repository)
- **Ollama** (for AI hints – free, local)

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/kmanche4675/sql-tutor-ai.git
cd sql-tutor-ai
```

---

## Step 2: Add the virtual environment section

After the closing backticks, add this entire block:

```markdown
### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1

python3 -m venv venv
source venv/bin/activate
```

## Step 3: Add the dependencies installation

```markdown
### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Add database setup

```markdown
### 4. Set up the SQLite database

```bash
python database/init_db.py
```

---

## Step 5: Add Ollama installation and AI hints setup

```markdown
### 5. Install and run Ollama (for AI hints)

Ollama runs a local LLM on your machine – completely free, no API key required.

- **Download Ollama** from [ollama.com](https://ollama.com/) and install it.
- **Pull the model** (one time, ~2GB):

```bash
ollama pull llama3.2

ollama list
```

---

## Step 6: Add the command to run the tutor

```markdown
### 6. Run the SQL Tutor

```bash
streamlit run app.py
```

---

## Step 7: (Optional but recommended) Add "How to Use" and other sections

You can add the rest from the complete README I gave you earlier (Features, How to Use, Project Structure, etc.). But for the **minimum working setup**, Steps 1-6 are enough.

Once you add these steps in order, your README will be complete and properly formatted. Would you like me to provide the remaining sections (How to Use, Project Structure, Extending, etc.) one by one as well?
