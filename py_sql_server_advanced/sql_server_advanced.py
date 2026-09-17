"""
SQL Server Advanced with Python — A Self-Guided Lesson
======================================================
Run this file (with `python sql_server_advanced.py`) and follow along.

This is the THIRD step in SQL Server. We assume you already completed
`py_sql_server_basics` (connecting with pyodbc, casting CSV strings to SQL
types, INSERT + OUTPUT, transactions) and `py_sql_server_intermediate`
(CRUD, JOINs, transactions, stored procedures). Here we level up to the
topics the intermediate folder explicitly deferred:

  1. Indexes            — make queries fast (CREATE INDEX, covering index)
  2. Query tuning       — read execution plans, write sargable predicates
  3. Views              — save a SELECT as a queryable object
  4. CTEs & windows     — WITH, ROW_NUMBER, RANK, LAG/LEAD, OVER(PARTITION BY)
  5. Bulk operations    — executemany, fast_executemany, BULK INSERT
  6. Dynamic SQL        — build queries safely with sp_executesql
  7. Transactions       — isolation levels, savepoints, deadlocks
  8. pandas integration — read_sql / to_sql via a SQLAlchemy engine
  9. Mini task          — combine several of the above

The example data lives in the `PyTestDb` database, created by
`create_pytestdb_advanced.sql` in this folder. It is the same store schema
as intermediate, plus indexes, views, and a trigger:

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


# The SQL script that creates the schema + seed data + indexes + views + trigger.
SETUP_SQL_FILE = data_path("create_pytestdb_advanced.sql")

# ---------------------------------------------------------------------------
# Connection string
# ---------------------------------------------------------------------------
# Same pattern as the basics/intermediate lessons. `Trusted_Connection` uses
# your Windows login; `TrustServerCertificate` skips the TLS cert check for
# local dev.
CONN_STR = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;DATABASE=PyTestDb;"
    "Trusted_Connection=yes;TrustServerCertificate=yes;"
)


def connect(autocommit=False):
    """Open a pyodbc connection to PyTestDb."""
    return pyodbc.connect(
        CONN_STR, autocommit=autocommit
    )  # Doc: https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows


# Title used for the statistics result sets that SET STATISTICS returns.
STATS_TITLE = "Statistics:"


def print_rows(cursor, title=None):
    """Print every row returned by a cursor, with column names as a header."""
    if title:
        print(f"\n{title}")
    # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#description
    cols = [
        d[0] for d in cursor.description
    ]  # Get the column names from the cursor description
    print(" | ".join(cols))  # Print the column headers
    print("-" * 60)  # Print a separator line
    # Print each row, joining the values with " | "
    for row in (
        cursor.fetchall()
    ):  # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#fetchall
        print(" | ".join(str(v) for v in row))


# ---------------------------------------------------------------------------
# SECTION 0: Setup — create the schema, seed data, indexes, views, trigger
# ---------------------------------------------------------------------------
# We run the .sql file by reading it and executing it. The `GO` lines are
# batch separators used by sqlcmd/SSMS — they are NOT valid T-SQL, so we split
# the script on them and execute each batch separately. This matters because
# `CREATE VIEW` / `CREATE TRIGGER` must be the FIRST statement in their batch.
# Docs: https://learn.microsoft.com/sql/tools/sqlcmd/sqlcmd-use-the-utility
def section_setup():
    print("=" * 60)
    print("SECTION 0: Setup — create schema, seed, indexes, views, trigger")
    print("=" * 60)

    # 
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
# SECTION 0b: Cleanup — drop the tables, views, trigger, and audit table
# ---------------------------------------------------------------------------
# So you can start fresh, this drops every object the setup created, plus the
# tables the pandas sections (8 & 9) write via to_sql. Child tables go first
# (OrderItems) so FOREIGN KEY constraints never block us, then parents, then
# the views/trigger/audit table.
# Docs: https://learn.microsoft.com/sql/t-sql/statements/drop-table-transact-sql


def section_cleanup():
    print("=" * 60)
    print("SETUP-CLEANUP: Drop all advanced tables, views, and trigger")
    print("=" * 60)

    # Doc: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
    # This single line does three things at once: opens a database connection, configures
    # it for automatic commits, and guarantees the connection will be cleanly closed when
    # the block ends.
    with connect(autocommit=True) as cn:
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor
        cur = cn.cursor()
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters
        # Drop the pandas-created tables first (sections 8 & 9 write these
        # via to_sql, so they are not part of the core schema).
        cur.execute(
            "IF OBJECT_ID('dbo.TopProductsByCategory', 'U') IS NOT NULL DROP TABLE dbo.TopProductsByCategory;"
        )
        cur.execute(
            "IF OBJECT_ID('dbo.OrderStatusSummary', 'U') IS NOT NULL DROP TABLE dbo.OrderStatusSummary;"
        )
        # Drop the views, trigger, and audit table next, then the child tables,
        # then the parent tables. This order avoids FOREIGN KEY constraint errors.
        cur.execute(
            "IF OBJECT_ID('dbo.v_ProductSales', 'V') IS NOT NULL DROP VIEW dbo.v_ProductSales;"
        )
        cur.execute(
            "IF OBJECT_ID('dbo.v_CustomerOrders', 'V') IS NOT NULL DROP VIEW dbo.v_CustomerOrders;"
        )
        cur.execute(
            "IF OBJECT_ID('dbo.trg_Orders_Audit', 'TR') IS NOT NULL DROP TRIGGER dbo.trg_Orders_Audit;"
        )
        cur.execute(
            "IF OBJECT_ID('dbo.OrderStatusAudit', 'U') IS NOT NULL DROP TABLE dbo.OrderStatusAudit;"
        )
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

    print("All advanced tables, views, and trigger dropped — you can start fresh.")
    print("Hint: run Setup (section 0) to recreate them.")


# ---------------------------------------------------------------------------
# SECTION 1: Indexes — CREATE INDEX, covering index, SET STATISTICS
# ---------------------------------------------------------------------------
# An index is a sorted copy of one or more columns. SQL Server can use it to
# find rows directly (an "index seek") instead of reading every row (a "table
# scan"). To SHOW the difference, we turn on `SET STATISTICS TIME, IO ON`,
# run a query, then read the statistics that SQL Server prints back.
#
# The statistics arrive as extra result sets on the cursor, so we use
# `nextset()` to walk past the actual rows to the stats.
# Docs: https://learn.microsoft.com/sql/relational-databases/indexes/indexes


def section_indexes():
    print("=" * 60)
    print("SECTION 1: Indexes — CREATE INDEX, covering index, statistics")
    print("=" * 60)

    # Doc: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
    # This single line does three things at once: opens a database connection, configures
    # it for automatic commits, and guarantees the connection will be cleanly closed when
    with connect() as cn:
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor
        cur = cn.cursor()

        # 1a. Turn on statistics. From now on, every statement reports its
        #     elapsed time and logical reads as extra result sets.
        cur.execute("SET STATISTICS TIME ON") # Execute the SQL command to enable statistics for time
        cur.execute("SET STATISTICS IO ON") # Execute the SQL command to enable statistics for I/O

        # 1b. A query that filters on Orders.CustomerId. The setup script
        #     created IX_Orders_CustomerId, so this should be an index seek.
        #     Look for "logical reads" and "CPU time" in the stats output.
        cur.execute(
            """
            SELECT OrderId, OrderDate, Status
            FROM dbo.Orders
            WHERE CustomerId = ?
            """,
            1,
        )
        print_rows(cur, "1b. Orders for customer 1 (uses IX_Orders_CustomerId):")
        # Walk to the statistics result sets and print them.
        while cur.nextset():
            if cur.description:
                print_rows(cur, STATS_TITLE)

        # 1c. A query that the covering index IX_OrderItems_OrderId_Product
        #     can answer entirely from the index (no table access). The
        #     INCLUDE columns (Quantity, UnitPrice) make it "covering".
        cur.execute(
            """
            SELECT OrderId, ProductId, Quantity, UnitPrice
            FROM dbo.OrderItems
            WHERE OrderId = ?
            """,
            1,
        )
        print_rows(cur, "1c. Line items for order 1 (covering index):")
        while cur.nextset():
            if cur.description:
                print_rows(cur, STATS_TITLE)

        # 1d. Show the indexes that exist on the tables, so you can see what
        #     the setup script created. sys.indexes lists every index.
        cur.execute(
            """
            SELECT t.name AS TableName, i.name AS IndexName, i.is_primary_key
            FROM sys.tables t
            JOIN sys.indexes i ON i.object_id = t.object_id
            WHERE t.name IN ('Orders', 'OrderItems')
            ORDER BY t.name, i.name
            """
        )
        print_rows(cur, "1d. Indexes on Orders and OrderItems:")

        # Turn statistics back off so later sections aren't noisy.
        cur.execute("SET STATISTICS TIME OFF")
        cur.execute("SET STATISTICS IO OFF")


# ---------------------------------------------------------------------------
# SECTION 2: Query tuning — execution plans, sargable predicates
# ---------------------------------------------------------------------------
# `SET SHOWPLAN_ALL ON` makes SQL Server return the EXECUTION PLAN for a
# query instead of running it. The plan shows the operations (scan vs. seek,
# join type, estimated rows) that tell you WHY a query is slow.
#
# We also compare a "sargable" predicate (one that can use an index) with a
# "non-sargable" one (a function call on the column, which forces a scan).
# Docs: https://learn.microsoft.com/sql/relational-databases/performance/execution-plans


def section_query_tuning():
    print("=" * 60)
    print("SECTION 2: Query tuning — execution plans, sargable predicates")
    print("=" * 60)

    # Doc: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
    # This single line does three things at once: opens a database connection, configures
    # it for automatic commits, and guarantees the connection will be cleanly closed when
    with connect() as cn:
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor
        cur = cn.cursor()

        # 2a. Show the execution plan for a JOIN query. The plan is returned
        #     as rows; we print the operation type and estimated rows.
        #     NOTE: SHOWPLAN_ALL does not accept bound `?` parameters, so we
        #     inline a fixed, whitelisted literal here (safe — it is not user
        #     input). The plan columns are: 4=PhysicalOp, 5=LogicalOp,
        #     6=Argument (the object), 8=EstimateRows.
        cur.execute("SET SHOWPLAN_ALL ON") # Execute the SQL command to enable the display of execution plans
        # Doc: https://learn.microsoft.com/sql/relational-databases/performance/execution-plans
        cur.execute(
            """
            SELECT o.OrderId, c.LastName, o.Status
            FROM dbo.Orders o
            JOIN dbo.Customers c ON c.CustomerId = o.CustomerId
            WHERE o.Status = 'Pending'
            """
        )
        print("\n2a. Execution plan for a JOIN (operation | object | est. rows):")
        # Walk through the result set and print the relevant columns from the execution plan
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#fetchall
        for row in cur.fetchall():
            op = row[4] or row[5]  # PhysicalOp, falling back to LogicalOp
            obj = row[6]  # Argument (the table/index object)
            est = row[8]  # EstimateRows
            if op:
                print(f"  {op} | {obj} | est. rows: {est}")
        cur.execute("SET SHOWPLAN_ALL OFF") # Execute the SQL command to disable the display of execution plans

        # 2b. Sargable vs. non-sargable. A predicate is "sargable" (search
        #     ARGument-able) when the column stands alone, so an index can be
        #     used. Wrapping the column in a function makes it non-sargable.
        #     Compare the logical reads of these two — the second scans.
        cur.execute("SET STATISTICS IO ON") # Execute the SQL command to enable statistics for I/O

        # Sargable: the column is compared directly. Can use an index.
        cur.execute(
            "SELECT OrderId, Status FROM dbo.Orders WHERE OrderDate = ?",
            "2026-06-01",
        )
        print_rows(cur, "2b. Sargable predicate (OrderDate = ?):")
        while cur.nextset():
            if cur.description:
                print_rows(cur, STATS_TITLE) # Print the statistics result set

        # Non-sargable: the column is wrapped in a function, so SQL Server
        # must evaluate the function for EVERY row — no index can help.
        cur.execute(
            "SELECT OrderId, Status FROM dbo.Orders WHERE YEAR(OrderDate) = ?",
            2026,
        )
        print_rows(cur, "2b. Non-sargable predicate (YEAR(OrderDate) = ?):")
        while cur.nextset():
            if cur.description:
                print_rows(cur, STATS_TITLE) # Print the statistics result set

        cur.execute("SET STATISTICS IO OFF") # Execute the SQL command to disable statistics for I/O

        # 2c. Avoid SELECT *. Naming only the columns you need lets a
        #     covering index answer the query and reduces network traffic.
        cur.execute(
            "SELECT ProductId, ProductName, UnitPrice FROM dbo.Products WHERE Category = ?",
            "Electronics",
        )
        print_rows(cur, "2c. Explicit column list (index-friendly):")


# ---------------------------------------------------------------------------
# SECTION 3: Views — CREATE VIEW, query through a view, update through a view
# ---------------------------------------------------------------------------
# A view is a saved SELECT statement you can query like a table. It does NOT
# store data — every SELECT from it runs the underlying query. Views hide
# JOIN complexity and centralize a query in one place.
#
# The setup script created two views:
#   • v_CustomerOrders — a customer + order JOIN
#   • v_ProductSales    — an aggregated sales summary
# Docs: https://learn.microsoft.com/sql/relational-databases/views/views


def section_views():
    print("=" * 60)
    print("SECTION 3: Views — query through and update through a view")
    print("=" * 60)

    # Doc: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
    # This single line does three things at once: opens a database connection, configures
    # it for automatic commits, and guarantees the connection will be cleanly closed when
    with connect() as cn:
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor
        cur = cn.cursor()

        # 3a. Query the JOIN view as if it were a table. No JOIN needed here —
        #     the view already did it.
        cur.execute(
            """
            SELECT OrderId, FirstName, LastName, City, Status
            FROM dbo.v_CustomerOrders
            WHERE City = ?
            ORDER BY OrderId
            """,
            "Seattle",
        )
        print_rows(cur, "3a. Seattle orders via v_CustomerOrders:")

        # 3b. Query the aggregated sales view.
        cur.execute(
            """
            SELECT ProductName, Category, TotalSold, TotalRevenue
            FROM dbo.v_ProductSales
            ORDER BY TotalRevenue DESC
            """
        )
        print_rows(cur, "3b. Product sales via v_ProductSales:")

        # 3c. UPDATE through a view. A view that maps to a SINGLE table (no
        #     JOIN, no aggregate) is "updatable" — the change flows to the
        #     underlying table. v_CustomerOrders is a JOIN, so it is NOT
        #     updatable; we use a direct UPDATE on Products instead to show
        #     the concept, then confirm it through the view.
        cur.execute(
            "UPDATE dbo.Products SET UnitsInStock = UnitsInStock + 10 WHERE ProductName = ?",
            "Desk Lamp",
        )
        cn.commit()
        cur.execute(
            """
            SELECT ProductName, UnitsInStock
            FROM dbo.Products
            WHERE ProductName = ?
            """,
            "Desk Lamp",
        )
        print_rows(cur, "3c. Updated stock, confirmed via the table:")


# ---------------------------------------------------------------------------
# SECTION 4: CTEs & window functions — WITH, ROW_NUMBER, RANK, LAG/LEAD
# ---------------------------------------------------------------------------
# A Common Table Expression (CTE) is a named, temporary result set you define
# with `WITH` and then SELECT from — like a view that lives only for one
# query. Window functions compute a value ACROSS a group of rows (a "window")
# WITHOUT collapsing them into one row (unlike GROUP BY).
# Docs: https://learn.microsoft.com/sql/t-sql/queries/with-common-table-expression-transact-sql


def section_ctes_windows():
    print("=" * 60)
    print("SECTION 4: CTEs & window functions")
    print("=" * 60)

    # Doc: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
    # This single line does three things at once: opens a database connection, configures
    # it for automatic commits, and guarantees the connection will be cleanly closed when
    with connect() as cn:
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor
        cur = cn.cursor()

        # 4a. A CTE that computes each order's total, then a query that uses
        #     it. The CTE is defined once and referenced by name.
        cur.execute(
            """
            WITH OrderTotals AS (
                SELECT OrderId, SUM(Quantity * UnitPrice) AS Total
                FROM dbo.OrderItems
                GROUP BY OrderId
            )
            SELECT o.OrderId, o.Status, ot.Total
            FROM dbo.Orders o
            JOIN OrderTotals ot ON ot.OrderId = o.OrderId
            ORDER BY ot.Total DESC
            """
        )
        print_rows(cur, "4a. Order totals via a CTE:")

        # 4b. ROW_NUMBER() — number each row within a partition. Here we
        #     number products within each category by price (1 = cheapest).
        cur.execute(
            """
            SELECT Category, ProductName, UnitPrice,
                   ROW_NUMBER() OVER (PARTITION BY Category ORDER BY UnitPrice) AS PriceRank
            FROM dbo.Products
            ORDER BY Category, PriceRank
            """
        )
        print_rows(cur, "4b. ROW_NUMBER() within each category:")

        # 4c. RANK() — like ROW_NUMBER but ties get the SAME rank (with gaps).
        cur.execute(
            """
            SELECT Category, ProductName, UnitPrice,
                   RANK() OVER (ORDER BY UnitPrice DESC) AS PriceRank
            FROM dbo.Products
            ORDER BY PriceRank
            """
        )
        print_rows(cur, "4c. RANK() over all products (ties share a rank):")

        # 4d. LAG() / LEAD() — look at the PREVIOUS / NEXT row. Here we show
        #     each order's date next to the customer's PREVIOUS order date.
        cur.execute(
            """
            SELECT OrderId, CustomerId, OrderDate,
                   LAG(OrderDate) OVER (PARTITION BY CustomerId ORDER BY OrderDate) AS PrevOrderDate
            FROM dbo.Orders
            ORDER BY CustomerId, OrderDate
            """
        )
        print_rows(cur, "4d. LAG() — previous order date per customer:")


# ---------------------------------------------------------------------------
# SECTION 5: Bulk operations — executemany, fast_executemany, BULK INSERT
# ---------------------------------------------------------------------------
# Inserting one row at a time is slow. `executemany()` reuses ONE prepared
# INSERT for many rows. `fast_executemany=True` (a pyodbc option) batches
# them into a single round-trip for a big speed-up.
#
# We also show `BULK INSERT`, which loads a CSV file directly into a table
# using SQL Server's own bulk loader — the fastest way to move a file in.
# Docs: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executemany


def section_bulk_operations():
    print("=" * 60)
    print("SECTION 5: Bulk operations — executemany, fast_executemany")
    print("=" * 60)

    # A list of (FirstName, LastName, Email, City) tuples to insert.
    new_customers = [
        ("Grace", "Lee", "grace.lee@example.com", "Seattle"),
        ("Hank", "Doe", "hank.doe@example.com", "Denver"),
        ("Ivy", "Patel", "ivy.patel@example.com", "Austin"),
        ("Jack", "Brown", "jack.brown@example.com", "Portland"),
    ]

    # 5a. executemany() — one prepared INSERT, many parameter sets.
    # Doc: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
    # This single line does three things at once: opens a database connection, configures
    # it for manual commits, and guarantees the connection will be cleanly closed when
    with connect(autocommit=False) as cn:
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor
        cur = cn.cursor()
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executemanysql-params-with-fast_executemanyfalse-the-default
        cur.executemany(
            """
            INSERT INTO dbo.Customers (FirstName, LastName, Email, City)
            VALUES (?, ?, ?, ?)
            """,
            new_customers,
        )
        cn.commit() # Commit the transaction to persist the inserted rows
        # NOTE: pyodbc does not track rowcount for executemany (it reports
        # -1), so we report the number of parameter sets we passed in.
        print(f"5a. executemany() inserted {len(new_customers)} rows.")

    # 5b. fast_executemany=True — the same thing, but pyodbc batches the
    #     rows into fewer round-trips. Enable it on the cursor.
    fast_customers = [
        ("Kim", "Chen", "kim.chen@example.com", "Seattle"),
        ("Leo", "Meyer", "leo.meyer@example.com", "Austin"),
    ]
    # Doc: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
    # This single line does three things at once: opens a database connection, configures
    # it for manual commits, and guarantees the connection will be cleanly closed when
    with connect(autocommit=False) as cn:
        cur = cn.cursor()
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executemanysql-params-with-fast_executemanytrue
        cur.fast_executemany = True # Enable fast_executemany for the cursor
        cur.executemany(
            """
            INSERT INTO dbo.Customers (FirstName, LastName, Email, City)
            VALUES (?, ?, ?, ?)
            """,
            fast_customers,
        )
        cn.commit() # Commit the transaction to persist the inserted rows
        print(f"5b. fast_executemany inserted {len(fast_customers)} rows.")

    # 5c. BULK INSERT — load a CSV file directly. The file must be readable
    #     by the SQL Server process, so we use a temp table + INSERT ... FROM
    #     OPENROWSET is complex; instead we show the classic BULK INSERT
    #     syntax against a file path. (Adjust the path to your machine.)
    #     Docs: https://learn.microsoft.com/sql/relational-databases/import-export/bulk-import-data
    print("\n5c. BULK INSERT loads a CSV directly into a table:")
    print("    (See the commented example below — it needs a server-side path.)")
    # Example (uncomment and adjust the path to run it):
    # with connect(autocommit=True) as cn:
    #     cn.execute(
    #         """
    #         BULK INSERT dbo.Customers
    #         FROM 'C:/path/to/customers.csv'
    #         WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\\n', FIRSTROW = 2)
    #         """
    #     )

    # Verify how many customers we now have (seed 5 + 6 inserted above).
    with connect() as cn:
        cur = cn.cursor()
        cur.execute("SELECT COUNT(*) FROM dbo.Customers")
        print(f"Total customers now: {cur.fetchone()[0]}")


