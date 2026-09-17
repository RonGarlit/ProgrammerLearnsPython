# 🔢 NumPy Advanced — `numpy` Library

A single-file, interactive Python lesson that teaches **advanced NumPy**.
This is the third and final step in the NumPy series, building directly on the
`numpy_intermediate` folder. Each section is its own function, so you can study
it in isolation and repeat it as many times as you like.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

> ✅ **Prerequisites:** Complete **`numpy_basics`** and **`numpy_intermediate`**
> first. This lesson assumes you know masking, broadcasting, and aggregation.

## What you'll learn

| #   | Concept                   | What it shows                                           |
| --- | ------------------------- | ------------------------------------------------------- |
| 0   | Clean up                  | No output files; included for consistency               |
| 1   | Structured arrays         | Mixed-type, named fields; `recarray` attribute access   |
| 2   | Vectorized strings        | `np.char` — `upper`, `startswith`, `replace`, `strip`   |
| 3   | `meshgrid` & broadcasting | Build coordinate grids; evaluate functions over a plane |
| 4   | Performance               | Vectorization vs loops (measured); `np.vectorize`       |
| 5   | Memory & dtype            | `float32` vs `float64`; `astype` vs `view`; `.nbytes`   |
| 6   | Advanced indexing         | `np.take`, `np.put`, `np.ix_`                           |
| 7   | Curve fitting             | `np.polyfit` / `np.polyval` — fit a line to data        |
| 8   | Missing data              | `np.nan`, `np.nanmean`, `np.isnan`, masked arrays       |
| 9   | Mini task                 | Sensor trend analysis — NaN handling + `polyfit`        |

> 💡 **Key idea:** Advanced NumPy is about **performance and real-world
> scale**. You learn to control memory with dtypes, handle missing data, fit
> models to data, and structure mixed-type data — the skills you need before
> moving to pandas and beyond.

---

## ✅ Prerequisites

- **Python 3.9 or newer** and **NumPy** installed (it's already declared in
  `pyproject.toml`, so `uv sync` installs it):

  ```powershell
  uv sync
  ```

- **Complete `numpy_basics` and `numpy_intermediate` first.**
- **VS Code** with the **Python extension** (by Microsoft) installed.

Check your Python version and NumPy:

```powershell
uv run python --version
uv run python -c "import numpy; print(numpy.__version__)"
```

---

## ▶️ How to run the program

### Option A — Run from the terminal

1. Open a terminal in this folder.
2. Run the script:

   ```powershell
   uv run numpy_advanced.py
   ```

3. You'll see a menu. Type a number `0`–`9` to run a section, or `q` to quit.

> 💡 **Tip:** The script resolves all file paths relative to its own folder, so
> it also works from the project root:
>
> ```powershell
> uv run numpy_advanced/numpy_advanced.py
> ```

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `numpy_advanced.py`.
3. Click the **Run ▶** button in the top-right corner of the editor
   (or press `Ctrl+F5`).
4. The program runs in the **Terminal** panel. Interact with it there.

> 💡 **Tip:** Because the program reads input with `input()`, always run it in
> the **Terminal** panel — not the "Output" panel, which can't accept typed input.

---

## 🗂️ What the program creates

This lesson is **predominantly in-memory** — it writes no output files.
`measurements.csv` is the **input** file (15 sensor readings) and is never
modified.

---

## 🐞 Debugging with VS Code (step-by-step, for beginners)

Debugging lets you **pause** the program at any line, **inspect** the values of
variables, and **step through** the code one line at a time.

### Step 1 — Set a breakpoint

1. Open `numpy_advanced.py`.
2. Click in the **gutter** (the narrow column to the left of the line numbers)
   next to a line of code. A **red dot** appears.

   For example, click next to the `np.polyfit(sd[valid], sr[valid], 1)` line
   inside `section_summary_task()`. Watching the trend line fit is a great way
   to understand curve fitting.

### Step 2: Start the debugger

1. Press **`F5`** (or go to **Run ▸ Start Debugging**).
2. The program starts and **pauses** when it hits your breakpoint.

### Step 3: Inspect variables

1. When paused, hover over a variable name (like `readings`) to see its value.
2. Use the **Variables** panel in the left sidebar to inspect all variables.
3. Use the **Debug Console** at the bottom to type expressions, e.g.:

   ```python
   readings.shape
   np.isnan(readings).sum()
   ```

4. Press **`F10`** to step to the next line, or **`F5`** to continue to the
   next breakpoint.

> 💡 **Tip:** In the Debug Console you can call any NumPy function, so you can
> experiment without editing the file.

---

## 📚 Further reading

- [NumPy structured arrays](https://numpy.org/doc/stable/user/basics.rec.html)
- [NumPy string operations](https://numpy.org/doc/stable/reference/routines.char.html)
- [NumPy `meshgrid`](https://numpy.org/doc/stable/reference/generated/numpy.meshgrid.html)
- [NumPy polynomials](https://numpy.org/doc/stable/reference/routines.polynomials.html)
- [NumPy masked arrays](https://numpy.org/doc/stable/reference/maskedarray.html)
