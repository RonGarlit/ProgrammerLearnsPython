# 🗄️ SQL Server Intermediate with Python

Below is a complete, runnable Python application designed to take a learner
**from SQL Server basics to intermediate-level database work**. Building on the
`py_sql_server_basics` folder, this interactive "study session" teaches the
**full CRUD cycle** — Create, Read, Update, Delete — using a small, realistic
relational store schema. It covers CRUD **two ways**: first with normal SQL
statements, then with **logical stored procedures**, so the learner sees both
methods of talking to the database.

> This folder covers **SQL Server intermediate**. Advanced topics (views,
> indexes, query tuning, dynamic SQL, pandas ↔ SQL Server integration, etc.)
> will be built out in a later advanced folder.

---

## Code Analysis Summary

- **Purpose:** A menu-driven teaching tool that walks through CRUD against a
  four-table store schema (`Customers`, `Products`, `Orders`, `OrderItems`).
- **Concepts covered:** `SELECT` with `WHERE`/`ORDER BY`/`TOP`/`DISTINCT`/
  aliases; filtering with `LIKE`/`IN`/`BETWEEN`/`IS NULL`; aggregates and
  `GROUP BY`/`HAVING`; `INNER`/`LEFT`/multi-table `JOIN`s; parameterized
  `INSERT`/`UPDATE`/`DELETE` with `OUTPUT`; explicit transactions with
  `COMMIT`/`ROLLBACK`; and executing stored procedures with **input and output
  parameters** via pyodbc.
- **Style:** Heavily commented so each construct is explained _where it
  appears_; safe for learners continuing from basics — it only modifies the
  `PyTestDb` database (it creates no files).
- **Notable patterns:** Reuses the `data_path()` helper and `CONN_STR` pattern
  from the basics lesson; a `print_rows()` helper that renders a result set
  with column headers; a `main()` menu loop and the classic
  `if __name__ == "__main__"` guard.

---

## The Concepts (one per section)

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

---

## Design Principles

### 1. Continues the series' progression

Basics taught **how to get data in** (connect, cast CSV strings, INSERT). This
lesson teaches **what to do with it once it's there** — the full CRUD cycle.
Every concept builds on the basics' `OUTPUT` clause and transaction pattern.

### 2. A realistic relational schema

Instead of the wide `PyTestTable`, this lesson uses a small store schema with
real foreign keys:

```
Customers ──< Orders ──< OrderItems >── Products
```

This makes `JOIN`s meaningful and lets the stored procedures do real work
(place an order, get order details). The seed data uses **fixed Ids**
(`SET IDENTITY_INSERT ON`) so every example is deterministic and repeatable.

### 3. CRUD two ways

The theme is CRUD, and it's taught **twice**:

- **Sections 1–8** use normal SQL statements (`SELECT`, `INSERT`, `UPDATE`,
  `DELETE`) — the direct method.
- **Section 9** re-implements Create and Read as **stored procedures**
  (`usp_PlaceOrder`, `usp_GetOrderDetails`) — the database method.

This mirrors how real applications work: simple operations inline, complex or
repeated logic in procedures.

### 4. Parameterized everything

Every value is passed as a `?` placeholder that pyodbc fills in safely. This
prevents SQL injection and is the single most important habit to build.

### 5. Transactions are explicit

Section 8 deliberately forces a `UNIQUE` constraint violation mid-transaction
to show `ROLLBACK` undoing earlier work. The lesson uses `autocommit=False`
throughout so nothing is saved until `commit()`.

### 6. One-concept-per-section

Like every other folder in this repo, each section is its own function so a
learner can study it in isolation and re-run any part on demand.

### 7. Progression from easy → applied

- Sections 1–4 are **Read** (querying): select, filter, aggregate, join.
- Sections 5–7 are **Write** (Create/Update/Delete).
- Section 8 hardens it with transactions.
- Section 9 moves logic into the database (stored procedures).
- Section 10 ties everything together with a realistic workflow.

---

## Files in this folder

```
py_sql_server_intermediate/
├── create_pytestdb.sql        # creates PyTestDb + schema + seed + procedures
├── sql_server_intermediate.py # the tutorial program (menu-driven)
├── Project_Objective.md       # design notes & concept breakdown (this file)
└── README.md                  # how to run & debug
```

> The lesson **does not create files** — it only reads from and writes to the
> `PyTestDb` database. `create_pytestdb.sql` is the only input file.

---

## Getting Started

```powershell
pip install pyodbc
# 1. (Optional) Run create_pytestdb.sql once in SSMS, OR
# 2. Just run the lesson and choose section 0 — it runs the script for you.
python sql_server_intermediate.py
```

Type a number `0`–`10` to run a section, or `q` to quit.

See `README.md` for full running and debugging instructions.