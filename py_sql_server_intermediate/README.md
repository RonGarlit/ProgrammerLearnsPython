# 🗄️ SQL Server Intermediate — CRUD with `pyodbc`

An interactive, menu-driven Python lesson that teaches the **full CRUD cycle**
(Create, Read, Update, Delete) against a small relational store schema in SQL
Server. Building on the `py_sql_server_basics` folder, it covers CRUD **two
ways**: with normal SQL statements, and with **logical stored procedures** —
so you see both methods of talking to the database.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

> ✅ **Prerequisite:** Complete the **`py_sql_server_basics`** folder first.
> This lesson assumes you know how to connect with pyodbc, use `?` parameters,
> the `OUTPUT` clause, and `autocommit=False` + `commit()`.

## What you'll learn

| #  | Concept                  | What it shows                                                          |
| -- | ------------------------ | ---------------------------------------------------------------------- |
| 0  | Setup                    | Runs `create_pytestdb.sql` to build the schema, seed data, procedures  |
| 1  | SELECT basics            | `WHERE`, `ORDER BY`, `TOP`, `DISTINCT`, column aliases                 |
| 2  | Filtering                | `LIKE`, `IN`, `BETWEEN`, `IS NULL`, comparison operators               |
| 3  | Aggregates & GROUP BY    | `COUNT`/`SUM`/`AVG`/`MIN`/`MAX`, `GROUP BY`, `HAVING`                  |
| 4  | JOINs                    | `INNER`, `LEFT`, and a 4-table JOIN across the whole schema            |
| 5  | CREATE (INSERT)          | Parameterized `INSERT` + `OUTPUT INSERTED.Id`                          |
| 6  | UPDATE                   | `UPDATE ... SET ... WHERE` with `OUTPUT`                               |
| 7  | DELETE                   | `DELETE ... WHERE` with `OUTPUT`                                       |
| 8  | Transactions             | `BEGIN`/`COMMIT`/`ROLLBACK` with a forced error to show rollback       |
| 9  | Stored procedures        | `EXEC` with input + output params; walking multiple result sets        |
| 10 | Mini task                | A full CRUD workflow combining everything                              |

> 💡 **Key idea:** Real database work is **CRUD** — Create, Read, Update,
> Delete. You can do all of it with plain SQL, or you can wrap logic in
> **stored procedures** and just call them. This lesson shows you both.

---

## ✅ Prerequisites

- **Python 3.11 or newer** (matches `requires-python` in `pyproject.toml`).
- **SQL Server** running locally (or a reachable server).
- **ODBC Driver 18 for SQL Server** installed on your machine.
- **pyodbc** installed (it's already declared in `pyproject.toml`, so `uv sync`
  installs it):

  ```powershell
  uv sync
  ```

- **VS Code** with the **Python extension** (by Microsoft) installed.

Check your Python version and pyodbc:

```powershell
uv run python --version
uv run python -c "import pyodbc; print(pyodbc.version)"
```

> If `uv sync` fails, try `uv add pyodbc` to add it to the project.

---

## 🗄️ Step 0 — Create the database, schema, and procedures

The lesson connects to a database named **`PyTestDb`** (the same one from
`py_sql_server_basics`). The `create_pytestdb.sql` script creates the database
if needed, then builds the store schema, seeds it with data, and creates the
two stored procedures. The script is **idempotent** — you can re-run it any
time to start fresh.

There are two ways to run it:

### Option A — Let the lesson do it (recommended)

Just run the program and choose **section 0**:

```powershell
uv run sql_server_intermediate.py
```

Section 0 reads `create_pytestdb.sql`, strips the `GO` batch separators (a
sqlcmd/SSMS feature that isn't valid T-SQL), and executes it for you.

### Option B — Run it yourself in SSMS / sqlcmd

```sql
-- In SSMS, open the file and press F5, or:
sqlcmd -S localhost -E -i create_pytestdb.sql
```

The script creates four tables:

```
Customers ──< Orders ──< OrderItems >── Products
```

---

## ▶️ How to run the program

### Option A — Run from the terminal

1. Open a terminal in this folder.
2. Run the program:

   ```powershell
   uv run sql_server_intermediate.py
   ```

3. You'll see a menu. Type a number `0`–`10` to run a section, `c` for
   cleanup, or `q` to quit.

> 💡 **Tip:** The script resolves all file paths relative to its own folder, so
> it also works from the project root:
>
> ```powershell
> uv run py_sql_server_intermediate/sql_server_intermediate.py
> ```

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `sql_server_intermediate.py`.
3. Click the **Run ▶** button in the top-right corner of the editor
   (or press `Ctrl+F5`).
4. The program runs in the **Terminal** panel. Interact with it there (it uses
   `input()` for the menu).

---

## 🗂️ What the program creates / uses

| File                    | Purpose                                                                 |
| ----------------------- | ----------------------------------------------------------------------- |
| `create_pytestdb.sql`   | Creates `PyTestDb` + store schema + seed data + stored procedures        |
| `sql_server_intermediate.py` | The menu-driven CRUD tutorial                                       |

The lesson **only modifies the database** — it does not create any files. To
start fresh, re-run section 0 (or re-run `create_pytestdb.sql`), which drops
and recreates all tables and procedures.

---

## 🐞 Debugging with VS Code (step-by-step, for beginners)

Debugging lets you **pause** the program at any line, **inspect** the values of
variables, and **step through** the code one line at a time.

### Step 1 — Set a breakpoint

1. Open `sql_server_intermediate.py`.
2. Click in the **gutter** (the narrow column left of the line numbers) next to
   a line of code. A **red dot** appears — that's your breakpoint.

   For example, click next to `cur.execute(...)` inside `section_select_basics`
   and watch the parameters and result rows flow.

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
its value.

### Step 5 — Walk through a section

Here's a suggested debugging session for **Section 5 (INSERT)**:

1. Set a breakpoint on `cur.execute(...)` inside `section_insert()`.
2. Press **F5**. Choose section `5` at the menu.
3. In **VARIABLES**, expand `new_customer` to see the tuple being inserted.
4. Press **F10** to run the insert, then inspect `new_id`.
5. Press **F5** to let the verification query run and print the new row.

> 💡 **Note:** Because the lesson uses `input()`, run it in the **integrated
> terminal** (not the Debug Console) so the menu prompts are visible.

---

## 🔍 Verifying the data in SQL Server

After running sections, you can inspect the data in SSMS:

```sql
USE PyTestDb;
-- All customers
SELECT * FROM dbo.Customers;
-- Orders with customer names
SELECT o.OrderId, c.LastName, o.OrderDate, o.Status
FROM dbo.Orders o
JOIN dbo.Customers c ON c.CustomerId = o.CustomerId;
```

---

## 📚 Further reading

- [pyodbc documentation](https://github.com/mkleehammer/pyodbc)
- [SELECT (Microsoft Learn)](https://learn.microsoft.com/sql/t-sql/queries/select-transact-sql)
- [JOIN (Microsoft Learn)](https://learn.microsoft.com/sql/t-sql/queries/from-transact-sql)
- [Stored procedures (Microsoft Learn)](https://learn.microsoft.com/sql/relational-databases/stored-procedures/stored-procedures-database-engine)
- [Transactions (Microsoft Learn)](https://learn.microsoft.com/sql/t-sql/language-elements/transactions-transact-sql)
