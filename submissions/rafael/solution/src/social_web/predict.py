"""Prediction service: turns a planned post into chances of being a top post, expected views/engagement and matching insights."""
from dataclasses import dataclass

import numpy as np
import pandas as pd

from social_insights import engagement_model, hit_probability, views_forecast
from social_insights.data import DAYPARTS, FOLLOWER_TIERS, LENGTH_BINS

METRICS = {"views": "views", "likes": "likes", "comments_count": "comentários"}
EVIDENCE_PLAIN = {"robusta (FDR)": "confirmado", "replicada (2 metades)": "se repetiu nos dois anos", "exploratória": "pista"}
MAX_POCKETS = 6


def _ratio(value: float) -> str:
    return f"{value:.1f}x".replace(".", ",")


def _bin(value: float, edges: dict) -> str:
    return next(label for label, edge in edges.items() if value < edge)


def build_row(post: dict, df: pd.DataFrame) -> dict:
    """Full feature row for one planned post: user inputs + derived bins + creator history (if a known creator is given)."""
    row = dict(post)
    row["daypart"] = _bin(post["hour"], DAYPARTS)
    row["follower_tier"] = _bin(post["follower_count"], FOLLOWER_TIERS)
    row["length_bin"] = _bin(post["content_length"], LENGTH_BINS)
    row["is_sponsored"] = str(post["is_sponsored"])
    row.update(views_forecast.creator_snapshot(df, post.get("creator_id") or ""))
    return row


def pocket_matches(pocket: dict, row: dict) -> bool:
    """Does a discovered pocket (conditions on pre-publication fields) apply to this post?"""
    if pocket["plataforma"] not in ("todas", row["platform"]) or not pocket["condicoes"]:
        return False
    for field, cond in pocket["condicoes"].items():
        if isinstance(cond, list):
            if not (cond[0] <= float(row.get(field, np.nan)) <= cond[1]):
                return False
        elif str(row.get(field)) != str(cond):
            return False
    return True


@dataclass
class PredictionService:
    df: pd.DataFrame
    hits: hit_probability.HitPredictor
    views: views_forecast.ViewsForecaster
    engagement: engagement_model.EngagementPredictor
    pockets: list[dict]

    def predict(self, post: dict) -> dict:
        row = build_row(post, self.df)
        frame = pd.DataFrame([row])
        chances = self._chances(row)
        views = self.views.predict(frame).iloc[0]
        eng = self.engagement.predict(frame).iloc[0]
        matched = [p for p in self.pockets if pocket_matches(p, row)]
        matched.sort(key=lambda p: (p["evidencia"].startswith("explor"), -abs(np.log(p["lift"]))))
        return {"post": row, "chances": chances["atual"], "por_formato": chances["formatos"],
                "views": {"estimativa": views["views previstas"], "min": views["intervalo 90% inf"], "max": views["intervalo 90% sup"],
                          "modelo": views["modelo"], "melhor_que_media": self.views.beats_baseline},
                "engajamento": {"estimativa": eng["engajamento estimado"] * 100, "min": eng["intervalo 90% inf"] * 100,
                                "max": eng["intervalo 90% sup"] * 100, "modelo": eng["modelo"], "melhor_que_media": self.engagement.beats_baseline},
                "descobertas": [{**p, "evidencia_simples": EVIDENCE_PLAIN.get(p["evidencia"], p["evidencia"])} for p in matched[:MAX_POCKETS]],
                "descobertas_total": len(matched), "resumo": self._summary(row, chances["atual"], matched)}

    def _chances(self, row: dict) -> dict:
        """Chance of top 5% per metric for the chosen format and for every other format."""
        formats = sorted(self.df["content_type"].unique())
        frame = pd.DataFrame([{**row, "content_type": f} for f in formats])
        pred = self.hits.predict(frame)
        out = []
        for _, r in pred.iterrows():
            low, high = (float(x) for x in r["segmento IC90 (%)"].split("–"))
            out.append({"formato": r["formato"], "metrica": r["métrica"], "chance": r["chance top 5% (%)"], "base": r["base (%)"],
                        "modelo": r["modelo"], "historico": r["sinal do segmento (%)"], "historico_min": low, "historico_max": high,
                        "posts_parecidos": r["posts no segmento"]})
        return {"atual": [c for c in out if c["formato"] == row["content_type"]], "formatos": out}

    def _summary(self, row: dict, chances: list[dict], matched: list[dict]) -> list[str]:
        """Plain-language sentences for the result card."""
        lines = []
        for c in chances:
            ratio = c["historico"] / c["base"] if c["base"] else 1
            name = METRICS[c["metrica"]]
            if c["historico_min"] > c["base"]:
                lines.append(f"Posts parecidos com este ({c['posts_parecidos']} no histórico) entraram no top 5% de {name} "
                             f"{_ratio(ratio)} mais que o normal. Vale priorizar.")
            elif c["historico_max"] < c["base"]:
                lines.append(f"Posts parecidos com este ficaram abaixo do normal em {name} ({_ratio(ratio)}). Considere outro formato ou idioma.")
        if not lines:
            lines.append("Para este perfil de post, o histórico não mostra vantagem nem desvantagem: a chance de bombar fica na média (~5%).")
        strong = [p for p in matched if not p["evidencia"].startswith("explor")]
        if strong:
            lines.append(f"{len(strong)} padrão(ões) que se repetiram nos dois anos se aplicam a este post. Veja abaixo.")
        return lines
