# Methodology — Green Cloud Sustainability Analysis

## 1. Scope of the comparison

This analysis covers AWS, Azure, and GCP — the three hyperscale providers that account for the majority of public-sector and regulated-industry cloud spend. Smaller providers (Oracle, IBM Cloud, OVH, Hetzner) and specialty AI clouds (CoreWeave, Lambda) are out of scope.

Comparison is operational only: published commitments, renewable sourcing strategies, reporting cadence and granularity, and per-region carbon data. **Embodied emissions of the underlying hardware** and the providers' **upstream Scope 3** are flagged but not scored — disclosure is too inconsistent for fair comparison.

## 2. Scoring rubric

Each dimension is scored 0–3 against an explicit rubric:

| Score | Rubric |
|-------|--------|
| 0 | Not reported / no public commitment |
| 1 | Reported as global aggregate; no breakdown |
| 2 | Reported with regional or category breakdown; not third-party assured |
| 3 | Reported with full granularity; third-party assured to ISAE 3000 or equivalent |

Twelve dimensions in `cloud_sustainability_matrix.csv`:

1. Net-zero commitment year (target year normalised to score; 2030 = 3, 2040 = 2, 2050 = 1)
2. 100% renewable energy commitment (annual matching) — year of attainment claimed
3. 24/7 carbon-free energy (CFE) commitment — % and target year
4. Average global PUE — published and dated
5. Per-region carbon intensity — published?
6. Per-region CFE % — published?
7. Reporting cadence (annual = 1, quarterly = 2, real-time tooling = 3)
8. Scope 1 reporting maturity
9. Scope 2 reporting maturity (location-based AND market-based)
10. Scope 3 reporting maturity (which categories disclosed)
11. Third-party assurance level
12. Customer carbon footprint tooling (built-in dashboards)

A weighted **transparency score** is computed as the unweighted mean across these 12 dimensions, scaled 0–100.

## 3. Mapping to the EU taxonomy

The EU taxonomy for sustainable finance requires that economic activities **substantially contribute** to one of six environmental objectives **without doing significant harm (DNSH)** to the others. For data-centre / cloud-compute activities, the relevant criteria sit under the *Climate change mitigation* objective (Annex I, section 8.1).

The substantial-contribution criterion for data centres requires evidence of:

- Compliance with the **EU Code of Conduct for Energy Efficiency in Data Centres** (Best Practices).
- Documented and reduced PUE.
- Refrigerants below specified GWP thresholds.
- Disclosure of energy and water consumption.

For **cloud customers** (which is where Rabobank-style institutions sit), the practical requirement collapses to: *can you obtain region-level carbon and PUE data from your provider that holds up under audit?* This is what `eu_taxonomy_alignment.csv` scores.

## 4. Mapping to GHG Protocol Scope 1/2/3

For a financial institution **using** cloud, the cloud provider's emissions are mostly the institution's **Scope 3 Category 1** (Purchased goods and services) — specifically the cloud spend portion. To report this credibly, the institution needs:

| Need | Where it sits |
|------|---------------|
| Per-account or per-region kgCO2 figures | Scope 3 Cat. 1 |
| Whether figures are location-based or market-based | Both methodologies are required by GHG Protocol Scope 2 guidance — the institution's accounting choice flows down |
| Whether figures cover compute + storage + network or compute only | Determines completeness |
| Cadence (monthly vs annual) | Determines whether year-end reporting is feasible without estimation |

`scope_alignment.csv` rates each provider against these needs.

## 5. Region recommendations

`region_recommendations.csv` shortlists low-carbon regions across the three providers, scored on:

- Grid carbon intensity (gCO2/kWh, annual avg)
- Reported CFE %
- Distance to common EU data residency requirements (within EU = 3, EEA = 2, outside = 0)
- Connectivity to typical Western European source data (latency / egress cost)

## 6. Sources

All data comes from primary published sources:

- **AWS:** [AWS Sustainability](https://sustainability.aboutamazon.com/), AWS Customer Carbon Footprint Tool documentation, Amazon's 2023 sustainability report.
- **Azure:** [Microsoft Cloud for Sustainability](https://www.microsoft.com/en-us/sustainability/cloud), Microsoft's 2023 environmental sustainability report, Emissions Impact Dashboard documentation.
- **GCP:** [Google Cloud Sustainability](https://cloud.google.com/sustainability), Google's 2023 environmental report, the Carbon Footprint product documentation.
- **Grid intensity:** Ember (yearly electricity data), IEA Electricity 2024.
- **PUE benchmarks:** Uptime Institute Global Data Center Survey.

Each row in the data CSVs has a `source` column with a short citation. `docs/` contains the dated provider URLs used.

## 7. Limitations

- **Self-reported.** Provider data is the providers' own reporting. Third-party assurance helps but doesn't fully eliminate self-report bias.
- **Methodology drift.** Providers periodically change methodology (e.g. how they account for unbundled RECs vs PPAs). Year-over-year comparisons must control for this.
- **Carbon-free energy ≠ low emissions.** A region at 90% CFE on annual average can still be on a high-intensity grid in the off-renewable hours. Hourly intensity matters and is not yet broadly reported.
- **Static snapshot.** The data reflects the state at time of writing. Re-pull annually before relying on it.
