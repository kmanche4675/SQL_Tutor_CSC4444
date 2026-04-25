import streamlit as st
from problems import get_problem, get_all_problems
from evaluator import evaluate, generate_hint, generate_ai_hint  # added generate_ai_hint
from student_model import load_model, update_knowledge, get_next_problem

st.set_page_config(page_title="SQL Tutor", page_icon="📚")
st.title("🧑‍🏫 Adaptive SQL Tutor")

# Initialize session state
if "current_problem_id" not in st.session_state:
    st.session_state.current_problem_id = 1
if "completed" not in st.session_state:
    st.session_state.completed = set()
if "attempts" not in st.session_state:
    st.session_state.attempts = {}
if "student_model" not in st.session_state:
    st.session_state.student_model = load_model()

# Get all problems
all_problems = get_all_problems()

# Sidebar: problem list + skill mastery
st.sidebar.header("Problems")
for p in all_problems:
    if p["id"] == st.session_state.current_problem_id:
        label = f"✅ {p['title']}" if p["id"] in st.session_state.completed else f"🔵 {p['title']}"
    else:
        label = f"✅ {p['title']}" if p["id"] in st.session_state.completed else f"⚪ {p['title']}"
    if st.sidebar.button(label, key=f"nav_{p['id']}"):
        st.session_state.current_problem_id = p["id"]
        st.rerun()

# Skill mastery display in sidebar
st.sidebar.divider()
st.sidebar.header("📊 Your Skill Mastery")
for skill, data in st.session_state.student_model.items():
    mastery = data["p_mastered"]
    confidence = data.get("confidence", 0.0)
    entropy = data.get("entropy", 0.0)
    obs_count = data.get("observation_count", 0)
    
    st.sidebar.progress(mastery)
    st.sidebar.write(f"**{skill}**: {mastery:.0%}")
    st.sidebar.write(f"_Confidence: {confidence:.0%} | Obs: {obs_count}_")
    if entropy > 0.5:
        st.sidebar.write("⚠️ High uncertainty")
    elif entropy < 0.1:
        st.sidebar.write("✅ Well-established")
    st.sidebar.write("---")

# Detailed probability stats
with st.sidebar.expander("🔍 Probability Details"):
    st.write("**Bayesian Knowledge Tracing Stats:**")
    for skill, data in st.session_state.student_model.items():
        st.write(f"**{skill}:**")
        st.write(f"- Mastery: {data['p_mastered']:.3f}")
        st.write(f"- Confidence: {data.get('confidence', 0):.3f}")
        st.write(f"- Entropy: {data.get('entropy', 0):.3f}")
        st.write(f"- Observations: {data.get('observation_count', 0)}")
        st.write("---")

# Main area
problem = get_problem(st.session_state.current_problem_id)
if problem is None:
    st.error("Problem not found")
    st.stop()

st.header(f"Problem {problem['id']}: {problem['title']}")
st.markdown(problem["description"])

with st.expander("📊 Database Schema"):
    st.code("""
employees (id, name, department, salary, manager_id)
departments (id, name, budget)
    """)

student_query = st.text_area("Write your SQL query:", height=150, key="sql_input")

# Four columns: Submit, Rule Hint, AI Hint, Reset
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Submit"):
        if not student_query.strip():
            st.warning("Please write a query.")
        else:
            correct, feedback = evaluate(problem, student_query)
            if correct:
                st.success(feedback)
                st.session_state.completed.add(problem["id"])
                # Update student model (correct)
                update_knowledge(st.session_state.student_model, problem.get("skills", []), was_correct=True)
                # Record attempt
                if problem["id"] not in st.session_state.attempts:
                    st.session_state.attempts[problem["id"]] = 1
                else:
                    st.session_state.attempts[problem["id"]] += 1
            else:
                st.error(feedback)
                # Update student model (incorrect)
                update_knowledge(st.session_state.student_model, problem.get("skills", []), was_correct=False)
                # Record attempt
                if problem["id"] not in st.session_state.attempts:
                    st.session_state.attempts[problem["id"]] = 1
                else:
                    st.session_state.attempts[problem["id"]] += 1

with col2:
    if st.button("💡 Rule Hint"):
        if not student_query.strip():
            st.warning("Write your query first, then ask for a hint.")
        else:
            hint = generate_hint(student_query, problem)
            st.info(f"**Rule-based Hint:** {hint}")

with col3:
    if st.button("🤖 AI Hint (Ollama)"):
        if not student_query.strip():
            st.warning("Write your query first, then ask for a hint.")
        else:
            with st.spinner("🤖 Thinking..."):
                ai_hint = generate_ai_hint(student_query, problem)
                st.info(ai_hint)

with col4:
    if st.button("Reset Problem"):
        # Remove this problem from completed set so it can be tried again
        st.session_state.completed.discard(problem["id"])
        st.rerun()

# Adaptive next problem button (appears if any problem completed)
if st.session_state.completed:
    next_id = get_next_problem(st.session_state.student_model, all_problems, st.session_state.completed)
    if next_id and st.button("🎯 Adaptive Next Problem"):
        st.session_state.current_problem_id = next_id
        st.rerun()

# Progress bar and stats
completed_count = len(st.session_state.completed)
total = len(all_problems)
st.progress(completed_count / total if total > 0 else 0)
st.write(f"Progress: {completed_count}/{total} problems solved")

if st.session_state.attempts:
    with st.expander("📈 Your attempt stats"):
        for pid, att in st.session_state.attempts.items():
            prob = get_problem(pid)
            if prob:
                st.write(f"Problem {pid} ({prob['title']}): {att} attempts")