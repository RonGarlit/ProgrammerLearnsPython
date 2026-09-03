# 🐍 Programmer Learns Python — Tutorial App

A single-file, interactive Python lesson that teaches the core building blocks of the
language one concept at a time. Each section is its own function, so you can study it
in isolation and repeat it as many times as you like.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

## What you'll learn

| #   | Concept                  | What it shows                                              |
| --- | ------------------------ | ---------------------------------------------------------- |
| 1   | Variables & Data Types   | `int`, `float`, `str`, `bool`, `type()`                    |
| 2   | Input & Type Conversion  | `input()` + `int()`                                        |
| 3   | Conditionals             | `if` / `elif` / `else`                                     |
| 4   | Loops                    | `for` + `range()`, `while`, `enumerate()`, `zip()`         |
| 5   | Lists & Dictionaries     | `append`, indexing, `len()`, `.items()`                    |
| 6   | Functions                | `def`, parameters, defaults, `return`                      |
| 7   | Error Handling           | `try` / `except`                                           |
| 8   | Sets & Tuples            | unique items, `add()`, `in`, union/intersection, unpacking |
| 9   | String Methods & Slicing | `.strip()`, `.split()`, `.join()`, `[start:stop:step]`     |

> 💡 **Bonus:** Section 5 also demonstrates **list comprehensions** — building and
> filtering a list in a single line. Section 2 uses a reusable `ask_int()` helper
> that combines a `while` loop with `try`/`except` to safely read numbers.

---

## ✅ Prerequisites

- **Python 3.11 or newer** (matches `requires-python` in `pyproject.toml`).
- **VS Code** with the **Python extension** (by Microsoft) installed.
  - The extension gives you IntelliSense, the debugger, and the Run button.

Check your Python version:

```powershell
python --version
```

---

## ▶️ How to run the program

### Option A — Run from the terminal

1. Open a terminal in this folder.
2. Run the script:

   ```powershell
   python builtins_essentials.py
   ```

3. You'll see a menu. Type a number `1`–`8` to run a section, or `q` to quit.

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `builtins_essentials.py`.
3. Click the **Run ▶** button in the top-right corner of the editor
   (or press `Ctrl+F5`).
4. The program runs in the **Terminal** panel. Interact with it there.

> 💡 **Tip:** Because the program reads input with `input()`, always run it in the
> **Terminal** panel — not the "Output" panel, which can't accept typed input.

---

## 🐞 Debugging with VS Code (step-by-step, for beginners)

Debugging lets you **pause** the program at any line, **inspect** the values of
variables, and **step through** the code one line at a time. It's the single best
way to understand _what your code is actually doing_.

### Step 1 — Set a breakpoint

A **breakpoint** is a marker that tells the debugger: _"pause here so I can look
around."_

1. Open `builtins_essentials.py`.
2. Click in the **gutter** (the narrow column to the left of the line numbers)
   next to a line of code. A **red dot** appears — that's your breakpoint.

   For example, click next to line `print(player_name, "has score", player_score)`
   inside `section_variables()`.

   - Click the red dot again to remove it.
   - You can set as many breakpoints as you want.

### Step 2: Start the debugger

1. Press **`F5`** (or go to **Run ▸ Start Debugging**).
2. The program starts, runs normally, and **pauses** when it hits your breakpoint.

> 💡 **Tip:** This project already includes a `.vscode/launch.json` file with a
> **"Python: Current File"** configuration, so pressing `F5` starts immediately
> with no setup. If you ever need to recreate it, here's how:

#### What the `.vscode/launch.json` file is

The `.vscode` folder holds VS Code workspace settings. `launch.json` inside it
defines **debug configurations** — instructions for how the debugger should start
your program. It's optional for a simple script, but it lets you control things
like which file to run, which interpreter to use, and where the program's input
and output go.

#### How to create it (if it's missing)

1. In VS Code, open the **Run and Debug** view (the ▶ icon in the left sidebar).
2. Click **create a launch.json file**.
3. Choose **Python** from the list.
4. VS Code generates a `.vscode/launch.json`. Replace its contents with:

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

