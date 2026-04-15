PROBLEMS = [
    {
        "id": 1,
        "title": "Find Engineers",
        "description": "Find the names of all employees in the Engineering department.",
        "expected_sql": "SELECT name FROM employees WHERE department = 'Engineering'",
        "compare_columns": ["name"],
        "order_matters": False,
        "skills": ["basic_where"]
    },
    {
        "id": 2,
        "title": "High Salary",
        "description": "Find the names of employees who earn more than 60000.",
        "expected_sql": "SELECT name FROM employees WHERE salary > 60000",
        "compare_columns": ["name"],
        "order_matters": False,
        "skills": ["comparison_operators"]
    },
    {
        "id": 3,
        "title": "Sales Department",
        "description": "Find all columns for employees in Sales.",
        "expected_sql": "SELECT * FROM employees WHERE department = 'Sales'",
        "compare_columns": None,  # compare all columns
        "order_matters": False,
        "skills": ["basic_where"]
    },
    {
        "id": 4,
        "title": "Average Salary per Department",
        "description": "Show each department name and the average salary of employees in that department.",
        "expected_sql": "SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department",
        "compare_columns": ["department", "avg_salary"],
        "order_matters": False,
        "skills": ["group_by_aggregate"]
    },
    {
        "id": 5,
        "title": "Employees with NULL Manager",
        "description": "Find the names of employees who have no manager (manager_id is NULL).",
        "expected_sql": "SELECT name FROM employees WHERE manager_id IS NULL",
        "compare_columns": ["name"],
        "order_matters": False,
        "skills": ["null_handling"]
    }
]

def get_problem(problem_id):
    return next((p for p in PROBLEMS if p["id"] == problem_id), None)

def get_all_problems():
    return PROBLEMS