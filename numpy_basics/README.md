# 🔢 NumPy Basics — `numpy` Library

A single-file, interactive Python lesson that teaches **how to work with
numerical data using NumPy** — the foundational library for fast computing in
Python. Each section is its own function, so you can study it in isolation and
repeat it as many times as you like.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

> This is the **basics** folder. Intermediate and advanced NumPy topics will
> be built out in later folders (`numpy_intermediate`, `numpy_advanced`).

## What you'll learn

| #   | Concept             | What it shows                                               |
| --- | ------------------- | ----------------------------------------------------------- |
| 0   | Clean up            | Deletes the two generated files so you can start fresh      |
| 1   | What is NumPy?      | The `ndarray`, `pip install numpy`, why it's fast           |
| 2   | Creating arrays     | `np.array`, `arange`, `zeros`, `ones`, `linspace`           |
| 3   | Exploring an array  | `shape`, `ndim`, `size`, `dtype`                            |
| 4   | Indexing & slicing  | `arr[i]`, `arr[row, col]`, slices are views                 |
| 5   | Vectorized math     | Element-wise `+ - * /`, comparisons, no loops               |
| 6   | Universal functions | `np.sqrt`, `np.round`, `np.abs`, `np.exp`, `np.log`, `clip` |
| 7   | Aggregations        | `sum`, `mean`, `min`, `max`, `std`, `argmax`, axes          |
| 8   | Saving & loading    | `savetxt`/`loadtxt`, `save`/`load` (.npy)                   |
| 9   | Mini task           | Sensor reading summary — loading + slicing + aggregating    |

> 💡 **Key idea:** NumPy's **ndarray** is a fast grid of numbers. Operations
> are **vectorized** — they run across the whole array at once (in C) instead
> of element-by-element in a Python loop. pandas is built on top of NumPy, so
> this is the foundation for everything that follows.

---

## ✅ Prerequisites

- **Python 3.9 or newer** (NumPy requires a recent Python).
- **NumPy** installed:

  ```powershell
  pip install numpy
  ```

- **VS Code** with the **Python extension** (by Microsoft) installed.
  - The extension gives you IntelliSense, the debugger, and the Run button.

Check your Python version and NumPy:

```powershell
python --version
python -c "import numpy; print(numpy.__version__)"
```

> If `pip install numpy` fails, try `python -m pip install numpy`.

---

## ▶️ How to run the program

### Option A — Run from the terminal

1. Open a terminal in this folder.
2. Run the script:

   ```powershell
   python numpy_basics.py
   ```

3. You'll see a menu. Type a number `0`–`9` to run a section, or `q` to quit.

> 💡 **Tip:** The script resolves all file paths relative to its own folder, so
> it also works from the project root:
>
> ```powershell
> python numpy_basics/numpy_basics.py
> ```
>
> No matter which folder you run it from, it reads and writes the files in
> `numpy_basics/`.

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `numpy_basics.py`.
3. Click the **Run ▶** button in the top-right corner of the editor
   (or press `Ctrl+F5`).
4. The program runs in the **Terminal** panel. Interact with it there.

> 💡 **Tip:** Because the program reads input with `input()`, always run it in
> the **Terminal** panel — not the "Output" panel, which can't accept typed input.

---

## 🗂️ What the program creates

| Section | File created      | Purpose                     |
| ------- | ----------------- | --------------------------- |
| 0       | (deletes files)   | Removes the generated files |
| 8       | `saved_array.txt` | Plain-text array output     |
| 8       | `saved_array.npy` | Binary array output         |

> `measurements.csv` is the **input** file (15 sensor readings) and is never
> modified. The generated files are optional and ignored by git.

---

## 🐞 Debugging with VS Code (step-by-step, for beginners)

Debugging lets you **pause** the program at any line, **inspect** the values of
variables, and **step through** the code one line at a time.

### Step 1 — Set a breakpoint

1. Open `numpy_basics.py`.
2. Click in the **gutter** (the narrow column to the left of the line numbers)
   next to a line of code. A **red dot** appears.

   For example, click next to the `a + 10` line inside `section_vectorized()`.
   Watching the element-wise math compute is a great way to understand
   vectorization.

### Step 2: Start the debugger

1. Press **`F5`** (or go to **Run ▸ Start Debugging**).
2. The program starts and **pauses** when it hits your breakpoint.

### Step 3: Inspect variables

1. When paused, hover over a variable name (like `a`) to see its value.
2. Use the **Variables** panel in the left sidebar to inspect all variables.
3. Use the **Debug Console** at the bottom to type expressions, e.g.:

   ```python
   a * 2
   a.shape
   ```

4. Press **`F10`** to step to the next line, or **`F5`** to continue to the
   next breakpoint.

> 💡 **Tip:** In the Debug Console you can call any NumPy function, so you can
> experiment without editing the file.

---

## 📚 Further reading

- [NumPy absolute beginners guide](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [NumPy array creation](https://numpy.org/doc/stable/reference/routines.array-creation.html)
- [NumPy indexing](https://numpy.org/doc/stable/user/basics.indexing.html)
- [NumPy ufuncs](https://numpy.org/doc/stable/reference/ufuncs.html)
- [NumPy statistics](https://numpy.org/doc/stable/reference/routines.statistics.html)