# ---------------------------------------------------------------------------
# SECTION 6: Dynamic SQL — build queries safely with sp_executesql
# ---------------------------------------------------------------------------
# Sometimes you must build part of a query at runtime (e.g. a column name or
# a sort direction that can't be a `?` parameter). The SAFE way is to pass
# the dynamic part to `sp_executesql` and keep the VALUES as bound parameters.
#
# NEVER build SQL by string concatenation with user input — that is how SQL
# injection happens. Here the dynamic part is a fixed, whitelisted column
# name, and the value is still a bound `?` parameter.
# Docs: https://learn.microsoft.com/sql/relational-databases/system-stored-procedures/sp-executesql-transact-sql


def section_dynamic_sql():
    print("=" * 60)
    print("SECTION 6: Dynamic SQL — sp_executesql with bound parameters")
    print("=" * 60)

    # Doc: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
    # This single line does three things at once: opens a database connection, configures
    # it for automatic commits, and guarantees the connection will be cleanly closed when
    with connect() as cn:
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor
        cur = cn.cursor()

        # 6a. A dynamic query: the SORT COLUMN is chosen at runtime, but the
        #     value is still a bound parameter. sp_executesql takes the SQL
        #     text, a parameter declaration, then the parameter values.
        sort_column = "UnitPrice"  # whitelisted — never take this from a user
        sql = f"""
            SELECT ProductName, Category, UnitPrice
            FROM dbo.Products
            WHERE Category = @cat
            ORDER BY {sort_column} DESC
        """
        cur.execute(
            "EXEC sp_executesql N'"
            + sql.replace("'", "''")
            + "', N'@cat NVARCHAR(50)', @cat=?",
            "Electronics",
        )
        print_rows(cur, "6a. Dynamic ORDER BY with a bound WHERE value:")

        # 6b. Show the danger we are avoiding: building SQL by concatenating
        #     a value is how injection happens. We do NOT run this — we just
        #     print what the unsafe version would look like.
        user_input = "Electronics' OR '1'='1"
        unsafe_sql = "SELECT * FROM dbo.Products WHERE Category = '" + user_input + "'"
        print("\n6b. NEVER do this (string concatenation):")
        print(f"    {unsafe_sql}")
        print("    The injected OR '1'='1' would return EVERY row.")
        print("    Always use a bound ? parameter instead.")


