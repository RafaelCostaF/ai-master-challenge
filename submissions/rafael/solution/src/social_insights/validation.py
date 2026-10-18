"""Method validation: inject a known effect into the data and check the pipeline recovers it (positive control)."""
import numpy as np
import pandas as pd

SEED = 42


def demo_segment(df: pd.DataFrame) -> pd.Series:
    """A plausible "real" winning recipe used as the planted effect."""
    return (df["platform"] == "TikTok") & (df["content_type"] == "video") & (df["content_category"] == "tech")


def inject_uplift(df: pd.DataFrame, mask: pd.Series, metric: str, uplift: float, seed: int = SEED) -> pd.DataFrame:
    """Copy of df where `metric` is redrawn as Poisson(mean × (1 + uplift)) on masked rows."""
    rng = np.random.default_rng(seed)
    out = df.copy()
    out.loc[mask, metric] = rng.poisson(out.loc[mask, metric] * (1 + uplift))
    return out
