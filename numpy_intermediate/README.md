# 🔢 NumPy Intermediate — `numpy` Library

A single-file, interactive Python lesson that teaches **intermediate NumPy**.
This is the second step in the NumPy series, building directly on the
`numpy_basics` folder. Each section is its own function, so you can study it
in isolation and repeat it as many times as you like.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

> ✅ **Prerequisites:** Complete **`numpy_basics`** first. This lesson assumes
> you know how to create arrays, index/slice, and use vectorized math.

## What you'll learn

| #   | Concept                 | What it shows                                              |
| --- | ----------------------- | ---------------------------------------------------------- | ----------------------------- |
| 0   | Clean up                | No output files; included for consistency                  |
| 1   | Reshaping & transposing | `reshape`, `ravel`, `transpose`/`.T`; views vs copies      |
| 2   | Stacking & splitting    | `concatenate`, `vstack`, `hstack`, `split`                 |
| 3   | Boolean masking         | Filter with conditions; `&`/`                              | `; count & replace with masks |
| 4   | Fancy indexing          | Select with arrays of indices; `np.where`                  |
| 5   | Broadcasting            | How arrays of different shapes work together               |
| 6   | Random numbers          | `np.random.default_rng`, seeds, distributions, simulations |
| 7   | Linear algebra          | `np.dot`, `@`/`matmul`, transpose, `np.linalg.inv`         |
| 8   | Advanced aggregation    | `percentile`, `median`, `unique`, `where`, `any`/`all`     |
| 9   | Mini task               | Sensor anomaly detection — masking + aggregation           |

> 💡 **Key idea:** Intermediate NumPy is about **selecting and combining**
> data. You learn to reshape arrays, filter with boolean masks, index with
> arrays, let broadcasting stretch shapes for you, and generate reproducible
> random data for simulations.

---

## ✅ Prerequisites

- **Python 3.9 or newer** and **NumPy** installed (it's already declared in
  `pyproject.toml`, so `uv sync` installs it):

  ```powershell
  uv sync
  ```

- **Complete `numpy_basics` first.**
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
   uv run numpy_intermediate.py
   ```

3. You'll see a menu. Type a number `0`–`9` to run a section, or `q` to quit.

> 💡 **Tip:** The script resolves all file paths relative to its own folder, so
> it also works from the project root:
>
> ```powershell
> uv run numpy_intermediate/numpy_intermediate.py
> ```

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `numpy_intermediate.py`.
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

1. Open `numpy_intermediate.py`.
2. Click in the **gutter** (the narrow column to the left of the line numbers)
   next to a line of code. A **red dot** appears.

   For example, click next to the `data - col_means` line inside
   `section_broadcasting()`. Watching the column means broadcast across rows
   is a great way to understand broadcasting.

### Step 2: Start the debugger

1. Press **`F5`** (or go to **Run ▸ Start Debugging**).
2. The program starts and **pauses** when it hits your breakpoint.

### Step 3: Inspect variables

1. When paused, hover over a variable name (like `data`) to see its value.
2. Use the **Variables** panel in the left sidebar to inspect all variables.
3. Use the **Debug Console** at the bottom to type expressions, e.g.:

   ```python
   data.shape
   data.mean(axis=0)
   ```

4. Press **`F10`** to step to the next line, or **`F5`** to continue to the
   next breakpoint.

> 💡 **Tip:** In the Debug Console you can call any NumPy function, so you can
> experiment without editing the file.

---

## 📚 Further reading

- [NumPy array manipulation](https://numpy.org/doc/stable/reference/routines.array-manipulation.html)
- [NumPy indexing](https://numpy.org/doc/stable/user/basics.indexing.html)
- [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [NumPy random](https://numpy.org/doc/stable/reference/random/index.html)
- [NumPy linear algebra](https://numpy.org/doc/stable/reference/routines.linalg.html)
