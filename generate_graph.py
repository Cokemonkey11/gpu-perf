"""
Fuck python.
"""

from collections import OrderedDict
import importlib

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

METRICS = OrderedDict(
    sorted({
        "GT 520M":     2.26 / 29.4,
        "GTX 1050":    1.,
        "GTX 1050-Ti": 1.22,
        "GTX 1650":    1.22 * 1.42,
        "GTX 1060":    1.22 * 1.42 * 1.12,
        "GTX 1660-Ti": 1.22 * 1.42 * 1.12 * 1.6,
        "RTX 2060":    1.22 * 1.42 * 1.12 * 1.6 * 1.19,
        "RTX 2070":    1.22 * 1.42 * 1.12 * 1.6 * 1.19 * 1.18,
        "RTX 2080":    1.22 * 1.42 * 1.12 * 1.6 * 1.19 * 1.18 * 1.1,
    }.items(), key=lambda x: x[1])
)

def render_graph(y, x, l, outname):
    """Render and generate a graph, resetting the imports (side effects)."""
    importlib.reload(matplotlib)
    importlib.reload(plt)
    importlib.reload(sns)

    sns.set(style="whitegrid")
    sns.set_color_codes("pastel")

    dpi = 120
    FIG, AXIS = plt.subplots(
        figsize=(1024. / dpi, 1024. / dpi),
        dpi=dpi,
    )

    plot = sns.barplot(
        y=y,
        x=x,
        label=l,
        color="b"
    )

    plot.set_xticklabels(plot.get_xticklabels(), rotation=45, ha="right")

    AXIS.set(xlim=(-1, 10), ylabel="", xlabel="Relative performance of mobile GPUs")
    sns.despine(left=True, bottom=True)

    plt.savefig(outname, bbox_inches="tight")

# With 520M for reference.
render_graph(
    list(map(lambda x: x / METRICS["GT 520M"], METRICS.values())),
    list(METRICS.keys()),
    list(METRICS.keys()),
    "graph.png"
)

# Without the 520M for reference.
render_graph(
    list(METRICS.values())[1:],
    list(METRICS.keys())[1:],
    list(METRICS.keys())[1:],
    "graph_no520m.png"
)
