# 🗄️ SQL Server Basics — `pyodbc` + SQL Server

A self-guided lesson that teaches **how to connect Python to SQL Server** and
load a CSV file into a table that exercises **every major SQL Server data type
family** — including the tricky ones (`XML`, `HIERARCHYID`, `GEOGRAPHY`,
`GEOMETRY`, `SQL_VARIANT`). It ships with a `CREATE TABLE` script, a CSV of
test data, and a `pyodbc` loader that shows how to map CSV strings back into
the proper SQL types.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

> This is the **basics** folder. Later folders will build on it with
> intermediate and advanced SQL Server topics (queries, stored procedures,
> transactions, etc.).

## What you'll learn

| #   | File / Concept                          | What it shows                                                          |
| --- | --------------------------------------- | ---------------------------------------------------------------------- |
| 1   | `create_pytesttable.sql`                | A `CREATE TABLE` covering every major SQL Server type family           |
| 2   | `pytesttable_data.csv`                  | Three rows of test data: max values, edge/negative values, NULLs + CSV edge cases |
| 3   | `load_pytesttable.py`                   | A **menu-driven** program: **Setup** (run the SQL), **Load** (CSV → SQL Server with casts, INSERT + OUTPUT, UPDATE `HIERARCHYID`, verify), **Cleanup** (drop the table) |

> 💡 **Key idea:** CSV cells are always **strings**. To load them into SQL
> Server you must **cast** each one to the right type — `CAST(? AS DATE)`,
> `CONVERT(VARBINARY, ?, 1)`, `GEOGRAPHY::STGeomFromText(?, 4326)`, and so on.
> The loader shows the exact mapping for every type family.

---

## ✅ Prerequisites

- **Python 3.11 or newer** (matches `requires-python` in `pyproject.toml`).
- **SQL Server** running locally (or a reachable server) with the **`PyTestDb`**
  database created.
- **ODBC Driver 18 for SQL Server** installed on your machine.
- **pyodbc** installed:

  ```powershell
  pip install pyodbc
  ```

- **VS Code** with the **Python extension** (by Microsoft) installed.

Check your Python version and pyodbc:

```powershell
python --version
python -c "import pyodbc; print(pyodbc.version)"
```

> If `pip install pyodbc` fails, try `python -m pip install pyodbc`.

---

## 🗄️ Step 0 — Create the database and table

The loader connects to a database named **`PyTestDb`**. Create it once in SQL
Server Management Studio (SSMS) or `sqlcmd`:

```sql
CREATE DATABASE PyTestDb;
```

Then run the `create_pytesttable.sql` script against `PyTestDb` to create the
`dbo.PyTestTable` table. The script is **idempotent** — it drops the table if
it already exists, then recreates it, so you can re-run it any time to start
fresh.

> 💡 **Note:** The table includes a `ROWVERSION` column. SQL Server manages it
> automatically — you **cannot** insert into it, which is why the loader's
> `INSERT` statement omits it.

---

## ▶️ How to run the program

### Option A — Run from the terminal

1. Open a terminal in this folder.
2. Run the loader:

   ```powershell
   python load_pytesttable.py
   ```

3. You'll see a menu with three actions. Type a number to run one, or `q` to
   quit:

   - **`1` Setup** — runs `create_pytesttable.sql` to create the table.
   - **`2` Load** — reads the CSV, inserts the rows, and runs a verification
     query. You'll see one line per inserted row (`Row 1 inserted (Id=1)`, ...),
     a `Data loaded successfully!` message, and then the verification output
     that prints a few of the tricky types converted back to readable text.
   - **`3` Cleanup** — drops the table so you can start fresh.

   > 💡 **Tip:** Run **Setup (1)** first if the table doesn't exist yet, then
   > **Load (2)**. Re-run **Setup** any time to reset the table.

> 💡 **Tip:** The script resolves all file paths relative to its own folder, so
> it also works from the project root:
>
> ```powershell
> python py_sql_server_basics/load_pytesttable.py
> ```
>
> No matter which folder you run it from, it reads `pytesttable_data.csv` in
> `py_sql_server_basics/`.

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `load_pytesttable.py`.
3. Click the **Run ▶** button in the top-right corner of the editor
   (or press `Ctrl+F5`).
4. The program runs in the **Terminal** panel. Interact with it there.

> 💡 **Tip:** This script uses `input()` for its menu, so run it in the
> **integrated terminal** (not the Output panel) so the menu prompts are
> visible.

---

## 🗂️ What the program creates / uses

