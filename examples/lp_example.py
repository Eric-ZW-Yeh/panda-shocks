"""Panel local projection of an outcome on the soft-power shock (SPS, z_birth_nat).

    y_{i,t+h} - y_{i,t-1} = a_i + l_t + b_h * z_{i,t} + e_{i,t+h},   h = 0..H

z = z_birth_nat, host and month fixed effects, standard errors clustered by month.
This is the reduced form without controls; add lags and controls as in the paper if needed.

Usage
    python examples/lp_example.py --outcome my_outcome.csv --var y       # columns host, month (YYYY-MM), y
    python examples/lp_example.py --synthetic                             # test on a simulated outcome

Requires pandas, numpy, statsmodels, matplotlib.

Synthetic test: y carries a permanent effect of 0.5 per unit of z. The estimate is 0.5 at h = 0 and drifts
slightly below it at long horizons (about 0.45 at h = 12, 0.4 at h = 24), because with host fixed effects
z_{i,t} is mildly negatively correlated with the host's later births, which also enter y_{t+h} - y_{t-1}.
A noise-free version of the same outcome gives 0.50 / 0.48 / 0.45 / 0.38 at h = 0 / 6 / 12 / 24.
"""
import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SHOCKS = os.path.join(HERE, "..", "data", "panda_shocks_monthly.csv")


def synthetic_outcome(z, beta=0.5, seed=0):
    """y = 100 + host trend + month effect + AR(1) noise + beta * sum of past z (a permanent level effect)."""
    rng = np.random.default_rng(seed)
    d = z[["host", "month", "z_birth_nat"]].copy().sort_values(["host", "month"])
    mon = {m: rng.normal(0, 1) for m in d["month"].unique()}
    out = []
    for h, g in d.groupby("host"):
        e = np.zeros(len(g))
        for k in range(1, len(g)):
            e[k] = 0.5 * e[k - 1] + rng.normal(0, 1)
        shock = beta * g["z_birth_nat"].fillna(0).cumsum().values
        out.append(g.assign(y=100 + 0.01 * np.arange(len(g)) + g["month"].map(mon).values + e + shock))
    return pd.concat(out)[["host", "month", "y"]]


def lp(df, y="y", z="z_birth_nat", H=24, start="2011-01"):
    df = df.sort_values(["host", "month"]).copy()
    g = df.groupby("host")[y]
    rows = []
    for h in range(H + 1):
        df["dy"] = g.shift(-h) - g.shift(1)
        s = df[(df["month"] >= start) & df["dy"].notna() & df[z].notna()]
        X = pd.concat([s[[z]],
                       pd.get_dummies(s["host"], prefix="h", drop_first=True, dtype=float),
                       pd.get_dummies(s["month"], prefix="m", drop_first=True, dtype=float)], axis=1)
        X = sm.add_constant(X)
        codes = pd.factorize(s["month"])[0]
        r = sm.OLS(s["dy"].values, X.values).fit(cov_type="cluster", cov_kwds={"groups": codes})
        rows.append(dict(h=h, b=r.params[1], se=r.bse[1], n=int(r.nobs)))
    return pd.DataFrame(rows)


def plot(res, title, path):
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.fill_between(res.h, res.b - 1.645 * res.se, res.b + 1.645 * res.se, color="#1f2d5c", alpha=0.15, lw=0)
    ax.fill_between(res.h, res.b - res.se, res.b + res.se, color="#1f2d5c", alpha=0.30, lw=0)
    ax.plot(res.h, res.b, color="#1f2d5c", lw=2)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xlabel("months after the birth announcement")
    ax.set_ylabel("response per unit of z")
    ax.set_title(title, fontsize=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    print("figure:", path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outcome", help="csv with columns host, month (YYYY-MM) and the outcome")
    ap.add_argument("--var", default="y")
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--H", type=int, default=24)
    ap.add_argument("--out", default=os.path.join(HERE, "lp_example.png"))
    a = ap.parse_args()

    z = pd.read_csv(SHOCKS)
    if a.synthetic:
        y, var, title = synthetic_outcome(z), "y", "Synthetic outcome (permanent effect 0.5 per unit of z)"
    else:
        if not a.outcome:
            ap.error("give --outcome or --synthetic")
        y, var, title = pd.read_csv(a.outcome), a.var, "Response of %s to z_birth_nat" % a.var
        y["month"] = pd.to_datetime(y["month"]).dt.strftime("%Y-%m")
    df = z.merge(y[["host", "month", var]], on=["host", "month"], how="inner")
    res = lp(df, y=var, H=a.H)
    print(res.round(3).to_string(index=False))
    plot(res, title, a.out)


if __name__ == "__main__":
    main()
