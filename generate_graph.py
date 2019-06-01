"""
Fuck python.
"""

from collections import OrderedDict

import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="whitegrid")
sns.set_color_codes("pastel")

DPI = 120
FIG, AXIS = plt.subplots(
    figsize=(1024. / DPI, 1024. / DPI),
    dpi=DPI,
)

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

PLOT = sns.barplot(
    y=list(map(lambda x: x / METRICS["GT 520M"], METRICS.values())),
    x=list(METRICS.keys()),
    label=list(METRICS.keys()),
    color="b"
)

PLOT.set_xticklabels(PLOT.get_xticklabels(), rotation=45, ha="right")

AXIS.set(xlim=(0, 10), ylabel="", xlabel="Relative performance of mobile GPUs")
sns.despine(left=True, bottom=True)

plt.savefig("graph.png", bbox_inches="tight")
