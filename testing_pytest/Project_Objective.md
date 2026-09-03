# 🧪 Testing with pytest

Below is a complete, runnable Python application designed to take a learner
**from writing code to verifying it with automated tests**. Building on the
`builtins_advanced` folder, this interactive "study session" introduces the
**pytest** test framework and teaches how to test functions, classes, and
exceptions — all using only the Python **standard library** plus pytest.

> This folder covers **testing with pytest**. It is the fourth lesson in this
> series (after `builtins_basics`, `builtins_intermediate`, and
> `builtins_advanced`), and the first to introduce a test framework.

---

## Code Analysis Summary

- **Purpose:** A single-file interactive teaching tool that demonstrates how
  to write automated tests with pytest, plus the real `test_*.py` files the
  learner runs.
- **Concepts covered:** `assert`, pytest discovery rules, test functions,
  fixtures (`@pytest.fixture`), parametrization (`@pytest.mark.parametrize`),
  testing classes, `pytest.raises` for exceptions, and markers (`skip`,
  `skipif`, `xfail`, custom).
- **Style:** Heavily commented so each construct is explained *where it
  appears*; safe for learners continuing from advanced built-ins.
- **Notable patterns:** Uses the familiar `main()` menu loop and a classic
  `if __name__ == "__main__"` guard, a `data_path()` helper for folder-relative
  paths, module-level testable classes, and a capstone mini task.

---

## The Concepts (one per section)

| # | Concept                   | What it shows                                                       |
|---|---------------------------|---------------------------------------------------------------------|
| 1 | What is testing & why     | `assert`, catching bugs early, regressions                          |
| 2 | pytest basics             | `test_*` files/functions, running `pytest`                          |
| 3 | Fixtures                  | `@pytest.fixture` — shared setup & teardown                         |
| 4 | Parametrization           | `@pytest.mark.parametrize` — one test, many inputs                  |
| 5 | Testing functions/classes | Testing a `BankAccount` class                                       |
| 6 | Testing exceptions        | `pytest.raises` for error paths                                     |
| 7 | Markers & skipping        | `skip`, `skipif`, `xfail`, custom markers                           |
| 8 | Mini task                 | Write a full test suite for the `Inventory` class                   |

---

## Design Principles

### 1. Assumes the built-ins series' prior lessons are done
This is the fourth lesson. It assumes fundamentals (`builtins_basics`),
everyday stdlib (`builtins_intermediate`), and design patterns
(`builtins_advanced`) are complete.

### 2. Built-in Python first, then pytest
Everything under test uses the Python **standard library** — no NumPy, no
pandas. The only third-party tool is **pytest** itself, which is already
listed in the `dev` dependency group of `pyproject.toml`.

### 3. Testable code lives at module level
The key idea of the lesson: **to test code, it must be importable**. The
classes under test (`BankAccount`, `Account`, `Inventory`) are defined at
**module level** in `testing_pytest.py`, mirroring the ones from
`builtins_advanced` (which were defined inside section functions and could not
be imported). This is a deliberate, teachable contrast.

### 4. One-concept-per-section
Consistent with every other folder, each section is its own function so a
learner can study it in isolation and re-run any part on demand.

### 5. Progression from easy → applied
- Section 1 introduces the *why* of testing with plain `assert`.
- Sections 2–4 cover pytest's core mechanics (discovery, fixtures,
  parametrization).
- Sections 5–6 apply those to real classes and error paths.
- Section 7 covers markers for controlling test runs.
- Section 8 ties everything together with a mini task: complete a test suite
  for the `Inventory` class.

### 6. Real test files ship with the lesson
Unlike the other lessons (which are single-file), this one ships **multiple
`test_*.py` files** — one per concept — so the learner sees pytest's file
discovery in action and can run `pytest` to get a real pass/fail report.

---

## Files in this folder

```
testing_pytest/
├── testing_pytest.py         # the tutorial program + code under test
├── test_math_helpers.py      # Section 2: pytest basics
├── test_fixtures.py          # Section 3: fixtures
├── test_parametrize.py       # Section 4: parametrization
├── test_bank_account.py      # Section 5: testing a class
├── test_exceptions.py        # Section 6: pytest.raises
├── test_markers.py           # Section 7: markers & skipping
├── test_inventory.py         # Section 8: mini task (complete it!)
├── Project_Objective.md      # design notes & concept breakdown (this file)
└── README.md                 # how to run & debug
```

> `.pytest_cache/` and `__pycache__/` are created automatically when you run
> `pytest` — they did not need to be checked in. Menu option **0** removes them.

---

## Getting Started

```powershell
python testing_pytest.py
```

Type a number `1`–`8` to run a section, or `q` to quit.

Then run the tests:

```powershell
pytest
```

See `README.md` for full running and debugging instructions.