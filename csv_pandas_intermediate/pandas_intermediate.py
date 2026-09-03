"""
Pandas Intermediate with Python — A Self-Guided Lesson
======================================================
Run this file (with `python pandas_intermediate.py`) and follow along.

This is the SECOND step in pandas. We assume you already completed
`csv_pandas_basics` (reading, exploring, filtering, grouping, and writing
a DataFrame). Here we level up with the tools you reach for on real data:

  1. Handling missing values (NaN) — the single most common real-world issue
  2. Sorting & ranking data
  3. Working with dates & times
  4. Merging & joining two DataFrames
  5. Multi-level grouping & pivoting (pivot_table)
  6. Vectorized & .apply() functions
  7. String operations on text columns
  8. Writing enhanced results back to CSV
  9. A real-world mini task that combines everything

The example data is in this folder:
  • sales_data.csv    — 20 sales records, DELIBERATELY missing some values
  • product_info.csv  — product category / supplier / cost lookup table

Docs: https://pandas.pydata.org/docs/
"""

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


# Sample data files used throughout this lesson.
SALES_FILE = data_path("sales_data.csv")
PRODUCT_FILE = data_path("product_info.csv")


def read_csv_pandas(filename):
    """Read a CSV file and return a pandas DataFrame."""
    return pd.read_csv(filename)


def write_csv_pandas(df, filename):
    """Write a DataFrame to a CSV file (without the index column)."""
    df.to_csv(filename, index=False)


# ---------------------------------------------------------------------------
# SECTION 1: Handling missing values (NaN)
# ---------------------------------------------------------------------------
# Real data is messy — cells are often empty. pandas represents a missing
# value as NaN (Not a Number). We can find, count, drop, and fill them.
# Docs: https://pandas.pydata.org/docs/user_guide/missing_data.html


