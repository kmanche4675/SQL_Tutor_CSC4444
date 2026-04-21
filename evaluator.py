import sqlite3
import pandas as pd
import re
from sqlglot import parse_one, errors
import ollama  # <-- NEW: for local LLM hints

DB_PATH = "database/tutor.db"

def execute_sql(query):
    """Run query and return (success, result_df or error_message)"""
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return True, df
    except Exception as e:
        conn.close()
        return False, str(e)

def generate_hint(student_query, problem):
    """Rule-based hint generator based on common SQL mistakes"""
    query_upper = student_query.upper()
    
    # Pattern 1: Using = NULL instead of IS NULL
    if re.search(r'=\s*NULL', query_upper) or re.search(r'<>\s*NULL', query_upper) or re.search(r'!=\s*NULL', query_upper):
        return "💡 Hint: In SQL, NULL is never equal to anything, not even NULL. Use `IS NULL` or `IS NOT NULL` instead of `= NULL` or `!= NULL`."
    
    # Pattern 2: GROUP BY without aggregate function
    if 'GROUP BY' in query_upper:
        aggregates = ['COUNT(', 'SUM(', 'AVG(', 'MAX(', 'MIN(']
        if not any(agg in query_upper for agg in aggregates):
            return "💡 Hint: You used GROUP BY but no aggregate function like COUNT, SUM, or AVG. When grouping, you usually want to calculate something per group."
    
    # Pattern 3: JOIN without ON condition
    if 'JOIN' in query_upper and ' ON ' not in query_upper:
        return "💡 Hint: You have a JOIN but no ON condition. Use `ON` to specify how the tables are related (e.g., `ON employees.dept_id = departments.id`)."
    
    # Pattern 4: Missing quotes around string
    if re.search(r"=\s*[A-Za-z][A-Za-z0-9_]*\s*(?:$|WHERE|GROUP|ORDER|LIMIT)", query_upper):
        if "='" not in student_query and '="' not in student_query:
            return "💡 Hint: Strings in SQL need single quotes. For example: `WHERE department = 'Engineering'`."
    
    # Pattern 5: Missing GROUP BY when using aggregate
    aggregates = ['COUNT(', 'SUM(', 'AVG(', 'MAX(', 'MIN(']
    has_aggregate = any(agg in query_upper for agg in aggregates)
    if has_aggregate and 'GROUP BY' not in query_upper:
        select_clause = re.split(r'FROM|WHERE|GROUP|ORDER', student_query, flags=re.IGNORECASE)[0]
        if select_clause and not re.search(r'COUNT\(|SUM\(|AVG\(|MAX\(|MIN\(', select_clause, re.IGNORECASE):
            return "💡 Hint: You used an aggregate function but didn't GROUP BY the other columns. Remember: when you use COUNT/SUM/AVG, all non-aggregated columns in SELECT must appear in GROUP BY."
    
    # Pattern 6: Syntax error from sqlglot
    try:
        parse_one(student_query)
    except errors.ParseError as e:
        return f"💡 Hint: There's a syntax error in your query. Check for missing commas, parentheses, or keywords. Details: {str(e)[:150]}"
    
    return "💡 Hint: Your query ran but returned a different result than expected. Check your WHERE conditions, column names, and ensure you're selecting the right tables."

def generate_ai_hint(student_query, problem, error_message=None):
    """Generate a smart hint using local Ollama LLM"""
    try:
        # Build a prompt for the LLM
        prompt = f"""You are a helpful SQL tutor. The student is solving:
Problem: {problem['description']}
Database schema:
employees (id, name, department, salary, manager_id)
departments (id, name, budget)

Student's SQL query:
{student_query}

"""
        if error_message:
            prompt += f"The system returned this error: {error_message}\n\n"
        else:
            prompt += "The query ran but produced wrong results.\n\n"
        
        prompt += """Give a short, specific, encouraging hint (2-3 sentences) that helps the student understand what might be wrong. Do NOT give the full correct SQL. Focus on the concept or mistake."""
        
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'user', 'content': prompt}
        ])
        hint = response['message']['content'].strip()
        return f"🤖 AI Hint: {hint}"
    except Exception as e:
        # Fallback to rule-based hint if AI fails
        print(f"AI hint failed: {e}")
        return generate_hint(student_query, problem)

def evaluate(problem, student_query):
    """Compare student's query result to expected result and return (correct, feedback)"""
    # Execute student query
    ok_student, student_result = execute_sql(student_query)
    if not ok_student:
        # Use AI hint for syntax errors too
        ai_hint = generate_ai_hint(student_query, problem, student_result)
        return False, f"**SQL Error:** {student_result}\n\n{ai_hint}"
    
    # Execute expected query
    ok_expected, expected_result = execute_sql(problem["expected_sql"])
    if not ok_expected:
        return False, f"Internal error: expected query failed. Please contact instructor."
    
    # Normalize: sort rows if order doesn't matter
    if not problem.get("order_matters", False):
        student_result = student_result.sort_values(by=student_result.columns.tolist()).reset_index(drop=True)
        expected_result = expected_result.sort_values(by=expected_result.columns.tolist()).reset_index(drop=True)
    
    # Compare only specified columns (or all if None)
    cols = problem.get("compare_columns")
    if cols is None:
        cols = student_result.columns.tolist()
    
    missing_cols = [c for c in cols if c not in student_result.columns]
    if missing_cols:
        ai_hint = generate_ai_hint(student_query, problem, f"Missing columns. Expected {cols}, got {list(student_result.columns)}")
        return False, f"**Column mismatch:** Your query returned columns {list(student_result.columns)} but expected {cols}. Missing: {missing_cols}\n\n{ai_hint}"
    
    if student_result[cols].equals(expected_result[cols]):
        return True, "✅ Correct! Great work."
    else:
        ai_hint = generate_ai_hint(student_query, problem, "Query returned wrong results")
        return False, f"**Wrong result.** Your output doesn't match the expected.\n\n{ai_hint}"