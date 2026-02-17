import os

dirs = [
    'app/api/v1/endpoints',
    'app/core',
    'app/db',
    'app/models',
    'app/schemas',
    'app/services',
    'app/utils'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    init_file = os.path.join(d, '__init__.py')
    with open(init_file, 'a'):
        pass

# Top level inits
top_level_inits = ['app', 'app/api', 'app/api/v1']
for d in top_level_inits:
    os.makedirs(d, exist_ok=True)
    init_file = os.path.join(d, '__init__.py')
    with open(init_file, 'a'):
        pass

print("Directories created successfully")
