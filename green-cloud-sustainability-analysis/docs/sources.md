# Source citations

All figures in `data/*.csv` are sourced from primary published documents.
This list captures the URLs consulted and the data they fed.

| Source | What it informed |
|--------|------------------|
| AWS — Customer Carbon Footprint Tool documentation | AWS reporting cadence, Scope 2 methodology, per-region availability |
| Amazon — 2023 Sustainability Report | AWS net-zero commitment, renewable matching status, global PUE |
| Microsoft — 2023 Environmental Sustainability Report | Azure scope coverage, water disclosure, Scope 3 detail |
| Microsoft — Emissions Impact Dashboard documentation | Azure customer tooling, reporting cadence, methodology |
| Google — 2023 Environmental Report | GCP commitment, 24/7 CFE target, per-region disclosure |
| Google Cloud — Carbon Footprint product docs | GCP customer tooling, methodology versioning |
| Ember — Yearly Electricity Data | Country-level grid carbon intensity (gCO2/kWh) |
| IEA — Electricity 2024 | Cross-check on country-level grid intensity |
| Uptime Institute — Global Data Center Survey 2023 | PUE benchmarks for cloud vs on-premise comparison |
| EU Taxonomy Climate Delegated Act, Annex I §8.1 | Substantial-contribution and DNSH criteria for data centres |
| GHG Protocol — Corporate Standard, Scope 2 Guidance | Scope 1/2/3 reporting maturity rubric |
| GHG Protocol — Scope 3 Standard | Scope 3 Cat. 1 (purchased goods/services) requirements for cloud spend |

## Data refresh policy

Provider sustainability data should be re-pulled at least annually. Methodologies change
year over year; scoring rubrics in METHODOLOGY.md are the stable reference for re-scoring.

The dataset in this repo is a **dated snapshot**, not a live source.
