# PYRA Setup Tool

You may have to **enable `*.ps1` scripts** in your security context - Powershell command (https://stackoverflow.com/a/49112322/8255842):

```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

<br/>

**Install Python3.10** from https:/python.org/. Make sure that the system interpreter (used when calling `python`) points to the Python 3.10 installation: Search “Edit the system environment variables” -> Environment Variables -> System variables -> Edit PATH for new Python 3.10 and the repective `pip` in "python/scripts".

<br/>

You also need to install Poetry (https://python-poetry.org/) and the GitHub CLI (https://cli.github.com/).
