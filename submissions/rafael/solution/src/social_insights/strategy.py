"""Strategy decisions for Challenge 004: where to focus, sponsorship policy, what to stop, quick wins.

Decision rule used throughout: options that are NOT significantly worse than the best are "equivalent";
among equivalents, the cheapest wins. Cost inputs are explicit, configurable assumptions (the data has no prices).
"""
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

from . import questions
from .data import PLATFORMS
from .questions import ALPHA, ENGAGEMENT, REACH, Answer

# --- Assumptions (replace with the company's real numbers) ---
COST_PER_FOLLOWER = questions.COST_PER_FOLLOWER       # US$ per follower per sponsored post (US$ 10 / 1K followers)
PRODUCTION_COST = {"text": 50, "image": 100, "mixed": 150, "video": 300}  # US$ per in-house post
TARGET_CPM = 10.0    # max US$ per 1,000 views worth paying (paid-social benchmark)
TARGET_CPE = 0.05    # max US$ per interaction (like/share/comment) worth paying
FOLLOWER_GRID = [5_000, 10_000, 25_000, 50_000, 100_000, 250_000, 500_000, 1_000_000]


@dataclass
class Recommendation(Answer):
    actions: list[str] = field(default_factory=list)

    def to_markdown(self, max_rows: int = 12) -> str:
        steps = "\n".join(f"{i}. {a}" for i, a in enumerate(self.actions, 1))
        return super().to_markdown(max_rows).replace("**Resposta:**", "**Decisão:**", 1) + (f"\n\n**Ações:**\n{steps}" if steps else "")


# ---------- building blocks ----------

def equivalence_table(df: pd.DataFrame, by: str, metric: str) -> pd.DataFrame:
    """Each option vs. the best one (Welch t, BH): equivalent = not significantly worse than the best."""
    means = df.groupby(by, observed=True)[metric].agg(["mean", "size"]).sort_values("mean", ascending=False)
    best = means.index[0]
    best_values = df.loc[df[by] == best, metric]
    rows = []
    for option in means.index:
        values = df.loc[df[by] == option, metric]
        p = 1.0 if option == best else stats.ttest_ind(best_values, values, equal_var=False).pvalue
        rows.append({by: option, "n": len(values), "média": values.mean(), "vs. melhor (%)": (values.mean() / best_values.mean() - 1) * 100, "p_value": p})
    table = pd.DataFrame(rows)
    table["q_value"] = multipletests(table["p_value"], method="fdr_bh")[1]
    table["equivalente ao melhor"] = table["q_value"] >= ALPHA
    return table.set_index(by)


def cheapest_equivalent(table: pd.DataFrame, cost: pd.Series) -> str:
    """Among options equivalent to the best, the one with the lowest cost per unit of result."""
    candidates = table[table["equivalente ao melhor"]].join(cost.rename("custo"))
    candidates["custo por resultado"] = candidates["custo"] / candidates["média"]
    return candidates["custo por resultado"].idxmin()


def frequency_effect(df: pd.DataFrame, metric: str = REACH) -> pd.DataFrame:
    """Per platform: do days with more posts get worse per-post results? (Spearman of daily volume vs. daily mean)."""
    daily = (df.assign(day=df["post_date"].dt.date)
               .groupby(["platform", "day"]).agg(posts=(metric, "size"), resultado=(metric, "mean")).reset_index())
    rows = []
    for platform, g in daily.groupby("platform"):
        rho, p = stats.spearmanr(g["posts"], g["resultado"])
        low, high = g["posts"].quantile([0.25, 0.75])
        rows.append({"plataforma": platform, "posts/dia (mediana)": g["posts"].median(), "ρ volume × resultado": rho, "p_value": p,
                     "resultado em dias de baixo volume": g.loc[g.posts <= low, "resultado"].mean(),
                     "resultado em dias de alto volume": g.loc[g.posts >= high, "resultado"].mean()})
    table = pd.DataFrame(rows).set_index("plataforma")
    table["q_value"] = multipletests(table["p_value"], method="fdr_bh")[1]
    table["saturação"] = (table["q_value"] < ALPHA) & (table["ρ volume × resultado"] < 0)
    return table


def implied_costs(df: pd.DataFrame, cost_per_follower: float = COST_PER_FOLLOWER) -> pd.DataFrame:
    """Sponsored posts with implied cost, CPM (per 1K views) and CPE (per interaction)."""
    sp = df[df["is_sponsored"].astype(bool)].copy()
    sp["custo"] = sp["follower_count"] * cost_per_follower
    sp["cpm"] = sp["custo"] / sp[REACH] * 1000
    sp["cpe"] = sp["custo"] / sp["interactions"]
    return sp


