"""
Fuck python.
"""

from collections import OrderedDict
from functools import reduce
import importlib
from typing import List

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Values are, tuple:
# -   relative_perf
# -   is mobile variant
# -   has maxq variant
METRICS = OrderedDict(
    sorted({
        "GT 520M":         (2.26 / 29.3, True,  False),
        "GeForce MX150":   (17.7 / 29.3, True,  False),
        "Intel HD 620":    (8.35 / 29.3, True,  False),
        "GTX 1050":        (1.,          True,  False),
        "Radeon Pro 560X": (26.6 / 29.3, True,  False),
        "GTX 1050-Ti":     (1.23,        True,  True),
        "GTX 1070":        (2.89,        True,  True),
        "GTX 1080":        (3.45,        True,  True),
        "GTX 1650":        (1.74,        False, False),
        "GTX 1060":        (1.94,        True,  True),
        "GTX 1660-Ti":     (3.11,        False, False),
        "RTX 2060":        (3.7,         False, False),
        "RTX 2070":        (4.38,        False, True),
        "RTX 2080":        (4.98,        False, True),
    }.items(), key=lambda x: x[1])
)

def metrics_values(maxq_only: bool) -> List[float]:
    return list(
        map(
            lambda x: x[0],
            filter(
                lambda v: v[2] if maxq_only else True,
                METRICS.values()
            )
        )
    )

def metrics_keys(star_maxq: bool) -> List[str]:
    return list(
        map(
            lambda kv: kv[0] if kv[1][1] else kv[0] + "*",
            METRICS.items()
        )
    )

# There are 6.  Values are provided relative to the same GTX 1050 baseline as in
# METRICS.
MAX_Q_METRICS = OrderedDict(
    sorted({
        "GTX 1050-Ti": 1.15,
        "GTX 1060":    1.87,
        "GTX 1070":    2.62,
        "GTX 1080":    2.99,
        "RTX 2070":    3.33,
        "RTX 2080":    3.62,
    }.items(), key=lambda x: x[1])
)

def render_graph(
    y: List[List[float]],
    x: List[List[str]],
    l: List[str],
    outname: str,
    label: str
):
    """Render and generate a graph, resetting the imports (side effects)."""
    importlib.reload(matplotlib)
    importlib.reload(plt)
    importlib.reload(sns)

    sns.set(style="whitegrid")
    sns.set_color_codes("pastel")

    dpi = 120
    _fig, axis = plt.subplots(
        figsize=(1024. / dpi, 1024. / dpi),
        dpi=dpi,
    )

    plot = sns.barplot(
        y=y[0],
        x=x[0],
        label=l,
        color="b"
    )

    plot.set_xticklabels(plot.get_xticklabels(), rotation=45, ha="right")

    axis.set(
        xlim=(-1, len(x[0]) + 1),
        ylabel="",
        xlabel=label
    )
    sns.despine(left=True, bottom=True)

    if len(x) > 1:
        sns.set_color_codes("muted")
        sns.barplot(y=y[1], x=x[1], color="b")

    plt.savefig(outname, bbox_inches="tight")

# With 520M for reference.
render_graph(
    [list(map(lambda x: x / METRICS["GT 520M"][0], metrics_values(False)))],
    [list(metrics_keys(True))],
    list(metrics_keys(True)),
    "graph.png",
    "Relative perf of mobile GPUs (* = no mobile-only benchmarks) c.f. GTX 1050"
)

# Without the 520M for reference.
render_graph(
    [list(metrics_values(False))[1:]],
    [list(metrics_keys(True))[1:]],
    list(metrics_keys(True))[1:],
    "graph_no520m.png",
    "Relative perf of mobile GPUs (* = no mobile-only benchmarks) c.f. 520M"
)

# Max-Q variants compared to normal (mobile where possible) variants:
render_graph(
    [
        metrics_values(True),
        list(MAX_Q_METRICS.values())
    ],
    [
        list(MAX_Q_METRICS.keys()),
        list(MAX_Q_METRICS.keys())
    ],
    list(MAX_Q_METRICS.keys()),
    "graph_cf_maxq.png",
    "Relative GPU performance, comparing Max-Q variants to normal/mobile"
)
