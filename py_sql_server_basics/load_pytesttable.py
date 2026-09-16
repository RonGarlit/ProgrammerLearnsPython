"""
PyTestTable Loader with pyodbc — A Self-Guided Lesson
=====================================================
Run this file (with `python load_pytesttable.py`) and follow the menu.

This is the FIRST step in SQL Server. We teach how to move data from a CSV
file into a SQL Server table. CSV cells are always *strings*, so we must cast
each one to the correct SQL Server type before inserting. We exercise *every
major type family* — including the tricky ones (XML, HIERARCHYID, GEOGRAPHY,
GEOMETRY, SQL_VARIANT) — with realistic boundary data, NULL handling, and CSV
edge cases all in one place.

This menu-driven lesson has three actions:

  1. Setup    — run `create_pytesttable.sql` to create the `dbo.PyTestTable`
                table (the script is idempotent, so re-running is safe).
  2. Load     — read the CSV, cast each value to the right SQL type, INSERT
                with an OUTPUT clause, set HIERARCHYID, commit, and verify.
  3. Cleanup  — drop the table so you can start fresh.

What we do, step by step:
  1. Connect to SQL Server with pyodbc.
  2. Read the test rows from `pytesttable_data.csv` (UTF-8 with BOM).
  3. INSERT each row with an OUTPUT clause to capture the new Id.
  4. UPDATE the HIERARCHYID value after the insert (it can't go in the
     same statement easily).
  5. Commit the transaction.
  6. Run a verification query and print the results.

Docs: https://github.com/mkleehammer/pyodbc
"""

# pyodbc is NOT built into Python — it must be installed first.
#   pip install pyodbc
# If this import fails, see the README.md "Prerequisites" section.
import csv
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


CSV_FILE = data_path("pytesttable_data.csv")  # Path to the CSV file with test data
SETUP_SQL_FILE = data_path(
    "create_pytesttable.sql"
)  # Path to the SQL script that creates the PyTestTable

# ---------------------------------------------------------------------------
# Connection string
# ---------------------------------------------------------------------------
# Adjust SERVER / DATABASE to match your environment. `Trusted_Connection`
# uses your Windows login (no password in the string). `TrustServerCertificate`
# skips the TLS cert check for local development.
CONN_STR = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;DATABASE=PyTestDb;"
    "Trusted_Connection=yes;TrustServerCertificate=yes;"
)

# ---------------------------------------------------------------------------
# INSERT statement with an OUTPUT clause
# ---------------------------------------------------------------------------
# The OUTPUT clause returns the auto-generated Id so we know what row was
# inserted. Each `?` is a placeholder that pyodbc fills in safely (no SQL
# injection). Notice the many CAST/CONVERT calls: the CSV gives us strings,
# and SQL Server needs them converted to the right data types.
# Docs: https://learn.microsoft.com/sql/t-sql/queries/output-clause-transact-sql
INSERT_SQL = """
INSERT INTO dbo.PyTestTable (
    ColBigInt, ColInt, ColSmallInt, ColTinyInt, ColBit,
    ColDecimal, ColNumeric, ColMoney, ColSmallMoney,
    ColFloat, ColReal,
    ColDate, ColTime, ColDateTime, ColDateTime2, ColDateTimeOffset, ColSmallDateTime,
    ColChar, ColVarChar, ColVarCharMax,
    ColNChar, ColNVarChar, ColNVarCharMax,
    ColBinary, ColVarBinary, ColVarBinaryMax,
    ColUniqueIdentifier,
    ColXml,
    ColSqlVariant,
    ColGeography,
    ColGeometry
) OUTPUT INSERTED.Id
VALUES (
    ?, ?, ?, ?, ?,
    CAST(? AS DECIMAL(18,4)), CAST(? AS NUMERIC(10,2)),
    CAST(? AS MONEY), CAST(? AS SMALLMONEY),
    ?, ?,
    CAST(? AS DATE), CAST(? AS TIME),
    CAST(? AS DATETIME), CAST(? AS DATETIME2),
    CAST(? AS DATETIMEOFFSET), CAST(? AS SMALLDATETIME),
    CAST(? AS CHAR(10)), ?, ?,
    CAST(? AS NCHAR(10)), ?, ?,
    CONVERT(BINARY(16), ?, 1),
    CONVERT(VARBINARY(100), ?, 1),
    CONVERT(VARBINARY(MAX), ?, 1),
    CAST(? AS UNIQUEIDENTIFIER),
    CAST(? AS XML),
    ?,
    GEOGRAPHY::STGeomFromText(?, 4326),
    GEOMETRY::STGeomFromText(?, 0)
);
"""

# UPDATE to set HIERARCHYID after INSERT. HIERARCHYID has no implicit
# conversion from a string in an INSERT, so we set it in a second statement.
UPDATE_HIERARCHYID_SQL = """
UPDATE dbo.PyTestTable
SET ColHierarchyId = CAST(? AS HIERARCHYID)
WHERE Id = ?;
"""


def to_sql_nullable(value):
    """Treat the literal string 'NULL' (and empty) as Python None."""
    if value is None or value == "" or value == "NULL":
        return None
    return value


