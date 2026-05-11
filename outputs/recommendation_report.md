# Cloud sustainability — recommendation

## At a glance

- **Most transparent provider:** GCP (95.2/100)
- **Runner-up:** Azure (92.1/100)
- **Top low-carbon EU region:** `gcp:europe-north1` — 79 g/kWh, CFE 97%
- **Runner-up region:** `aws:eu-north-1` — 42 g/kWh, CFE 96%

## Recommendation

For a regulated financial workload requiring EU data residency and credible Scope 3 reporting, deploy to **`gcp:europe-north1`**. It combines the lowest absolute grid carbon intensity in the EU with the highest published CFE % and per-region carbon disclosure that aligns directly with EU taxonomy and CSRD reporting needs.

If multi-region is required for resilience, pair with **`aws:eu-north-1`** as a secondary, both keep the workload inside the EU and on low-carbon grids.

## Why

1. **Grid intensity dominates emissions.** Across all hyperscalers, choice of region drives 5–10× swings
   in operational emissions. Region matters more than provider.
2. **Per-region disclosure is non-negotiable for CSRD.** A provider that only reports global aggregate
   numbers cannot supply the data the institution needs to audit its own Scope 3 figures.
3. **24/7 CFE matters more than annual matching as the EU grid decarbonises.** Annual matching
   conceals high-emission hours; 24/7 CFE forces real-time low-carbon generation.

## Provider summary

| Provider | Strengths | Weaknesses |
|----------|-----------|------------|
| **AWS** | Largest EU footprint; lowest intensity in `eu-north-1`/`eu-west-3` | Slowest customer reporting cadence; no per-region CFE % |
| **Azure** | Most granular Scope 3; strong customer dashboard | No 24/7 CFE commitment; mid-range grid in primary EU regions |
| **GCP** | 24/7 CFE target; per-region CFE published; near-real-time tooling | Smaller EU footprint; less Scope 3 detail than Azure |

## Provider × dimension matrix

| dimension                      | aws           | azure         | gcp           | notes                                                                         |
|:-------------------------------|:--------------|:--------------|:--------------|:------------------------------------------------------------------------------|
| net_zero_year                  | 2040          | 2030          | 2030          | AWS Climate Pledge 2040; Microsoft 2030 carbon negative; Google 2030 net zero |
| renewables_100pct_year         | 2025          | 2025          | 2017_achieved | Google claims annual matching since 2017; AWS targets 2025; MS claims 2025    |
| cfe_24x7_target                | not_committed | not_committed | 2030          | Only Google has a 24/7 CFE target                                             |
| global_avg_pue                 | 1.15          | 1.18          | 1.10          | All published 2023 figures                                                    |
| per_region_intensity_published | partial       | yes           | yes           | AWS publishes only for some regions; Azure and GCP per-region                 |
| per_region_cfe_pct_published   | no            | partial       | yes           | Google publishes per-region CFE %; Azure indirectly; AWS not yet              |
| reporting_cadence_score        | 2             | 3             | 3             | AWS quarterly via tool; Azure monthly via dashboard; GCP near-real-time       |
| scope1_maturity                | 3             | 3             | 3             | All three report Scope 1 with assurance                                       |
| scope2_maturity_loc_and_market | 3             | 3             | 3             | All three report both location- and market-based                              |
| scope3_maturity                | 2             | 3             | 2             | Microsoft has the most granular Scope 3 disclosure                            |
| third_party_assurance          | 3             | 3             | 3             | All three carry ISAE 3000 / equivalent on emissions                           |
| customer_footprint_tool        | 2             | 3             | 3             | AWS has CCFT; Azure has Emissions Impact Dashboard; GCP has Carbon Footprint  |

## Scope 1/2/3 reporting maturity

