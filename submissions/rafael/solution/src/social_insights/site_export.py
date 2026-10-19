"""Builds the JSON payload of the delivery website from the analysis modules (every number and sentence is data-driven)."""
import json
from datetime import datetime

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

from . import (attribute_scan, creators, discovery, engagement_model, focus, hit_probability, questions, strategy, validation,
               views_forecast)
from .data import FOLLOWER_TIERS, LENGTH_BINS, METRICS, PLATFORMS

TARGETS = ["views", "likes", "comments_count"]
VALUE_LABELS = {"Spanish": "espanhol", "English": "inglês", "Chinese": "chinês", "Hindi": "hindi", "Japanese": "japonês",
                "video": "vídeo", "image": "imagem", "text": "texto", "mixed": "misto"}
METRIC_LABELS = {"views": "views", "likes": "likes", "comments_count": "comentários", "shares": "shares"}
GROUP_DIMS = {"platform": "Plataforma", "content_type": "Formato", "content_category": "Categoria", "follower_tier": "Porte do creator"}
SIM_FIELDS = ["platform", "content_type", "content_category", "language", "is_sponsored", "weekday", "audience_gender_distribution",
              "audience_age_distribution", "audience_location"]
POCKET_CARDS = 8
LIGHT_ENGAGEMENT_MODELS = ["Média (baseline)", "Ridge", "LightGBM", "CatBoost"]


# ---------- serialization helpers ----------

