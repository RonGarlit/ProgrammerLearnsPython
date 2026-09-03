"""
Pandas Basics with Python — A Self-Guided Lesson
================================================
Run this file (with `python pandas_basics.py`) and follow along.

pandas is a powerful, open-source Python library for working with
**tabular data** (data that looks like a spreadsheet or a CSV file).
It gives us a DataFrame — a 2-D table with labeled rows and columns —
plus a huge toolbox of methods to read, explore, filter, group,
aggregate, and write data with far less code than the built-in `csv`
module.

This lesson is the *basics only*. We will cover intermediate and
advanced pandas in later folders. Here we focus on:

  1. What pandas is & how to install it
  2. Reading a CSV into a DataFrame
  3. Exploring a DataFrame (head, info, describe, shape)
  4. Selecting columns & rows (loc / iloc)
  5. Filtering rows by a condition
  6. Adding & modifying columns
  7. Grouping & aggregating (groupby + sum/mean/count)
  8. Writing a DataFrame back to CSV
  9. A real-world mini task that combines everything

The example data used here is `sales_data.csv` (20 rows of sales records).

Docs: https://pandas.pydata.org/docs/
"""

# pandas is NOT built into Python — it must be installed first.
#   pip install pandas
# If this import fails, see the README.md "Prerequisites" section.
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Path handling with pathlib
# ---------------------------------------------------------------------------
# pathlib is the modern, object-oriented way to handle file paths (the
# intermediate built-ins lesson teaches it in depth). `Path(__file__)` is
# this script's own location; `.resolve()` makes it absolute; `.parent`
# walks up to the folder containing it. The `/` operator joins path pieces.
# Using BASE_DIR means the lesson works no matter WHERE you run it from.
# Docs: https://docs.python.org/3/library/pathlib.html

BASE_DIR = Path(__file__).resolve().parent


def data_path(filename):
    """Return the full path to a file inside this script's folder."""
    return BASE_DIR / filename


# The sample data file used throughout this lesson.
SALES_FILE = data_path("sales_data.csv")


# ---------------------------------------------------------------------------
# SECTION 1: What is pandas & how to install it
# ---------------------------------------------------------------------------
# pandas is a third-party library, so unlike the built-in `csv` module it
# must be installed. It is the de-facto standard for data analysis in
# Python. The core object is the **DataFrame** — a labeled 2D table.
# Docs: https://pandas.pydata.org/docs/getting_started/index.html


def section_intro():
    print("=" * 50)
    print("SECTION 1: What is pandas?")
    print("=" * 50)

    print("pandas is a Python library for working with tabular data.")
    print("Its two main objects are:\n")
    print("  • Series  — a single labeled column (1D).")
    print("  • DataFrame — a labeled 2D table (rows + columns).")
    print()
    print("To install it, run in your terminal:")
    print("  pip install pandas")
    print()
    print("Let's confirm it's installed and see the version:")
    print("  pandas version:", pd.__version__)
    print()
    print("A DataFrame is like a spreadsheet: it has column names,")
    print("row labels (an index), and holds data of many types.")
    print()


# ---------------------------------------------------------------------------
# SECTION 2: Reading a CSV into a DataFrame
# ---------------------------------------------------------------------------
# pd.read_csv() is the pandas way to load a CSV file. It returns a
# DataFrame. Unlike the built-in csv module, pandas automatically:
#   • parses the header row into column names,
#   • infers data types (numbers become int/float, not strings),
#   • gives every row a label (the index).
# Docs: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html


def read_csv_pandas(filename):
    """Read a CSV file and return a pandas DataFrame."""
    return pd.read_csv(filename)


def section_reading():
    print("=" * 50)
    print("SECTION 2: Reading a CSV into a DataFrame")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.\n")
    print("The DataFrame:")
    print(df)
    print()
    print("Notice the difference vs the built-in csv module:")
    print("  • 'amount' and 'quantity' are now NUMBERS (int), not strings.")
    print("  • There is a leftmost 'index' column (0, 1, 2, ...).")
    print("  • The data is aligned into a neat table.")
    print()
    print("The column names are:")
    print("  ", list(df.columns))
    print()
    print("The data types of each column (dtypes):")
    print(df.dtypes)
    print()


