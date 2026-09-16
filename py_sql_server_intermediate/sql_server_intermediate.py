"""
SQL Server Intermediate with Python — A Self-Guided Lesson
==========================================================
Run this file (with `python sql_server_intermediate.py`) and follow along.

This is the SECOND step in SQL Server. We assume you already completed
`py_sql_server_basics` (connecting with pyodbc, casting CSV strings to SQL
types, INSERT + OUTPUT, transactions). Here we level up to real-world CRUD:

  C reate  — INSERT rows (direct SQL, then a stored procedure)
  R ead    — SELECT, filter, aggregate, JOIN
  U pdate  — UPDATE rows
  D elete  — DELETE rows

The theme is CRUD, and we cover it TWO ways:
  1. With normal SQL statements (sections 1-8), and
  2. With logical stored procedures (section 9), so you see both methods.

The example data lives in the `PyTestDb` database, created by
`create_pytestdb.sql` in this folder. It is a small store schema:

    Customers ──< Orders ──< OrderItems >── Products

Docs: https://github.com/mkleehammer/pyodbc
"""

import re
from pathlib import Path

import pyodbc

# ---------------------------------------------------------------------------
# Path handling with pathlib
# ---------------------------------------------------------------------------
# `Path(__file__)` is this script's own location; `.resolve()` makes it
# absolute; `.parent` walks up to the folder containing it. Using BASE_DIR
# means the lesson works no matter WHERE you run it from.
# Docs: https://docs.python.org/3/library/pathlib.html

BASE_DIR = Path(__file__).resolve().parent


def data_path(filename):
    """Return the full path to a file inside this script's folder."""
    return BASE_DIR / filename


# The SQL script that creates the schema + seed data + stored procedures.
SETUP_SQL_FILE = data_path("create_pytestdb.sql")

# ---------------------------------------------------------------------------
# Connection string
# ---------------------------------------------------------------------------
# Same pattern as the basics lesson. `Trusted_Connection` uses your Windows
# login; `TrustServerCertificate` skips the TLS cert check for local dev.
CONN_STR = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;DATABASE=PyTestDb;"
    "Trusted_Connection=yes;TrustServerCertificate=yes;"
)


def connect(autocommit=False):
    """Open a pyodbc connection to PyTestDb."""
    return pyodbc.connect(CONN_STR, autocommit=autocommit) # Doc: https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows


def print_rows(cursor, title=None):
    """Print every row returned by a cursor, with column names as a header."""
    if title:
        print(f"\n{title}")
    # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#description
    cols = [d[0] for d in cursor.description] # Get the column names from the cursor description
    print(" | ".join(cols)) # Print the column headers
    print("-" * 60) # Print a separator line
    # Print each row, joining the values with " | "
    for row in cursor.fetchall(): # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#fetchall
        print(" | ".join(str(v) for v in row))


# ---------------------------------------------------------------------------
# SECTION 0: Setup — create the schema, seed data, and stored procedures
# ---------------------------------------------------------------------------
# We run the .sql file by reading it and executing it. The `GO` lines are
# batch separators used by sqlcmd/SSMS — they are NOT valid T-SQL, so we split
# the script on them and execute each batch separately. This matters because
# `CREATE PROCEDURE` must be the FIRST statement in its batch.
# Docs: https://learn.microsoft.com/sql/tools/sqlcmd/sqlcmd-use-the-utility
def section_setup():
    print("=" * 60)
    print("SECTION 0: Setup — create schema, seed data, and procedures")
    print("=" * 60)

    sql = SETUP_SQL_FILE.read_text(encoding="utf-8")

    # Split on whole-line `GO` separators (case-insensitive) and drop empties.
    batches = [b for b in re.split(r"(?im)^\s*GO\s*$", sql) if b.strip()]

    # autocommit=True so each batch commits as it runs (the script has its
    # own DDL/DML and we want it to persist regardless of later errors).
    with connect(autocommit=True) as cn:
        for batch in batches:
            cn.execute(batch)

    print("Schema created and seeded. Tables now contain:")
    # Doc: https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module#connect
    with connect() as cn:
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor
        cur = cn.cursor()
        cur.execute(
            """
            SELECT 'Customers' AS TableName, COUNT(*) AS TotalRows FROM dbo.Customers
            UNION ALL SELECT 'Products',  COUNT(*) FROM dbo.Products
            UNION ALL SELECT 'Orders',    COUNT(*) FROM dbo.Orders
            UNION ALL SELECT 'OrderItems',COUNT(*) FROM dbo.OrderItems
            """
        )
        print_rows(cur, "Row counts:")


