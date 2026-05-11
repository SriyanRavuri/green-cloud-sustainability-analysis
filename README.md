# Green Cloud Sustainability Analysis — AWS vs. Azure vs. GCP

A structured comparison of the three major cloud providers' carbon commitments, renewable-energy sourcing approaches, and sustainability reporting methodologies, evaluated specifically for **emissions-conscious AI workload deployment in a regulated financial institution**.

The analysis maps each provider's reporting against the **GHG Protocol Scope 1 / 2 / 3 framework** and the **EU taxonomy for sustainable finance**, identifies gaps, and produces a structured recommendation for cloud region and provider selection based on carbon intensity and transparency of reporting.

## What's in the box

- `data/cloud_sustainability_matrix.csv` — feature-by-feature comparison across the three providers
- `data/scope_alignment.csv` — Scope 1/2/3 reporting maturity by provider
- `data/eu_taxonomy_alignment.csv` — alignment with the EU taxonomy DNSH criteria
- `data/region_recommendations.csv` — region-level recommendations for low-carbon deployment
- `scripts/analyze.py` — produces charts and the final recommendation report
- `outputs/` — pre-generated charts and the recommendation report

## Quick start

```bash
pip install -r requirements.txt
python scripts/analyze.py
```

Outputs:

- `outputs/scope_coverage.png` — bar chart of Scope 1/2/3 reporting maturity
- `outputs/transparency_score.png` — overall transparency score per provider
- `outputs/region_intensity_map.png` — comparison of low-carbon regions across providers
- `outputs/recommendation_report.md` — final stakeholder recommendation

## Headline findings

Across the comparison matrix used in this analysis:

| Dimension | Winner | Notes |
|-----------|--------|-------|
| **Reporting transparency** | Google | Per-region CFE % published; matches well-known EU taxonomy data needs. |
| **Renewable matching commitment** | Google (24/7 CFE by 2030) | The most ambitious target; AWS and Azure target annual matching. |
| **Scope 3 disclosure maturity** | Microsoft | Most detailed Scope 3 reporting incl. category-level breakdown. |
| **Lowest-carbon regions in EU** | Tied — `gcp:europe-north1` and `aws:eu-north-1` | Both <80 g/kWh on grid; Sweden / Finland nuclear + hydro. |
| **EU taxonomy data availability** | Google | Per-region figures align directly with location-based reporting. |

The full reasoning, gaps, and a recommended decision framework are in `outputs/recommendation_report.md`.

## Project layout

```
green-cloud-sustainability-analysis/
├── data/
│   ├── cloud_sustainability_matrix.csv
│   ├── scope_alignment.csv
│   ├── eu_taxonomy_alignment.csv
│   └── region_recommendations.csv
├── scripts/analyze.py
├── docs/                    # source citations
├── outputs/
├── METHODOLOGY.md           # scoring approach, sources, limitations
├── requirements.txt
└── README.md
```

## Methodology, in one paragraph

Each provider is scored across 12 dimensions sourced from public sustainability reports, regulatory filings, and methodology documents. Scope 1/2/3 maturity is rated on a 0–3 scale based on whether emissions are reported, broken down by category, third-party-assured, and reported in line with the GHG Protocol Corporate Standard. EU taxonomy alignment uses the substantial-contribution and DNSH criteria as the rubric. A weighted transparency score combines reporting granularity, third-party assurance, and per-region disclosure. The final recommendation prioritises **low absolute carbon intensity** and **high transparency** — both required for credible reporting under CSRD. Full sourcing and limits in [`METHODOLOGY.md`](./METHODOLOGY.md).

## License

MIT