def section_missing_values():
    print("=" * 50)
    print("SECTION 1: Handling missing values (NaN)")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Spot missing values with isna() / notna().
    print("Boolean mask of missing values (df.isna()):")
    print(df.isna())
    print()

    # Count missing values per column.
    print("Missing values per column (df.isna().sum()):")
    print(df.isna().sum())
    print()

    # How many rows have ANY missing value?
    print("Rows with any missing value:", df.isna().any(axis=1).sum())
    print("Rows with NO missing values:", df.notna().all(axis=1).sum())
    print()

    # NaNs come from reading empty cells. Let's see the dtype of 'rating'
    # (it became float because the missing cell forces a float).
    print("dtype of 'rating' (has NaN):", df["rating"].dtype)
    print()

    # Option 1: drop rows that have any missing value.
    clean = df.dropna()
    print(f"After dropna(): {len(clean)} of {len(df)} rows remain.")
    print()

    # Option 2: fill missing values with a chosen value.
    filled_amount = df["amount"].fillna(0)
    print("fillna(0) on 'amount' (first 5):")
    print(filled_amount.head())
    print()

    # Option 3: fill numeric columns with their column MEAN (imputation).
    # This is a very common real-world technique.
    print("Filling numeric columns with their mean:")
    df_filled = df.copy()
    for col in ["amount", "quantity", "rating"]:
        if df_filled[col].isna().any():
            df_filled[col] = df_filled[col].fillna(df_filled[col].mean())
            print(f"  {col}: filled with mean {df_filled[col].mean():.2f}")
    print()

    print("After imputation, missing per column:")
    print(df_filled.isna().sum())
    print()

    # --- ⚠️ The #1 beginner trap: SettingWithCopyWarning -------------------
    # When you FILTER a DataFrame and then try to modify the result, pandas
    # can't tell whether you want to change the original or the filtered
    # copy — so it warns you and your change may silently NOT stick.
    #
    # DEBUGGING NOTE: if your assignment "doesn't work" but raises no error,
    # this trap is the usual suspect. The behavior differs by pandas version:
    #   • pandas 2.x  → prints a SettingWithCopyWarning; the change MAY or
    #                   MAY NOT land in the original df (unpredictable).
    #   • pandas 3.x  → raises a ChainedAssignmentError outright (safer, but
    #                   still confusing if you've never seen it).
    # Docs: https://pandas.pydata.org/docs/user_guide/indexing.html
    print("⚠️  The SettingWithCopyWarning trap:")
    low_rated = df[df["rating"] < 3]  # a filtered view/copy — which is it?
    try:
        low_rated["rating"] = 0  # ❌ chained-style assignment → warning risk
        # If we reach here, pandas allowed the write. But did it stick?
        # Check the ORIGINAL df: are the low ratings still there?
        original_untouched = (df["rating"] < 3).any()
        print("  Assigned to filtered rows — but did it change df?")
        if original_untouched:
            print("  → NO: df is unchanged (the write went to a throwaway copy).")
        else:
            print("  → YES: df was modified (pandas treated the filter as a view).")
    except Exception as assignment_error:  # pandas 3.x path: refused outright
        print(f"  pandas refused the assignment: {type(assignment_error).__name__}")
        print("  → The write never happened; df is untouched.")
    print(
        "  df still has its original ratings?",
        df["rating"].isna().sum() > 0 or df["rating"].min() > 0,
    )

    # ✅ FIX 1: use .loc[row_condition, column] to assign in one step.
    # .loc is unambiguous — it always means "change the ORIGINAL df".
    # There is no intermediate filtered object, so there is nothing to be
    # ambiguous about. This is the pattern to reach for 95% of the time.
    df.loc[df["rating"] < 3, "rating"] = 0
    print(
        "  After df.loc[df['rating'] < 3, 'rating'] = 0, min rating:",
        df["rating"].min(),
    )

    # ✅ FIX 2: if you genuinely WANT an independent copy to edit, say so
    # explicitly with .copy(). Then pandas knows your intent and assignments
    # to the copy are safe — they just won't affect the original df.
    # DEBUGGING NOTE: forgetting .copy() is the mirror-image mistake —
    # you edit your "copy" expecting the original to stay pristine, and
    # sometimes it changes anyway (when the filter returned a view).
    low_rated_copy = df[df["rating"] < 3].copy()
    low_rated_copy["rating"] = -1  # safe: this is a real, independent copy
    print("  With .copy(): edited copy's min rating:", low_rated_copy["rating"].min())
    print("  ...but the original df is untouched:", df["rating"].min() == 0)
    print()
    print("  💡 Rule: filter + assign separately → warning risk;")
    print("     df.loc[condition, column] = value → always safe;")
    print("     df[condition].copy() → independent copy you can edit freely.")
    print()


# ---------------------------------------------------------------------------
# SECTION 2: Sorting & ranking data
# ---------------------------------------------------------------------------
# sort_values() orders rows by a column. It's essential for "top N" and
# "best/worst" questions.
# Docs: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html


def section_sorting():
    print("=" * 50)
    print("SECTION 2: Sorting & ranking data")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Sort by a single column, descending (largest first).
    by_amount = df.sort_values("amount", ascending=False)
    print("Top 5 sales by amount (descending):")
    print(by_amount[["product", "amount"]].head())
    print()

    # Sort by MULTIPLE columns: region (A-Z), then amount (largest first).
    multi = df.sort_values(["region", "amount"], ascending=[True, False])
    print("Sorted by region, then amount (desc):")
    print(multi[["region", "product", "amount"]].head(8))
    print()

    # iloc[] keeps the original row numbers even after sorting — proving it
    # returns a NEW DataFrame with a new order but the same index.
    print("Index of top sale:", by_amount.iloc[0]["id"], "(original id)")
    print()

    # Rank values 1..N. NaNs are skipped by default.
    df["rank"] = df["amount"].rank(ascending=False, method="min")
    print("Ranks for the first 8 rows (1 = highest amount):")
    print(df[["id", "amount", "rank"]].head(8))
    print()


