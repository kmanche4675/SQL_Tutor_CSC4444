import re

# Read the file
with open('c:\\Users\\jedir\\OneDrive\\Documents\\GitHub\\SQL_Tutor_CSC4444\\student_model.py', 'r') as f:
    content = f.read()

# Fix the load_model indentation
# Remove the wrongly placed line
content = re.sub(r'(\n        model\[skill\]\["observation_count"\] = 0)', '', content)

# Add it inside the for loop
content = re.sub(r'(model\[skill\] = PARAMS\[skill\]\.copy\(\))', r'\1\n            model[skill]["observation_count"] = 0', content)

# Write back
with open('c:\\Users\\jedir\\OneDrive\\Documents\\GitHub\\SQL_Tutor_CSC4444\\student_model.py', 'w') as f:
    f.write(content)

print('File fixed successfully')