# ---------------------------------------------------------------------------
# SECTION 0b: Cleanup — drop the tables and stored procedures
# ---------------------------------------------------------------------------
# So you can start fresh, this drops every object the setup created. Child
# tables go first (OrderItems) so FOREIGN KEY constraints never block us,
# then parents, then the stored procedures.
# Docs: https://learn.microsoft.com/sql/t-sql/statements/drop-table-transact-sql


def section_cleanup():
    print("=" * 60)
    print("SETUP-CLEANUP: Drop all intermediate tables and procedures")
    print("=" * 60)

    with connect(autocommit=True) as cn:
        cur = cn.cursor()
        cur.execute(
            "IF OBJECT_ID('dbo.OrderItems', 'U') IS NOT NULL DROP TABLE dbo.OrderItems;"
        )
        cur.execute(
            "IF OBJECT_ID('dbo.Orders', 'U') IS NOT NULL DROP TABLE dbo.Orders;"
        )
        cur.execute(
            "IF OBJECT_ID('dbo.Products', 'U') IS NOT NULL DROP TABLE dbo.Products;"
        )
        cur.execute(
            "IF OBJECT_ID('dbo.Customers', 'U') IS NOT NULL DROP TABLE dbo.Customers;"
        )
        cur.execute(
            "IF OBJECT_ID('dbo.usp_PlaceOrder', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_PlaceOrder;"
        )
        cur.execute(
            "IF OBJECT_ID('dbo.usp_GetOrderDetails', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_GetOrderDetails;"
        )

    print(
        "All intermediate tables and stored procedures dropped — you can start fresh."
    )
    print("Hint: run Setup (section 0) to recreate them.")


# ---------------------------------------------------------------------------
# SECTION 1: SELECT basics — WHERE, ORDER BY, TOP, DISTINCT, aliases
# ---------------------------------------------------------------------------
# Reading data is the R in CRUD. This section covers the most common SELECT
# clauses. Every value is passed as a `?` placeholder (parameterized) so we
# never build SQL by string concatenation.
# Docs: https://learn.microsoft.com/sql/t-sql/queries/select-transact-sql


def section_select_basics():
    print("=" * 60)
    print("SECTION 1: SELECT basics — WHERE, ORDER BY, TOP, DISTINCT")
    print("=" * 60)

    with connect() as cn:
        cur = cn.cursor() # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor

        # 1a. WHERE + ORDER BY — filter rows, then sort them.
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters
        cur.execute(
            """
            SELECT ProductId, ProductName, Category, UnitPrice
            FROM dbo.Products
            WHERE Category = ?
            ORDER BY UnitPrice DESC
            """,
            "Electronics"
        )
        print_rows(cur, "1a. Electronics products, most expensive first:")

        # 1b. TOP — limit how many rows come back.
        cur.execute(
            """
            SELECT TOP 3 ProductName, UnitPrice
            FROM dbo.Products
            ORDER BY UnitPrice DESC
            """
        )
        print_rows(cur, "1b. Top 3 most expensive products:")

        # 1c. DISTINCT — unique values in a column.
        cur.execute("SELECT DISTINCT City FROM dbo.Customers ORDER BY City")
        print_rows(cur, "1c. Distinct customer cities:")

        # 1d. Column alias — rename a column in the result.
        cur.execute(
            """
            SELECT ProductName AS Name, UnitPrice AS Price
            FROM dbo.Products
            WHERE UnitsInStock < 20
            """
        )
        print_rows(cur, "1d. Low-stock products (aliased columns):")