| scope_category          | what_a_customer_needs                            |   aws_score |   azure_score |   gcp_score | notes                                                            |
|:------------------------|:-------------------------------------------------|------------:|--------------:|------------:|:-----------------------------------------------------------------|
| scope1_visibility       | Provider Scope 1 emissions disclosed and assured |           3 |             3 |           3 | Provider's own direct emissions; relevant for full upstream view |
| scope2_location_based   | Per-account location-based kgCO2                 |           2 |             3 |           3 | GCP and Azure expose per-project; AWS by region only             |
| scope2_market_based     | Per-account market-based kgCO2                   |           2 |             3 |           3 | Required for Scope 2 GHG Protocol dual reporting                 |
| scope3_cat1_attribution | Cloud spend allocated to customer Scope 3 Cat 1  |           2 |             3 |           2 | Microsoft most granular                                          |
| reporting_lag           | Time from period end to data availability        |           1 |             3 |           3 | AWS 3 months; Azure ~30 days; GCP near-real-time                 |
| audit_trail             | Methodology versioning + change log              |           2 |             2 |           3 | GCP publishes versioned methodology                              |

## EU taxonomy alignment

| criterion                   | what_it_requires                                                 |   aws_score |   azure_score |   gcp_score | notes                                                                |
|:----------------------------|:-----------------------------------------------------------------|------------:|--------------:|------------:|:---------------------------------------------------------------------|
| eu_code_of_conduct_dc       | Compliance with EU Code of Conduct for DC Energy Efficiency      |           3 |             3 |           3 | All three have facilities accredited                                 |
| pue_disclosure              | Documented and reduced PUE                                       |           3 |             3 |           3 | All publish global PUE; some publish regional                        |
| refrigerant_gwp             | Refrigerants below GWP thresholds                                |           2 |             2 |           3 | GCP publishes most detail on cooling                                 |
| energy_water_disclosure     | Disclosure of energy and water consumption                       |           2 |             3 |           3 | Microsoft publishes water by region; Google by region; AWS aggregate |
| dnsh_circular_economy       | Hardware refurbishment / e-waste                                 |           2 |             2 |           3 | Google has the most detailed circular hardware program disclosure    |
| dnsh_pollution              | Diesel backup runtime disclosure                                 |           1 |             2 |           2 | Limited disclosure across all three                                  |
| customer_data_for_reporting | Per-region data sufficient for customer's own taxonomy reporting |           2 |             3 |           3 | AWS region coverage incomplete                                       |

## Region shortlist

| region_id         | provider   | country   |   grid_intensity_g_per_kwh |   cfe_pct | eu_residency   |   recommendation_score | notes                                                                     |
|:------------------|:-----------|:----------|---------------------------:|----------:|:---------------|-----------------------:|:--------------------------------------------------------------------------|
| gcp:europe-north1 | gcp        | FI        |                         79 |        97 | yes            |                    9.5 | Top pick — lowest intensity in EU + highest CFE + per-region transparency |
| aws:eu-north-1    | aws        | SE        |                         42 |        96 | yes            |                    9.3 | Lowest absolute intensity; CFE % indirect via market matching             |
| aws:eu-west-3     | aws        | FR        |                         24 |        80 | yes            |                    9   | Very low intensity (FR nuclear); reporting maturity moderate              |
| gcp:europe-west1  | gcp        | BE        |                        166 |        90 | yes            |                    8.2 | Good middle option; strong CFE                                            |
| gcp:europe-west4  | gcp        | NL        |                        328 |        82 | yes            |                    7.8 | High CFE despite mid-range grid; data residency NL                        |
| azure:northeurope | azure      | IE        |                        287 |        72 | yes            |                    7.2 | Strong reporting; grid intensity higher than Nordics                      |
| aws:eu-west-1     | aws        | IE        |                        287 |        72 | yes            |                    7   | Same Irish grid as Azure NE; AWS reporting lags                           |
| azure:westeurope  | azure      | NL        |                        328 |        68 | yes            |                    6.8 | Same NL grid; tooling strong                                              |

## Caveats

- All provider figures are self-reported (with third-party assurance for emissions totals).
- Static snapshot — re-pull annually before relying on it for reporting.
- Annual-average grid intensity hides hourly variation; 24/7 CFE matters increasingly.
- Embodied / Scope 3 upstream of the provider hardware is not scored due to inconsistent disclosure.

_See METHODOLOGY.md for sourcing and the full scoring rubric._