# ---------------------------------------------------------------------------
# SECTION 7: Transactions & isolation — isolation levels, savepoints, deadlock
# ---------------------------------------------------------------------------
# An isolation level controls how much one transaction can "see" of another's
# uncommitted changes. We also show SAVEPOINT (roll back part of a
# transaction) and how a deadlock is detected and handled.
# Docs: https://learn.microsoft.com/sql/t-sql/statements/set-transaction-isolation-level-transact-sql


def section_transactions_isolation():
    print("=" * 60)
    print("SECTION 7: Transactions & isolation — levels, savepoints, deadlock")
    print("=" * 60)

    # Doc: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
    # This single line does three things at once: opens a database connection, configures
    # it for automatic commits, and guarantees the connection will be cleanly closed when
    with connect() as cn:
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor
        cur = cn.cursor()

        # 7a. Show the current isolation level, then set it explicitly.
        cur.execute("SELECT @@TRANCOUNT AS OpenTransactions") # Execute the SQL command to get the current open transaction count
        print_rows(cur, "7a. Current open transaction count (0 = none):")
        cur.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED") # Execute the SQL command to set the isolation level to READ COMMITTED
        print("    Isolation level set to READ COMMITTED (the default).")

        # 7b. SAVEPOINT — mark a point you can roll back TO without undoing
        #     the whole transaction. We insert a row, set a savepoint, insert
        #     another, then roll back to the savepoint: the first insert
        #     survives, the second is undone.
        #     SQL Server calls these "savepoints" but uses the syntax
        #     `SAVE TRANSACTION <name>` and `ROLLBACK TRANSACTION <name>`.
        cur.execute("BEGIN TRANSACTION") # Begin a new transaction
        cur.execute(
            "INSERT INTO dbo.Customers (FirstName, LastName, Email, City) VALUES (?, ?, ?, ?)",
            "Mia",
            "Clark",
            "mia.clark@example.com",
            "Denver",
        )
        cur.execute("SAVE TRANSACTION sp_after_mia") # Set a savepoint named 'sp_after_mia'
        cur.execute(
            "INSERT INTO dbo.Customers (FirstName, LastName, Email, City) VALUES (?, ?, ?, ?)",
            "Noah",
            "Wong",
            "noah.wong@example.com",
            "Austin",
        )
        cur.execute("ROLLBACK TRANSACTION sp_after_mia")
        cn.commit()
        print("7b. Inserted 'Mia Clark', set a savepoint, inserted 'Noah Wong',")
        print("    then rolled back to the savepoint. Mia survives, Noah is undone.")

        # 7c. Deadlock handling. A deadlock happens when two transactions each
        #     hold a lock the other needs. SQL Server picks a victim and
        #     raises error 1205. We simulate it with two THREADS: each locks
        #     one product row, then each tries to lock the OTHER's row. They
        #     can never both finish, so SQL Server kills one (error 1205).
        #     We catch that error and roll back the loser.
        #     Docs: https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-deadlocks-guide?view=sql-server-ver17
        import threading # Import the threading module to create concurrent threads

        print("\n7c. Simulating a deadlock (two threads, opposite lock order)...")
        results = {}

        def worker(name, first_row, second_row):
            conn = connect(autocommit=False)
            try:
                # Lock our own row first.
                conn.execute(
                    "UPDATE dbo.Products SET UnitsInStock = UnitsInStock WHERE ProductId = ?",
                    first_row,
                )
                # Give the other thread time to lock ITS row, then try to
                # lock the other's row. This is where the deadlock happens.
                import time

                time.sleep(0.5)
                conn.execute(
                    "UPDATE dbo.Products SET UnitsInStock = UnitsInStock WHERE ProductId = ?",
                    second_row,
                )
                conn.commit()
                results[name] = "committed"
            except pyodbc.Error as e:
                conn.rollback()
                results[name] = f"deadlock victim: {e}"
            finally:
                conn.close()

        t1 = threading.Thread(target=worker, args=("conn1", 1, 2))
        t2 = threading.Thread(target=worker, args=("conn2", 2, 1))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        for name in ("conn1", "conn2"):
            print(f"    {name}: {results.get(name)}")
        print("    SQL Server chose a victim (error 1205). In real code you")
        print("    would ROLLBACK and retry the losing transaction.")

        # 7d. Show the audit trigger fired: the trigger in the setup script
        #     logs Status changes. We change an order's status and read the
        #     audit table to show the automatic log row.
        cur.execute("UPDATE dbo.Orders SET Status = 'Shipped' WHERE OrderId = 2")
        cn.commit()
        cur.execute(
            """
            SELECT OrderId, OldStatus, NewStatus, ChangedAt
            FROM dbo.OrderStatusAudit
            ORDER BY AuditId
            """
        )
        print_rows(cur, "7d. Audit log written automatically by the trigger:")


