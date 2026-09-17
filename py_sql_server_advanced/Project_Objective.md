# 🗄️ SQL Server Advanced with Python

Below is a complete, runnable Python application designed to take a learner
**from SQL Server intermediate to advanced database work**. Building on the
`py_sql_server_intermediate` folder, this interactive "study session" teaches
the topics that folder explicitly deferred: **indexes, query tuning, views,
CTEs & window functions, bulk operations, dynamic SQL, transactions &
isolation, and pandas ↔ SQL Server integration** — using the same small,
realistic store schema.

> This folder covers **SQL Server advanced**. It completes the SQL Server
> learning path (basics → intermediate → advanced).

---

## Code Analysis Summary

- **Purpose:** A menu-driven teaching tool that walks through performance,
  schema, and integration topics against the four-table store schema
  (`Customers`, `Products`, `Orders`, `OrderItems`).
- **Concepts covered:** `CREATE INDEX` and covering indexes; `SET STATISTICS
  TIME, IO ON` and execution plans (`SET SHOWPLAN_ALL`); `CREATE VIEW` and
  querying/updating through views; CTEs (`WITH`) and window functions
  (`ROW_NUMBER`, `RANK`, `LAG`/`LEAD`, `OVER(PARTITION BY)`); bulk inserts
  with `executemany()` and `fast_executemany=True`; dynamic SQL via
  `sp_executesql`; isolation levels, savepoints, and deadlock handling; and
  `pd.read_sql()` / `to_sql()` through a SQLAlchemy engine.
- **Style:** Heavily commented so each construct is explained _where it
  appears_; safe for learners continuing from intermediate — it only modifies
  the `PyTestDb` database (it creates no files).
- **Notable patterns:** Reuses the `data_path()` helper, `CONN_STR`, and
  `connect()`/`print_rows()` helpers from the intermediate lesson; a `main()`
  menu loop and the classic `if __name__ == "__main__"` guard.

---

## The Concepts (one per section)

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

---

## Design Principles

### 1. Continues the series' progression

Basics taught **how to get data in**; intermediate taught **what to do with
it** (CRUD). This lesson teaches **how to make it fast, safe, and integrated**
— performance (indexes, tuning), schema (views), advanced querying (CTEs,
window functions), scale (bulk ops), flexibility (dynamic SQL), correctness
(isolation), and interop (pandas).

### 2. Reuses the same realistic schema

It builds on the same store schema from intermediate, adding the objects an
advanced lesson needs:

```
Customers ──< Orders ──< OrderItems >── Products
```

`create_pytestdb_advanced.sql` recreates the four tables, seeds them, and adds
**indexes**, **views**, and a **trigger** so every section has real objects to
work with. The seed data uses **fixed Ids** (`SET IDENTITY_INSERT ON`) so every
example is deterministic and repeatable.

### 3. Measure before and after

Sections 1 and 2 use `SET STATISTICS TIME, IO ON` and `SET SHOWPLAN_ALL` to
show the **actual cost** of a query — then re-run the same query after adding
an index or rewriting the predicate so the learner sees the difference in real
numbers, not theory.

### 4. Parameterized everything (even dynamic SQL)

Every value is passed as a `?` placeholder that pyodbc fills in safely. The
dynamic SQL section shows the **safe** way to build dynamic queries with
`sp_executesql` (parameters stay bound) versus the dangerous string
concatenation you must avoid.

### 5. Transactions are explicit

Section 7 explores isolation levels and savepoints, and shows how a deadlock
is detected and handled. The lesson uses `autocommit=False` throughout so
nothing is saved until `commit()`.

### 6. One-concept-per-section

Like every other folder in this repo, each section is its own function so a
learner can study it in isolation and re-run any part on demand.

### 7. Progression from performance → integration

- Sections 1–2 are **performance**: indexes, then reading execution plans.
- Section 3 is **schema**: views.
- Section 4 is **advanced querying**: CTEs and window functions.
- Section 5 is **scale**: bulk operations.
- Section 6 is **flexibility**: dynamic SQL.
- Section 7 is **correctness**: transactions & isolation.
- Section 8 is **integration**: pandas ↔ SQL Server.
- Section 9 ties everything together with a realistic workflow.

---

## Files in this folder

```
py_sql_server_advanced/
├── create_pytestdb_advanced.sql # creates PyTestDb + schema + seed + indexes + views + trigger
├── sql_server_advanced.py       # the tutorial program (menu-driven)
├── Project_Objective.md         # design notes & concept breakdown (this file)
└── README.md                    # how to run & debug
```

> The lesson **does not create files** — it only reads from and writes to the
> `PyTestDb` database. `create_pytestdb_advanced.sql` is the only input file.

---

## Getting Started

```powershell
pip install pyodbc sqlalchemy
# 1. (Optional) Run create_pytestdb_advanced.sql once in SSMS, OR
# 2. Just run the lesson and choose section 0 — it runs the script for you.
python sql_server_advanced.py
```

Type a number `0`–`9` to run a section, or `q` to quit.

See `README.md` for full running and debugging instructions.