def _clean(value):
    """Recursively convert numpy/pandas scalars and NaN to JSON-friendly values."""
    if isinstance(value, dict):
        return {str(k): _clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_clean(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        return None if np.isnan(value) else round(float(value), 6)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    return value


def records(frame: pd.DataFrame, index: bool = False) -> list[dict]:
    out = frame.reset_index() if index else frame
    return _clean(out.to_dict(orient="records"))


def to_json(payload: dict) -> str:
    """JSON safe to inline inside a <script> tag."""
    return json.dumps(_clean(payload), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


# ---------- sections ----------

def meta(df: pd.DataFrame) -> dict:
    return {"posts": len(df), "creators": df["creator_id"].nunique(), "inicio": df["post_date"].min().date().isoformat(),
            "fim": df["post_date"].max().date().isoformat(), "plataformas": PLATFORMS,
            "formatos": sorted(df["content_type"].unique()), "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M")}


def data_quality(df: pd.DataFrame) -> dict:
    stats_table = pd.DataFrame({m: {"média": df[m].mean(), "desvio": df[m].std(), "cv (%)": df[m].std() / df[m].mean() * 100,
                                    "mín": df[m].min(), "máx": df[m].max()} for m in METRICS}).T
    corr = df[METRICS].corr("spearman")
    length_by_type = df.groupby("content_type")["content_length"].quantile([0.25, 0.5, 0.75]).unstack()
    return {"metricas": records(stats_table.rename_axis("métrica"), index=True),
            "correlacao": {"labels": METRICS, "matriz": _clean(corr.values.tolist())},
            "max_corr_abs": float(np.abs(corr.values[np.triu_indices(len(METRICS), 1)]).max()),
            "consistencia_creator": _clean(views_forecast.creator_consistency(df)),
            "mde_views": focus.mde_two_groups(df["views"].std(), len(df) // 2, len(df) // 2),
            "duracao_por_formato": records(length_by_type.rename(columns=lambda q: f"p{int(q * 100)}").rename_axis("formato"), index=True),
            "nomes_por_creator": float(df.groupby("creator_id")["creator_name"].nunique().median()) if "creator_name" in df else None}


def _group_ci(df: pd.DataFrame, col: str, metric: str) -> list[dict]:
    g = df.groupby(col, observed=True)[metric].agg(["mean", "sem", "size"])
    overall = df[metric].mean()
    g["indice"] = g["mean"] / overall * 100
    g["lo"], g["hi"] = (g["mean"] - 1.96 * g["sem"]) / overall * 100, (g["mean"] + 1.96 * g["sem"]) / overall * 100
    return records(g.rename_axis("grupo")[["indice", "lo", "hi", "size"]], index=True)


def answers(df: pd.DataFrame) -> dict:
    q1, q2, q3, q4 = questions.answer_all(df)
    cost = q2.details["Custo implícito por porte de creator (patrocinados)"]
    mix = (pd.crosstab(df["content_type"], df["audience_gender_distribution"], normalize="index") * 100)
    return {
        "q1": {"pergunta": q1.question, "veredito": q1.verdict, "efeitos": records(q1.evidence),
               "grupos": {dim: {"titulo": title, "dados": _group_ci(df, dim, questions.ENGAGEMENT)} for dim, title in GROUP_DIMS.items()},
               "segmentos_testados": int(len(questions.segment_scan(df, questions.DIMENSIONS, questions.ENGAGEMENT)))},
        "q2": {"pergunta": q2.question, "veredito": q2.verdict, "diferencas": records(q2.evidence.rename_axis("medida"), index=True),
               "condicoes": records(q2.details["Em que condições? (uplift do patrocínio por condição)"].head(17)),
               "custo_por_porte": records(cost.rename_axis("porte"), index=True)},
        "q3": {"pergunta": q3.question, "veredito": q3.verdict, "efeitos": records(q3.evidence),
               "mix_formato_genero": {"linhas": mix.index.tolist(), "colunas": mix.columns.tolist(), "valores": _clean(mix.values.tolist())},
               "contextos_testados": int(len(q3.details["Por contexto (plataforma, formato, categoria)"]))},
        "q4": {"pergunta": q4.question, "veredito": q4.verdict, "crencas": records(q4.evidence)},
    }


def strategy_section(df: pd.DataFrame) -> dict:
    recs = strategy.recommend_all(df)
    be = strategy.break_even(df)
    return {"recomendacoes": [{"pergunta": r.question, "decisao": r.verdict, "acoes": r.actions} for r in recs],
            "quick_wins": records(recs[3].evidence), "break_even": records(be["grade"].rename_axis("seguidores"), index=True),
            "threshold": be["threshold"], "premissas": {"custo_por_seguidor": strategy.COST_PER_FOLLOWER, "cpm_alvo": strategy.TARGET_CPM,
                                                         "cpe_alvo": strategy.TARGET_CPE, "custo_producao": strategy.PRODUCTION_COST}}


def _pocket_conditions(dimension: str, value: str) -> dict:
    """Machine-readable condition of a pocket: {column: value} or {column: [lo, hi]} for numeric windows."""
    if dimension.endswith("(janela)"):
        col = dimension.replace(" (janela)", "")
        lo, hi = (float(x.replace(",", "")) for x in value.split("–"))
        return {col: [lo, hi]}
    cols = dimension.split(" × ")
    values = value.split(" · ")
    return dict(zip(cols, values)) if len(cols) == len(values) else {}


def _pocket_records(table: pd.DataFrame, platform: str | None = None) -> list[dict]:
    keep = table[table["evidência"] != "—"]
    rows = []
    for _, r in keep.iterrows():
        rows.append({"plataforma": platform or r.get("plataforma") or "todas", "metrica": r["alvo"], "dimensao": r["dimensão"],
                     "bolsao": r["bolsão"], "condicoes": _pocket_conditions(r["dimensão"], r["bolsão"]), "posts": r["posts"],
                     "taxa": r["taxa top 5% (%)"], "lift": r["lift"], "lift_1": r["lift 1ª metade"], "lift_2": r["lift 2ª metade"],
                     "q": r["q_value"], "evidencia": r["evidência"]})
    return _clean(rows)


def insights(df: pd.DataFrame) -> dict:
    global_tables = {m: discovery.scan_pockets(df, m) for m in TARGETS}
    by_platform = pd.concat([discovery.scan_by_platform(df, m, platforms=PLATFORMS) for m in TARGETS], ignore_index=True)
    by_platform["q_global"] = multipletests(by_platform["p_value"], method="fdr_bh")[1]
    best = by_platform.sort_values("p_value").iloc[0]
    daypart = discovery.daypart_top_rate(df, "comments_count").reindex(PLATFORMS)
    return {
        "resumo_global": {m: discovery.replication_summary(t) for m, t in global_tables.items()},
        "resumo_plataforma": records(discovery.platform_summary(by_platform)[["descobertos na 1ª metade", "replicaram na 2ª metade", "robustos (FDR)"]], index=True),
        "cards_global": {m: records(discovery.insight_cards(t, n=POCKET_CARDS)) for m, t in global_tables.items()},
        "bolsoes": _pocket_records(pd.concat(global_tables.values())) + _pocket_records(by_platform),
        "destaque": _clean({"plataforma": best["plataforma"], "metrica": best["alvo"], "dimensao": best["dimensão"], "bolsao": best["bolsão"],
                            "posts": best["posts"], "taxa": best["taxa top 5% (%)"], "lift": best["lift"], "lift_1": best["lift 1ª metade"],
                            "lift_2": best["lift 2ª metade"], "q": best["q_value"], "q_global": best["q_global"], "testes": len(by_platform)}),
        "horario_comentarios": records(daypart.rename_axis("plataforma"), index=True),
    }


def models(df: pd.DataFrame, views_eval: pd.DataFrame, light: bool = False) -> dict:
    candidates = engagement_model.candidate_models()
    if light:
        candidates = {k: v for k, v in candidates.items() if k in LIGHT_ENGAGEMENT_MODELS}
    eng_summary, _ = engagement_model.compare_models(df, models=candidates)
    sens_models = {k: v for k, v in engagement_model.candidate_models().items() if k in LIGHT_ENGAGEMENT_MODELS}
    planted = validation.inject_engagement_uplift(df, validation.demo_segment(df), uplift=0.05)
    sens, _ = engagement_model.compare_models(planted, models=sens_models)
    scan = attribute_scan.scan(df)
    matrix = attribute_scan.summary_matrix(scan)[TARGETS]
    matrix = matrix.loc[matrix.max(axis=1).sort_values(ascending=False).index]
    return {
        "engajamento": records(eng_summary.rename_axis("modelo"), index=True),
        "sensibilidade": records(sens.rename_axis("modelo")[["R² validação", "supera baseline"]], index=True),
        "views": records(views_eval),
        "varredura": {"atributos": matrix.index.tolist(), "metricas": TARGETS, "valores": _clean(matrix.values.tolist()),
                      "testes": len(scan), "p05": int((scan["p_value"] < 0.05).sum()), "significativos": int(scan["significativo"].sum())},
    }


HIST_BINS = 40


def creators_section(df: pd.DataFrame) -> dict:
    """Creator × results: variance share, spread vs. chance (histograms), persistence of the best and an honest top 10."""
    spread = creators.spread_vs_chance(df)
    edges = np.linspace(min(spread["medias"].min(), spread["medias_acaso"].min()), max(spread["medias"].max(), spread["medias_acaso"].max()), HIST_BINS + 1)
    pers = creators.persistence(df)
    return {"variancia": records(creators.variance_share(df), index=True),
            "dispersao": {"observado": spread["desvio observado"], "acaso": spread["desvio esperado por acaso"], "p_value": spread["p_value"],
                          "centros": ((edges[:-1] + edges[1:]) / 2).round(0).tolist(),
                          "reais": np.histogram(spread["medias"], edges)[0].tolist(), "sorteio": np.histogram(spread["medias_acaso"], edges)[0].tolist()},
            "persistencia": {k: v for k, v in pers.items() if k != "tabela"},
            "ranking": records(creators.leaderboard(df).rename_axis("creator"), index=True), "media_geral": df["views"].mean()}


def video_length(df: pd.DataFrame) -> dict:
    videos = df[df["content_type"] == "video"]
    bins = pd.cut(videos["content_length"], np.arange(0, 630, 30))
    g = videos.groupby(bins, observed=True)["views"].agg(["median", "min", "max", "size"])
    g.index = [int(iv.left) + 15 for iv in g.index]
    faixas = videos.groupby("length_bin", observed=True)["views"].agg(["size", "median", "min", "max"]).reindex(list(LENGTH_BINS))
    return {"bins": records(g.rename_axis("centro"), index=True), "faixas": records(faixas.rename_axis("faixa"), index=True)}


def simulator(df: pd.DataFrame, hit_predictor: hit_probability.HitPredictor, views_fc: views_forecast.ViewsForecaster) -> dict:
    """Everything the in-browser simulator needs: options, base rates, segment tables and the official model per (metric, type)."""
    segments = {}
    for (metric, media), seg in hit_predictor.segment_tables.items():
        table = {}
        for key in seg.table_.index:
            low, high = seg.interval(key)
            table[key] = [round(float(seg.table_[key]) * 100, 2), round(low * 100, 2), round(high * 100, 2), int(seg.sizes_[key])]
        segments[f"{metric}|{media}"] = table
    low, high = views_fc.residual_quantiles
    return _clean({
        "opcoes": {f: sorted(df[f].astype(str).unique().tolist()) for f in SIM_FIELDS},
        "faixas_seguidores": {k: (None if np.isinf(v) else v) for k, v in FOLLOWER_TIERS.items()},
        "faixas_duracao": {k: (None if np.isinf(v) else v) for k, v in LENGTH_BINS.items()},
        "base": {f"{m}|{t}": round(v * 100, 2) for (m, t), v in hit_predictor.base_rates.items()},
        "modelo": {f"{m}|{t}": v for (m, t), v in hit_predictor.chosen.items()},
        "segmentos": segments,
        "views": {"modelo": views_fc.model_name, "estimativa": views_fc.fallback_mean, "lo": views_fc.fallback_mean + low,
                  "hi": views_fc.fallback_mean + high, "supera": views_fc.beats_baseline},
        "avaliacao": records(hit_predictor.evaluation[["métrica", "formato", "modelo", "AUC", "q (AUC)", "ganho Brier vs. base (%)", "adotável"]]),
    })


def build_payload(df: pd.DataFrame, light: bool = False, hit_predictor: hit_probability.HitPredictor | None = None,
                  views_fc: views_forecast.ViewsForecaster | None = None, views_eval: pd.DataFrame | None = None) -> dict:
    """Full site payload. Pass already-trained models to avoid retraining; `light=True` trims the slowest comparison (tests)."""
    views_eval = views_forecast.evaluate(df) if views_eval is None else views_eval
    hit_predictor = hit_probability.HitPredictor.train(df) if hit_predictor is None else hit_predictor
    views_fc = views_forecast.ViewsForecaster.train(df, views_eval) if views_fc is None else views_fc
    payload = {"meta": meta(df), "dados": data_quality(df), "respostas": answers(df), "estrategia": strategy_section(df),
               "insights": insights(df), "modelos": models(df, views_eval, light), "duracao": video_length(df), "criadores": creators_section(df),
               "simulador": simulator(df, hit_predictor, views_fc)}
    payload["kpis"] = headline_kpis(payload)
    return _clean(payload)


def headline_kpis(payload: dict) -> list[dict]:
    """Four figures for the top of the page, read from the payload."""
    scan = payload["modelos"]["varredura"]
    cost = payload["respostas"]["q2"]["custo_por_porte"]
    cpm = [c["cpm_implicito_mediano"] for c in cost]
    hl = payload["insights"]["destaque"]
    hour = min(payload["insights"]["horario_comentarios"], key=lambda r: r["q (hora)"])
    return [
        {"valor": f"{scan['significativos']} de {scan['testes']}", "rotulo": "combinações atributo × métrica com efeito real"},
        {"valor": f"{max(cpm) / min(cpm):.0f}x", "rotulo": "mais caro por mil views no creator mega do que no nano"},
        {"valor": f"{hl['lift']:.1f}x", "rotulo": f"chance de top 5% em {METRIC_LABELS.get(hl['metrica'], hl['metrica'])}: "
                                                 f"{hl['plataforma']} · " + " · ".join(VALUE_LABELS.get(v, v) for v in hl["bolsao"].split(" · "))},
        {"valor": f"{hour['hora mediana top']:.0f}h", "rotulo": f"hora mediana do top 1% de comentários no {hour['plataforma']} (resto: {hour['hora mediana demais']:.0f}h)"},
    ]
