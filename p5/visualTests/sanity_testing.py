import os
import shutil
from subprocess import run, PIPE, TimeoutExpired
from contextlib import contextmanager

dirname = os.path.dirname(os.path.realpath(__file__))

renderers_2D = {
    "vispy":
        """
if __name__ == '__main__':
    run(renderer='vispy', mode='P2D')
        """,
#     "skia":
#         """
# if __name__ == '__main__':
#     run(renderer='skia', mode='P2D')
#         """
}

renderers_3D = {
    "vispy":
        """
if __name__ == '__main__':
    run(renderer='vispy', mode='P3D')
        """
}

@contextmanager
def setup_test_file(test_file_path, code_stub):
    test_file_name = os.path.basename(test_file_path)
    tmp_test_file_path = f'{dirname}/sanityTests/tmp_{test_file_name}'

    shutil.copy(test_file_path, tmp_test_file_path)
    with open(tmp_test_file_path, 'a') as f:
        f.write(code_stub)

    yield tmp_test_file_path
    os.remove(tmp_test_file_path)


test_names_2d = [f'{dirname}/sanityTests/2DSanityTests/{name}' for name in
                 os.listdir(os.path.join(dirname, 'sanityTests/2DSanityTests'))
                 if name not in ['__init__.py', '__pycache__']]

test_names_3d = [f'{dirname}/sanityTests/3DSanityTests/{name}' for name in
                 os.listdir(os.path.join(dirname, 'sanityTests/3DSanityTests'))
                 if name not in ['__init__.py', '__pycache__']]


def run_test(renderer, code_stub, test_names):
    for test_file_path in test_names:
        print(f'Running {test_file_path} for renderer {renderer}')

        exception = None
        # create a temporary test file for current selected renderer
        with setup_test_file(test_file_path, code_stub) as tmp_test_file_path:
            try:
                # Run each test for 2s then raise a timeout
                process = run(['python', tmp_test_file_path], stderr=PIPE, encoding='utf-8', timeout=2)
            except TimeoutExpired:
                pass
            else:
                # If any error was found raise an exception
                if process.stderr:
                    exception = process.stderr

        if exception:
            raise Exception(f'{process.stderr} in {test_file_path}')


print('============================= Running 2D tests =============================')
for renderer in renderers_2D:
    code_stub = renderers_2D[renderer]
    run_test(renderer, code_stub, test_names_2d)

print('============================= Running 3D tests =============================')
for renderer in renderers_3D:
    code_stub = renderers_3D[renderer]
    run_test(renderer, code_stub, test_names_3d)
