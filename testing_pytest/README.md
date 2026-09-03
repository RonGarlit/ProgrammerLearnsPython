# 🧪 Testing with pytest — Write Automated Tests for Your Python

A single-file, interactive Python lesson that teaches **how to write automated
tests** for the pure-Python code you already know how to write. This is the
**fourth step** in the path, building directly on the `builtins_advanced`
folder — and it is the first lesson that introduces a **test framework**
(`pytest`) rather than just running code.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

> ✅ **Prerequisites:** Complete **`builtins_basics`**, **`builtins_intermediate`**,
> and **`builtins_advanced`** first. This lesson assumes you can write
> functions, classes, and custom exceptions.

## What you'll learn

| #   | Concept                     | What it shows                                      |
| --- | --------------------------- | -------------------------------------------------- |
| 0   | Clean up                    | Removes the pytest cache folders                   |
| 1   | What is testing & why       | `assert`, catching bugs early, regressions         |
| 2   | pytest basics               | `test_*` files/functions, running `pytest`         |
| 3   | Fixtures                    | `@pytest.fixture` — shared setup & teardown        |
| 4   | Parametrization             | `@pytest.mark.parametrize` — one test, many inputs |
| 5   | Testing functions & classes | Testing a `BankAccount` class                      |
| 6   | Testing exceptions          | `pytest.raises` for error paths                    |
| 7   | Markers & skipping          | `skip`, `skipif`, `xfail`, custom markers          |
| 8   | Mini task                   | Write a full test suite for the `Inventory` class  |

> 💡 **Key idea:** To test code, it must be **importable**. The classes you
> test here (`BankAccount`, `Account`, `Inventory`) are defined at **module
> level** in `testing_pytest.py` — they mirror the ones you built inside the
> section functions of `builtins_advanced`, but now they can be imported by
> the `test_*.py` files.

---

## ✅ Prerequisites

- **Python 3.11 or newer** (matches `requires-python` in `pyproject.toml`).
- **VS Code** with the **Python extension** (by Microsoft) installed.
- **pytest** installed. It is already listed in the `dev` dependency group of
  `pyproject.toml`. If you use `uv`, it is available via:

  ```powershell
  uv run pytest --version
  ```

  Or install it directly:

  ```powershell
  pip install pytest
  ```

> 💡 **Note:** This lesson uses only the Python **standard library** plus
> **pytest** — no NumPy, no pandas. The code under test is pure Python.

---

## ▶️ How to run the program

### Option A — Run from the terminal

1. Open a terminal in this folder.
2. Run the script:

   ```powershell
   python testing_pytest.py
   ```

3. You'll see a menu. Type a number `0`–`8` to run a section, or `q` to quit.

> 💡 **Tip:** The script resolves all file paths relative to its own folder, so
> it also works from the project root:
>
> ```powershell
> python testing_pytest/testing_pytest.py
> ```

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `testing_pytest.py`.
3. Click the **Run ▶** button in the top-right corner of the editor
   (or press `Ctrl+F5`).
4. The program runs in the **Terminal** panel. Interact with it there.

> 💡 **Tip:** Because the program reads input with `input()`, always run it in
> the **Terminal** panel — not the "Output" panel, which can't accept typed input.

---

## ▶️ How to run the tests

The real payoff of this lesson is running the test files with pytest. From
this folder:

```powershell
pytest                 # run every test_*.py file
pytest -v              # verbose: show each test name
pytest test_bank_account.py   # run one file
pytest -k deposit      # run tests whose name contains "deposit"
pytest -m "not slow"   # skip tests marked "slow"
```

You should see a green summary like `N passed`. If a test fails, pytest shows
you the exact assertion and the values involved.

---

## 🗂️ What the program creates

Running the lesson itself is **predominantly in-memory** — the sections print
explanations and code samples. Running **pytest** creates cache folders:

| Command  | Folder created   | Purpose                                  |
| -------- | ---------------- | ---------------------------------------- |
| `pytest` | `.pytest_cache/` | pytest's internal cache                  |
| `pytest` | `__pycache__/`   | Python bytecode cache for imported files |

> Menu option **0** removes these cache folders so you can start fresh. The
> `test_*.py` files are **kept** — they are the point of the lesson.

---

## 🐞 Debugging with VS Code (step-by-step, for beginners)

Debugging lets you **pause** the program at any line, **inspect** the values of
variables, and **step through** the code one line at a time.

### Step 1 — Set a breakpoint

1. Open `testing_pytest.py`.
2. Click in the **gutter** (the narrow column to the left of the line numbers)
   next to a line of code. A **red dot** appears.

   For example, click next to `self.balance += amount` inside the
   `BankAccount.deposit` method. Stepping through shows how the balance
   changes.

### Step 2: Start the debugger

1. Press **`F5`** (or go to **Run ▸ Start Debugging**).
2. The program starts and **pauses** when it hits your breakpoint.

> 💡 **Which config to pick?** The project ships **two** debug configs in
> `.vscode/launch.json`:
> - **"Python: Current File"** — runs whatever `.py` file is open. Use this to
>   debug the menu program (`testing_pytest.py`).
> - **"Python: Debug pytest (current file)"** — runs pytest on whatever test
>   file is open. Use this to debug the `test_*.py` files (see the section
>   below).
>
> Select the one you want from the **dropdown** in the **Run and Debug** view
> (`Ctrl+Shift+D`) before pressing `F5`.

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
    },
    {
      "name": "Python: Debug pytest (current file)",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": ["${file}", "-v"],
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

While paused, look at the **VARIABLES** panel for **Locals** (like the `acct`
object) and **Globals**.

In the **DEBUG CONSOLE**, type expressions to evaluate them right now, e.g.
after Section 5:

```python
acct.report()
```

### Step 5 — Walk through the tutorial

Suggested session: set a breakpoint at the top of `main()`, press `F5`, then
type `5` to run the "Testing functions & classes" section. Step Into
`section_testing_classes()` and watch how each test builds its own account.

---

## 🐞 Debugging the individual test files (e.g. `test_fixtures.py`)

The section above debugs the **menu program** (`testing_pytest.py`). But the
real point of this lesson is the **`test_*.py` files** — and you can (and
should) debug those too. This is where you'll spend most of your time once
you start writing real tests.

### Why debug a test file?

When a test fails, the failure message tells you *what* went wrong, but not
always *why*. Stepping through the test with the debugger lets you:

- **Watch the fixture run** — see the `account` fixture create a fresh
  `BankAccount` before each test, and confirm each test gets its own instance.
- **Inspect the object state** — pause inside `test_deposit` and look at
  `account.balance` in the **VARIABLES** panel *before* and *after* the
  `deposit(50)` call.
- **Trace the call into the code under test** — Step Into `account.deposit()`
  to watch `self.balance += amount` execute inside `testing_pytest.py`.
- **Confirm the setup/teardown order** — see exactly when the fixture is
  created and when it's torn down.

### How to debug a test file

The key difference: instead of running the `.py` file directly, you run
**pytest** under the debugger. The project already ships a ready-made config
in `.vscode/launch.json` called **"Python: Debug pytest (current file)"**:

```json
{
  "name": "Python: Debug pytest (current file)",
  "type": "debugpy",
  "request": "launch",
  "module": "pytest",
  "args": ["${file}", "-v"],
  "console": "integratedTerminal"
}
```

> 💡 **How it works:** `"module": "pytest"` tells the debugger to launch pytest
> itself (not a `.py` file). The magic is `"${file}"` in `args` — it resolves
> to **whatever test file you currently have open in the editor**. That means
> this **one** config works on *any* test file: open `test_fixtures.py` and it
> debugs `test_fixtures.py`; open `test_bank_account.py` and it debugs that.
> You never have to edit `args`.

Then:

1. Open the test file you want to debug (e.g. `test_fixtures.py`).
2. Set a **breakpoint** inside a test — for example, on the line
   `account.deposit(50)` inside `test_deposit`.
3. Open the **Run and Debug** view (`Ctrl+Shift+D`).
4. In the **dropdown** at the top of that view, select
   **"Python: Debug pytest (current file)"**.
5. Press **`F5`** (or click the green **Start Debugging** ▶).
6. pytest starts, runs the tests in the open file, and **pauses** at your
   breakpoint.
7. Use **Step Over** (`F10`) / **Step Into** (`F11`) to walk through the test.
   Step Into `account.deposit(50)` to jump into the method in
   `testing_pytest.py` and watch `self.balance` change.

> 💡 **Tip:** To debug a *single* test instead of the whole file, add `-k` to
> the args, e.g. `"args": ["${file}", "-k", "test_deposit", "-v"]`. This runs
> only `test_deposit`, so you don't step through every test.

### A suggested debugging session for `test_fixtures.py`

1. Set a breakpoint on the `@pytest.fixture` line and on `account.deposit(50)`.
2. Press `F5` with **"Python: Debug pytest (current file)"** selected.
3. The debugger pauses at the fixture first — Step Over to see the
   `BankAccount("Ada", 100)` being created and returned.
4. Continue (`F5`) to the breakpoint inside `test_deposit`. In the **VARIABLES**
   panel, expand `account` and note `balance == 100`.
5. Step Into `account.deposit(50)` and watch `self.balance` become `150`.
6. Step Out (`Shift+F11`) back to the test, then Continue to finish.

This is the same workflow you'll use to debug *any* failing test in your own
projects — it's a core skill, not just a lesson exercise.

---

## 🧠 Common gotchas

- **`ModuleNotFoundError: No module named 'testing_pytest'`?** Run pytest from
  **inside** the `testing_pytest/` folder (or the project root), so the module
  is on the path.
- **Test not discovered?** Make sure the file is named `test_*.py` and the
  functions are named `test_*`. pytest only collects those by default.
- **`assert` does nothing?** `assert` only raises when the condition is
  **False**. If your test passes when it shouldn't, check the condition — a
  common mistake is `assert is_even(4)` (truthy) instead of
  `assert is_even(4) is True`.
- **Fixture not found?** The fixture must be defined in the same file (or a
  `conftest.py`) and the test must accept it as an **argument**.
- **`pytest.raises` failing?** It fails if the exception is **not** raised.
  Make sure the code path you expect to raise actually runs.
- **`xfail` still shows as failed?** Use `strict=False` (the default) so a
  passing xfail test is reported as `xpassed` rather than an error.
- **Breakpoint not hit?** Start with **Run ▸ Start Debugging** (`F5`), not
  `Ctrl+F5`.

---

## 🧭 Project structure

```
testing_pytest/               (this folder)
├── testing_pytest.py         # the tutorial program + code under test
├── test_math_helpers.py      # Section 2: pytest basics
├── test_fixtures.py          # Section 3: fixtures
├── test_parametrize.py       # Section 4: parametrization
├── test_bank_account.py      # Section 5: testing a class
├── test_exceptions.py        # Section 6: pytest.raises
├── test_markers.py           # Section 7: markers & skipping
├── test_inventory.py         # Section 8: mini task (complete it!)
├── Project_Objective.md      # design notes & concept breakdown
└── README.md                 # this file
```

---

## 🚀 Where to go next

You now know how to write automated tests for pure Python. To keep growing:

- **Test the CSV lessons** — write pytest tests for the `csv_basics_built_in`
  helpers once you reach them.
- **Test data code** — after the pandas lessons, use `pytest` + `tmp_path`
  fixtures to test functions that read/write CSV files.
- **Test-driven development (TDD)** — write the test _first_, watch it fail,
  then write the code to make it pass.
- Or continue the path with the **CSV / pandas** folders to apply Python to
  data analysis.