# ---------------------------------------------------------------------------
# SECTION 2: Filtering — LIKE, IN, BETWEEN, IS NULL, comparisons
# ---------------------------------------------------------------------------
# WHERE gets more expressive with these operators. They are pure T-SQL and
# work exactly the same whether you run them from Python or SSMS.
# Docs: https://learn.microsoft.com/sql/t-sql/queries/where-transact-sql


def section_filtering():
    print("=" * 60)
    print("SECTION 2: Filtering — LIKE, IN, BETWEEN, IS NULL")
    print("=" * 60)

    with connect() as cn:
        cur = cn.cursor() # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor

        # 2a. LIKE — pattern matching. % matches any number of characters.
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters
        cur.execute(
            "SELECT ProductName, Category FROM dbo.Products WHERE ProductName LIKE ?",
            "%Keyboard%",
        )
        print_rows(cur, "2a. Products whose name contains 'Keyboard':")

        # 2b. IN — match any value in a list.
        cur.execute(
            "SELECT FirstName, LastName, City FROM dbo.Customers WHERE City IN (?, ?)",
            "Seattle",
            "Austin",
        )
        print_rows(cur, "2b. Customers in Seattle or Austin:")

        # 2c. BETWEEN — inclusive range.
        cur.execute(
            "SELECT ProductName, UnitPrice FROM dbo.Products WHERE UnitPrice BETWEEN ? AND ?",
            20.00,
            100.00,
        )
        print_rows(cur, "2c. Products priced between $20 and $100:")

        # 2d. IS NULL — find missing values. (Our seed has none, but the
        #     syntax is the key lesson.)
        cur.execute("SELECT CustomerId, Email FROM dbo.Customers WHERE Email IS NULL")
        print_rows(cur, "2d. Customers with a NULL email (should be empty):")


# ---------------------------------------------------------------------------
# SECTION 3: Aggregates & GROUP BY — COUNT, SUM, AVG, MIN, MAX, HAVING
# ---------------------------------------------------------------------------
# Aggregates collapse many rows into one summary value. GROUP BY splits the
# data into groups first; HAVING filters the groups (WHERE filters rows).
# Docs: https://learn.microsoft.com/sql/t-sql/queries/select-group-by-transact-sql


def section_aggregates():
    print("=" * 60)
    print("SECTION 3: Aggregates & GROUP BY")
    print("=" * 60)

    with connect() as cn:
        cur = cn.cursor() # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor

        # 3a. Simple aggregates over the whole table.
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters
        cur.execute(
            """
            SELECT COUNT(*) AS NumProducts,
                   AVG(UnitPrice) AS AvgPrice,
                   MIN(UnitPrice) AS MinPrice,
                   MAX(UnitPrice) AS MaxPrice
            FROM dbo.Products
            """
        )
        print_rows(cur, "3a. Product summary stats:")

        # 3b. GROUP BY — one summary row per category.
        cur.execute(
            """
            SELECT Category, COUNT(*) AS NumProducts, SUM(UnitsInStock) AS TotalStock
            FROM dbo.Products
            GROUP BY Category
            """
        )
        print_rows(cur, "3b. Stock totals per category:")

        # 3c. HAVING — filter the groups (like WHERE, but for GROUP BY).
        cur.execute(
            """
            SELECT Category, COUNT(*) AS NumProducts
            FROM dbo.Products
            GROUP BY Category
            HAVING COUNT(*) >= 2
            """
        )
        print_rows(cur, "3c. Categories with 2 or more products:")


# ---------------------------------------------------------------------------
# SECTION 4: JOINs — INNER, LEFT, and multi-table
# ---------------------------------------------------------------------------
# JOINs combine rows from two or more tables using a key. This is why the
# schema is relational: Orders links to Customers, OrderItems links to both
# Orders and Products.
# Docs: https://learn.microsoft.com/sql/t-sql/queries/from-transact-sql


