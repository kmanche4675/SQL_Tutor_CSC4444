import re

# Read the file
with open('c:\\Users\\jedir\\OneDrive\\Documents\\GitHub\\SQL_Tutor_CSC4444\\student_model.py', 'r') as f:
    content = f.read()

# Add import math if not present
if 'import math' not in content:
    content = content.replace('import os', 'import os\nimport math')

# Add the functions if not present
functions = '''
def calculate_entropy(p):
    if p == 0 or p == 1:
        return 0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

def calculate_confidence(count):
    return 1 - math.exp(-count / 10.0)
'''

if 'def calculate_entropy' not in content:
    # Add after PARAMS
    content = re.sub(r'(PARAMS = \{[^}]*\})', r'\1\n' + functions, content, flags=re.DOTALL)

# Modify load_model to add observation_count
content = re.sub(r'(model\[skill\] = PARAMS\[skill\]\.copy\(\))', r'\1\n        model[skill]["observation_count"] = 0', content)

# Modify update_knowledge to add the lines
content = re.sub(r'(model\[skill\]\["p_mastered"\] = min\(1\.0, new_p\))', r'\1\n        model[skill]["observation_count"] += 1\n        model[skill]["entropy"] = calculate_entropy(model[skill]["p_mastered"])\n        model[skill]["confidence"] = calculate_confidence(model[skill]["observation_count"])', content)

# Write back
with open('c:\\Users\\jedir\\OneDrive\\Documents\\GitHub\\SQL_Tutor_CSC4444\\student_model.py', 'w') as f:
    f.write(content)

print('File edited successfully')