# ---------------------------------------------------------------------------
# SECTION 3: Working with dates & times
# ---------------------------------------------------------------------------
# 'date' is stored as text. We convert it to a datetime with pd.to_datetime()
# so we can extract years/months/weekdays and do date math.
# Docs: https://pandas.pydata.org/docs/user_guide/timeseries.html


def section_dates():
    print("=" * 50)
    print("SECTION 3: Working with dates & times")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    print("Before: dtype of 'date' is", df["date"].dtype)
    df["date"] = pd.to_datetime(df["date"])
    print("After:  dtype of 'date' is", df["date"].dtype)
    print()

    # Extract new columns from the datetime.
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["weekday"] = df["date"].dt.day_name()
    print("Extracted year / quarter / weekday:")
    print(df[["date", "year", "quarter", "weekday"]].head())
    print()

    # Date math: how many days ago? (relative to the latest sale)
    latest = df["date"].max()
    df["days_since_last"] = (latest - df["date"]).dt.days
    print(f"Latest sale date: {latest.date()}")
    print("Days since latest sale (first 5):")
    print(df[["date", "days_since_last"]].head())
    print()

    # 'month' was a text column; now we can derive a proper month number.
    df["month_num"] = df["date"].dt.month
    print("Month numbers (df['date'].dt.month):")
    print(df["month_num"].head())
    print()


# ---------------------------------------------------------------------------
# SECTION 4: Merging & joining two DataFrames
# ---------------------------------------------------------------------------
# Real analyses usually combine several tables. pd.merge() joins two
# DataFrames on a common key column — just like a SQL JOIN.
# Docs: https://pandas.pydata.org/docs/user_guide/merging.html


def section_merging():
    print("=" * 50)
    print("SECTION 4: Merging & joining two DataFrames")
    print("=" * 50)

    sales = read_csv_pandas(SALES_FILE)
    products = read_csv_pandas(PRODUCT_FILE)

    print("sales_data.csv columns:")
    print(" ", list(sales.columns))
    print()
    print("product_info.csv (lookup table):")
    print(products)
    print()

    # Inner merge: keep rows where key exists in BOTH tables.
    merged = pd.merge(
        sales, products, on="product", how="inner", validate="many_to_one"
    )
    print(f"Inner merge: {len(merged)} rows (sales) x product_info")
    print(
        merged[
            ["id", "product", "quantity", "amount", "category", "supplier", "cost"]
        ].head()
    )
    print()

    # Now we can compute profit = amount - (cost * quantity) using the merged cost!
    merged["profit"] = merged["amount"] - (merged["cost"] * merged["quantity"])
    print("Added 'profit' column (amount - cost * quantity):")
    print(merged[["product", "quantity", "amount", "cost", "profit"]].head())
    print()

    # A left merge keeps ALL sales rows even if no product match exists.
    left = pd.merge(sales, products, on="product", how="left", validate="many_to_one")
    print("Left merge row count:", len(left), "(same as sales)")
    print(
        "Any missing supplier after left join?", left["supplier"].isna().sum(), "rows"
    )
    print()


# ---------------------------------------------------------------------------
# SECTION 5: Multi-level grouping & pivot tables
# ---------------------------------------------------------------------------
# Basics did single-key groupby. Intermediate adds:
#   • groupby MULTIPLE columns (nested groups)
#   • .pivot_table() — reshape data into a spreadsheet-style summary
# Docs: https://pandas.pydata.org/docs/user_guide/reshaping.html


