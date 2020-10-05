=======================
VS Code Integration
=======================

Using VS Code as your code editor for p5py will be a great choice as of pylinter integration and a lot of autocomplete features!

Before you start using VS Code as your code editor for p5py. We recommend that you turn off some pylint settings, for that you would require a settings file. The setup is simple so do not panic!

=======================
Setup
=======================

1. Go into the directory in which keep all of your p5py projects.
2. In that directory create a folder called ``.vscode``
3. In the ``.vscode`` directory create a file called ``settings.json``
4. In that file copy and paste all of these json settings:

.. code:: 

    {
        "python.linting.pylintArgs": [
            "--disable", "E0102", 
            "--disable", "C0111",
            "--disable", "W0401",
            "--disable", "C0304",
            "--disable", "W0614",
            "--disable", "W0622"
        ]
    }

5. Save the file and you are ready to write some amazing projects in VS Code and p5py!!