def section_joins():
    print("=" * 60)
    print("SECTION 4: JOINs — INNER, LEFT, multi-table")
    print("=" * 60)

    with connect() as cn:
        cur = cn.cursor() # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor

        # 4a. INNER JOIN — only rows that match in BOTH tables.
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters
        cur.execute(
            """
            SELECT o.OrderId, c.FirstName, c.LastName, o.OrderDate, o.Status
            FROM dbo.Orders o
            INNER JOIN dbo.Customers c ON c.CustomerId = o.CustomerId
            ORDER BY o.OrderId
            """
        )
        print_rows(cur, "4a. Orders with their customer (INNER JOIN):")

        # 4b. LEFT JOIN — ALL customers, even those with no orders.
        cur.execute(
            """
            SELECT c.FirstName, c.LastName, COUNT(o.OrderId) AS NumOrders
            FROM dbo.Customers c
            LEFT JOIN dbo.Orders o ON o.CustomerId = c.CustomerId
            GROUP BY c.FirstName, c.LastName
            ORDER BY NumOrders DESC
            """
        )
        print_rows(cur, "4b. Every customer + order count (LEFT JOIN):")

        # 4c. Multi-table JOIN — Orders + Customers + OrderItems + Products.
        cur.execute(
            """
            SELECT o.OrderId, c.LastName, p.ProductName, oi.Quantity, oi.UnitPrice
            FROM dbo.Orders o
            JOIN dbo.Customers c  ON c.CustomerId  = o.CustomerId
            JOIN dbo.OrderItems oi ON oi.OrderId    = o.OrderId
            JOIN dbo.Products p   ON p.ProductId    = oi.ProductId
            ORDER BY o.OrderId
            """
        )
        print_rows(cur, "4c. Full order detail (4-table JOIN):")

# The following sections (5-10) are not shown here, but they continue 
# the lesson with INSERT, UPDATE, DELETE that are configured for transactions
# ┌─────────────────────────────────────────────────────────────┐
# │ GENERIC DML TRANSACTION FLOW (INSERT / UPDATE / DELETE)     │
# ├─────────────────────────────────────────────────────────────┤
# │ 1. BEGIN TRANSACTION                                        │
# │    with connect(autocommit=False) as cn                     │
# │    → First SQL statement starts implicit transaction        │
# ├─────────────────────────────────────────────────────────────┤
# │ 2. EXECUTE DML OPERATION                                    │
# │    • INSERT ... OUTPUT INSERTED ... /                       │
# │      UPDATE ... SET ... OUTPUT INSERTED ... /               │
# │      DELETE ... OUTPUT DELETED ...                          │
# │    • WHERE clause with parameter placeholder (?)            │
# │    • Parameter passed separately (?, "value")               │
# ├─────────────────────────────────────────────────────────────┤
# │ 3. FETCH OUTPUT RESULTS                                     │
# │    • INSERT: cur.fetchone()[0] → generated ID               │
# │    • UPDATE: cur.fetchall() → new column values             │
# │    • DELETE: cur.fetchall() → deleted IDs                   │
# │    • OUTPUT clause returns post-insert/updated/deleted rows │
# ├─────────────────────────────────────────────────────────────┤
# │ 4. COMMIT                                                   │
# │    cn.commit()                                              │
# │    • Persists changes to database                           │
# │    • Releases row/page locks                                │
# │    • Flushes transaction log to disk                        │
# ├─────────────────────────────────────────────────────────────┤
# │ 5. VERIFY (optional)                                        │
# │    New connection with SELECT to confirm final state        │
# ├─────────────────────────────────────────────────────────────┤
# │ 6. END TRANSACTION                                          │
# │    with block exits → connection closed                     │
# └─────────────────────────────────────────────────────────────┘
# Error Path:
# Any exception before commit → implicit rollback → no changes persisted


# ---------------------------------------------------------------------------
# SECTION 5: CREATE — INSERT with OUTPUT (the C in CRUD)
# ---------------------------------------------------------------------------
# We already saw INSERT in the basics lesson. Here we reuse the OUTPUT clause
# to capture the new identity value, and we wrap it in a transaction so a
# failure rolls back cleanly.
# Docs: https://learn.microsoft.com/sql/t-sql/queries/output-clause-transact-sql


