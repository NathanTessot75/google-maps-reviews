import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import MaxNLocator, FuncFormatter
import numpy as np, pandas as pd
for f in font_manager.findSystemFonts(["/usr/share/texmf/fonts/opentype/public/lm"]): font_manager.fontManager.addfont(f)
INK, INK2, GRID, BLUE = "#0b0b0b","#52514e","#e4e3df","#2a78d6"
plt.rcParams.update({"font.family":["Latin Modern Roman","DejaVu Serif"],"font.size":8.5,"xtick.labelsize":7.5,"ytick.labelsize":7.5,
 "axes.edgecolor":INK2,"xtick.color":INK2,"ytick.color":INK2,"axes.linewidth":0.6,"axes.spines.top":False,"axes.spines.right":False,
 "axes.grid":True,"grid.color":GRID,"grid.linewidth":0.5,"axes.axisbelow":True,"pdf.fonttype":42})
df = pd.read_csv("../../data/reviews_annotated.csv")
panels = [("review_rating","Review rating (1–5)",[1,2,3,4,5]),("is_positive","Positive sentiment",[0,1]),
          ("total_reviews","Total reviews of the restaurant",None),
          ("food_quality_score","Food quality",range(-2,3)),("price_quality_score","Value for money",range(-2,3)),
          ("service_score","Service",range(-2,3)),("wait_time_score","Wait time",range(-2,3)),
          ("atmosphere_score","Atmosphere",range(-2,3)),("cleanliness_score","Cleanliness",range(-2,3))]
fig, axs = plt.subplots(3, 3, figsize=(6.3, 5.2))
thousands = FuncFormatter(lambda v, _: f"{int(v):,}")
for ax, (col, lab, levels), letter in zip(axs.flat, panels, "abcdefghi"):
    if levels is None:
        bins = np.logspace(0, np.log10(df[col].max()+1), 30)
        ax.hist(df[col]+1, bins=bins, color=BLUE, edgecolor="white", linewidth=0.6)
        ax.set_xscale("log"); ax.grid(axis="x", visible=False)
    else:
        levels = list(levels); counts = df[col].value_counts().reindex(levels, fill_value=0)
        ax.bar(levels, counts.values, width=0.72, color=BLUE)
        ax.set_xticks(levels, [(f"{l:+d}".replace("-", "−") if l else "0") if col.endswith("_score") else str(l) for l in levels])
        ax.grid(axis="x", visible=False)
    ax.set_xlabel(lab); ax.yaxis.set_major_locator(MaxNLocator(4, integer=True, steps=[1, 2, 5, 10])); ax.yaxis.set_major_formatter(thousands)
    ax.set_title(f"({letter})", loc="left", fontsize=8.5, color=INK)
for ax in axs[:,0]: ax.set_ylabel("Reviews")
fig.tight_layout(h_pad=1.4, w_pad=1.2)
fig.savefig("../figures/fig2_descriptives.pdf", bbox_inches="tight")