# ---------------------------------------------------------------------------
# SECTION 8: pandas ↔ SQL Server — read_sql and to_sql via SQLAlchemy
# ---------------------------------------------------------------------------
# pandas can read a SQL query straight into a DataFrame and write a DataFrame
# back to a table. The cleanest way is a SQLAlchemy engine, which wraps the
# pyodbc connection string. This is how you move data between your analysis
# (pandas) and your database.
# Docs: https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html


def section_pandas():
    print("=" * 60)
    print("SECTION 8: pandas ↔ SQL Server — read_sql and to_sql")
    print("=" * 60)

    # Lazy imports
    # Import pandas and SQLAlchemy lazily so the rest of the lesson works
    # even if they aren't installed.
    import pandas as pd
    from sqlalchemy import create_engine

    # Building the engine
    # Build a SQLAlchemy engine from the same ODBC connection string. The
    # `mssql+pyodbc://` prefix tells SQLAlchemy which dialect + driver to use.
    # -------------------------------------------------------------------------
    # The SQLAlchemy engine is the entry point to the database — think of it
    # as a connection factory with a built-in connection pool (roughly analogous
    # to a connection pool in ADO.NET).
    engine = create_engine(
        "mssql+pyodbc://"
        "?odbc_connect=" + CONN_STR.replace(";", "%3B").replace("=", "%3D")
    )
    # Explanation of the connection string encoding:
    # mssql+pyodbc:// — dialect (mssql) + DBAPI driver (pyodbc). This is how SQLAlchemy knows what to talk to and how.
    # "?odbc_connect=" — a special parameter that lets you hand the raw ODBC connection string straight through to pyodbc,
    # instead of spelling out server/database/credentials in SQLAlchemy's own URL format.
    # The .replace() calls URL-encode the ODBC string: ; becomes %3B and = becomes %3D. This is necessary
    # because ; and = are structurally meaningful in a URL (parameter separators and key/value delimiters), so
    # the raw string like DRIVER=...;SERVER=... would otherwise be mangled during URL parsing.

    # 8a. read_sql — run a query and get a DataFrame.
    # (DataBase → DataFrame)
    # ------------------------------------------------------------------------
    # What this does:
    # Runs a SELECT with a JOIN and returns the result as a DataFrame, which is essentially an in-memory rectangular
    # dataset — the pandas equivalent of filling a DataTable. Passing the "engine" (rather than an open connection)
    # lets pandas borrow a pooled connection, run the query, and return it automatically. df.to_string(index=False)
    # just prints the data without pandas' synthetic row-number index column.
    df = pd.read_sql(
        """
        SELECT o.OrderId, c.LastName, o.OrderDate, o.Status
        FROM dbo.Orders o
        JOIN dbo.Customers c ON c.CustomerId = o.CustomerId
        ORDER BY o.OrderId
        """,
        engine,
    )
    print("8a. Orders as a pandas DataFrame:")
    print(df.to_string(index=False))

    # 8b. to_sql — write a DataFrame to a NEW table. `if_exists='replace'` drops any existing table of that name first.
    # (DataFrame → DataBase)
    # ------------------------------------------------------------------------
    # This is GROUP BY Status, COUNT(*): group by Status, count rows per group, then promote the index
    # back into a real column named OrderCount.
    summary = df.groupby("Status").size().reset_index(name="OrderCount")
    # The next line Creates a table named OrderStatusSummary (in the login's default schema — typically
    # dbo on SQL Server) and inserts the rows. Column SQL types are inferred from the DataFrame dtypes.
    # Note that the if_exists="replace" drops the table first if it already exists. The three options are worth knowing:
    # - 'fail': Raise a ValueError if the table already exists.
    # - 'replace': Drop the existing table and create a new one.
    # - 'append': Append the DataFrame to the existing table.
    summary.to_sql("OrderStatusSummary", engine, if_exists="replace", index=False)
    print("\n8b. Wrote a summary DataFrame to dbo.OrderStatusSummary.")

    # 8c. Read it back to confirm the round-trip.
    back = pd.read_sql("SELECT * FROM dbo.OrderStatusSummary ORDER BY Status", engine)
    print("8c. Read back from the new table:")
    print(back.to_string(index=False))

    # Cleanup
    #  closes all pooled connections. Not strictly required (the process exit would clean up
    # anyway), but good hygiene in longer-lived scripts.
    engine.dispose()