def section_insert():
    print("=" * 60)
    print("SECTION 5: CREATE — INSERT with OUTPUT")
    print("=" * 60)

    # A brand-new customer to insert.
    new_customer = ("Frank", "Ortiz", "frank.ortiz@example.com", "Denver")
    # Using autocommit=False here so we can commit or rollback as a unit.
    # Disables autocommit — changes won't be saved until you explicitly call cn.commit().
    # This is the foundation of the transaction.
    with connect(autocommit=False) as cn:
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor
        cur = cn.cursor()
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters
        # NOTE: SQL Server–specific clause that returns the auto-generated CustomerId
        # immediately after insert (like RETURNING in PostgreSQL).
        # Unpacks the tuple into four separate parameters for the four ? placeholders.
        cur.execute(
            """
            INSERT INTO dbo.Customers (FirstName, LastName, Email, City)
            OUTPUT INSERTED.CustomerId
            VALUES (?, ?, ?, ?)
            """,
            *new_customer,
        )
        # Reads the single-row result from OUTPUT INSERTED.CustomerId to get the new ID.
        new_id = cur.fetchone()[0]
        # Commits the transaction — makes the insert permanent. 
        # Without this, the insert would be rolled back when the with block exits.
        cn.commit()
        print(
            f"Inserted customer '{new_customer[0]} {new_customer[1]}' with Id={new_id}"
        )
        # Critical: If an exception occurs before cn.commit(), the with block exits 
        # and the connection closes, triggering an implicit rollback. The insert never happens.

    # Verify it round-tripped.
    with connect() as cn: # autocommit defaults to True here
        cur = cn.cursor()
        cur.execute(
            "SELECT CustomerId, FirstName, LastName, City FROM dbo.Customers WHERE CustomerId = ?",
            new_id,
        )
        print_rows(cur, "Verification — the new customer:")


# ---------------------------------------------------------------------------
# SECTION 6: UPDATE — change existing rows (the U in CRUD)
# ---------------------------------------------------------------------------
# UPDATE always needs a WHERE clause — without one it changes EVERY row.
# The OUTPUT clause can report which rows changed.
# Docs: https://learn.microsoft.com/sql/t-sql/queries/update-transact-sql


def section_update():
    print("=" * 60)
    print("SECTION 6: UPDATE — change existing rows")
    print("=" * 60)
    # Using autocommit=False here so we can commit or rollback as a unit.
    # Disables autocommit — changes won't be saved until you explicitly call cn.commit().
    # This is the foundation of the transaction.
    with connect(autocommit=False) as cn: # autocommit=False means SQL changes are not saved automatically.
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor
        cur = cn.cursor()
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters
        # NOTE: SQL Server–specific clause that returns the auto-generated 
        # INSERTED.ProductId, INSERTED.ProductName, INSERTED.UnitPrice
        # immediately after insert.
        # Unpacks the tuple into a separate parameter for the ? placeholder.
        # "Desk Lamp" is passed separately as the parameter.
        cur.execute(
            """
            UPDATE dbo.Products
            SET UnitPrice = UnitPrice * 1.10
            OUTPUT INSERTED.ProductId, INSERTED.ProductName, INSERTED.UnitPrice
            WHERE ProductName = ?
            """,
            "Desk Lamp",
        )
        # fetchall() retrieves every row returned by the OUTPUT clause.
        rows = cur.fetchall()
        # Commits the transaction — makes the insert permanent. 
        # Without this, the insert would be rolled back when the with block exits.
        cn.commit()
        # This makes the price change permanent. After the commit: 
        # The database log is made durable. 
        # Other database sessions can see the new price. 
        # Locks held by this transaction are released.
        print("Updated product(s):") # Display the returned values
        for r in rows:
            print(f"  Id={r[0]}, {r[1]}, new price={r[2]:.2f}")

    # Verify through another connection.
    with connect() as cn:
        cur = cn.cursor()
        cur.execute(
            "SELECT ProductName, UnitPrice FROM dbo.Products WHERE ProductName = ?",
            "Desk Lamp",
        )
        print_rows(cur, "Verification — updated price:")


