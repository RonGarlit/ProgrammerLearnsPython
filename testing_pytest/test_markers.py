"""
Test file for the pytest lesson — Section 7: markers & skipping.

Markers tag tests with metadata. Built-in markers include skip, skipif, and
xfail. Custom markers (like @pytest.mark.slow) can be registered in
pyproject.toml and selected with `pytest -m slow`.

Docs: https://docs.pytest.org/en/stable/how-to/mark.html

Run it from this folder with:
    pytest test_markers.py -v
"""

import sys

import pytest


# ---------------------------------------------------------------------------
# @pytest.mark.skip  ->  ALWAYS skipped
# ---------------------------------------------------------------------------
# A MARKER is a small tag you put on a test to give pytest extra instructions.
# `@pytest.mark.skip` tells pytest: "do not run this test at all."
#
# In the verbose output this shows up as:
#     test_future_feature SKIPPED (feature not implemented yet)
#
# The `reason=` text is what pytest prints in parentheses — it is your note to
# future-you (and to anyone reading the report) about WHY the test is skipped.
# A skipped test is NOT a failure: it is deliberately excluded from the run.
# Docs: https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-skip
@pytest.mark.skip(reason="feature not implemented yet")
def test_future_feature():
    # This body never runs — pytest skips the whole function before executing
    # a single line. The `raise` here is just a placeholder so that IF someone
    # removes the marker, the test fails loudly instead of silently passing.
    raise NotImplementedError("not implemented yet")


# ---------------------------------------------------------------------------
# @pytest.mark.skipif  ->  skipped only when a CONDITION is True
# ---------------------------------------------------------------------------
# `skipif` is a CONDITIONAL skip. The first argument is a boolean expression;
# if it evaluates to True, the test is skipped. Here the condition is
# `sys.platform == "win32"` — i.e. "are we on Windows?"
#
# You are on Windows, so the condition is True and the test is skipped:
#     test_unix_only SKIPPED (this test only makes sense on non-Windows platforms)
#
# If you ran this same file on macOS or Linux, the condition would be False
# and the test WOULD run (and pass). This is how you write tests that are
# platform-specific without breaking the suite on other machines.
# Docs: https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-skipif
@pytest.mark.skipif(
    sys.platform == "win32",
    reason="this test only makes sense on non-Windows platforms",
)
def test_unix_only():
    # This line only runs on non-Windows platforms. On Windows, pytest never
    # reaches it. The assert is a sanity check: it passes as long as we are
    # NOT on Windows (which is exactly the condition under which we run).
    assert sys.platform != "win32"


# ---------------------------------------------------------------------------
# @pytest.mark.xfail  ->  EXPECTED to fail (and that is OK)
# ---------------------------------------------------------------------------
# `xfail` marks a test that is KNOWN to fail — usually because of a bug that
# has not been fixed yet. Instead of failing the whole suite, pytest reports
# it as:
#     test_known_bug XFAIL (known bug #42 — will be fixed later)
#
# This is useful because:
#   * The suite stays GREEN (a known failure does not block other work).
#   * You still SEE the failure in the report, so it is not forgotten.
#   * If the bug is later fixed and the test starts passing, pytest reports
#     it as XPASS — a signal that you can now remove the xfail marker.
# Docs: https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-xfail
@pytest.mark.xfail(reason="known bug #42 — will be fixed later")
def test_known_bug():
    # This assert is intentionally wrong (1 is never equal to 2), so the test
    # fails — but because of the xfail marker, pytest records it as an
    # EXPECTED failure instead of a suite failure.
    assert 1 == 2


# ---------------------------------------------------------------------------
# A CUSTOM marker  ->  @pytest.mark.slow
# ---------------------------------------------------------------------------
# `slow` is NOT a built-in marker — it is a CUSTOM one we defined. Custom
# markers let you tag tests by category and then select them on the command
# line. This one is registered in pyproject.toml under:
#     [tool.pytest.ini_options]
#     markers = ["slow: marks tests that are slow to run ..."]
#
# Try these commands to see selection in action:
#     pytest -m slow          # run ONLY tests marked "slow"
#     pytest -m "not slow"    # run everything EXCEPT "slow"
# Docs: https://docs.pytest.org/en/stable/how-to/mark.html
@pytest.mark.slow
def test_slow_but_fast_here():
    # This test is tagged "slow" for demonstration, but it is actually fast.
    # The marker is metadata — it does not change what the test does.
    assert 1 + 1 == 2
