import subprocess
import os
from subprocess import run, PIPE

e = SystemExit()

dirname = os.path.dirname(__file__)
test_names_2d = [f'{dirname}/sanityTests/2DSanityTests/{name}' for name in
                 os.listdir(os.path.join(dirname, 'sanityTests/2DSanityTests'))
                 if name not in ['__init__.py', '__pycache__']]

test_names_3d = [f'{dirname}/sanityTests/3DSanityTests/{name}' for name in
                 os.listdir(os.path.join(dirname, 'sanityTests/3DSanityTests'))
                 if name not in ['__init__.py', '__pycache__']]

print('============================= Running 2D tests =============================')
for name in test_names_2d:
    print('Running', name)
    try:
        # Run each test for 2s then raise a timeout
        process = run(['python', name], stderr=PIPE, encoding='utf-8', timeout=2)
    except subprocess.TimeoutExpired:
        pass
    else:
        # If any error was found raise and exception
        if process.stderr:
            raise Exception(f'{process.stderr} in {name}')


print('============================= Running 3D tests =============================')
for name in test_names_3d:
    print('Running', name)
    try:
        # Run each test for 2s then raise a timeout
        process = run(['python', name], stderr=PIPE, encoding='utf-8', timeout=2)
    except subprocess.TimeoutExpired:
        pass
    else:
        # If any error was found raise and exception
        if process.stderr:
            raise Exception(f'{process.stderr} in {name}')