def break_even(df: pd.DataFrame, cost_per_follower: float = COST_PER_FOLLOWER, target_cpm: float = TARGET_CPM,
               target_cpe: float = TARGET_CPE) -> dict:
    """Follower threshold where a sponsored post stops paying off, and the engagement each creator size needs."""
    views, interactions = df[REACH].median(), df["interactions"].median()
    max_followers_cpm = target_cpm * views / 1000 / cost_per_follower
    max_followers_cpe = target_cpe * interactions / cost_per_follower
    grid = pd.DataFrame({"seguidores": FOLLOWER_GRID})
    grid["custo do post (US$)"] = grid["seguidores"] * cost_per_follower
    grid["CPM esperado (US$)"] = grid["custo do post (US$)"] / views * 1000
    grid["CPE esperado (US$)"] = grid["custo do post (US$)"] / interactions
    grid["views necessárias p/ CPM-alvo"] = grid["custo do post (US$)"] / target_cpm * 1000
    grid["engajamento necessário p/ CPE-alvo"] = grid["custo do post (US$)"] / (target_cpe * views)
    grid["vale a pena?"] = (grid["CPM esperado (US$)"] <= target_cpm) & (grid["CPE esperado (US$)"] <= target_cpe)
    return {"views medianas": views, "interações medianas": interactions, "teto de seguidores (CPM)": max_followers_cpm,
            "teto de seguidores (CPE)": max_followers_cpe, "threshold": min(max_followers_cpm, max_followers_cpe), "grade": grid.set_index("seguidores")}


# ---------- 1. Where to focus ----------

def where_to_focus(df: pd.DataFrame, production_cost: dict = PRODUCTION_COST, cost_per_follower: float = COST_PER_FOLLOWER) -> Recommendation:
    platform = equivalence_table(df, "platform", REACH).join(equivalence_table(df, "platform", ENGAGEMENT)[["vs. melhor (%)", "equivalente ao melhor"]], rsuffix=" (engajamento)")
    content = equivalence_table(df, "content_type", ENGAGEMENT)
    content["custo de produção (US$)"] = pd.Series(production_cost)
    tier = equivalence_table(df, "follower_tier", ENGAGEMENT)
    tier["custo mediano patrocinado (US$)"] = implied_costs(df, cost_per_follower).groupby("follower_tier", observed=True)["custo"].median()
    frequency = frequency_effect(df)

    platform_tie = platform["equivalente ao melhor"].all() and platform["equivalente ao melhor (engajamento)"].all()
    best_platform = platform.index[0]
    best_format = cheapest_equivalent(content, pd.Series(production_cost))
    best_tier = cheapest_equivalent(tier, tier["custo mediano patrocinado (US$)"])
    saturated = frequency.index[frequency["saturação"]].tolist()

    decision = (
        (f"Plataforma: nenhuma vence (diferenças ≤ {platform['vs. melhor (%)'].abs().max():.2f}%), então concentre em 1–2 por custo operacional e presença do público-alvo. "
         if platform_tie else f"Plataforma: {best_platform} (significativamente melhor). ")
        + f"Formato: {best_format} (mesmo engajamento que o melhor e menor custo por resultado, pela premissa de custo de produção). "
        + f"Creators: {best_tier} (equivalente em engajamento e mais barato). "
        + (f"Frequência: há saturação em {', '.join(saturated)}." if saturated else
           "Frequência: postar mais não reduz o desempenho por post em nenhuma plataforma, então o limite é a capacidade de produção.")
    )
    actions = [
        f"Fixar o mix de produção em {best_format} como padrão; formatos mais caros só com hipótese a testar.",
        f"Priorizar creators {best_tier} nas próximas contratações.",
        "Concentrar o time em 1–2 plataformas (critério: onde está o cliente-alvo e o menor custo operacional)." if platform_tie
        else f"Realocar esforço para {best_platform}.",
        "Aumentar a frequência até o limite da capacidade e reavaliar a saturação mensalmente (`frequency_effect`).",
    ]
    return Recommendation("1. Onde concentrar esforço?", decision, platform,
                          {"Formato (engajamento × custo)": content, "Faixa de creator": tier, "Frequência (saturação por plataforma)": frequency},
                          actions)


# ---------- 2. Sponsorship policy ----------