def section_pivot():
    print("=" * 50)
    print("SECTION 5: Multi-level grouping & pivot tables")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Group by TWO columns: sums for each (region, product) pair.
    pair = df.groupby(["region", "product"])["amount"].sum()
    print("Total sales per (region, product) pair:")
    print(pair)
    print()

    # reset_index() flattens the multi-level result back into columns.
    pair_df = pair.reset_index()
    print("After reset_index() — a flat DataFrame:")
    print(pair_df.head())
    print()

    # pivot_table() reshapes: rows = region, columns = product, cells = amount.
    pivot = df.pivot_table(
        index="region",
        columns="product",
        values="amount",
        aggfunc="sum",
        fill_value=0,
    )
    print("pivot_table: regions (rows) x products (columns):")
    print(pivot)
    print()

    # Same with MEAN as the aggregation.
    pivot_mean = df.pivot_table(
        index="region",
        columns="product",
        values="amount",
        aggfunc="mean",
        fill_value=0,
    )
    print("pivot_table (mean amount per region/product):")
    print(pivot_mean)
    print()


# ---------------------------------------------------------------------------
# SECTION 6: Vectorized & .apply() functions
# ---------------------------------------------------------------------------
# pandas is FAST because most operations are vectorized (they run across the
# whole column at once, in C). When you need custom per-row logic, use
# .apply() with a function.
# Docs: https://pandas.pydata.org/docs/user_guide/apply.html


def section_apply():
    print("=" * 50)
    print("SECTION 6: Vectorized & .apply() functions")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # 1) Vectorized: arithmetic on a whole column at once.
    df["tax"] = df["amount"].fillna(0) * 0.08
    print("Vectorized: tax = amount * 0.08 (first 5):")
    print(df[["id", "amount", "tax"]].head())
    print()

    # 2) .apply() with a custom function along a row (axis=1).
    def categorize(row):
        if row["amount"] > 1000:
            return "high"
        if row["amount"] > 500:
            return "medium"
        return "low"

    df["tier"] = df.apply(categorize, axis=1)
    print("Custom .apply() row-by-row → 'tier' (first 8):")
    print(df[["id", "amount", "tier"]].head(8))
    print()

    # 3) .apply() with a lambda on a single column.
    df["product_tag"] = df["product"].apply(lambda p: p.upper()[:3])
    print("Lambda .apply on one column (last 3):")
    print(df["product_tag"].tail(3))
    print()

    # 4) The same result can often be done vectorized with .loc — faster.
    df["tier2"] = "low"
    df.loc[df["amount"] > 500, "tier2"] = "medium"
    df.loc[df["amount"] > 1000, "tier2"] = "high"
    print("Vectorized tier via .loc (compare to apply result):")
    print(df[["id", "tier", "tier2"]].head(8))
    print()


# ---------------------------------------------------------------------------
# SECTION 7: String operations on text columns
# ---------------------------------------------------------------------------
# Text needs its own toolset. Use .str. to access vectorized string methods
# like upper(), strip(), contains(), replaces, and splitting.
# Docs: https://pandas.pydata.org/docs/user_guide/text.html


def section_strings():
    print("=" * 50)
    print("SECTION 7: String operations on text columns")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Lowercase + strip whitespace.
    df["product_lower"] = df["product"].str.lower()
    print("Lowercased product names:")
    print(df["product_lower"].unique())
    print()

    # Does the string CONTAIN a substring? (boolean mask → filter)
    has_ket = df[df["product"].str.contains("Ket")]  # 'Keyboard' vs others
    print("Rows whose product contains 'Ket':")
    print(has_ket[["id", "product"]])
    print()

    # Startswith / endswith.
    starts_lap = df[df["product"].str.startswith("Lap")]
    print("Products starting with 'Lap':")
    print(starts_lap["product"].unique())
    print()

    # Replace part of a string (here just for illustration).
    df["product_alt"] = df["product"].str.replace("Mouse", "PointingDevice")
    print("Replaced 'Mouse' with 'PointingDevice':")
    print(df["product_alt"].unique())
    print()