# ---------------------------------------------------------------------------
# SECTION 7: DELETE — remove rows (the D in CRUD)
# ---------------------------------------------------------------------------
# DELETE also needs a WHERE clause. We delete a row we created earlier so the
# seed data stays intact and the lesson is repeatable.
# Docs: https://learn.microsoft.com/sql/t-sql/queries/delete-transact-sql


def section_delete():
    print("=" * 60)
    print("SECTION 7: DELETE — remove rows")
    print("=" * 60)

    # Using autocommit=False here so we can commit or rollback as a unit.
    # Disables autocommit — changes won't be saved until you explicitly call cn.commit().
    # This is the foundation of the transaction.
    with connect(autocommit=False) as cn:
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor
        cur = cn.cursor()

        # Delete the customer we inserted in Section 5 (by email, to be safe).
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters
        cur.execute(
            "DELETE FROM dbo.Customers OUTPUT DELETED.CustomerId WHERE Email = ?",
            "frank.ortiz@example.com",
        )
        # fetchall() retrieves every row returned by the OUTPUT clause.
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#fetchall
        deleted = cur.fetchall() 
        # Commits the transaction — makes the delete permanent.
        cn.commit()
        print(f"Deleted {len(deleted)} customer row(s): {[r[0] for r in deleted]}")

    # Verify.
    with connect() as cn:
        cur = cn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM dbo.Customers WHERE Email = ?",
            "frank.ortiz@example.com",
        )
        print(f"Remaining rows with that email: {cur.fetchone()[0]}")


# ---------------------------------------------------------------------------
# SECTION 8: Explicit Transactions — BEGIN / COMMIT / ROLLBACK
# ---------------------------------------------------------------------------
# A transaction groups several statements so they all succeed or all fail.
# We deliberately force an error mid-way to show ROLLBACK undoing the work.
# Docs: https://learn.microsoft.com/sql/t-sql/language-elements/transactions-transact-sql
# ┌─────────────────────────────────────────────────────────────┐
# │ Connection opened with autocommit = False                   │
# │    → No automatic commit; every statement is pending.       │
# ├─────────────────────────────────────────────────────────────┤
# │ BEGIN TRANSACTION (explicit)                                │
# │    → Transaction is started; all subsequent DML statements  │
# │      are part of this single unit of work.                  │
# ├─────────────────────────────────────────────────────────────┤
# │ INSERT #1 (Grace Lee)                                       │
# │    → Row is written to the transaction log, but not yet     │
# │      committed to the database.                             │
# ├─────────────────────────────────────────────────────────────┤
# │ INSERT #2 (Hank Doe) – violates UNIQUE constraint           │
# │    → DB raises an error→ control jumps to the `except` block│
# ├─────────────────────────────────────────────────────────────┤
# │ ROLLBACK (executed in except)                               │
# │    → All changes made after BEGIN are undone; the DB log    │
# │      is rolled back to the state at the start of the trans  │
# │    → Grace Lee’s row is removed from the transaction’s view │
# ├─────────────────────────────────────────────────────────────┤
# │ End of `with` block – connection closed                     │
# │    → If a commit had occurred, it would have been persisted;│
# │      otherwise implicit rollback (because autocommit=False) │
# │      ensures the transaction is cleaned up.                 │
# └─────────────────────────────────────────────────────────────┘