Here's what each setting means:

| Setting   | Value                    | Why                                                                   |
| --------- | ------------------------ | --------------------------------------------------------------------- |
| `name`    | `"Python: Current File"` | The label shown in the debugger dropdown.                             |
| `type`    | `"debugpy"`              | The modern Python debugger engine.                                    |
| `request` | `"launch"`               | Start a new process (vs. `"attach"` to an existing one).              |
| `program` | `"${file}"`              | Debug whatever file is currently open in the editor.                  |
| `console` | `"integratedTerminal"`   | **Important for this app** — runs in the terminal so `input()` works. |

> 💡 **Tip:** The debugger pauses at the breakpoint _before_ running that line.
> The highlighted (yellow) line is the **next** line that will execute.

### Step 3: Use the debugging toolbar

When the program pauses, a small toolbar appears at the top of the screen:

| Button        | Shortcut        | What it does                                                               |
| ------------- | --------------- | -------------------------------------------------------------------------- |
| **Continue**  | `F5`            | Run until the next breakpoint (or the end).                                |
| **Step Over** | `F10`           | Run the current line, then pause on the next. Skips _into_ function calls. |
| **Step Into** | `F11`           | Run the current line; if it calls a function, jump _inside_ that function. |
| **Step Out**  | `Shift+F11`     | Finish the current function and pause back at the caller.                  |
| **Restart**   | `Ctrl+Shift+F5` | Start the debug session over.                                              |
| **Stop**      | `Shift+F5`      | End the debug session.                                                     |

### Step 4: Inspect variables

While paused, look at the **VARIABLES** panel (usually on the left, or in the
**Run and Debug** view):

- **Locals** — variables in the current function.
- **Globals** — variables defined at the top level of the module.

You can also **hover** your mouse over any variable in the editor to see its
current value in a tooltip.

### Step 5 — Use the Debug Console

The **DEBUG CONSOLE** panel lets you type Python expressions and evaluate them
_right now_, using the current state of the program.

For example, while paused inside `section_variables()`, type:

```python
player_score * 2
```

and press Enter — it returns `20` without changing the program.

### Step 6 — Walk through the tutorial

Here's a suggested debugging session to learn the flow:

1. Set a breakpoint on the first line of `main()`.
2. Press `F5` to start.
3. Use **Step Over** (`F10`) to watch the menu print.
4. When the program asks for input, type `1` in the terminal and press Enter.
5. The debugger now pauses inside `section_variables()`.
6. Use **Step Over** to walk each line and watch `player_score`, `player_name`,
   and `is_playing` appear in the **VARIABLES** panel.
7. Try **Step Into** (`F11`) on a line that calls a function to see how the
   debugger follows the call into the function body.

> 💡 **Tip:** When the program is waiting for `input()`, the debugger is _not_
> paused — it's running normally. Type your answer in the terminal, then the
> debugger will pause again at the next breakpoint.

---

## 🧠 Common debugging gotchas

- **Breakpoint not hit?** Make sure the file you're debugging is the one with the
  breakpoint, and that you started with **Run ▸ Start Debugging** (`F5`), not just
  **Run** (`Ctrl+F5`). `Ctrl+F5` runs _without_ debugging and ignores breakpoints.
- **Can't type input?** The program reads from the **Terminal** panel. If you're
  looking at the Output panel, switch to Terminal.
- **"No module named..."?** This project uses only the Python standard library —
  no third-party packages — so there's nothing to install.

---

## 🧭 Project structure

```
builtins_basics/
├── builtins_essentials.py  # the tutorial program
├── Project_Objective.md   # design notes & concept breakdown
├── README.md              # this file
└── .vscode/
    └── launch.json        # debug configuration (see Step 2)
```

---

## 🚀 Next steps

- Try adding a **Section 9** for `map` / `filter` or generator expressions.
- Split the sections into separate `.py` files and import them.
