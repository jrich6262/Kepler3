from astroquery.jplhorizons import Horizons
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
import numpy as np

DEGREES_PER_ORBIT = 360
DAYS_PER_YEAR = 365.2564

PLANETS = {
    "Mercury": 199,
    "Venus": 299,
    "Earth": 399,
    "Mars": 499,
    "Jupiter": 599,
    "Saturn": 699,
    "Uranus": 799,
    "Neptune": 899
}

t2 = []
a3 = []
names = []

for name, moon_id in PLANETS.items():
    obj = Horizons(id=moon_id, location='@sun')
    table = obj.elements()
    a = float(table['a'][0])
    n = float(table['n'][0])

    t = (DEGREES_PER_ORBIT / n) / DAYS_PER_YEAR

    t2.append(t**2)
    a3.append(a**3)
    names.append(name)

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xscale("log")
ax.set_yscale("log")

# Graph data.
ax.plot(t2, a3, lw=0, marker="o", markersize=6, color="firebrick", zorder=2)

# Add names.
for x, y, name in zip(t2, a3, names):
    ax.annotate(
        name,
        (x, y),
        textcoords="offset points",
        xytext=(7, -7),
        fontsize=10,
        fontweight="bold",
        color="0.2"
    )

# Line of best fit (in log space).
log_t2, log_a3 = np.log10(t2), np.log10(a3)
r_squared = (np.corrcoef(log_t2, log_a3)[0, 1])**2
ax.plot([min(t2), max(t2)], [min(a3), max(a3)], color="gray", linestyle="--",
        label=f"Line of best fit ($\\mathbf{{R^2}}$ = {r_squared:.4f})", zorder=1)

# Create borders.
for spine in ("bottom", "left"):
    ax.spines[spine].set_linewidth(2.5)
    ax.spines[spine].set_color("0.2")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Format ticks and labels.
ax.xaxis.set_minor_locator(NullLocator())
ax.yaxis.set_minor_locator(NullLocator())
ax.tick_params(width=2.5, color="0.2")
plt.setp(ax.get_xticklabels() + ax.get_yticklabels(),
         size=14, weight="bold", color="0.2")

# Create titles.
ax.set_xlabel(r"Period ($\mathbf{years^2}$)", fontsize=14, weight="bold", color="0.2")
ax.set_ylabel(r"Semi-major axis ($\mathbf{AU^3}$)", fontsize=14, weight="bold", color="0.2")
ax.set_title("Kepler's Third Law for Major Bodies", fontsize=14, weight="bold", color="0.2")

ax.legend(frameon=False, prop={"weight": "bold", "size": 12}, labelcolor="0.2")

fig.savefig("MAJOR_BODIES.pdf", bbox_inches="tight", dpi=250, facecolor="white")
plt.close(fig)