def section_transactions():
    print("=" * 60)
    print("SECTION 8: Transactions — COMMIT and ROLLBACK")
    print("=" * 60)

    with connect(autocommit=False) as cn:
        cur = cn.cursor()

        # Start an explicit transaction.
        cur.execute("BEGIN TRANSACTION")
        try:
            # This insert succeeds...
            cur.execute(
                """
                INSERT INTO dbo.Customers (FirstName, LastName, Email, City)
                VALUES (?, ?, ?, ?)
                """,
                "Grace",
                "Lee",
                "grace.lee@example.com",
                "Seattle",
            )
            print("Inserted 'Grace Lee' (will be rolled back)")

            # ...but this one violates the UNIQUE constraint on Email, so it
            # raises an error. The whole transaction is now doomed.
            cur.execute(
                """
                INSERT INTO dbo.Customers (FirstName, LastName, Email, City)
                VALUES (?, ?, ?, ?)
                """,
                "Hank",
                "Doe",
                "grace.lee@example.com",
                "Denver",
            )
            cn.commit()
            print("Committed (you should NOT see this)")
        except pyodbc.Error as e:
            # Undo everything since BEGIN TRANSACTION.
            cur.execute("ROLLBACK")
            print(f"Error caught: {e}")
            print("Rolled back — 'Grace Lee' was NOT saved.")

    # Verify Grace is gone.
    with connect() as cn:
        cur = cn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM dbo.Customers WHERE Email = ?",
            "grace.lee@example.com",
        )
        print(f"Rows with grace.lee@example.com after rollback: {cur.fetchone()[0]}")


# ---------------------------------------------------------------------------
# SECTION 9: Stored procedures — CRUD via the database, not raw SQL
# ---------------------------------------------------------------------------
# A stored procedure is SQL logic saved in the database. Calling it from
# Python is just `cursor.execute("EXEC dbo.ProcName ?, ?", ...)`. We use the
# two procedures created in create_pytestdb.sql:
#   • usp_PlaceOrder     — CREATE (inserts an order + line item)
#   • usp_GetOrderDetails— READ (returns header, items, and a total)
# Docs: https://learn.microsoft.com/sql/relational-databases/stored-procedures/execute-a-stored-procedure


def section_stored_procedures():
    print("=" * 60)
    print("SECTION 9: Stored procedures — CRUD both ways")
    print("=" * 60)

    with connect(autocommit=False) as cn:
        cur = cn.cursor()

        # 9a. CREATE via stored procedure. pyodbc has no built-in "output
        #     param" marker, so we wrap the EXEC in a batch that DECLAREs the
        #     output variable, calls the proc, then SELECTs the variable back.
        #     That SELECT is the one result set we read with fetchval().
        order_id = cur.execute(
            """
            DECLARE @OrderId INT;
            EXEC dbo.usp_PlaceOrder
                @CustomerId = ?,   -- Bob Smith
                @ProductId  = ?,   -- Wireless Mouse
                @Quantity   = ?,
                @OrderId    = @OrderId OUTPUT;
            SELECT @OrderId AS OrderId;
            """,
            2,  # CustomerId (Bob Smith)
            1,  # ProductId (Wireless Mouse)
            3,  # Quantity
        ).fetchval()
        cn.commit()
        print(f"usp_PlaceOrder created OrderId={order_id}")

        # 9b. READ via stored procedure. It returns TWO result sets (header
        #     + items) from inside the proc, plus a third from our trailing
        #     `SELECT @Total`. We use nextset() to walk all three.
        cur.execute(
            """
            DECLARE @Total DECIMAL(10,2);
            EXEC dbo.usp_GetOrderDetails
                @OrderId = ?,
                @Total   = @Total OUTPUT;
            SELECT @Total AS Total;
            """,
            order_id,
        )
        print_rows(cur, "9b. Order header (result set 1):")
        cur.nextset()
        print_rows(cur, "9b. Order line items (result set 2):")
        cur.nextset()
        print_rows(cur, "9b. Order total (result set 3, from OUTPUT param):")


# ---------------------------------------------------------------------------
# SECTION 10: Mini task — a full CRUD workflow
# ---------------------------------------------------------------------------
# Combine everything: create a customer, place an order via a stored proc,
# update a price, and delete a stale order. This mirrors a real day of work.


