"""Tests for the web app: explorer aggregations, prediction service and every page/API route (synthetic data, light models)."""
import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient

from social_web import explore, predict, server
from social_web.state import load_state
from test_questions import make_posts


@pytest.fixture(scope="module")
def client(tmp_path_factory) -> TestClient:
    df = make_posts()
    df["creator_id"] = "c" + (df.index % 400).astype(str)
    df["creator_name"] = "n" + (df.index % 900).astype(str)
    df["content_url"] = np.where(df.index % 2 == 0, "https://a.com/", "http://b.org/")
    state = load_state(df=df, cache_dir=tmp_path_factory.mktemp("cache"), light=True)
    return TestClient(server.create_app(state))


@pytest.fixture
def posts() -> pd.DataFrame:
    return explore.prepare(make_posts())


def test_filters_and_kpis(posts):
    sub = explore.apply_filters(posts, {"platform": ["TikTok"], "content_type": ["video", "image"]})
    assert set(sub.platform) == {"TikTok"} and set(sub.content_type) <= {"video", "image"}
    cards = {c["id"]: c for c in explore.kpis(sub, posts)}
    assert cards["posts"]["valor"] == len(sub) and abs(cards["top5_views"]["total"] - 5) < 1


def test_breakdown_flags_real_difference(posts):
    posts.loc[posts.platform == "TikTok", "views"] += 300
    rows = {r["grupo"]: r for r in explore.breakdown(posts, "platform", "views")}
    assert rows["TikTok"]["diferente"] and rows["TikTok"]["vs_resto"] > 2
    assert all(r["vs_resto"] < 0 for g, r in rows.items() if g != "TikTok")  # everyone else sits below a boosted rest


def test_breakdown_natural_order(posts):
    assert [r["grupo"] for r in explore.breakdown(posts, "daypart", "views")] == ["madrugada", "manhã", "tarde", "noite"]


def test_explore_rejects_unknown_dimension(posts):
    with pytest.raises(ValueError):
        explore.explore(posts, dimension="nope")


def test_pocket_matching():
    row = {"platform": "TikTok", "content_category": "beauty", "language": "Spanish", "content_length": 200}
    assert predict.pocket_matches({"plataforma": "TikTok", "condicoes": {"content_category": "beauty", "language": "Spanish"}}, row)
    assert predict.pocket_matches({"plataforma": "todas", "condicoes": {"content_length": [174, 316]}}, row)
    assert not predict.pocket_matches({"plataforma": "YouTube", "condicoes": {"content_category": "beauty"}}, row)


@pytest.mark.parametrize("path", ["/", "/perguntas", "/estrategia", "/descobertas", "/explorar", "/prever", "/metodo"])
def test_pages_render(client, path):
    res = client.get(path)
    assert res.status_code == 200 and "Auditoria 52K Posts" in res.text and "{{" not in res.text


def test_api_explore_and_options(client):
    opts = client.get("/api/options").json()
    assert "platform" in opts["filtros"] and "views" in opts["metricas"]
    res = client.post("/api/explore", json={"filtros": {"platform": ["TikTok"]}, "dimensao": "content_type", "metrica": "top5_likes"})
    body = res.json()
    assert res.status_code == 200 and body["posts"] > 0 and body["breakdown"] and body["matriz"]["linhas"] == ["TikTok"]
    assert client.post("/api/explore", json={"dimensao": "nope"}).status_code == 422


def test_api_predict(client):
    res = client.post("/api/predict", json={"platform": "YouTube", "content_type": "image", "hour": 8, "is_sponsored": True})
    body = res.json()
    assert res.status_code == 200
    assert {c["metrica"] for c in body["chances"]} == {"views", "likes", "comments_count"}
    assert len(body["por_formato"]) == 3 * len({c["formato"] for c in body["por_formato"]}) and body["resumo"] and body["post"]["sponsor_category"] != "Not sponsors"
    assert client.post("/api/predict", json={"hour": 30}).status_code == 422


def test_timeseries_drops_partial_months(posts):
    posts = posts.copy()
    posts.loc[posts.index[:5], "month"] = "2020-01"  # a sparse edge month
    assert "2020-01" not in [r["mes"] for r in explore.timeseries(posts, "views")]
