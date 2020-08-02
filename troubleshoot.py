import sys
import os

if "win" in str(sys.platform):
    vispy_amd = "vispy‑0.6.4‑cp39‑cp39‑win_amd64.whl"

    version = str(sys.version).split("(")[0].split(".")

    if "Intel" in str(sys.version):
        cp = str(version[0]) + str(version[1])

        command = f"pip install https://download.lfd.uci.edu/pythonlibs/w3jqiv8s/vispy-0.6.4-cp{cp}-cp{cp}-win32.whl"
        print(command)
        os.system(str(command))
        os.system("pip install numpy")
        os.system("pip install p5")

    else:
        command = f"pip install https://download.lfd.uci.edu/pythonlibs/w3jqiv8s/vispy-0.6.4-cp{cp}-cp{cp}-win_amd64.whl"

        print(command)
        os.system(str(command))
        os.system("pip install numpy")
        os.system("pip install p5")

else:
    os.system("pip install vispy")
    os.system("pip install numpy")
    os.system("pip install p5")