def section_mini_task():
    print("=" * 60)
    print("SECTION 10: Mini task — a full CRUD workflow")
    print("=" * 60)

    with connect(autocommit=False) as cn:
        cur = cn.cursor()

        # 1. CREATE a customer.
        cur.execute(
            """
            INSERT INTO dbo.Customers (FirstName, LastName, Email, City)
            OUTPUT INSERTED.CustomerId
            VALUES (?, ?, ?, ?)
            """,
            "Ivy",
            "Patel",
            "ivy.patel@example.com",
            "Austin",
        )
        cust_id = cur.fetchone()[0]
        print(f"1. Created customer Id={cust_id}")

        # 2. CREATE an order for them via the stored procedure.
        order_id = cur.execute(
            """
            DECLARE @OrderId INT;
            EXEC dbo.usp_PlaceOrder
                @CustomerId = ?,
                @ProductId  = ?,
                @Quantity   = ?,
                @OrderId    = @OrderId OUTPUT;
            SELECT @OrderId AS OrderId;
            """,
            cust_id,
            5,
            2,
        ).fetchval()
        print(f"2. Placed order Id={order_id} via usp_PlaceOrder")

        # 3. UPDATE — raise the Notebook price.
        cur.execute(
            "UPDATE dbo.Products SET UnitPrice = UnitPrice * 1.05 WHERE ProductName = ?",
            "Notebook (Pack)",
        )
        print("3. Raised Notebook price by 5%")

        # 4. READ — confirm the order total via the stored procedure.
        cur.execute(
            """
            DECLARE @Total DECIMAL(10,2);
            EXEC dbo.usp_GetOrderDetails
                @OrderId = ?,
                @Total   = @Total OUTPUT;
            SELECT @Total AS Total;
            """,
            order_id,
        )
        cur.nextset()
        cur.nextset()
        total = cur.fetchone()[0]
        print(f"4. Order {order_id} total = {total:.2f}")

        # 5. DELETE — remove the order we just created (clean up).
        cur.execute("DELETE FROM dbo.OrderItems WHERE OrderId = ?", order_id)
        cur.execute("DELETE FROM dbo.Orders WHERE OrderId = ?", order_id)
        print(f"5. Deleted order {order_id} and its line items")

        cn.commit()
        print("\nMini task complete — all changes committed.")


# ---------------------------------------------------------------------------
# Menu loop
# ---------------------------------------------------------------------------
# Each section is its own function, so you can study it in isolation and
# re-run any part on demand. Type a number to run a section, or `q` to quit.


def main():
    sections = {
        "0": section_setup,
        "c": section_cleanup,
        "1": section_select_basics,
        "2": section_filtering,
        "3": section_aggregates,
        "4": section_joins,
        "5": section_insert,
        "6": section_update,
        "7": section_delete,
        "8": section_transactions,
        "9": section_stored_procedures,
        "10": section_mini_task,
    }

    print("\n🗄️  SQL Server Intermediate — CRUD with pyodbc")
    print("=" * 60)
    print("  0  Setup (create schema + seed + procedures)")
    print("  c  Cleanup (drop tables + procedures to start fresh)")
    print("  1  SELECT basics (WHERE, ORDER BY, TOP, DISTINCT)")
    print("  2  Filtering (LIKE, IN, BETWEEN, IS NULL)")
    print("  3  Aggregates & GROUP BY")
    print("  4  JOINs (INNER, LEFT, multi-table)")
    print("  5  CREATE — INSERT with OUTPUT")
    print("  6  UPDATE — change rows")
    print("  7  DELETE — remove rows")
    print("  8  Transactions — COMMIT / ROLLBACK")
    print("  9  Stored procedures — CRUD both ways")
    print(" 10  Mini task — full CRUD workflow")
    print("  q  Quit")
    print("=" * 60)

    while True:
        choice = (
            input("\nChoose a section (0-10, c for cleanup, or q to quit): ")
            .strip()
            .lower()
        )
        if choice == "q":
            print("Goodbye!")
            break
        if choice in sections:
            try:
                sections[choice]()
            except pyodbc.Error as e:
                print(f"\n⚠️  SQL error: {e}")
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
