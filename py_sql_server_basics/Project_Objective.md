# 🗄️ SQL Server Basics with Python

Below is a complete, runnable Python application designed to teach a beginner
**how to connect Python to SQL Server and load CSV data into a table that
exercises every major SQL Server data type family**. It's a small, focused
lesson that walks through each concept with real working code, heavy
commenting, and links to the official documentation for further reading.

> This folder covers **SQL Server basics only**. Intermediate and advanced
> topics (queries, stored procedures, transactions, etc.) will be built out in
> later folders.

---

## Code Analysis Summary

- **Purpose:** A three-file lesson that creates a SQL Server table covering
  every major type family, provides three rows of boundary/edge/NULL test data,
  and loads that data from CSV into SQL Server using **pyodbc**.
- **Concepts covered:** connecting with `pyodbc`, parameterized `INSERT` with
  an `OUTPUT` clause, casting CSV strings to SQL types (`CAST`/`CONVERT`),
  spatial types (`GEOGRAPHY`/`GEOMETRY`), `HIERARCHYID`, `XML`,
  `SQL_VARIANT`, `UNIQUEIDENTIFIER`, binary strings, transactions
  (`autocommit=False` + `commit()`), and a verification query.
- **Style:** Heavily commented so each construct is explained _where it
  appears`; safe for beginners — the only thing it modifies is the database
  table (it creates no files).
- **Notable patterns:** `BASE_DIR`/`data_path()` path handling (the same
  pattern as the other lessons), a `to_sql_nullable()` helper that maps the
  literal string `"NULL"`/empty to Python `None`, a `main()` entry point, and
  a classic `if __name__ == "__main__"` guard.

---

## The Files (one per concept)

| # | File / Concept | What it shows |
|---|----------------|---------------|
| 1 | `create_pytesttable.sql` | A `CREATE TABLE` covering every major SQL Server type family |
| 2 | `pytesttable_data.csv` | Three rows of test data: max values, edge/negative values, NULLs + CSV edge cases |
| 3 | `load_pytesttable.py` | Connect with `pyodbc`, cast CSV strings to SQL types, INSERT + OUTPUT, UPDATE `HIERARCHYID`, verify |

---

## Design Principles

### 1. Third-party, but one install

Unlike the built-in `csv` module, connecting to SQL Server requires `pyodbc`:

```powershell
pip install pyodbc
```

After that, everything in this lesson uses `pyodbc` only — no other packages.

### 2. CSV cells are strings — cast them

The core lesson is that CSV cells are always **strings**. To load them into SQL
Server you must **cast** each one to the right type. The loader shows the exact
mapping for every type family:

| CSV representation | SQL conversion |
| --- | --- |
| `"0x010203..."` | `CONVERT(VARBINARY, ?, 1)` — style `1` expects the `0x` prefix |
| `"POINT(...)"` / `"LINESTRING(...)"` | `GEOGRAPHY::STGeomFromText(?, 4326)` / `GEOMETRY::STGeomFromText(?, 0)` |
| `"/1/2/3/"` | `HIERARCHYID::Parse(?)` (set via a separate `UPDATE`) |
| `"A1B2C3D4-..."` | `CAST(? AS UNIQUEIDENTIFIER)` |
| `"<root>...</root>"` | `CAST(? AS XML)` |
| `"2026-09-15T14:30:45.1234567+05:30"` | `CAST(? AS DATETIMEOFFSET)` (ISO 8601) |
| `"NULL"` / `""` | Python `None` → SQL `NULL` |

### 3. Parameterized queries

Every value is passed as a `?` placeholder that pyodbc fills in safely. This
prevents SQL injection and handles quoting/escaping for us.

### 4. The `OUTPUT` clause

The `INSERT` uses `OUTPUT INSERTED.Id` so we capture the auto-generated
identity value — needed to set `HIERARCHYID` in a follow-up `UPDATE`.

### 5. Transactions

The connection uses `autocommit=False`, so nothing is saved until `commit()`.
If something fails midway, we can roll back instead of leaving half-written
data.

### 6. Type coverage

The table exercises **every major type family**:

| Family | Types covered |
| --- | --- |
| Exact numeric | `BIGINT`, `INT`, `SMALLINT`, `TINYINT`, `BIT`, `DECIMAL`, `NUMERIC`, `MONEY`, `SMALLMONEY` |
| Approximate numeric | `FLOAT`, `REAL` |
| Date/time | `DATE`, `TIME`, `DATETIME`, `DATETIME2`, `DATETIMEOFFSET`, `SMALLDATETIME` |
| Char (non-Unicode) | `CHAR`, `VARCHAR`, `VARCHAR(MAX)` |
| NChar (Unicode) | `NCHAR`, `NVARCHAR`, `NVARCHAR(MAX)` |
| Binary | `BINARY`, `VARBINARY`, `VARBINARY(MAX)` |
| Other | `UNIQUEIDENTIFIER`, `XML`, `SQL_VARIANT`, `HIERARCHYID`, `GEOGRAPHY`, `GEOMETRY` |
| Auto | `ROWVERSION` (cannot be inserted — SQL Server manages it) |

Legacy types `TEXT`, `NTEXT`, and `IMAGE` are intentionally omitted — they've
been deprecated since SQL Server 2005 and Microsoft recommends the `(MAX)`
variants instead.

---

## Files in this folder

```
py_sql_server_basics/
├── create_pytesttable.sql   # creates the dbo.PyTestTable table (run once)
├── pytesttable_data.csv     # input test data (3 rows, UTF-8 with BOM)
├── load_pytesttable.py      # the loader program (CSV → SQL Server)
├── Project_Objective.md     # design notes & concept breakdown (this file)
└── README.md                # how to run & debug
```

> `pytesttable_data.csv` is the **input** sample data and is never modified.
> The loader inserts rows into the database — it does not create files.

---

## Getting Started

```powershell
pip install pyodbc
# 1. Create the PyTestDb database (once)
# 2. Run create_pytesttable.sql against PyTestDb (once)
python load_pytesttable.py
```

See `README.md` for full running and debugging instructions.