# ---------------------------------------------------------------------------
# SECTION 3: Exploring a DataFrame
# ---------------------------------------------------------------------------
# Before analyzing data, we explore it. pandas gives us quick methods:
#   df.head()  -> first n rows
#   df.tail()  -> last n rows
#   df.info()  -> summary of columns, dtypes, and non-null counts
#   df.describe() -> statistics for numeric columns
#   df.shape   -> (rows, columns)
# Docs: https://pandas.pydata.org/docs/user_guide/basics.html


def section_explore():
    print("=" * 50)
    print("SECTION 3: Exploring a DataFrame")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    print("First 5 rows (df.head()):")
    print(df.head())
    print()

    print("Last 3 rows (df.tail(3)):")
    print(df.tail(3))
    print()

    print("Data info (df.info()):")
    df.info()
    print()

    print("Summary statistics (df.describe()):")
    print(df.describe())
    print()

    print("Shape (rows, columns):", df.shape)
    print("Number of rows:", len(df))
    print("Number of columns:", df.shape[1])
    print()

    print("Unique regions:", df["region"].unique())
    print("Unique months:", df["month"].unique())
    print()


# ---------------------------------------------------------------------------
# SECTION 4: Selecting columns & rows (loc / iloc)
# ---------------------------------------------------------------------------
# A DataFrame has two axes: columns (by name) and rows (by label/position).
#   df['col']      -> one column as a Series
#   df[['a','b']]  -> several columns as a DataFrame
#   df.loc[row]    -> select by LABEL (index value)
#   df.iloc[row]   -> select by POSITION (integer)
# Docs: https://pandas.pydata.org/docs/user_guide/indexing.html


def section_selecting():
    print("=" * 50)
    print("SECTION 4: Selecting columns & rows")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    print("One column as a Series (df['amount']):")
    print(df["amount"])
    print()

    print("Several columns (df[['region', 'amount']]):")
    print(df[["region", "amount"]])
    print()

    print("Row by label (df.loc[2]):")
    print(df.loc[2])
    print()

    print("Row by position (df.iloc[0]):")
    print(df.iloc[0])
    print()

    print("A slice of rows by position (df.iloc[0:3]):")
    print(df.iloc[0:3])
    print()

    print("A specific cell (df.loc[2, 'amount']):", df.loc[2, "amount"])
    print("A specific cell (df.iloc[0, 4]):", df.iloc[0, 4])
    print()


# ---------------------------------------------------------------------------
# SECTION 5: Filtering data by a condition
# ---------------------------------------------------------------------------
# This is where pandas shines. Instead of a list comprehension, we write a
# boolean condition and pandas keeps the rows where it is True.
#   df[df['amount'] > 1000]
# Docs: https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing


def section_filtering():
    print("=" * 50)
    print("SECTION 5: Filtering data by a condition")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Keep only rows where amount is greater than 1000.
    high_sales = df[df["amount"] > 1000]
    print(f"Rows with amount > 1000 ({len(high_sales)} rows):")
    print(high_sales)
    print()

    # Combine conditions with & (and) and | (or). Parentheses are required!
    north_laptop = df[(df["region"] == "North") & (df["product"] == "Laptop")]
    print("North region AND Laptop product:")
    print(north_laptop)
    print()

    # Filter on a string column.
    west = df[df["region"] == "West"]
    print(f"West region rows ({len(west)}):")
    print(west)
    print()

    # Filter with .isin() for a list of values.
    north_south = df[df["region"].isin(["North", "South"])]
    print(f"North or South rows ({len(north_south)}):")
    print(north_south)
    print()


