"""Tests for strategy decisions: equivalence rule, break-even math, saturation detection and planted winners."""
import pandas as pd
import pytest

from social_insights import strategy
from test_questions import _boost_likes, make_posts


@pytest.fixture
def posts() -> pd.DataFrame:
    return make_posts()


def test_break_even_formula(posts):
    be = strategy.break_even(posts, cost_per_follower=0.01, target_cpm=10, target_cpe=1e9)
    assert be["threshold"] == pytest.approx(10 * posts["views"].median() / 1000 / 0.01)


def test_cheapest_equivalent_picks_cheapest_tied_option():
    table = pd.DataFrame({"média": [1.0, 1.0, 0.5], "equivalente ao melhor": [True, True, False]}, index=["video", "text", "image"])
    assert strategy.cheapest_equivalent(table, pd.Series({"video": 300, "text": 50, "image": 10})) == "text"


def test_where_to_focus_picks_better_format_even_if_expensive(posts):
    boosted = _boost_likes(posts, posts.content_type == "video", 1.15)
    focus = strategy.where_to_focus(boosted)
    assert "Formato: video" in focus.verdict


def test_frequency_detects_saturation(posts):
    posts = posts.copy()
    day = posts["post_date"].dt.date
    volume = posts.groupby([posts.platform, day])["views"].transform("size")
    posts["views"] = posts["views"] - volume * 150
    assert strategy.frequency_effect(posts)["saturação"].all()


def test_sponsorship_policy_yes_only_with_effect(posts):
    assert "NÃO" in strategy.sponsorship_policy(posts).verdict
    assert "SIM" in strategy.sponsorship_policy(_boost_likes(posts, posts.is_sponsored, 1.10)).verdict


def test_quick_wins_has_owner_and_effort(posts):
    wins = strategy.quick_wins(posts).evidence
    assert {"ação", "esforço", "impacto", "dono"} <= set(wins.columns) and len(wins) >= 5
