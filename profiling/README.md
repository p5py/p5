### Profiling

The provided profiling script uses the built-in Python cProfile module. To start profiling, run `python main.py`. This will render each sample scene listed in `main.py` for 100 frames and write profiling information as .prof files. They can then be opened by programs such as snakeviz.

Because the existing Python harness is unstable due to possible global states not being cleaned up properly, a bash harness is in the works. As of now this harness does not output profiling information but merely runs each scene for 3 seconds. Can be useful for integration testing. Use `./main.sh` to run.
