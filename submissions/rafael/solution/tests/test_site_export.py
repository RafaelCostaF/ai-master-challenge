"""Tests for the website payload: complete sections, JSON-safe output, pocket conditions and template rendering."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from social_insights import site_export as se
from test_questions import make_posts

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "site"))
import build_site  # noqa: E402


@pytest.fixture(scope="module")
def payload() -> dict:
    df = make_posts()
    df["creator_id"] = "c" + (df.index % 400).astype(str)
    df["creator_name"] = "name" + (df.index % 900).astype(str)
    df["content_url"] = np.where(df.index % 2 == 0, "https://a.com/", "http://b.org/")
    return se.build_payload(df, light=True)


def test_payload_has_every_section(payload):
    assert {"meta", "dados", "respostas", "estrategia", "insights", "modelos", "duracao", "simulador", "kpis"} <= set(payload)
    assert {"q1", "q2", "q3", "q4"} <= set(payload["respostas"]) and len(payload["kpis"]) == 4
    assert len(payload["estrategia"]["recomendacoes"]) == 4


def test_payload_is_json_safe(payload):
    text = se.to_json(payload)
    assert "NaN" not in text and "</" not in text
    assert json.loads(text)["meta"]["posts"] == payload["meta"]["posts"]


def test_simulator_tables_cover_every_metric_and_type(payload):
    sim = payload["simulador"]
    for metric in ["views", "likes", "comments_count"]:
        for media in payload["meta"]["formatos"]:
            key = f"{metric}|{media}"
            assert key in sim["base"] and key in sim["modelo"] and sim["segmentos"][key]


@pytest.mark.parametrize("dimension, value, expected", [
    ("platform × content_category", "TikTok · tech", {"platform": "TikTok", "content_category": "tech"}),
    ("content_length (janela)", "174–316", {"content_length": [174.0, 316.0]}),
    ("follower_count (janela)", "599,598–799,657", {"follower_count": [599598.0, 799657.0]}),
])
def test_pocket_conditions(dimension, value, expected):
    assert se._pocket_conditions(dimension, value) == expected


def test_render_inlines_payload():
    html = build_site.render('{"a":1}', "<script>const DATA = /*__SITE_DATA__*/null;</script>")
    assert 'const DATA = {"a":1};' in html
    with pytest.raises(ValueError):
        build_site.render("{}", "<p>no placeholder</p>")