# ---------------------------------------------------------------------------
# SECTION 8: Writing enhanced results back to CSV
# ---------------------------------------------------------------------------
# Reuse the basics helper to save our analysis. Here we persist the merged,
# enriched DataFrame and the pivot summary.
# Docs: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html


def section_writing():
    print("=" * 50)
    print("SECTION 8: Writing enhanced results back to CSV")
    print("=" * 50)

    sales = read_csv_pandas(SALES_FILE)
    products = read_csv_pandas(PRODUCT_FILE)

    # Merge, then add profit to prove the enriched data persists.
    merged = pd.merge(sales, products, on="product", how="left", validate="many_to_one")
    merged["profit"] = merged["amount"] - (merged["cost"] * merged["quantity"])
    write_csv_pandas(merged, data_path("enriched_sales.csv"))
    print(f"Wrote {len(merged)} rows to enriched_sales.csv (merged + profit).")

    # Build & persist a pivot summary.
    pivot = sales.pivot_table(
        index="region",
        columns="product",
        values="amount",
        aggfunc="sum",
        fill_value=0,
    ).reset_index()
    write_csv_pandas(pivot, data_path("pivot_summary.csv"))
    print("Wrote pivot_summary.csv (regions x products).")

    print()
    print("Open enriched_sales.csv and pivot_summary.csv in VS Code to")
    print("inspect the results. Note: no index column (index=False).")
    print()


# ---------------------------------------------------------------------------
# SECTION 9: A real-world mini task (all concepts combined)
# ---------------------------------------------------------------------------
# Task: find the most profitable product per region. This pulls together
# missing-data handling, merging, computing a derived column, sorting, and
# grouping — everything in this lesson.


def section_summary_task():
    print("=" * 50)
    print("SECTION 9: Mini task — most profitable product per region")
    print("=" * 50)

    sales = read_csv_pandas(SALES_FILE)
    products = read_csv_pandas(PRODUCT_FILE)

    # 1) Merge to bring in cost (drop rows whose product has no cost info).
    merged = pd.merge(
        sales, products, on="product", how="inner", validate="many_to_one"
    )

    # 2) Handle a missing amount before doing math.
    merged["amount"] = merged["amount"].fillna(0)

    # 3) Compute profit per row.
    merged["profit"] = merged["amount"] - (merged["cost"] * merged["quantity"])

    # 4) Total profit per region (groupby).
    region_profit = merged.groupby("region")["profit"].sum()
    print("Total profit per region:")
    print(region_profit)
    print()

    # 5) Best product per region: for each group, find the row with the
    #    highest profit. .idxmax() returns the index of that row per group.
    best_idx = merged.groupby("region")["profit"].idxmax()  # Series: region -> idx
    best = merged.loc[best_idx]

    print("Most profitable product per region:")
    print(best[["region", "product", "profit", "quantity"]])
    print()

    # 6) State the overall winner.
    total = merged["profit"].sum()
    print(f"Overall total profit: ${total:,.2f}")
    print()


# ---------------------------------------------------------------------------
# OPTION 0: Clean up the generated CSV files
# ---------------------------------------------------------------------------
# The writing section creates two output files. This helper deletes them so
# you can start fresh.


CLEANUP_FILES = [data_path("enriched_sales.csv"), data_path("pivot_summary.csv")]


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
    "1": ("Handling missing values (NaN)", section_missing_values),
    "2": ("Sorting & ranking data", section_sorting),
    "3": ("Working with dates & times", section_dates),
    "4": ("Merging & joining two DataFrames", section_merging),
    "5": ("Multi-level grouping & pivot tables", section_pivot),
    "6": ("Vectorized & .apply() functions", section_apply),
    "7": ("String operations on text columns", section_strings),
    "8": ("Writing enhanced results back to CSV", section_writing),
    "9": ("Mini task: most profitable product per region", section_summary_task),
}


def main():
    print("\n📊 Welcome to the Pandas Intermediate Tutorial!\n")
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