def sponsorship_policy(df: pd.DataFrame, cost_per_follower: float = COST_PER_FOLLOWER, target_cpm: float = TARGET_CPM,
                       target_cpe: float = TARGET_CPE) -> Recommendation:
    answer = questions.does_sponsorship_work(df, cost_per_follower)
    eng = answer.evidence.loc[f"{ENGAGEMENT} — estratificado"]
    conditions = answer.details["Em que condições? (uplift do patrocínio por condição)"]
    good_conditions = conditions[conditions["significativo"] & (conditions["uplift engajamento (%)"] > 0)]
    be = break_even(df, cost_per_follower, target_cpm, target_cpe)
    costs = implied_costs(df, cost_per_follower)
    within = costs[costs["follower_count"] <= be["threshold"]]
    profile = costs.groupby("follower_tier", observed=True).agg(
        posts=("custo", "size"), cpm_mediano=("cpm", "median"), cpe_mediano=("cpe", "median"), engajamento=(ENGAGEMENT, "mean"))
    profile["dentro do threshold"] = profile["cpm_mediano"] <= target_cpm

    lift = eng["p_value"] < ALPHA and eng["diferença"] > 0
    decision = (
        ("Patrocinar para ganhar desempenho: SIM, " if lift else "Patrocinar para ganhar desempenho: NÃO. O patrocínio não muda engajamento nem alcance. ")
        + ("nas condições com efeito: " + ", ".join(good_conditions["condição"]) + ". " if len(good_conditions) else "Nenhuma condição tem efeito. ")
        + f"Patrocinar só se o post se pagar como mídia: até ~{be['threshold']:,.0f} seguidores "
          f"(até US$ {target_cpm:.0f} por mil views e US$ {target_cpe:.2f} por interação, com ~{be['views medianas']:,.0f} views e ~{be['interações medianas']:,.0f} interações por post). "
        + f"Hoje só {len(within) / len(costs):.0%} dos posts patrocinados estão dentro desse limite. "
        + f"Perfil: {', '.join(profile.index[profile['dentro do threshold']]) or 'nenhuma faixa atual'}, em qualquer plataforma ou categoria. "
          "O engajamento histórico não serve de critério, porque não diferencia creators."
    )
    actions = [
        f"Teto de contratação: {be['threshold']:,.0f} seguidores por post (ou pagamento por desempenho acima disso).",
        f"Contratar por resultado: até US$ {target_cpm:.0f} por mil views ou US$ {target_cpe:.2f} por interação, em vez de preço fixo por post.",
        "Sinalizar publicidade de forma explícita (ex.: #publi): não reduz o engajamento e elimina o risco regulatório.",
        "Todo novo patrocínio entra com grupo de comparação (posts orgânicos parecidos) para medir o ganho real.",
    ]
    return Recommendation("2. Política de patrocínio", decision, answer.evidence,
                          {"Ponto de equilíbrio por tamanho de creator": be["grade"], "Perfil de influenciador (patrocinados)": profile,
                           "Condições testadas": conditions}, actions)


# ---------- 3. Stop doing ----------