# ---------------------------------------------------------------------------
# SECTION 9: Mini task — a combined workflow
# ---------------------------------------------------------------------------
# Combine several advanced ideas: use a CTE + window function to find the
# top-selling product, read it into pandas, and write a summary back — all in
# one realistic workflow.


def section_mini_task():
    print("=" * 60)
    print("SECTION 9: Mini task — CTE + window + pandas workflow")
    print("=" * 60)

    # Lazy imports
    # Import pandas and SQLAlchemy lazily so the rest of the lesson works
    # even if they aren't installed.
    import pandas as pd
    from sqlalchemy import create_engine

    # Building the engine
    # Build a SQLAlchemy engine from the same ODBC connection string. The
    # `mssql+pyodbc://` prefix tells SQLAlchemy which dialect + driver to use.
    # -------------------------------------------------------------------------
    # The SQLAlchemy engine is the entry point to the database — think of it
    # as a connection factory with a built-in connection pool (roughly analogous
    # to a connection pool in ADO.NET).
    engine = create_engine(
        "mssql+pyodbc://"
        "?odbc_connect=" + CONN_STR.replace(";", "%3B").replace("=", "%3D")
    )
    # Explanation of the connection string encoding:
    # mssql+pyodbc:// — dialect (mssql) + DBAPI driver (pyodbc). This is how SQLAlchemy knows what to talk to and how.
    # "?odbc_connect=" — a special parameter that lets you hand the raw ODBC connection string straight through to pyodbc,
    # instead of spelling out server/database/credentials in SQLAlchemy's own URL format.
    # The .replace() calls URL-encode the ODBC string: ; becomes %3B and = becomes %3D. This is necessary
    # because ; and = are structurally meaningful in a URL (parameter separators and key/value delimiters), so
    # the raw string like DRIVER=...;SERVER=... would otherwise be mangled during URL parsing.
    # -------------------------------------------------------------------------
    # 1. Use a CTE + ROW_NUMBER to rank products by revenue within category.
    # The SQL — the real meat of this section
    # The query answers: "What's the best-selling product in each category, by revenue?"
    df = pd.read_sql(
        """
        WITH Ranked AS (
            SELECT p.ProductName, p.Category,
                   SUM(oi.Quantity * oi.UnitPrice) AS Revenue,
                   ROW_NUMBER() OVER (PARTITION BY p.Category
                                      ORDER BY SUM(oi.Quantity * oi.UnitPrice) DESC) AS rn
            FROM dbo.Products p
            LEFT JOIN dbo.OrderItems oi ON oi.ProductId = p.ProductId
            GROUP BY p.ProductName, p.Category
        )
        SELECT ProductName, Category, Revenue
        FROM Ranked
        WHERE rn = 1
        ORDER BY Revenue DESC
        """,
        engine,
    )
    print("1. Top-selling product in each category (CTE + ROW_NUMBER):")
    print(df.to_string(index=False)) # Print the resulting DataFrame without the index column

    # 2. Write the result to a table via pandas.
    # The next line creates a table named TopProductsByCategory (in the login's default schema — typically
    # dbo on SQL Server) and inserts the rows. Column SQL types are inferred from the DataFrame dtypes.
    # Note that the if_exists="replace" drops the table first if it already exists.
    df.to_sql("TopProductsByCategory", engine, if_exists="replace", index=False)
    print("\n2. Wrote the top-products DataFrame to dbo.TopProductsByCategory.")

    # 3. Read it back with plain pyodbc to confirm the round-trip.
    # Doc: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
    with connect() as cn:
        # Doc: https://pyodbc.readthedocs.io/en/latest/ref/cursor.html
        cur = cn.cursor()
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters
        cur.execute(
            "SELECT ProductName, Category, Revenue FROM dbo.TopProductsByCategory ORDER BY Revenue DESC"
        )
        print_rows(cur, "3. Confirmed via pyodbc:")
    # Cleanup
    engine.dispose()


