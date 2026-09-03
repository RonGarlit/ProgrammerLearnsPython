# 🔧 Intermediate Built-ins — Practical Stdlib Tools

A single-file, interactive Python lesson that teaches the **practical Python
standard library** you reach for right after fundamentals. Building on the
`builtins_basics` folder, each section is its own function, so you can study it
in isolation and repeat it as many times as you like.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

> ✅ **Prerequisite:** Complete **`builtins_basics`** first. This lesson
> assumes you know variables, loops, and functions.

## What you'll learn

| #   | Concept                   | What it shows                                            |
| --- | ------------------------- | -------------------------------------------------------- |
| 0   | Clean up                  | Removes the generated text/JSON files to start fresh     |
| 1   | Text files with `pathlib` | `Path.read_text` / `write_text`, `exists()`, `stat()`    |
| 2   | The `json` module         | `json.dumps` / `loads`, reading and writing JSON files   |
| 3   | The `datetime` module     | `datetime.now()`, `strftime`, `timedelta`, date math     |
| 4   | The `collections` module  | `Counter`, `defaultdict`, `namedtuple`, `deque`          |
| 5   | Comprehensions            | List/dict/set comprehensions, with conditions            |
| 6   | Generators                | `yield`, generator expressions, laziness, memory savings |
| 7   | `*args` / `**kwargs`      | Flexible positional & keyword parameters, unpacking      |
| 8   | `lambda` + map/filter     | Anonymous functions; applying and filtering sequences    |
| 9   | Mini task                 | Read a JSON log, count with `Counter`, write a summary   |

> 💡 **Key idea:** Python's **standard library** is a treasure chest of
> built-in tools — no `pip install` needed. This lesson covers the modules and
> syntax you'll use every single day.

---

## ✅ Prerequisites

- **Python 3.11 or newer** (matches `requires-python` in `pyproject.toml`).
- **VS Code** with the **Python extension** (by Microsoft) installed.

Check your Python version:

```powershell
python --version
```

> 💡 **Note:** This lesson uses only the Python standard library — there is
> nothing to `pip install`.

---

## ▶️ How to run the program

### Option A — Run from the terminal

1. Open a terminal in this folder.
2. Run the script:

   ```powershell
   python builtins_intermediate.py
   ```

3. You'll see a menu. Type a number `0`–`9` to run a section, or `q` to quit.

> 💡 **Tip:** The script resolves all file paths relative to its own folder, so
> it also works from the project root:
>
> ```powershell
> python builtins_intermediate/builtins_intermediate.py
> ```

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `builtins_intermediate.py`.
3. Click the **Run ▶** button in the top-right corner of the editor
   (or press `Ctrl+F5`).
4. The program runs in the **Terminal** panel. Interact with it there.

> 💡 **Tip:** Because the program reads input with `input()`, always run it in
> the **Terminal** panel — not the "Output" panel, which can't accept typed input.

---

## 🗂️ What the program creates

Running the sections creates small text/JSON files **in the same folder**. These
are meant to be inspected — open them in VS Code to see the result:

| Section | File created       | Purpose                                              |
| ------- | ------------------ | ---------------------------------------------------- |
| 0       | (deletes files)    | Removes `copied_notes.txt`, `log_summary.json`       |
| 1       | `copied_notes.txt` | An uppercased copy of `notes.txt`                    |
| 9       | `log_summary.json` | A per-user summary of the event log, written as JSON |

> `notes.txt`, `settings.json`, and `log.json` are the **input** sample files
> and are never modified.

---

## 🐞 Debugging with VS Code (step-by-step, for beginners)

Debugging lets you **pause** the program at any line, **inspect** the values of
variables, and **step through** the code one line at a time.

### Step 1 — Set a breakpoint

1. Open `builtins_intermediate.py`.
2. Click in the **gutter** (the narrow column to the left of the line numbers)
   next to a line of code. A **red dot** appears.

   For example, click next to `counter.most_common(2)` inside
   `section_collections()`. Watching the `Counter` build is a great way to see
   how it tallies items.

### Step 2: Start the debugger

1. Press **`F5`** (or go to **Run ▸ Start Debugging**).
2. The program starts and **pauses** when it hits your breakpoint.

> 💡 **Tip:** If you don't have a `launch.json` yet, VS Code will prompt you to
> create one. Choose **Python** and the **"Python: Current File"** configuration
> with `console: "integratedTerminal"` so `input()` works.

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    }
  ]
}
```

### Step 3: Use the debugging toolbar

| Button        | Shortcut        | What it does                                                               |
| ------------- | --------------- | -------------------------------------------------------------------------- |
| **Continue**  | `F5`            | Run until the next breakpoint (or the end).                                |
| **Step Over** | `F10`           | Run the current line, then pause on the next. Skips _into_ function calls. |
| **Step Into** | `F11`           | Run the current line; if it calls a function, jump _inside_ that function. |
| **Step Out**  | `Shift+F11`     | Finish the current function and pause back at the caller.                  |
| **Restart**   | `Ctrl+Shift+F5` | Start the debug session over.                                              |
| **Stop**      | `Shift+F5`      | End the debug session.                                                     |

### Step 4: Inspect variables & use the Debug Console

While paused, look at the **VARIABLES** panel for **Locals** (like the
`counter` object) and **Globals**.

In the **DEBUG CONSOLE**, type expressions to evaluate them right now, e.g.
after Section 4:

```python
counter['apple']
```

### Step 5 — Walk through the tutorial

Suggested session: set a breakpoint at the top of `main()`, press `F5`, then
type `4` to run the collections section. Step Into `section_collections()` and
watch the `Counter` tally the words.

---

## 🧠 Common gotchas

- **`ModuleNotFoundError`?** This lesson uses only the standard library, so if
  one appears a module has been renamed in your Python version — check the
  docs linked in the code.
- **`pathlib` errors on Windows?** Use forward-slashes or `Path("folder/file")`.
  `pathlib` handles platform paths for you.
- **JSON load fails?** The JSON file has a syntax error (missing quote/comma).
  Use a JSON validator or open it in VS Code.
- **`deque` vs list?** `deque` is faster for appending/popping at **both ends**;
  use a list when you mostly index randomly.
- **Breakpoint not hit?** Make sure the file you're debugging is the one with
  the breakpoint, and start with **Run ▸ Start Debugging** (`F5`), not **Run**
  (`Ctrl+F5`).
- **Can't type input?** Run in the **Terminal** panel, not the Output panel.

---

## 🧭 Project structure

```
builtins_intermediate/            (this folder)
├── builtins_intermediate.py      # the tutorial program
├── notes.txt                     # sample text file (Section 1)
├── settings.json                 # sample JSON config (Section 2)
├── log.json                      # sample JSON event log (Section 9)
├── copied_notes.txt              # generated by Section 1
├── log_summary.json              # generated by Section 9
├── Project_Objective.md          # design notes & concept breakdown
└── README.md                     # this file
```

---

## 🚀 Progressing to the next steps

- Try adding a **Section 10** that parses the `date`/`time` fields in
  `log.json` using `datetime.strptime`.
- Experiment with `filter()` and a comprehension to build a custom report from
  `log.json`.
- When you're comfortable here, move on to the **`builtins_advanced`** folder,
  which introduces object-oriented programming, decorators, context managers,
  type hints, and deeper standard-library tools.
