#!/usr/bin/env python3
"""
_origdata.py -- load the data arrays out of the original plotting scripts.

Task 7 Parts A and B require the regenerated panels to plot *exactly* the same values
as the figures they replace. Transcribing a few hundred numbers by hand is the obvious
way to get that wrong, so nothing is transcribed: each original script under
plots/MaestroRAG/Plots/ is executed with its file-writing and display calls stubbed out,
in a scratch working directory, and its module globals are handed back. The regenerated
figures then read the same list and DataFrame objects the originals plotted.

plots/MaestroRAG/Plots/ is never written to. The stubs make savefig a no-op, and the
scratch cwd catches anything else a script might try to emit.
"""

import contextlib
import os
import runpy
import tempfile

ORIG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "MaestroRAG", "Plots",
)

_CACHE = {}


@contextlib.contextmanager
def _sandbox():
    """Run with savefig/show/close stubbed and cwd pointed at a throwaway directory."""
    import matplotlib.pyplot as plt
    import matplotlib.figure as mfigure

    saved = {
        "savefig": plt.savefig,
        "show": plt.show,
        "fig_savefig": mfigure.Figure.savefig,
        "rc": dict(plt.rcParams),
        "cwd": os.getcwd(),
    }
    plt.savefig = lambda *a, **k: None
    plt.show = lambda *a, **k: None
    mfigure.Figure.savefig = lambda self, *a, **k: None
    tmp = tempfile.mkdtemp(prefix="origdata-")
    os.chdir(tmp)
    try:
        yield
    finally:
        os.chdir(saved["cwd"])
        plt.savefig = saved["savefig"]
        plt.show = saved["show"]
        mfigure.Figure.savefig = saved["fig_savefig"]
        # The originals call sns.set_theme, which mutates rcParams globally.
        plt.rcParams.update(saved["rc"])
        plt.close("all")


def load(script_name):
    """Execute one original script in the sandbox and return its globals."""
    if script_name in _CACHE:
        return _CACHE[script_name]
    path = os.path.join(ORIG_DIR, script_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"original script not found: {path}")
    with _sandbox():
        ns = runpy.run_path(path, run_name="__origdata__")
    _CACHE[script_name] = ns
    return ns


def records(ns, key, value_field):
    """Pull an ordered list of numbers out of a list-of-dicts global."""
    return [r[value_field] for r in ns[key]]
