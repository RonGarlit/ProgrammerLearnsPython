# 🗄️ SQL Server Advanced — Performance, Schema & Integration with `pyodbc`

An interactive, menu-driven Python lesson that teaches the **advanced** SQL
Server topics the intermediate folder deferred: **indexes, query tuning,
views, CTEs & window functions, bulk operations, dynamic SQL, transactions &
isolation, and pandas ↔ SQL Server integration** — all against the same small
store schema.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

> ✅ **Prerequisite:** Complete the **`py_sql_server_intermediate`** folder
> first. This lesson assumes you know how to connect with pyodbc, use `?`
> parameters, the `OUTPUT` clause, `autocommit=False` + `commit()`, and stored
> procedures.

## What you'll learn

| #  | Concept                  | What it shows                                                          |
| -- | ------------------------ | ---------------------------------------------------------------------- |
| 0  | Setup                    | Runs `create_pytestdb_advanced.sql` to build schema, seed, indexes, views, trigger |
| 1  | Indexes                  | `CREATE INDEX`, covering index, `SET STATISTICS TIME, IO ON` before/after |
| 2  | Query tuning             | Execution plans (`SET SHOWPLAN_ALL`), sargable predicates, avoiding `SELECT *` |
| 3  | Views                    | `CREATE VIEW`, `SELECT` through a view, updating through a view         |
| 4  | CTEs & window functions  | `WITH`, `ROW_NUMBER()`, `RANK()`, `LAG`/`LEAD`, `OVER(PARTITION BY)`    |
| 5  | Bulk operations          | `executemany()`, `fast_executemany=True`, `BULK INSERT` from a CSV      |
| 6  | Dynamic SQL              | `sp_executesql`, safe parameterization of dynamic queries               |
| 7  | Transactions & isolation | Isolation levels, savepoints, deadlock handling                         |
| 8  | pandas ↔ SQL Server      | `pd.read_sql()` and `to_sql()` via a SQLAlchemy engine                  |
| 9  | Mini task                | A combined workflow tying several sections together                     |

> 💡 **Key idea:** Once you can CRUD, the next questions are **"is it fast?"**
> (indexes, tuning), **"is it safe?"** (dynamic SQL, isolation), and **"does it
> talk to my data tools?"** (pandas). This lesson answers all three.

---

## ✅ Prerequisites

- **Python 3.11 or newer** (matches `requires-python` in `pyproject.toml`).
- **SQL Server** running locally (or a reachable server).
- **ODBC Driver 18 for SQL Server** installed on your machine.
- **pyodbc** and **SQLAlchemy** installed (both are already declared in
  `pyproject.toml`, so `uv sync` installs them):

  ```powershell
  uv sync
  ```

- **VS Code** with the **Python extension** (by Microsoft) installed.

Check your Python version and packages:

```powershell
uv run python --version
uv run python -c "import pyodbc; print(pyodbc.version)"
uv run python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

> If `uv sync` fails, try `uv add pyodbc sqlalchemy` to add them to the
> project.

---

## 🗄️ Step 0 — Create the database, schema, and objects

The lesson connects to a database named **`PyTestDb`** (the same one from the
basics and intermediate lessons). The `create_pytestdb_advanced.sql` script
creates the database if needed, then builds the store schema, seeds it, and
adds **indexes**, **views**, and a **trigger**. The script is **idempotent** —
you can re-run it any time to start fresh.

There are two ways to run it:

### Option A — Let the lesson do it (recommended)

Just run the program and choose **section 0**:

```powershell
uv run sql_server_advanced.py
```

Section 0 reads `create_pytestdb_advanced.sql`, strips the `GO` batch
separators (a sqlcmd/SSMS feature that isn't valid T-SQL), and executes it for
you.

### Option B — Run it yourself in SSMS / sqlcmd

```sql
-- In SSMS, open the file and press F5, or:
sqlcmd -S localhost -E -i create_pytestdb_advanced.sql
```

The script creates four tables plus supporting objects:

```
Customers ──< Orders ──< OrderItems >── Products
```

---

## ▶️ How to run the program

### Option A — Run from the terminal

1. Open a terminal in this folder.
2. Run the program:

   ```powershell
   uv run sql_server_advanced.py
   ```

3. You'll see a menu. Type a number `0`–`9` to run a section, `c` for
   cleanup, or `q` to quit.

> 💡 **Tip:** The script resolves all file paths relative to its own folder, so
> it also works from the project root:
>
> ```powershell
> uv run py_sql_server_advanced/sql_server_advanced.py
> ```

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `sql_server_advanced.py`.
3. Click the **Run ▶** button in the top-right corner of the editor
   (or press `Ctrl+F5`).
4. The program runs in the **Terminal** panel. Interact with it there (it uses
   `input()` for the menu).

---

## 🗂️ What the program creates / uses

| File                          | Purpose                                                                 |
| ----------------------------- | ----------------------------------------------------------------------- |
| `create_pytestdb_advanced.sql`| Creates `PyTestDb` + store schema + seed + indexes + views + trigger     |
| `sql_server_advanced.py`      | The menu-driven advanced tutorial                                        |

The lesson **only modifies the database** — it does not create any files. To
start fresh, re-run section 0 (or re-run `create_pytestdb_advanced.sql`),
which drops and recreates all tables and objects.

---

## 🐞 Debugging with VS Code (step-by-step, for beginners)

Debugging lets you **pause** the program at any line, **inspect** the values of
variables, and **step through** the code one line at a time.

### Step 1 — Set a breakpoint

1. Open `sql_server_advanced.py`.
2. Click in the **gutter** (the narrow column left of the line numbers) next to
   a line of code. A **red dot** appears — that's your breakpoint.

   For example, click next to `cur.execute(...)` inside `section_indexes` and
   watch the `SET STATISTICS` output and result rows flow.

### Step 2 — Start the debugger

1. Press **`F5`** (or go to **Run ▸ Start Debugging**).
2. The program starts, runs normally, and **pauses** when it hits your
   breakpoint.

> 💡 **Tip:** If you don't have a `launch.json` yet, VS Code will prompt you to
> create one. Choose **Python** and the **"Python: Current File"** configuration
> with `console: "integratedTerminal"`. Here's the config:

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

### Step 3 — Use the debugging toolbar

| Button        | Shortcut        | What it does                                                               |
| ------------- | --------------- | -------------------------------------------------------------------------- |
| **Continue**  | `F5`            | Run until the next breakpoint (or the end).                                |
| **Step Over** | `F10`           | Run the current line, then pause on the next. Skips _into_ function calls. |
| **Step Into** | `F11`           | Run the current line; if it calls a function, jump _inside_ that function. |
| **Step Out**  | `Shift+F11`     | Finish the current function and pause back at the caller.                  |
| **Restart**   | `Ctrl+Shift+F5` | Start the debug session over.                                              |
| **Stop**      | `Shift+F5`      | End the debug session.                                                     |

### Step 4 — Inspect variables

While paused, look at the **VARIABLES** panel (usually on the left, or in the
**Run and Debug** view): **Locals** shows variables in the current function,
**Globals** shows module-level ones. Hover any variable in the editor to see
its current value.

### Step 5 — Watch the call stack

The **CALL STACK** panel shows the chain of function calls that led to the
current line. When you're inside `section_indexes`, you'll see it called from
`main()`. Click any frame to jump to that line.

> 💡 **Pro tip:** In the **DEBUG CONSOLE**, you can type expressions and run
> them live while paused — e.g. type `cur.rowcount` or `len(rows)` to inspect
> values without adding print statements.