# ---------------------------------------------------------------------------
# SECTION 6: Adding & modifying columns
# ---------------------------------------------------------------------------
# We can create new columns by assigning to a name that doesn't exist yet.
# The new column is computed element-wise from existing columns.
# Docs: https://pandas.pydata.org/docs/user_guide/basics.html#column-selection


def section_modifying():
    print("=" * 50)
    print("SECTION 6: Adding & modifying columns")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Create a new column: unit price = amount / quantity.
    df["unit_price"] = df["amount"] / df["quantity"]
    print("Added 'unit_price' column (amount / quantity):")
    print(df[["product", "quantity", "amount", "unit_price"]])
    print()

    # Create a categorical label based on a condition.
    df["size"] = df["amount"].apply(lambda x: "big" if x > 1000 else "small")
    print("Added 'size' column (big if amount > 1000):")
    print(df[["amount", "size"]])
    print()

    # Modify an existing column in place.
    df["amount"] = df["amount"] * 1.0  # convert to float
    print("Converted 'amount' to float:")
    print(df.dtypes)
    print()


# ---------------------------------------------------------------------------
# SECTION 7: Grouping & aggregating
# ---------------------------------------------------------------------------
# groupby() splits the data into groups, applies an aggregation (sum, mean,
# count, ...), and combines the results. This is the heart of pandas.
#   df.groupby('month')['amount'].sum()
# Docs: https://pandas.pydata.org/docs/user_guide/groupby.html


def section_grouping():
    print("=" * 50)
    print("SECTION 7: Grouping & aggregating")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Total sales per month.
    monthly_sales = df.groupby("month")["amount"].sum()
    print("Total sales per month (groupby + sum):")
    print(monthly_sales)
    print()

    # Average sale per region.
    region_mean = df.groupby("region")["amount"].mean()
    print("Average sale per region (groupby + mean):")
    print(region_mean)
    print()

    # Count of rows per product.
    product_count = df.groupby("product")["amount"].count()
    print("Number of sales per product (groupby + count):")
    print(product_count)
    print()

    # Multiple aggregations at once with .agg().
    summary = df.groupby("region")["amount"].agg(["sum", "mean", "count"])
    print("Multiple aggregations per region (.agg):")
    print(summary)
    print()

    # reset_index() turns the group labels back into a normal column.
    monthly_df = monthly_sales.reset_index()
    print("After reset_index(), 'month' is a column again:")
    print(monthly_df)
    print()


# ---------------------------------------------------------------------------
# SECTION 8: Writing a DataFrame back to CSV
# ---------------------------------------------------------------------------
# df.to_csv() writes a DataFrame to a CSV file. We pass index=False so the
# row numbers (the index) are NOT written — usually we don't want them.
# Docs: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html


def write_csv_pandas(df, filename):
    """Write a DataFrame to a CSV file (without the index column)."""
    df.to_csv(filename, index=False)


def section_writing():
    print("=" * 50)
    print("SECTION 8: Writing a DataFrame back to CSV")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Filter, then write the result.
    high_sales = df[df["amount"] > 1000]
    write_csv_pandas(high_sales, data_path("high_sales.csv"))
    print(f"Wrote {len(high_sales)} rows to high_sales.csv (index=False).")

    # Group, then write the result.
    monthly_sales = df.groupby("month")["amount"].sum().reset_index()
    write_csv_pandas(monthly_sales, data_path("monthly_summary.csv"))
    print(f"Wrote {len(monthly_sales)} rows to monthly_summary.csv.")

    print()
    print("Open high_sales.csv and monthly_summary.csv in VS Code to")
    print("see the results. Notice there is NO index column — that's the")
    print("index=False we passed.")
    print()


# ---------------------------------------------------------------------------
# SECTION 9: A real-world mini task (all concepts combined)
# ---------------------------------------------------------------------------
# Let's do a small, practical task: find the top-selling product by total
# revenue, and the region with the highest average sale. This pulls
# together reading, filtering, grouping, and aggregating.


