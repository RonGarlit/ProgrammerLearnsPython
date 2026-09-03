"""
Pandas Advanced with Python — A Self-Guided Lesson
===================================================
Run this file (with `python pandas_advanced.py`) and follow along.

This is the THIRD step in pandas. We assume you completed `csv_pandas_basics`
(reading, exploring, filtering, grouping) and `csv_pandas_intermediate`
(missing values, sorting, dates, merging, pivot tables, .apply(), strings).

Here we go to the advanced level. Advanced pandas is about **large, complex,
and time-based data**. We focus on:

  1. MultiIndex — hierarchical row & column labels
  2. Reshaping with `stack()` / `unstack()`
  3. Reshaping with `melt()` — converting wide → long format
  4. Categorical data — reducing memory & ordering categories
  5. Window functions — rolling (moving) & expanding calculations
  6. Time-series resampling — downsampling / upsampling by calendar period
  7. Function pipelines with `.pipe()` and `map()`
  8. Advanced aggregation — multiple keys, multiple funcs, custom funcs
  9. A real-world mini task that combines all of it

The example data is `sales_data.csv` — 50 daily sales records spanning
January–June 2024, which is rich enough for real time-series work.

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


# Sample data file used throughout this lesson.
SALES_FILE = data_path("sales_data.csv")


def read_csv_pandas(filename):
    """Read a CSV file and return a pandas DataFrame."""
    return pd.read_csv(filename, parse_dates=["date"])


def write_csv_pandas(df, filename):
    """Write a DataFrame to a CSV file (without the index column)."""
    df.to_csv(filename, index=False)


# ---------------------------------------------------------------------------
# SECTION 1: MultiIndex (hierarchical labels)
# ---------------------------------------------------------------------------
# A MultiIndex lets rows (or columns) be labeled by MORE than one level.
# We create one with set_index() on several columns, or with groupby().
# Docs: https://pandas.pydata.org/docs/user_guide/advanced.html


def section_multiindex():
    print("=" * 50)
    print("SECTION 1: MultiIndex (hierarchical labels)")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Set a 2-level row index: (region, product).
    # sort_index() sorts the levels for fast, warning-free slicing by tuple.
    mi = df.set_index(["region", "product"]).sort_index()
    print("2-level index (region, product) — sorted:")
    print(mi.head())
    print()
    print("Index levels:", mi.index.names)
    print("Index nlevels:", mi.index.nlevels)
    print()

    # `.loc` with a full tuple addresses BOTH levels at once. It returns a
    # scalar, a Series, or a DataFrame depending on how many rows match —
    # here three rows match, so we get a DataFrame we can loop over.
    print("mi.loc[('North', 'Laptop')] — all North Laptop sales:")
    print(mi.loc[("North", "Laptop")])
    print()

    # Select all rows for one level with a partial tuple.
    print("mi.loc['West'] — all West sales (first 5):")
    print(mi.loc["West"].head())
    print()

    # .xs() lets us cross-section down one level.
    print("mi.xs('Mouse', level='product') (first 5):")
    print(mi.xs("Mouse", level="product").head())
    print()


# ---------------------------------------------------------------------------
# SECTION 2: Reshaping with stack() / unstack()
# ---------------------------------------------------------------------------
# stack() pivots one level of the COLUMN index down to the ROW index,
# producing longer data. unstack() does the reverse — pivots a row index
# level UP into columns, producing wider data.
# Docs: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.stack.html


def section_stack_unstack():
    print("=" * 50)
    print("SECTION 2: Reshaping with stack() / unstack()")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Start from a tidy summary: average amount per (region, product).
    summary = df.groupby(["region", "product"])["amount"].mean()
    print("Grouped summary (region, product) -> mean amount:")
    print(summary)
    print()

    # unstack(): move the 'product' level of the index up to COLUMNS.
    wide = summary.unstack()
    print("After .unstack() — products become columns:")
    print(wide)
    print()

    # stack(): move the product COLUMN level back DOWN to the row index.
    long = wide.stack()
    print("After .stack() — back to a long Series:")
    print(long)
    print()

    print("wide vs long row counts:", len(wide), "vs", len(long))
    print()


# ---------------------------------------------------------------------------
# SECTION 3: Reshaping with melt() — wide → long
# ---------------------------------------------------------------------------
# Real world data often arrives WIDE (many columns). .melt() unpivots a
# block of columns into 'variable' + 'value' columns — the "long" format
# that groupby and plotting love.
# Docs: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.melt.html


def section_melt():
    print("=" * 50)
    print("SECTION 3: Reshaping with melt() — wide to long")
    print("=" * 50)

    # Build a classic WIDE table: sales by region x quarter.
    wide = pd.DataFrame(
        {
            "region": ["North", "South", "East", "West"],
            "Q1": [2400, 2500, 2100, 1900],
            "Q2": [2600, 2400, 2200, 2100],
            "Q3": [2700, 2300, 2300, 2200],
        }
    )
    print("WIDE table (region x quarter):")
    print(wide)
    print()

    # melt() turns the quarter columns into rows.
    long = wide.melt(
        id_vars="region",  # keep 'region' as an identifier
        var_name="quarter",  # name for the former column headers
        value_name="amount",  # name for the former cell values
    )
    print("After .melt() — LONG format (region, quarter, amount):")
    print(long)
    print()

    # Now we can group the long data normally.
    by_q = long.groupby("quarter")["amount"].sum()
    print("Total per quarter (now that it's long):")
    print(by_q)
    print()


# ---------------------------------------------------------------------------
# SECTION 4: Categorical data
# ---------------------------------------------------------------------------
# When a column holds a small set of repeated labels, we can store it as
# a 'category' dtype. This uses less memory AND lets us define an ORDER.
# Docs: https://pandas.pydata.org/docs/user_guide/categorical.html


def section_categorical():
    print("=" * 50)
    print("SECTION 4: Categorical data")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    before = df.memory_usage(deep=True).sum()
    print(f"Memory before: {before / 1024:.1f} KB")

    # Convert to categorical.
    for col in ["region", "product"]:
        df[col] = df[col].astype("category")
    after = df.memory_usage(deep=True).sum()
    print(
        f"Memory after categories: {after / 1024:.1f} KB (saved "
        f"{(before - after) / 1024:.1f} KB)"
    )
    print()

    # Categories are now known up front.
    print("Product categories:", df["product"].cat.categories.tolist())
    print("Region categories:", df["region"].cat.categories.tolist())
    print()

    # We can impose an ORDER, enabling min/max/sort on the labels.
    order = pd.Categorical(
        df["region"], categories=["East", "North", "South", "West"], ordered=True
    )
    print("Ordered categories sort by our custom order (first 6):")
    print(pd.DataFrame({"region": order})["region"].head(6).tolist())
    print()


# ---------------------------------------------------------------------------
# SECTION 5: Window functions — rolling & expanding
# ---------------------------------------------------------------------------
# .rolling() computes a statistic over a sliding window (e.g. last 3 rows),
# great for moving averages and smoothing noise. .expanding() includes ALL
# rows up to the current point — a running/cumulative view.
# Docs: https://pandas.pydata.org/docs/user_guide/window.html


def section_window():
    print("=" * 50)
    print("SECTION 5: Window functions — rolling & expanding")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE).sort_values("date")
    # Total sales per day, so the time axis is dense.
    daily = df.groupby("date")["amount"].sum().sort_index()
    print("Daily sales (first 8 days):")
    print(daily.head(8))
    print()

    # Rolling mean over a 7-day window.
    rolling = daily.rolling(window=7).mean()
    print("7-day rolling mean (moving average):")
    print(rolling.head(10))
    print()

    # Expanding: cumulative running totals.
    expanding = daily.expanding().sum()
    print("Expanding (running) total — last 5:")
    print(expanding.tail())
    print()

    # A rolling SUM window is handy too.
    print("3-day rolling sum (last 5):")
    print(daily.rolling(window=3).sum().tail())
    print()


# ---------------------------------------------------------------------------
# SECTION 6: Time-series resampling
# ---------------------------------------------------------------------------
# Resampling changes the time FRQUENCY of the data — downsampling (daily ->
# weekly/monthly) aggregates periods; upsampling (daily -> hourly) fills gaps.
# Docs: https://pandas.pydata.org/docs/user_guide/timeseries.html#resampling


def section_resample():
    print("=" * 50)
    print("SECTION 6: Time-series resampling")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)
    daily = df.groupby("date")["amount"].sum().sort_index()

    # Downsample daily -> MONTHLY (aggregate with sum).
    monthly = daily.resample("ME").sum()
    print("Monthly totals (resample('ME').sum()):")
    print(monthly)
    print()

    # Downsample daily -> WEEKLY (aggregate with mean).
    weekly = daily.resample("W").mean()
    print("Weekly averages (resample('W').mean()) — first 4:")
    print(weekly.head(4))
    print()

    # Upsample and fill gaps with ffill.
    # First ensure we have a full calendar range, then backfill.
    full_index = daily.resample("D").asfreq()
    filled = full_index.ffill()
    print("Upsampled to daily then forward-filled (first 5):")
    print(filled.head(5))
    print()


# ---------------------------------------------------------------------------
# SECTION 7: Function pipelines — .pipe() and map()
# ---------------------------------------------------------------------------
# .pipe() chains several DataFrame transformations into one readable,
# testable call. It's the pandas idiom for building data pipelines.
# Docs: https://pandas.pydata.org/docs/user_guide/basics.html#pipe


def section_pipe():
    print("=" * 50)
    print("SECTION 7: Function pipelines — .pipe()")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Define small, reusable transformation functions.
    def add_profit(block, margin=0.2):
        block["profit"] = block["amount"] * margin
        return block

    def top_n(block, n=5):
        return block.sort_values("profit", ascending=False).head(n)

    # Compose them with .pipe() — clean, readable data pipeline.
    result = (
        df.groupby("product")["amount"].sum().reset_index().pipe(add_profit).pipe(top_n)
    )
    print("Pipeline result (product profit, top 5):")
    print(result)
    print()


# ---------------------------------------------------------------------------
# SECTION 8: Advanced aggregation
# ---------------------------------------------------------------------------
# Combine groupby with named and multiple aggregations, plus custom
# functions — controlled, flexible summaries.
# Docs: https://pandas.pydata.org/docs/user_guide/groupby.html


def section_advanced_agg():
    print("=" * 50)
    print("SECTION 8: Advanced aggregation")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # Multiple aggregations on one column, with named results.
    named = df.groupby("region")["amount"].agg(
        total="sum",
        avg="mean",
        count="count",
        max="max",
    )
    print("Named aggregations per region:")
    print(named)
    print()

    # A custom function passed to agg.
    def price_range(series):
        return series.max() - series.min()

    custom = df.groupby("region")["amount"].agg([sum, "mean", price_range])
    custom.columns = ["total", "mean", "range"]
    print("Custom aggregation (sum, mean, range):")
    print(custom)
    print()

    # Aggregate DIFFERENT columns with DIFFERENT functions.
    mixed = df.groupby("region").agg(
        total_amount=("amount", "sum"),
        total_qty=("quantity", "sum"),
        avg_qty=("quantity", "mean"),
    )
    print("Mixed aggregation (amount sum, quantity sum/mean):")
    print(mixed)
    print()


# ---------------------------------------------------------------------------
# SECTION 9: A real-world mini task (all concepts combined)
# ---------------------------------------------------------------------------
# Task: build a 4-week rolling performance report of total monthly profit,
# from the raw daily sales. Combines date parsing, resampling, merging-free
# derived columns, rolling windows, and pivot-style output.


def section_summary_task():
    print("=" * 50)
    print("SECTION 9: Mini task — weekly profit & rolling report")
    print("=" * 50)

    df = read_csv_pandas(SALES_FILE)

    # 1) Derived column: profit (assume a 25% margin on amount).
    df["profit"] = df["amount"] * 0.25

    # 2) Time-series: daily mean profit, then resample to weekly totals.
    daily = df.groupby("date")["profit"].mean()
    weekly = daily.resample("W").sum()

    print("Weekly total profit:")
    print(weekly)
    print()

    # 3) Window function: 4-week rolling total to smooth weekly spikes.
    rolling = weekly.rolling(window=4).sum()
    print("4-week ROLLING total profit (first 6):")
    print(rolling.head(6))
    print()

    # 4) Aggregate region performance as a tidy long summary.
    by_region = df.groupby("region")["profit"].sum().sort_values(ascending=False)
    print("Total profit by region (long):")
    print(by_region)
    print()

    # 5) Pivot-style output for the report (region x month, mean amount).
    month = df.set_index("date").resample("ME")
    pivot = month["amount"].mean().reset_index()
    pivot["month"] = pivot["date"].dt.strftime("%Y-%m")
    print("Monthly mean amount (report snippet — first 3):")
    print(pivot[["month", "amount"]].head(3))
    print()

    best_region = by_region.index[0]
    best_revenue = by_region.iloc[0]
    print(f"Top region by profit: {best_region} (${best_revenue:,.2f})")
    print()


# ---------------------------------------------------------------------------
# OPTION 0: Clean up the generated CSV files
# ---------------------------------------------------------------------------
# The advanced lesson is predominantly in-memory; it writes only optional
# pipeline output. We include a cleanup routine for consistency.


CLEANUP_FILES = [data_path("pipeline_output.csv")]


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
    print("The file will be recreated automatically when needed.")
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
    "1": ("MultiIndex (hierarchical labels)", section_multiindex),
    "2": ("Reshaping with stack() / unstack()", section_stack_unstack),
    "3": ("Reshaping with melt() (wide → long)", section_melt),
    "4": ("Categorical data", section_categorical),
    "5": ("Window functions (rolling & expanding)", section_window),
    "6": ("Time-series resampling", section_resample),
    "7": ("Function pipelines with .pipe()", section_pipe),
    "8": ("Advanced aggregation", section_advanced_agg),
    "9": ("Mini task: weekly profit & rolling report", section_summary_task),
}


def main():
    print("\n🚀 Welcome to the Pandas Advanced Tutorial!\n")
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
