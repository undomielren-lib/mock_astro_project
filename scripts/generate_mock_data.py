"""
generate_mock_data.py
---------------------
Generates the SYNTHETIC multi-epoch V- and I-band photometry of RR Lyrae
stars in the fictional globular cluster "Kestrel-7".

All values are simulated. Kestrel-7 does not exist; this dataset is for
teaching, testing, and documentation exercises only.

Output:
    data/raw/kestrel7_photometry.csv
    data/raw/kestrel7_star_list.csv   (positions + true input parameters)

Usage:
    python scripts/generate_mock_data.py --seed 2026
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

# --- "True" cluster parameters baked into the simulation --------------------
TRUE_MU0 = 15.12          # true distance modulus (mag)  -> ~10.6 kpc
TRUE_EBV = 0.08           # reddening E(B-V)
R_V = 3.1
A_V = R_V * TRUE_EBV      # V-band extinction
A_I = 0.60 * A_V          # I-band extinction (Cardelli-like ratio)

# I-band PL relation (fundamental-mode, fixed metallicity), mock coefficients
PL_SLOPE_I = -1.13
PL_ZP_I = 0.47
M_V_HB = 0.62             # nearly flat V-band absolute magnitude

CLUSTER_RA = 274.6150     # deg (fictional)
CLUSTER_DEC = -24.8710    # deg (fictional)

N_RRAB = 28
N_RRC = 14
N_EPOCHS = 62
BASELINE_DAYS = 118.0
MJD_START = 61210.0       # mock observing season start


def rrab_shape(phase, amp):
    """Asymmetric saw-tooth light curve: fast rise, slow decline (in mag)."""
    rise = 0.15
    m = np.where(
        phase < rise,
        1.0 - phase / rise,                     # rising branch (brightening)
        (phase - rise) / (1.0 - rise),          # declining branch
    )
    return amp * (m - 0.5)


def rrc_shape(phase, amp):
    """Near-sinusoidal light curve for first-overtone pulsators."""
    return 0.5 * amp * np.sin(2 * np.pi * phase + 0.3)


def main(seed: int, outdir: Path):
    rng = np.random.default_rng(seed)
    stars = []

    for i in range(N_RRAB + N_RRC):
        is_ab = i < N_RRAB
        star_id = f"K7-V{i + 1:03d}"
        if is_ab:
            period = rng.uniform(0.47, 0.74)
            logp_f = np.log10(period)
            amp_v = np.clip(rng.normal(0.95, 0.20), 0.45, 1.35)
        else:
            period = rng.uniform(0.27, 0.41)
            logp_f = np.log10(period) + 0.127  # fundamentalized period
            amp_v = np.clip(rng.normal(0.45, 0.08), 0.25, 0.60)

        m_i_abs = PL_SLOPE_I * logp_f + PL_ZP_I + rng.normal(0, 0.035)  # intrinsic scatter
        m_v_abs = M_V_HB + rng.normal(0, 0.05)

        stars.append(
            dict(
                star_id=star_id,
                ra_deg=CLUSTER_RA + rng.normal(0, 0.02),
                dec_deg=CLUSTER_DEC + rng.normal(0, 0.02),
                true_type="RRab" if is_ab else "RRc",
                true_period_d=period,
                true_amp_V=amp_v,
                true_mean_V=m_v_abs + TRUE_MU0 + A_V,
                true_mean_I=m_i_abs + TRUE_MU0 + A_I,
                epoch0_mjd=MJD_START + rng.uniform(0, period),
            )
        )

    star_df = pd.DataFrame(stars)

    rows = []
    for s in stars:
        mjd = np.sort(MJD_START + rng.uniform(0, BASELINE_DAYS, N_EPOCHS))
        phase = ((mjd - s["epoch0_mjd"]) / s["true_period_d"]) % 1.0
        shape = rrab_shape if s["true_type"] == "RRab" else rrc_shape
        for band, mean, amp in (
            ("V", s["true_mean_V"], s["true_amp_V"]),
            ("I", s["true_mean_I"], 0.63 * s["true_amp_V"]),
        ):
            err = 0.008 + 0.004 * np.exp(mean - 15.5) + rng.uniform(0, 0.004, N_EPOCHS)
            mag = mean + shape(phase, amp) + rng.normal(0, err)
            for t, m, e in zip(mjd, mag, err):
                rows.append((s["star_id"], round(t, 5), band, round(m, 4), round(e, 4)))

    phot = pd.DataFrame(rows, columns=["star_id", "mjd", "band", "mag", "mag_err"])

    # A handful of flagged bad points to make data cleaning realistic
    bad = rng.choice(phot.index, size=25, replace=False)
    phot["flag"] = 0
    phot.loc[bad, "mag"] += rng.choice([-1, 1], size=25) * rng.uniform(0.6, 1.5, 25)
    phot.loc[bad, "flag"] = 1

    outdir.mkdir(parents=True, exist_ok=True)
    phot.to_csv(outdir / "kestrel7_photometry.csv", index=False)
    star_df.round(5).to_csv(outdir / "kestrel7_star_list.csv", index=False)
    print(f"Wrote {len(phot)} photometry rows for {len(star_df)} stars to {outdir}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--outdir", type=Path, default=Path(__file__).resolve().parents[1] / "data" / "raw")
    args = ap.parse_args()
    main(args.seed, args.outdir)