| File                    | Purpose                                                                 |
| ----------------------- | ----------------------------------------------------------------------- |
| `create_pytesttable.sql`| Creates the `dbo.PyTestTable` table (run via menu action **1 Setup**)    |
| `pytesttable_data.csv`  | **Input** test data (3 rows, UTF-8 with BOM) — never modified           |
| `load_pytesttable.py`   | The menu-driven program: Setup / Load (CSV → SQL Server) / Cleanup      |

The loader **inserts rows into the database** — it does not create files. To
start fresh, run menu action **3 Cleanup** (or re-run `create_pytesttable.sql`,
which drops + recreates the table) and then re-run **2 Load**.

---

## 🐞 Debugging with VS Code (step-by-step, for beginners)

Debugging lets you **pause** the program at any line, **inspect** the values of
variables, and **step through** the code one line at a time. It's the single
best way to understand _what your code is actually doing_.

### Step 1 — Set a breakpoint

A **breakpoint** is a marker that tells the debugger: _"pause here so I can look
around."_

1. Open `load_pytesttable.py`.
2. Click in the **gutter** (the narrow column to the left of the line numbers)
   next to a line of code. A **red dot** appears — that's your breakpoint.

   For example, click next to `cur.execute(INSERT_SQL, params)` inside the
   `for` loop. Watching `params` build up is a great way to see how CSV strings
   become SQL parameters.

   - Click the red dot again to remove it.
   - You can set as many breakpoints as you want.

### Step 2: Start the debugger

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

- **Locals** — variables in the current function (like `params`, `new_id`).
- **Globals** — variables defined at the top level of the module.

You can also **hover** your mouse over any variable in the editor to see its
current value in a tooltip.

### Step 5 — Use the Debug Console

The **DEBUG CONSOLE** panel lets you type Python expressions and evaluate them
_right now_, using the current state of the program.

For example, while paused after building `params`, type:

```python
params
```

and press Enter — it returns the list of values about to be sent to SQL Server.

### Step 6 — Walk through the tutorial

Here's a suggested debugging session to learn the flow:

1. Set a breakpoint on `cur.execute(INSERT_SQL, params)`.
2. Press **F5** to start. At the menu, type **`2`** (Load) and press Enter.
3. The program pauses before the first insert. In **VARIABLES**, expand
   `params` and `row` to see the CSV values.
4. Press **F10** (Step Over) to run the insert, then inspect `new_id`.
5. Press **F5** (Continue) to jump to the next row's insert.
6. Repeat until the loop finishes, then watch the verification query print.

---

## 🔍 Verifying the data in SQL Server

After loading, you can run this query in SSMS to sanity-check the round-trip —
it shows the auto-managed `ROWVERSION`, a few typed columns, and the spatial
types converted back to WKT:

```sql
SELECT
    Id, ColRowVersion,
    ColBigInt, ColInt, ColBit,
    ColVarChar, ColNVarChar,
    ColUniqueIdentifier,
    ColGeography.STAsText() AS GeoWKT,
    ColGeometry.STAsText()   AS GeomWKT
FROM dbo.PyTestTable;
```

---

## 📚 Key mapping rules (CSV → SQL)

| CSV representation | SQL conversion |
| --- | --- |
| `"0x010203..."` | `CONVERT(VARBINARY, ?, 1)` — style `1` expects the `0x` prefix |
| `"POINT(...)"` / `"LINESTRING(...)"` | `GEOGRAPHY::STGeomFromText(?, 4326)` / `GEOMETRY::STGeomFromText(?, 0)` |
| `"/1/2/3/"` | `HIERARCHYID::Parse(?)` (set via a separate `UPDATE`) |
| `"A1B2C3D4-..."` | `CAST(? AS UNIQUEIDENTIFIER)` |
| `"<root>...</root>"` | `CAST(? AS XML)` |
| `"2026-09-15T14:30:45.1234567+05:30"` | `CAST(? AS DATETIMEOFFSET)` (ISO 8601) |
| `"NULL"` / `""` | Python `None` → SQL `NULL` |

---

## 📚 Further reading

- [pyodbc documentation](https://github.com/mkleehammer/pyodbc)
- [SQL Server data types (Microsoft Learn)](https://learn.microsoft.com/sql/t-sql/data-types/data-types-transact-sql)
- [OUTPUT clause (Microsoft Learn)](https://learn.microsoft.com/sql/t-sql/queries/output-clause-transact-sql)
- [ODBC Driver for SQL Server (Microsoft Learn)](https://learn.microsoft.com/sql/connect/odbc/microsoft-odbc-driver-for-sql-server)