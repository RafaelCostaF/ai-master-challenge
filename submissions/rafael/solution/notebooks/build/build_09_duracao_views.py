# Builds 09_duracao_views.ipynb: histograms of video length × views (also exports PNGs for the site).
import sys

from nbbuilder import SETUP, Notebook

nb = Notebook()
nb.md("""
# 09 — Duração do vídeo × views

Somente posts de **vídeo** (`content_type == "video"`); `content_length` = duração em segundos.
Figuras exportadas para `docs/figures/` (uso no site).
""")
nb.code(SETUP + '''
from scipy import stats
from social_insights.data import LENGTH_BINS
FIG_DIR = ROOT / "docs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)
videos = df[df.content_type == "video"].copy()
videos["faixa de duração"] = videos["length_bin"].astype(str)
print(f"{len(videos):,} vídeos · duração {videos.content_length.min()}–{videos.content_length.max()} s · views {videos.views.min():,}–{videos.views.max():,}")
''')

nb.md("## 1. Histograma 2D: duração × views")
nb.code("""
fig, ax = plt.subplots(figsize=(11, 5.5))
counts, xedges, yedges, image = ax.hist2d(videos.content_length, videos.views, bins=[40, 40], cmap="Blues")
fig.colorbar(image, ax=ax, label="nº de vídeos")
bins = pd.cut(videos.content_length, np.arange(0, 630, 30))
med = videos.groupby(bins, observed=True).agg(x=("content_length", "median"), y=("views", "median"))
ax.plot(med.x, med.y, "o-", color=plots.ORANGE, linewidth=2, markersize=5, label="mediana de views (faixas de 30 s)")
ax.set_xlabel("duração do vídeo (segundos)"); ax.set_ylabel("views")
ax.set_title("Duração do vídeo × views (31.500 vídeos)"); ax.legend(loc="upper right", fontsize=8); ax.grid(False)
fig.tight_layout(); fig.savefig(FIG_DIR / "duracao_x_views_hist2d.png", dpi=150); plt.show()
""")

nb.md("## 2. Distribuição de views por faixa de duração")
nb.code("""
order = list(LENGTH_BINS)
colors = [plots.BLUE, plots.ORANGE, "#1baf7a", "#6250d6"]
fig, axes = plt.subplots(1, 2, figsize=(15, 4.8), gridspec_kw={"width_ratios": [1.6, 1]})
edges = np.arange(videos.views.min(), videos.views.max() + 10, 10)
for label, color in zip(order, colors):
    v = videos.loc[videos["faixa de duração"] == label, "views"]
    axes[0].hist(v, bins=edges, density=True, histtype="step", linewidth=2, color=color, label=f"{label} · n={len(v):,} · mediana {v.median():,.0f}")
axes[0].set_xlabel("views"); axes[0].set_ylabel("densidade"); axes[0].set_title("Histograma de views por faixa de duração")
axes[0].legend(fontsize=8)
axes[1].hist(videos.content_length, bins=np.arange(0, 630, 15), color=plots.BLUE, edgecolor="white", linewidth=0.5)
for edge in [60, 180, 360]:
    axes[1].axvline(edge, color=plots.GRAY, linestyle="--", linewidth=1)
axes[1].set_xlabel("duração do vídeo (segundos)"); axes[1].set_ylabel("nº de vídeos"); axes[1].set_title("Histograma de duração (tracejado = faixas)")
fig.tight_layout(); fig.savefig(FIG_DIR / "views_por_faixa_de_duracao.png", dpi=150); plt.show()

summary = videos.groupby("faixa de duração")["views"].agg(["size", "mean", "median", "std"]).loc[order]
summary["vs. média geral (%)"] = (summary["mean"] / videos.views.mean() - 1) * 100
summary.round(2)
""")
nb.code("""
rho, p = stats.spearmanr(videos.content_length, videos.views)
h, p_kw = stats.kruskal(*[g.values for _, g in videos.groupby("faixa de duração")["views"]])
display(Markdown(f"**Spearman duração × views:** ρ = {rho:+.4f} (p = {p:.2f}) · **Kruskal entre faixas:** p = {p_kw:.2f}"))
""")
nb.code("""
short, long_ = videos[videos.content_length < 200].views, videos[videos.content_length >= 200].views
display(Markdown(f"**< 200 s:** {len(short):,} vídeos ({len(short) / len(videos):.0%}), média {short.mean():,.1f} views · "
                 f"**≥ 200 s:** {len(long_):,} vídeos, média {long_.mean():,.1f} views · "
                 f"p = {stats.ttest_ind(short, long_, equal_var=False).pvalue:.2f}"))
""")
nb.md("""
**Leitura:**
- **Duração:** não é uniforme. 58% dos vídeos têm entre ~20 e 200 s (≈ 2,9x mais vídeos por segundo de duração que acima de 200 s), e de 200 a 600 s a distribuição é plana. A mesma forma aparece em imagem, texto e misto, o que confirma que `content_length` não é uma duração real por formato.
- **Histograma 2D:** a mancha mais escura à esquerda é **quantidade de vídeos, não mais views**. Na vertical, a faixa é a mesma em toda duração (~10.000–10.200), e a mediana (laranja) é uma linha reta.
- **Histogramas por faixa:** as 4 curvas se sobrepõem, com medianas de 10.099 a 10.102. Spearman ρ = 0,001 e Kruskal p = 0,83; abaixo × acima de 200 s, p = 0,79.
- **Conclusão: a duração do vídeo não muda as views.** Vídeo curto ou longo deve ser escolhido por custo de produção e formato da plataforma, não por alcance esperado.
""")

nb.save(sys.argv[1])