# ---------------------------------------------------------------------------
# Menu loop
# ---------------------------------------------------------------------------
# Each section is its own function, so you can study it in isolation and
# re-run any part on demand. Type a number to run a section, or `q` to quit.


def main():
    sections = {
        "0": section_setup,
        "c": section_cleanup,
        "1": section_indexes,
        "2": section_query_tuning,
        "3": section_views,
        "4": section_ctes_windows,
        "5": section_bulk_operations,
        "6": section_dynamic_sql,
        "7": section_transactions_isolation,
        "8": section_pandas,
        "9": section_mini_task,
    }

    print("\n🗄️  SQL Server Advanced — Performance, Schema & Integration")
    print("=" * 60)
    print("  0  Setup (create schema + seed + indexes + views + trigger)")
    print("  c  Cleanup (drop tables + views + trigger to start fresh)")
    print("  1  Indexes (CREATE INDEX, covering index, statistics)")
    print("  2  Query tuning (execution plans, sargable predicates)")
    print("  3  Views (query through, update through)")
    print("  4  CTEs & window functions (ROW_NUMBER, RANK, LAG/LEAD)")
    print("  5  Bulk operations (executemany, fast_executemany)")
    print("  6  Dynamic SQL (sp_executesql, safe parameterization)")
    print("  7  Transactions & isolation (levels, savepoints, deadlock)")
    print("  8  pandas ↔ SQL Server (read_sql, to_sql)")
    print("  9  Mini task — combined workflow")
    print("  q  Quit")
    print("=" * 60)

    while True:
        choice = (
            input("\nChoose a section (0-9, c for cleanup, or q to quit): ")
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
