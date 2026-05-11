"""Loads the comparison CSVs, produces charts and the recommendation report."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "outputs"

PROVIDERS = ["aws", "azure", "gcp"]
PROVIDER_LABELS = {"aws": "AWS", "azure": "Azure", "gcp": "GCP"}
PROVIDER_COLORS = {"aws": "#FF9900", "azure": "#0078D4", "gcp": "#4285F4"}


def load_data():
    return {
        "matrix": pd.read_csv(DATA / "cloud_sustainability_matrix.csv"),
        "scope": pd.read_csv(DATA / "scope_alignment.csv"),
        "taxonomy": pd.read_csv(DATA / "eu_taxonomy_alignment.csv"),
        "regions": pd.read_csv(DATA / "region_recommendations.csv"),
    }


def chart_scope_coverage(scope_df: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(scope_df))
    width = 0.27
    for i, p in enumerate(PROVIDERS):
        col = f"{p}_score"
        offset = (i - 1) * width
        ax.bar([xi + offset for xi in x], scope_df[col],
               width=width, label=PROVIDER_LABELS[p], color=PROVIDER_COLORS[p])
    ax.set_xticks(list(x))
    ax.set_xticklabels(scope_df["scope_category"], rotation=20, ha="right")
    ax.set_ylabel("Maturity (0-3)")
    ax.set_ylim(0, 3.3)
    ax.set_title("Scope 1/2/3 reporting maturity by provider")
    ax.legend()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=120)
    plt.close(fig)


def chart_transparency_score(matrix_df: pd.DataFrame, scope_df: pd.DataFrame,
                             taxonomy_df: pd.DataFrame, path: Path) -> dict:
    """Compute transparency scores from the three CSVs and bar chart them."""
    # Only score the rows of the matrix where values are 0-3 (the maturity-style rows).
    scoring_rows = ["per_region_intensity_published", "per_region_cfe_pct_published",
                    "reporting_cadence_score", "scope1_maturity",
                    "scope2_maturity_loc_and_market", "scope3_maturity",
                    "third_party_assurance", "customer_footprint_tool"]
    yn_to_score = {"yes": 3, "partial": 2, "no": 0}
    matrix_subset = matrix_df[matrix_df["dimension"].isin(scoring_rows)].copy()

    def coerce(v):
        if isinstance(v, str) and v.lower() in yn_to_score:
            return yn_to_score[v.lower()]
        try:
            return float(v)
        except (TypeError, ValueError):
            return 0

    scores = {}
    for p in PROVIDERS:
        m_scores = [coerce(x) for x in matrix_subset[p].tolist()]
        s_scores = scope_df[f"{p}_score"].tolist()
        t_scores = taxonomy_df[f"{p}_score"].tolist()
        all_scores = m_scores + s_scores + t_scores
        scores[p] = sum(all_scores) / (len(all_scores) * 3) * 100

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar([PROVIDER_LABELS[p] for p in PROVIDERS],
                  [scores[p] for p in PROVIDERS],
                  color=[PROVIDER_COLORS[p] for p in PROVIDERS])
    for b, p in zip(bars, PROVIDERS):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1,
                f"{scores[p]:.1f}", ha="center", fontsize=11)
    ax.set_ylabel("Transparency score (0-100)")
    ax.set_ylim(0, 105)
    ax.set_title("Overall transparency score — weighted across 26 dimensions")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=120)
    plt.close(fig)

    return scores


def chart_region_intensity(regions_df: pd.DataFrame, path: Path) -> None:
    df = regions_df.sort_values("grid_intensity_g_per_kwh")
    colors = [PROVIDER_COLORS[p] for p in df["provider"]]
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(df["region_id"], df["grid_intensity_g_per_kwh"], color=colors)
    ax.set_xlabel("Grid carbon intensity (gCO2/kWh)")
    ax.set_title("Recommended low-carbon EU regions, by grid intensity")
    ax.invert_yaxis()
    for b, val, cfe in zip(bars, df["grid_intensity_g_per_kwh"], df["cfe_pct"]):
        ax.text(val + 5, b.get_y() + b.get_height() / 2,
                f"{val:.0f} g/kWh • CFE {cfe}%", va="center", fontsize=9)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=120)
    plt.close(fig)


def write_recommendation_report(matrix_df, scope_df, taxonomy_df, regions_df,
                                 transparency_scores: dict, path: Path) -> None:
    top_region = regions_df.sort_values("recommendation_score", ascending=False).iloc[0]
    runner_up = regions_df.sort_values("recommendation_score", ascending=False).iloc[1]
    ranked = sorted(transparency_scores.items(), key=lambda kv: -kv[1])

    lines = [
        "# Cloud sustainability — recommendation",
        "",
        "## At a glance",
        "",
        f"- **Most transparent provider:** {PROVIDER_LABELS[ranked[0][0]]} ({ranked[0][1]:.1f}/100)",
        f"- **Runner-up:** {PROVIDER_LABELS[ranked[1][0]]} ({ranked[1][1]:.1f}/100)",
        f"- **Top low-carbon EU region:** `{top_region['region_id']}` — {top_region['grid_intensity_g_per_kwh']:.0f} g/kWh, CFE {top_region['cfe_pct']}%",
        f"- **Runner-up region:** `{runner_up['region_id']}` — {runner_up['grid_intensity_g_per_kwh']:.0f} g/kWh, CFE {runner_up['cfe_pct']}%",
        "",
        "## Recommendation",
        "",
        f"For a regulated financial workload requiring EU data residency and credible Scope 3 reporting, "
        f"deploy to **`{top_region['region_id']}`**. It combines the lowest absolute grid carbon intensity in the EU "
        f"with the highest published CFE % and per-region carbon disclosure that aligns directly with EU taxonomy "
        f"and CSRD reporting needs.",
        "",
        "If multi-region is required for resilience, pair with **`" + str(runner_up['region_id']) + "`** "
        "as a secondary, both keep the workload inside the EU and on low-carbon grids.",
        "",
        "## Why",
        "",
        "1. **Grid intensity dominates emissions.** Across all hyperscalers, choice of region drives 5–10× swings",
        "   in operational emissions. Region matters more than provider.",
        "2. **Per-region disclosure is non-negotiable for CSRD.** A provider that only reports global aggregate",
        "   numbers cannot supply the data the institution needs to audit its own Scope 3 figures.",
        "3. **24/7 CFE matters more than annual matching as the EU grid decarbonises.** Annual matching",
        "   conceals high-emission hours; 24/7 CFE forces real-time low-carbon generation.",
        "",
        "## Provider summary",
        "",
        "| Provider | Strengths | Weaknesses |",
        "|----------|-----------|------------|",
        "| **AWS** | Largest EU footprint; lowest intensity in `eu-north-1`/`eu-west-3` | Slowest customer reporting cadence; no per-region CFE % |",
        "| **Azure** | Most granular Scope 3; strong customer dashboard | No 24/7 CFE commitment; mid-range grid in primary EU regions |",
        "| **GCP** | 24/7 CFE target; per-region CFE published; near-real-time tooling | Smaller EU footprint; less Scope 3 detail than Azure |",
        "",
        "## Provider × dimension matrix",
        "",
        matrix_df.to_markdown(index=False),
        "",
        "## Scope 1/2/3 reporting maturity",
        "",
        scope_df.to_markdown(index=False),
        "",
        "## EU taxonomy alignment",
        "",
        taxonomy_df.to_markdown(index=False),
        "",
        "## Region shortlist",
        "",
        regions_df.sort_values("recommendation_score", ascending=False).to_markdown(index=False),
        "",
        "## Caveats",
        "",
        "- All provider figures are self-reported (with third-party assurance for emissions totals).",
        "- Static snapshot — re-pull annually before relying on it for reporting.",
        "- Annual-average grid intensity hides hourly variation; 24/7 CFE matters increasingly.",
        "- Embodied / Scope 3 upstream of the provider hardware is not scored due to inconsistent disclosure.",
        "",
        "_See METHODOLOGY.md for sourcing and the full scoring rubric._",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    data = load_data()
    OUT.mkdir(parents=True, exist_ok=True)

    chart_scope_coverage(data["scope"], OUT / "scope_coverage.png")
    chart_region_intensity(data["regions"], OUT / "region_intensity_map.png")
    scores = chart_transparency_score(
        data["matrix"], data["scope"], data["taxonomy"],
        OUT / "transparency_score.png",
    )
    write_recommendation_report(
        data["matrix"], data["scope"], data["taxonomy"], data["regions"],
        scores, OUT / "recommendation_report.md",
    )

    print("Transparency scores:")
    for p, s in scores.items():
        print(f"  {PROVIDER_LABELS[p]}: {s:.1f}/100")
    print(f"Wrote outputs to {OUT}")


if __name__ == "__main__":
    main()