def stop_doing(df: pd.DataFrame, production_cost: dict = PRODUCTION_COST, cost_per_follower: float = COST_PER_FOLLOWER,
               target_cpm: float = TARGET_CPM, target_cpe: float = TARGET_CPE) -> Recommendation:
    be = break_even(df, cost_per_follower, target_cpm, target_cpe)
    costs = implied_costs(df, cost_per_follower)
    above = costs[costs["follower_count"] > be["threshold"]]
    fair_price = np.minimum(above[REACH] / 1000 * target_cpm, above["interactions"] * target_cpe)
    sponsorship_waste = (above["custo"] - fair_price).sum()

    content = equivalence_table(df, "content_type", ENGAGEMENT)
    cheapest = cheapest_equivalent(content, pd.Series(production_cost))
    equivalent_formats = content.index[content["equivalente ao melhor"]]
    extra = df[df["content_type"].isin(equivalent_formats)]["content_type"].map(production_cost) - production_cost[cheapest]
    production_waste = extra.clip(lower=0).sum()

    beliefs = questions.what_does_not_work(df).evidence
    rows = [
        {"investimento": f"Patrocínio acima de {be['threshold']:,.0f} seguidores", "posts": len(above),
         "% dos patrocinados": len(above) / len(costs) * 100, "gasto implícito (US$)": above["custo"].sum(),
         "excedente sobre preço justo (US$)": sponsorship_waste, "evidência": "views e engajamento não crescem com seguidores"},
        {"investimento": f"Formatos mais caros que {cheapest} sem ganho", "posts": int((extra > 0).sum()),
         "% dos patrocinados": np.nan, "gasto implícito (US$)": df["content_type"].map(production_cost).sum(),  # total production spend
         "excedente sobre preço justo (US$)": production_waste, "evidência": "engajamento equivalente entre formatos"},
    ]
    for belief in beliefs[beliefs["se sustenta?"] == "não"]["crença de mercado"]:
        rows.append({"investimento": f"Otimizar com base em: {belief}", "posts": np.nan, "% dos patrocinados": np.nan,
                     "gasto implícito (US$)": np.nan, "excedente sobre preço justo (US$)": np.nan, "evidência": "efeito nulo (q ≥ 0,05)"})
    table = pd.DataFrame(rows).set_index("investimento")
    decision = (f"Parar de pagar por alcance que não vem: {len(above):,} posts patrocinados acima do threshold geram ~US$ {sponsorship_waste:,.0f} "
                f"de excedente sobre o preço justo ({sponsorship_waste / costs['custo'].sum():.0%} de todo o gasto implícito com patrocínio). Parar de produzir formatos caros sem ganho (economia potencial ~US$ {production_waste:,.0f}). "
                f"Parar rotinas de otimização sem efeito ({int((beliefs['se sustenta?'] == 'não').sum())} práticas testadas sem efeito).")
    actions = ["Congelar renovações de creators acima do threshold até renegociar por desempenho.",
               f"Migrar a produção padrão para {cheapest}; formatos caros só com teste A/B aprovado.",
               "Retirar do checklist de publicação: \"melhor horário\", \"número ideal de hashtags\" e \"legenda longa\"."]
    return Recommendation("3. O que parar de fazer", decision, table, {"Crenças testadas": beliefs}, actions)


# ---------- 4. Quick wins ----------

def quick_wins(df: pd.DataFrame, **assumptions) -> Recommendation:
    """Actions for this week, derived from the other three recommendations (ordered by impact ÷ effort)."""
    focus, policy, stop = where_to_focus(df), sponsorship_policy(df, **assumptions), stop_doing(df, **assumptions)
    be = break_even(df, **assumptions)
    cheapest = cheapest_equivalent(focus.details["Formato (engajamento × custo)"], pd.Series(PRODUCTION_COST))
    wins = pd.DataFrame([
        {"ação": f"Teto de {be['threshold']:,.0f} seguidores para novos contratos", "esforço": "baixo (regra de compra)",
         "impacto": f"evita ~US$ {stop.evidence.iloc[0]['excedente sobre preço justo (US$)']:,.0f} de excedente", "dono": "Head de Marketing / Compras"},
        {"ação": "Renegociar contratos ativos acima do teto para pagamento por resultado (views ou interações)", "esforço": "médio",
         "impacto": "custo por resultado no nível do mercado", "dono": "Parcerias"},
        {"ação": "Sinalização de publicidade explícita (#publi) como padrão", "esforço": "baixo", "impacto": "conformidade legal sem perda de engajamento", "dono": "Social media"},
        {"ação": f"Mix de produção padrão em {cheapest}",
         "esforço": "baixo", "impacto": f"economia potencial ~US$ {stop.evidence.iloc[1]['excedente sobre preço justo (US$)']:,.0f}", "dono": "Conteúdo"},
        {"ação": "Retirar \"melhor horário\" e \"hashtags ideais\" do checklist", "esforço": "baixo", "impacto": "horas do time liberadas", "dono": "Social media"},
        {"ação": "Recalcular este diagnóstico com os dados da empresa e rodar o 1º teste A/B (patrocinado vs. orgânico parecido)", "esforço": "médio",
         "impacto": "medir o ganho real com dados da empresa", "dono": "AI Master / Analytics"},
    ])
    decision = ("6 ações executáveis nesta semana, sem nova contratação nem ferramenta: 3 cortam custo (teto, renegociação, mix de produção), "
                "1 reduz risco (disclosure), 1 libera tempo do time (checklist) e 1 cria a medição contínua (A/B).")
    return Recommendation("4. Quick wins (esta semana)", decision, wins,
                          {"Base: onde concentrar": pd.DataFrame({"decisão": [focus.verdict]}),
                           "Base: política de patrocínio": pd.DataFrame({"decisão": [policy.verdict]})}, wins["ação"].tolist())


def recommend_all(df: pd.DataFrame) -> list[Recommendation]:
    return [where_to_focus(df), sponsorship_policy(df), stop_doing(df), quick_wins(df)]
