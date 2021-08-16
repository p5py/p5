import subprocess, os, sys
from subprocess import run, PIPE
import sys

e = SystemExit()
dirname = os.path.dirname(__file__)
test_names = [f'{dirname}/sanityTests/2DSanityTests/{name}' for name in
              os.listdir(os.path.join(dirname, 'sanityTests/2DSanityTests'))
              if name not in ['__init__.py', '__pycache__']]

for name in test_names:
    print('Running', name)
    try:
        process = run(['python', name], stderr=PIPE, encoding='utf-8', timeout=2)
    except subprocess.TimeoutExpired:
        pass
    else:
        if process.stderr:
            raise Exception(f'{process.stderr} in {name}')