def section_summary_task():
    print("=" * 50)
    print("SECTION 9: Mini task — top product & best region")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Total revenue per product.
    product_revenue = df.groupby("product")["amount"].sum()
    print("Total revenue per product:")
    print(product_revenue)
    print()

    top_product = product_revenue.idxmax()
    top_value = product_revenue.max()
    print(f"Top-selling product: {top_product} (${top_value:,.0f})")
    print()

    # Average sale per region.
    region_mean = df.groupby("region")["amount"].mean()
    print("Average sale per region:")
    print(region_mean)
    print()

    best_region = region_mean.idxmax()
    print(f"Region with highest average sale: {best_region}")
    print()

    # How many rows are above the overall average amount?
    overall_mean = df["amount"].mean()
    above = df[df["amount"] > overall_mean]
    print(f"Overall average amount: ${overall_mean:,.2f}")
    print(f"Rows above average: {len(above)} of {len(df)}")
    print()


# ---------------------------------------------------------------------------
# OPTION 0: Clean up the generated CSV files
# ---------------------------------------------------------------------------
# The writing section creates two CSV files. This helper deletes them so
# you can start fresh. We only delete a file if it exists, so it's safe
# to run any time.


CLEANUP_FILES = [data_path("high_sales.csv"), data_path("monthly_summary.csv")]


def section_cleanup():
    print("=" * 50)
    print("OPTION 0: Cleaning up the CSV files")
    print("=" * 50)

    removed = []
    for filename in CLEANUP_FILES:
        if filename.exists():  # pathlib: no os.path.exists() needed
            filename.unlink()  # pathlib's "delete this file"
            removed.append(filename.name)  # .name = just the filename part

    if removed:
        print("Removed:")
        for filename in removed:
            print(f"  - {filename}")
    else:
        print("Nothing to remove — none of the CSV files were found.")

    print()
    print("The files will be recreated automatically the next time you run")
    print("the section that needs them.")
    print()


# ---------------------------------------------------------------------------
# MAIN MENU — brings all sections together
# ---------------------------------------------------------------------------
# The `if __name__ == "__main__":` guard ensures this code only runs
# when the script is executed directly, not when imported as a module.

# A DICT as a "dispatch table": each menu number maps to a (title, function)
# pair. This replaces a long if/elif chain — to add a section you just add
# one line here, and the menu printing + lookup below handle the rest.
# Docs: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
SECTIONS = {
    "0": ("Clean up the generated CSV files", section_cleanup),
    "1": ("What is pandas & how to install it", section_intro),
    "2": ("Reading a CSV into a DataFrame", section_reading),
    "3": ("Exploring a DataFrame", section_explore),
    "4": ("Selecting columns & rows (loc / iloc)", section_selecting),
    "5": ("Filtering data by a condition", section_filtering),
    "6": ("Adding & modifying columns", section_modifying),
    "7": ("Grouping & aggregating (groupby)", section_grouping),
    "8": ("Writing a DataFrame back to CSV", section_writing),
    "9": ("Mini task: top product & best region", section_summary_task),
}


def main():
    print("\n📄 Welcome to the Pandas Basics Tutorial!\n")
    print("You'll explore these concepts, one step at a time:\n")
    # Print the menu straight from the SECTIONS dict — no duplication.
    for number, (title, _section_function) in SECTIONS.items():
        print(f"  {number}. {title}")
    print()

    keep_going = True
    while keep_going:
        choice = input("Type a number (0-9) to run a section, or q to quit: ").strip()

        if choice.lower() == "q":
            print("Thanks for learning with us. Goodbye!")
            keep_going = False
        elif choice in SECTIONS:
            # dict lookup: we've already checked membership with `in`,
            # so indexing SECTIONS[choice] is safe here.
            _title, section_function = SECTIONS[choice]
            section_function()  # call the function stored in the dict!
        else:
            print("Hmm, that isn't a valid option. Try a number 0-9 or 'q'.")


if __name__ == "__main__":
    main()
