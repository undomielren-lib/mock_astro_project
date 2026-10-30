"""
rrlyrae_pl.py
-------------
Analysis pipeline for the (mock) Kestrel-7 RR Lyrae survey.

Steps
  1. Load raw time-series photometry and drop flagged epochs.
  2. Find each star's pulsation period with a Lomb-Scargle periodogram.
  3. Fit a truncated Fourier series to the phased light curve and compute
     intensity-averaged mean magnitudes and amplitudes in V and I.
  4. Classify stars as RRab (fundamental) or RRc (first overtone).
  5. Fit the I-band period-luminosity (PL) relation and derive the cluster's
     distance modulus using an adopted absolute calibration.
  6. Save the processed catalog, a results summary, and figures.

Usage
  python src/rrlyrae_pl.py                       # run full pipeline
  python src/rrlyrae_pl.py --no-figures          # skip plotting
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import lombscargle

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "kestrel7_photometry.csv"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "figures"

# Adopted calibration (from the mock literature in papers/; see Okafor & Lindqvist 2023)
ADOPTED_PL_SLOPE_I = -1.13
ADOPTED_PL_ZP_I = 0.47
ADOPTED_EBV = 0.08
A_I_PER_EBV = 0.60 * 3.1
FUNDAMENTALIZE_OFFSET = 0.127   # log P_F = log P_1O + 0.127
RRC_PERIOD_CUT = 0.43           # days


# ---------------------------------------------------------------------------
# I/O and cleaning
# ---------------------------------------------------------------------------
def load_photometry(path: Path = RAW, drop_flagged: bool = True) -> pd.DataFrame:
    df = pd.read_csv(path)
    if drop_flagged and "flag" in df:
        df = df[df["flag"] == 0]
    return df.reset_index(drop=True)


def sigma_clip(mag: np.ndarray, nsig: float = 4.0) -> np.ndarray:
    """Boolean mask of points within nsig robust sigma of the median."""
    med = np.median(mag)
    mad = 1.4826 * np.median(np.abs(mag - med))
    return np.abs(mag - med) < nsig * max(mad, 1e-3) * 2.5


# ---------------------------------------------------------------------------
# Period search
# ---------------------------------------------------------------------------
def find_period(t, mag, pmin=0.2, pmax=1.0, n_freq=60000):
    """Return the best period (days) and the periodogram arrays."""
    freqs = np.linspace(1 / pmax, 1 / pmin, n_freq)
    power = lombscargle(t, mag - mag.mean(), 2 * np.pi * freqs, normalize=True)
    best = freqs[np.argmax(power)]
    return 1.0 / best, freqs, power


# ---------------------------------------------------------------------------
# Light-curve modeling
# ---------------------------------------------------------------------------
def fourier_fit(phase, mag, err, order=4):
    """Weighted least-squares Fourier-series fit. Returns a callable model."""
    cols = [np.ones_like(phase)]
    for k in range(1, order + 1):
        cols += [np.cos(2 * np.pi * k * phase), np.sin(2 * np.pi * k * phase)]
    A = np.vstack(cols).T
    w = 1.0 / err
    coef, *_ = np.linalg.lstsq(A * w[:, None], mag * w, rcond=None)

    def model(ph):
        out = np.full_like(ph, coef[0], dtype=float)
        for k in range(1, order + 1):
            out += coef[2 * k - 1] * np.cos(2 * np.pi * k * ph) + coef[2 * k] * np.sin(2 * np.pi * k * ph)
        return out

    return model


def mean_mag_and_amp(model):
    grid = np.linspace(0, 1, 1000, endpoint=False)
    curve = model(grid)
    flux_mean = np.mean(10 ** (-0.4 * curve))
    return -2.5 * np.log10(flux_mean), curve.max() - curve.min()


# ---------------------------------------------------------------------------
# Per-star pipeline
# ---------------------------------------------------------------------------
def analyze_star(star_df: pd.DataFrame) -> dict:
    v = star_df[star_df.band == "V"]
    v = v[sigma_clip(v.mag.values)]
    period, _, _ = find_period(v.mjd.values, v.mag.values)

    result = {"star_id": star_df.star_id.iloc[0], "period_d": period}
    for band in ("V", "I"):
        b = star_df[star_df.band == band]
        b = b[sigma_clip(b.mag.values)]
        phase = (b.mjd.values / period) % 1.0
        model = fourier_fit(phase, b.mag.values, b.mag_err.values)
        mean, amp = mean_mag_and_amp(model)
        resid = b.mag.values - model(phase)
        result[f"mean_{band}"] = mean
        result[f"amp_{band}"] = amp
        result[f"rms_{band}"] = np.std(resid)
        result[f"n_{band}"] = len(b)

    result["type"] = "RRc" if period < RRC_PERIOD_CUT else "RRab"
    result["logP_F"] = np.log10(period) + (FUNDAMENTALIZE_OFFSET if result["type"] == "RRc" else 0.0)
    return result


def build_catalog(phot: pd.DataFrame) -> pd.DataFrame:
    rows = [analyze_star(g) for _, g in phot.groupby("star_id")]
    return pd.DataFrame(rows).sort_values("star_id").reset_index(drop=True)


# ---------------------------------------------------------------------------
# PL relation and distance
# ---------------------------------------------------------------------------
def fit_pl(catalog: pd.DataFrame, band="I"):
    x = catalog["logP_F"].values
    y = catalog[f"mean_{band}"].values
    (slope, intercept), cov = np.polyfit(x, y, 1, cov=True)
    resid = y - (slope * x + intercept)
    return {
        "band": band,
        "slope": slope,
        "slope_err": np.sqrt(cov[0, 0]),
        "intercept": intercept,
        "intercept_err": np.sqrt(cov[1, 1]),
        "scatter": np.std(resid, ddof=2),
        "n_stars": len(x),
    }


def distance_modulus(catalog: pd.DataFrame, n_boot: int = 2000, seed: int = 1):
    """Fix the slope to the adopted calibration, solve for mu0, bootstrap errors."""
    rng = np.random.default_rng(seed)
    a_i = A_I_PER_EBV * ADOPTED_EBV
    m_abs = ADOPTED_PL_SLOPE_I * catalog["logP_F"].values + ADOPTED_PL_ZP_I
    mu_each = catalog["mean_I"].values - a_i - m_abs
    mu0 = np.mean(mu_each)
    boots = [np.mean(rng.choice(mu_each, len(mu_each))) for _ in range(n_boot)]
    stat = np.std(boots)
    sys_err = 0.07  # adopted zero-point + reddening systematic (mock value)
    dist_kpc = 10 ** (mu0 / 5 + 1) / 1000
    return {
        "mu0": mu0,
        "mu0_stat_err": stat,
        "mu0_sys_err": sys_err,
        "distance_kpc": dist_kpc,
        "A_I": a_i,
    }


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def make_figures(phot, catalog, pl, outdir: Path = FIGURES):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    outdir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "font.family": "serif"})
    colors = {"RRab": "#2b5d8a", "RRc": "#c8642a"}

    # Fig 1: PL relation
    fig, ax = plt.subplots(figsize=(5.2, 4.0))
    for t, g in catalog.groupby("type"):
        ax.scatter(g.logP_F, g.mean_I, s=22, c=colors[t], label=t, edgecolor="k", lw=0.3)
    xx = np.linspace(catalog.logP_F.min() - 0.02, catalog.logP_F.max() + 0.02, 50)
    ax.plot(xx, pl["slope"] * xx + pl["intercept"], "k-", lw=1,
            label=f"fit: slope = {pl['slope']:.2f} ± {pl['slope_err']:.2f}")
    ax.invert_yaxis()
    ax.set_xlabel(r"$\log P_F$ [days]")
    ax.set_ylabel(r"$\langle I \rangle$ [mag]")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(outdir / "fig1_pl_relation_I.png", dpi=200)
    plt.close(fig)

    # Fig 2: Bailey (period-amplitude) diagram
    fig, ax = plt.subplots(figsize=(5.2, 4.0))
    for t, g in catalog.groupby("type"):
        ax.scatter(np.log10(g.period_d), g.amp_V, s=22, c=colors[t], label=t, edgecolor="k", lw=0.3)
    ax.set_xlabel(r"$\log P$ [days]")
    ax.set_ylabel(r"$A_V$ [mag]")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(outdir / "fig2_bailey_diagram.png", dpi=200)
    plt.close(fig)

    # Fig 3: example phased light curves
    examples = [catalog[catalog.type == "RRab"].star_id.iloc[0],
                catalog[catalog.type == "RRc"].star_id.iloc[0]]
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.2), sharey=False)
    for ax, sid in zip(axes, examples):
        row = catalog.set_index("star_id").loc[sid]
        for band, c in (("V", "#2b5d8a"), ("I", "#a23b3b")):
            b = phot[(phot.star_id == sid) & (phot.band == band)]
            ph = (b.mjd / row.period_d) % 1
            ax.errorbar(np.r_[ph, ph + 1], np.r_[b.mag, b.mag], yerr=np.r_[b.mag_err, b.mag_err],
                        fmt="o", ms=2.5, c=c, lw=0.5, label=band)
        ax.invert_yaxis()
        ax.set_title(f"{sid} ({row.type}, P = {row.period_d:.4f} d)", fontsize=9)
        ax.set_xlabel("Phase")
        ax.set_ylabel("mag")
        ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(outdir / "fig3_example_lightcurves.png", dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------------------
def main(make_figs=True):
    phot = load_photometry()
    catalog = build_catalog(phot)
    pl = fit_pl(catalog, "I")
    dist = distance_modulus(catalog)

    PROCESSED.mkdir(parents=True, exist_ok=True)
    catalog.round(5).to_csv(PROCESSED / "kestrel7_rrlyrae_catalog.csv", index=False)
    results = {"pl_fit_I": pl, "distance": dist,
               "n_rrab": int((catalog.type == "RRab").sum()),
               "n_rrc": int((catalog.type == "RRc").sum())}
    with open(PROCESSED / "results_summary.json", "w") as f:
        json.dump(results, f, indent=2, default=float)

    if make_figs:
        make_figures(phot, catalog, pl)

    print(f"Stars analyzed: {len(catalog)} ({results['n_rrab']} RRab, {results['n_rrc']} RRc)")
    print(f"I-band PL slope: {pl['slope']:.3f} ± {pl['slope_err']:.3f}  (scatter {pl['scatter']:.3f} mag)")
    print(f"Distance modulus: {dist['mu0']:.3f} ± {dist['mu0_stat_err']:.3f} (stat) ± {dist['mu0_sys_err']:.2f} (sys)")
    print(f"Distance: {dist['distance_kpc']:.2f} kpc")
    return catalog, results


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Kestrel-7 RR Lyrae PL pipeline")
    ap.add_argument("--no-figures", action="store_true")
    a = ap.parse_args()
    main(make_figs=not a.no_figures)
