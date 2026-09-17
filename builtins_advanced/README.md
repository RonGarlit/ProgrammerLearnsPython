# 🚀 Advanced Built-ins — Design Patterns & Stdlib Power Tools

A single-file, interactive Python lesson that teaches the **advanced, design-
oriented features** of Python. This is the capstone of the built-ins series,
building directly on the `builtins_intermediate` folder. Each section is its
own function, so you can study it in isolation and repeat it as many times as
you like.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

> ✅ **Prerequisites:** Complete **`builtins_basics`** and
> **`builtins_intermediate`** first.

## What you'll learn

| #   | Concept               | What it shows                                          |
| --- | --------------------- | ------------------------------------------------------ |
| 0   | Clean up              | Removes the generated file so you can start fresh      |
| 1   | OOP: classes          | `class`, `__init__`, attributes, methods, `@dataclass` |
| 2   | Inheritance & dunders | Subclassing, polymorphism, `__str__`, `__eq__`         |
| 3   | Decorators            | Function decorators, `@property`, `@staticmethod`      |
| 4   | Context managers      | Custom `with` via `__enter__`/`__exit__`               |
| 5   | `itertools` module    | `chain`, `product`, `count`, `groupby`                 |
| 6   | `functools` module    | `reduce`, `lru_cache`, `partial`                       |
| 7   | Type hints (`typing`) | `Optional`, `Union`, `Callable`, annotations           |
| 8   | Deep error handling   | Custom exceptions, `try/except/else/finally`           |
| 9   | Mini task             | Inventory system — class + exception + type hints      |

> 💡 **Key idea:** Advanced Python is about **design**. You learn to bundle
> data with behavior (classes), reuse and customize (inheritance), wrap
> behavior (decorators, context managers), and document your code's contract
> (type hints).

---

## ✅ Prerequisites

- **Python 3.11 or newer** (matches `requires-python` in `pyproject.toml`).
- **VS Code** with the **Python extension** (by Microsoft) installed.

Check your Python version:

```powershell
uv run python --version
```

> 💡 **Note:** This lesson uses only the Python standard library — nothing to
> install. Run it with `uv run` so it uses the project's virtual environment.
> Type hints use the built-in `typing` module.

---

## ▶️ How to run the program

### Option A — Run from the terminal

1. Open a terminal in this folder.
2. Run the script:

   ```powershell
   uv run builtins_advanced.py
   ```

3. You'll see a menu. Type a number `0`–`9` to run a section, or `q` to quit.

> 💡 **Tip:** The script resolves all file paths relative to its own folder, so
> it also works from the project root:
>
> ```powershell
> uv run builtins_advanced/builtins_advanced.py
> ```

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `builtins_advanced.py`.
3. Click the **Run ▶** button in the top-right corner of the editor
   (or press `Ctrl+F5`).
4. The program runs in the **Terminal** panel. Interact with it there.

> 💡 **Tip:** Because the program reads input with `input()`, always run it in
> the **Terminal** panel — not the "Output" panel, which can't accept typed input.

---

## 🗂️ What the program creates

This lesson is **predominantly in-memory** — most sections build objects and
compute results without writing files. The only output is one small text file:

| Section | File created       | Purpose                                  |
| ------- | ------------------ | ---------------------------------------- |
| 0       | (deletes files)    | Removes `managed_file.txt`               |
| 4       | `managed_file.txt` | Demo of a context manager writing a file |

> `managed_file.txt` is created automatically by Section 4 and ignored by git.

---

## 🐞 Debugging with VS Code (step-by-step, for beginners)

Debugging lets you **pause** the program at any line, **inspect** the values of
variables, and **step through** the code one line at a time.

### Step 1 — Set a breakpoint

1. Open `builtins_advanced.py`.
2. Click in the **gutter** (the narrow column to the left of the line numbers)
   next to a line of code. A **red dot** appears.

   For example, click next to the `speak()` override inside
   `section_inheritance()`. Stepping through shows how `Dog.speak` replaces
   `Pet.speak`.

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

While paused, look at the **VARIABLES** panel for **Locals** (like the `buddy`
object) and **Globals**.

In the **DEBUG CONSOLE**, type expressions to evaluate them right now, e.g.
after Section 2:

```python
buddy.speak()
```

### Step 5 — Walk through the tutorial

Suggested session: set a breakpoint at the top of `main()`, press `F5`, then
type `2` to run the inheritance section. Step Into `section_inheritance()` and
watch how `Dog.speak()` overrides `Pet.speak()`.

---

## 🧠 Common gotchas

- **`TypeError: object() takes no parameters`?** You defined `__init__`
  incorrectly (usually a typo — note the double underscores on both sides).
- **`__str__` vs `__repr__`?** `__str__` is for humans (`print`); `__repr__` is
  the "official" representation for debugging. This lesson uses `__str__`.
- **Decorator returns the wrong thing?** A decorator's `wrapper` must `return`
  the function's result, otherwise you get `None`.
- **`with` block not closing?** Make sure your context manager's `__exit__`
  returns and doesn't raise. Returning `True` suppresses exceptions
  (usually not what you want).
- **`lru_cache` growing?** `maxsize=None` caches everything; set a number for
  big/unique inputs.
- **Type hints not catching bugs?** They're documentation + static-analysis
  tools (Pylance). They don't enforce at runtime — consider adding
  assertions or `pydantic` later.
- **Breakpoint not hit?** Start with **Run ▸ Start Debugging** (`F5`), not
  `Ctrl+F5`.

---

## 🧭 Project structure

```
builtins_advanced/            (this folder)
├── builtins_advanced.py      # the tutorial program
├── managed_file.txt          # generated by Section 4
├── Project_Objective.md      # design notes & concept breakdown
└── README.md                 # this file
```

---

## 🚀 Where to go next

The built-ins series (basics → intermediate → advanced) is now complete. To
keep growing:

- **Testing** — add `pytest` to test the classes you created.
- **Packaging** — learn to structure multi-file projects with `uv pip install -e .`.
- **Standard-library deep dives** — explore `asyncio`, `threading`, `sqlite3`,
  and `http` for real applications.
- Or jump into the **CSV / pandas** folders to apply Python to data analysis.
