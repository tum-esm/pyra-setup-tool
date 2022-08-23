# PYRA Setup Tool

## What does this tool do?

-   Download PYRA's code for specific versions
-   Download the respective UI and run the installer
-   Create a desktop shortcut to the pyra-directory
-   Create the `pyra-cli.bat` alias file
-   Migrate the config.json file from an old version

These steps could all be done manually. However, they require a lot of copying and editing of files which could lead to typos or other human errors. All temporary files (pyra-cli.bat, config.json, etc.) have to be rewritten.

When upgrading versions frequently, this can be very annoying. Hence this tool provides an opinionated way of upgrading to new PYRA versions in less than 30 seconds.

<br/>

## How to run this tool?

1. Do the manual installation steps below (only required once - when setting up the computer)
2. Download this tool from https://github.com/tum-esm/pyra-setup-tool
3. Use the tool by running `run.py` with Python 3.10

_The tool does not have any dependencies except for the standard Python 3.10 library._

<br/>

## Manual installation steps

You may have to **enable `*.ps1` scripts** in your security context - Powershell command (https://stackoverflow.com/a/49112322/8255842):

```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

<br/>

**Install Python3.10** from https:/python.org/. Make sure that the system interpreter (used when calling `python`) points to the Python 3.10 installation: Search “Edit the system environment variables” -> Environment Variables -> System variables -> Edit PATH for new Python 3.10 and the respective `pip` in "python/scripts".

<br/>

You also need to install **Poetry** (https://python-poetry.org/) and the GitHub CLI (https://cli.github.com/).

<br/>

## Email Account for error emails

_documentation coming soon_

With Gmail accounts, "Less Secure Apps" have been deactivated.
https://support.google.com/accounts/answer/6010255?hl=de&visit_id=637914296292859831-802637670&p=less-secure-apps&rd=1

Solution: Use "App passwords", which require 2FA