def run_sql_file(sql_file):
    """Execute a .sql file, splitting on whole-line `GO` batch separators.

    `GO` is a sqlcmd/SSMS batch separator, NOT valid T-SQL, so we split the
    script on those lines and execute each batch separately. This lets the
    script run directly from Python via pyodbc.
    Docs: https://learn.microsoft.com/sql/tools/sqlcmd/sqlcmd-use-the-utility
    """
    import re

    sql = sql_file.read_text(encoding="utf-8")
    batches = [b for b in re.split(r"(?im)^\s*GO\s*$", sql) if b.strip()]

    # autocommit=True so each batch commits as it runs (it contains DDL, and
    # we want it to persist regardless of later errors).
    with pyodbc.connect(CONN_STR, autocommit=True) as cn:
        for batch in batches:
            cn.execute(batch)


def section_setup():
    """Action 1 — create the PyTestTable from create_pytesttable.sql."""
    print("\n🔨 Setting up the PyTestTable...\n")
    run_sql_file(SETUP_SQL_FILE)
    print("Table `dbo.PyTestTable` is ready (idempotent — safe to re-run).")


def section_cleanup():
    """Action 3 — drop the table so you can start fresh."""
    print("\n🧹 Cleaning up — dropping dbo.PyTestTable...\n")
    # autocommit=True so the DROP commits immediately. The IF OBJECT_ID guard
    # means this is safe even if the table doesn't exist yet.
    # Doc: https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module#pyodbc-functions
    # Doc: https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module#connect
    with pyodbc.connect(CONN_STR, autocommit=True) as cn:
        # Doc: https://github.com/mkleehammer/pyodbc/wiki/Cursor#executesql-parameters
        cn.execute(
            "IF OBJECT_ID('dbo.PyTestTable', 'U') IS NOT NULL "
            "DROP TABLE dbo.PyTestTable;"
        )
    print("Table `dbo.PyTestTable` dropped. You can now start fresh.")


def section_load():
    print("\n🔌 Loading PyTestTable data into SQL Server...\n")

    # `with pyodbc.connect(...)` opens a connection and closes it for us
    # when the block exits. `autocommit=False` means nothing is saved until
    # we call `cn.commit()` at the end — if something fails midway, we can
    # roll back instead of leaving half-written data.
    # Docs: https://github.com/mkleehammer/pyodbc/wiki/Transactions
    # Doc: https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module#connect
    with pyodbc.connect(CONN_STR, autocommit=False) as cn:
        # Open the CSV with encoding='utf-8-sig' to strip the UTF-8 BOM.
        # DictReader maps each row to a dict keyed by the header names.
        # Doc: https://docs.python.org/3.11/library/functions.html#open
        # Doc: https://docs.python.org/3.11/library/codecs.html#standard-encodings
        with open(CSV_FILE, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            cur = cn.cursor()

            for row_num, row in enumerate(reader, 1):
                # Build the params list EXCLUDING ColHierarchyId (it is set
                # separately in the UPDATE). The order must match the columns
                # in INSERT_SQL exactly.
                params = [
                    to_sql_nullable(row[c])
                    for c in reader.fieldnames
                    if c != "ColHierarchyId"
                ]

                # INSERT the row and get the auto-generated Id via OUTPUT.
                cur.execute(INSERT_SQL, params)
                new_id = cur.fetchone()[0]

                # UPDATE the HIERARCHYID value using the captured Id.
                hid_value = to_sql_nullable(row["ColHierarchyId"])
                if hid_value is not None:
                    cur.execute(UPDATE_HIERARCHYID_SQL, hid_value, new_id)

                print(f"Row {row_num} inserted (Id={new_id})")

        cn.commit()

    print("\nData loaded successfully!")

    # Verification query — confirm the round-trip and show a few of the
    # tricky types converted back to readable text (WKT / hierarchy path).
    print("\n--- Verification ---")
    with pyodbc.connect(CONN_STR) as cn:
        cur = cn.cursor()
        cur.execute(
            """
            SELECT
                Id,
                ColBigInt,
                ColVarChar,
                ColHierarchyId.ToString() AS HierarchyPath,
                ColGeography.STAsText() AS GeoWKT
            FROM dbo.PyTestTable
            ORDER BY Id
            """
        )

        for row in cur.fetchall():
            print(
                f"Id={row[0]}, BigInt={row[1]}, VarChar={row[2]}, "
                f"Hierarchy={row[3]}, Geo={row[4]}"
            )


# ---------------------------------------------------------------------------
# Menu loop
# ---------------------------------------------------------------------------
# Each action is its own function, so you can study it in isolation and run
# any part on demand. Type a number to run an action, or `q` to quit.


def main():
    actions = {
        "1": section_setup,
        "2": section_load,
        "3": section_cleanup,
    }

    print("\n🗄️  SQL Server Basics — CSV → SQL Server with pyodbc")
    print("=" * 60)
    print("  1  Setup    — create dbo.PyTestTable (idempotent)")
    print("  2  Load     — insert CSV data and verify")
    print("  3  Cleanup  — drop the table to start fresh")
    print("  q  Quit")
    print("=" * 60)

    while True:
        choice = input("\nChoose an action (1-3, or q to quit): ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        if choice in actions:
            try:
                actions[choice]()
            except pyodbc.Error as e:
                print(f"\n⚠️  SQL error: {e}")
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
