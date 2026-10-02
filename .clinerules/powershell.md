# Windows PowerShell Execution Rules

## Environment

This workspace runs exclusively on Windows.

The integrated terminal is PowerShell 7 running inside Visual Studio Code.

Assume every terminal command will be pasted directly into a PowerShell prompt.

Never assume Bash, WSL, Git Bash, Linux, macOS, CMD, or any POSIX shell unless the user explicitly requests it.

---

# CRITICAL TERMINAL RULES

## NEVER wrap commands in quotes

Commands must be executable when pasted directly into PowerShell.

❌ WRONG

'python script.py'

'Remove-Item file.txt'

'git status'

'cmd /c "copy file1 file2"'

These are string literals in PowerShell and DO NOT execute.

✔ CORRECT

python script.py

Remove-Item file.txt

git status

---
# Python Environment

This project uses a Python virtual environment.

Assume the virtual environment is already activated unless explicitly told otherwise.

All Python commands must target the active virtual environment.

Always prefer:

python -m pip ...

instead of:

pip ...

Never install Python packages into the global Python installation.

If a virtual environment does not exist, create one first:

python -m venv .venv

Activate it (PowerShell):

.\.venv\Scripts\Activate.ps1

Note: this repository currently has no committed `.venv`; the active interpreter is
`C:\Python314\python.exe`. Create and activate a venv with the commands above if you
want isolation.

Only after the virtual environment is active may packages be installed.

---
## NEVER generate Bash escaping

Never generate any of the following:

'\''
$'...'
\' outside Python source code
export
source
chmod
./script.sh
bash -c
sh -c
rm -rf
cp
mv
cat >
touch
ls -la
pwd
which
&&
||

These are Bash syntax.

---

## PowerShell command chaining

Use one command per execution whenever possible.

If multiple commands are necessary, separate them with semicolons:

Command1;
Command2;
Command3

Do NOT use && or ||.

---

# Python Execution Rules

## Prefer temporary scripts over python -c

If Python code:

- is longer than one line
- contains quotes
- contains regular expressions
- contains Windows paths
- edits files
- contains multiline strings
- imports modules
- performs more than one operation

DO NOT use:

python -c "..."

Instead:

1. Create a temporary Python file.
2. Execute it.
3. Delete it afterwards.

This is the preferred workflow.

---

## Simple python -c usage

Only use python -c for extremely small commands like:

python -c "print('hello')"

Anything larger should become a temporary script.

---

## Windows Paths

Always use raw strings inside Python.

Correct:

r"C:\Users\name\file.txt"

Never use Bash escaping.

Never generate:

r'\''C:\Users...'\''

---

# File Operations

Prefer PowerShell cmdlets.

Delete

Remove-Item -Force

Delete recursively

Remove-Item -Recurse -Force

Copy

Copy-Item

Move

Move-Item

Rename

Rename-Item

Exists

Test-Path

Create directory

New-Item -ItemType Directory

Read

Get-Content

Write

Set-Content

Append

Add-Content

Never use:

rm
cp
mv
touch
cat
echo > file

unless explicitly requested.

---

# Git

Use normal git commands.

Examples

git status

git diff

git add .

git commit

Do not wrap git commands in quotes.

---

# Command Validation

Before executing ANY terminal command verify ALL of the following:

✓ It is valid PowerShell syntax.

✓ It is NOT wrapped in quotes.

✓ It contains NO Bash escaping.

✓ It contains NO Bash operators.

✓ It will execute correctly if pasted directly into PowerShell.

If any check fails, rewrite the command before executing.

---

# Editing Files

Prefer the built-in editing tools over shell commands.

If a shell command would be required to edit a file, use the file editing tool instead.

Do not use PowerShell to rewrite entire files unless explicitly required.

---

# Search

Prefer the built-in search tools.

Avoid grep.

Avoid find.

Avoid sed.

Avoid awk.

Use PowerShell only when necessary.

---

# Terminal Behavior

Never execute commands simply to test syntax.

Think first.

Generate the correct command once.

Execute it once.

Avoid repeated trial-and-error.

---

# Recovery

If a terminal command fails:

1. Read the exact error.
2. Determine the root cause.
3. Fix the command.
4. Retry only once.

Do not repeatedly execute similar broken commands.

---

# Safety

Never delete files unless required.

Never overwrite files unless required.

Before destructive operations:

- verify the path
- verify the filename
- verify the intention

---

# Absolute Rule

Every terminal command must be something that a Windows developer can copy directly into a PowerShell terminal and execute successfully without modifying it.

If there is any uncertainty between Bash syntax and PowerShell syntax, ALWAYS choose PowerShell.