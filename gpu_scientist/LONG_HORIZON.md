# The 2–3 year value of an H100 and an A100

This part can't be scored by Sunday. It is an argument from public evidence, with every assumption stated, three scenarios instead of one number, and a list of the things that would change the view. Numbers are reproducible with `GPU_PACK=<pack> python -m gpu_scientist.long_horizon` (writes `long_horizon.json` and `long_horizon.png`). Anchor date: November 2026, the origin of the short-horizon forecast.

Rental and resale are kept apart throughout. They are different markets with different buyers, and in 2025 they moved in opposite directions (American Compute: H100 rents fell while median resale prices rose). Converting one into the other would hide that.

![scenarios](long_horizon.png)

## 1. The answer

| | Nov 2026 (anchor) | Nov 2028: low / **base** / high | Nov 2029: low / **base** / high |
|---|---|---|---|
| H100 rental, $/GPU-hr | 3.00 | 1.27 / **2.32** / 3.18 | 0.82 / **2.04** / 3.28 |
| A100 rental, $/GPU-hr | 1.65 | 0.59 / **1.19** / 1.65 | 0.36 / **1.01** / 1.65 |
| H100 resale, $ per used SXM module | 14,250 | 3,600 / **8,000** / 12,100 | 1,800 / **6,000** / 11,100 |
| A100 resale, $ per used SXM 80GB module | 5,400 | 1,100 / **2,600** / 4,400 | 500 / **1,900** / 3,900 |

Rental is a "market midpoint": between spot and on-demand, close to 1- to 12-month reserved. Resale is a typical realized sale of a bare module, not a dealer ask and not a whole HGX node (whole nodes sell for more per GPU; see 2). Rents are posted prices, the competition's measure; transacted A100 rent is about a third lower (H4 in section 3). The base case is more bearish than the market's forward curve (hollow diamonds), on purpose (section 4A).

In one sentence: in the base case an H100 still rents for about $2 an hour in 2029, roughly what an A100 rents for now, while its resale value falls faster than its rent, to around 40% of today's realized price.

## 2. Anchors (what is true today)

Rental, from our pack (GetDeploying weekly medians, week of 2026-11-02, `aggregator_medians.csv`):

| GPU | spot | reserved 1m | reserved 12m | on-demand |
|---|---|---|---|---|
| A100 | 1.51 | 1.70 | 1.68 | 1.99 |
| H100 | 2.52 | 3.36 | 3.21 | 4.02 |
| H200 | 3.46 | 3.95 | 3.56 | 4.87 |
| B200 | 4.78 | 8.09 | 7.64 | 7.80 |

Outside checks: Ornn's OCPI H100 index at $2.92 on 2026-10-01 (three-month range $2.46–$3.17); SemiAnalysis 1-year H100 contract midpoint around $2.80 in October 2026, up from a $1.70 trough in October 2025; Akash A100 80GB average $1.54 (August 2026). So $3.00 for H100 and $1.65 for A100 are the midpoint anchors.

Resale, from American Compute's October 2026 Rack Report (data through August 2026): used H100 SXM 80GB typical realized sale $14,250 (25th percentile $13,200, dealer ask 1.16× realized); HGX 8×H100 node $195,000 ($24,400 per GPU). Used A100 SXM4 80GB $4,700–5,400, down about 35% over the year; HGX 8×A100 80GB node $95,200 ($11,900 per GPU). Dealer and listing prices run much higher (used H100 $18–22k, used A100 80GB $12–18k on GPUnex), which is why we anchor on realized sales.

The last year went the "wrong" way for a depreciation story. In our pack, over Nov 2025 → Nov 2026, A100 on-demand rose from $1.60 to $1.99 and H100 from $2.98 to $4.02. CoreWeave signed an A100 contract that runs into 2029 and said prior-generation pricing is at or above where it was years ago. The base case must explain this, not ignore it.

## 3. Five hypotheses, tested before they are assumed

Each assumption below was first written as a hypothesis and checked against our pack or against outside data. Pack numbers come from `long_horizon.py` (GetDeploying weekly medians, first four weeks of Nov 2025 against the last four weeks to Nov 2026; `long_horizon.json`, key `pack_tests`).

| # | Hypothesis | Evidence | Verdict |
|---|---|---|---|
| H1 | The price gap between generations today equals how fast one GPU's price falls over time | Pack, Nov 2026: across A100, H100, H200 and B200, rent falls 25–26% per year of age in every pricing mode (on-demand, 1- and 12-month reserved, spot). Over the same year the A100 itself moved between -32% and +23%, and the H100 between -16% and +33%, depending on the mode. CCIR's cross-section gives -21% per year of age (Sep 2026); Dilikoglu's gives 33–45%, and both say it is not a time series. | **Rejected.** The cross-section is an upper bound on the decline, not the decline itself. |
| H2 | Rental and resale move together | A100 resale fell about 35% over the year (American Compute) while posted A100 on-demand rent rose 23% (pack). In 2025, H100 rents fell while H100 resale rose. | **Rejected.** They are forecast separately. |
| H3 | Older GPUs drift down to performance parity | A100 ÷ H100 price is now 0.47–0.55 depending on the mode (pack), between parity on compute (0.41, MLPerf units) and on memory bandwidth (0.61). It fell in three of four modes over the year (on-demand 0.51 → 0.47, 12-month 0.82 → 0.55). CCIR finds rents per unit of memory bandwidth almost flat across generations. | **Partly supported.** A100 is converging on compute parity but is priced closer to bandwidth. That is why A100's base decline (-15%/yr) is steeper than H100's (-12%). |
| H4 | Posted prices are what deals clear at | Ornn's transacted A100 index is $1.02–1.10 against our posted midpoint of $1.65; for H100 it is $2.96–3.19 against $3.00. In early 2026 Ornn ran 25–30% below Silicon Data's posted-rate index. | **Rejected for A100, close for H100.** Our view is on posted prices (the competition's measure); transacted A100 rent is about a third lower. |
| H5 | The market already expects a steep decline | Silicon Data's 36-month forwards (3 Sep 2026): H100 -12.3% and A100 -24.9% in total, about -4% and -9% a year. The forward curve is ordered by chip age, and B200's is flat. | **Rejected.** The market prices a slow decline; our base case is more bearish than the forward (see below). |

## 4. Assumptions (the argument)

**A. Newer generations push older ones down, but slower than the cross-section suggests (H1, H3).** The H100's own history gives the range of plausible decline rates. SemiAnalysis's composite fell about 34% a year from $6.62 (H2 2023) to $2.84 (Oct 2025), and 1-year contracts about 21% a year to a $1.70 trough. Then rents recovered: 1-year contracts reached about $2.40 by April 2026, 41% above the trough, and late-October 2026 spot indices were back around a year earlier's level. The forward curve says -4% a year. Our base (-12% H100, -15% A100) sits between the forward and the historical rates, because Rubin (H2 2026), Rubin Ultra (H2 2027) and Feynman (2028) will add supply the forward may underweight, while the rebound shows the catch-up decline of 2023–25 is not the steady state.

**B. Power and buildings slow the slide.** Air-cooled A100 racks draw about 6.5 kW, in halls built for about 20 kW per rack; GB200/GB300 racks draw 120–140 kW. Per unit of power, air-cooled chips rent at $4.49–5.75 per kW-hour against $6.85–7.03 for liquid-cooled Blackwell (CCIR). This is the reason given for CoreWeave's A100-to-2029 contract.

**C. Rent has a floor.** Below cash operating cost (power at PUE 1.3 and $0.08/kWh, colocation around $150 per kW-month, a share of network and staff) an owner turns the GPU off rather than renting it. We put this at about $0.35/hr for H100 (700 W) and $0.25/hr for A100 (400 W). The low scenarios stay above it. The BLS electricity price index is the input to watch.

**D. Resale falls faster than rent, because remaining life shrinks (H2).** A buyer pays for the cash a GPU will still earn. Today a used node sells for about 1.5–1.6 years of net rental cash (H100: $24,400 per GPU against about $15,300 a year at 70% utilisation; A100: $11,900 against $7,900). In the base case for 2028 that multiple falls to about 1.1–1.2 years. Utilisation is the weakest input: there is no public source, operators report 85–90%, and 65% is a common bearish figure.

**E. Scenario rates (annual, from the November 2026 anchor).**

| | low | base | high | market forward |
|---|---|---|---|---|
| H100 rental | -35% | -12% | +3% | about -4% |
| A100 rental | -40% | -15% | 0% | about -9% |
| H100 resale | -50% | -25% | -8% | none |
| A100 resale | -55% | -30% | -10% | none |

- Low = glut: Rubin ships in volume, AI demand growth slows, rebuilt halls take Blackwell and Rubin, older capacity is dumped. Rents fall at the 2023–25 catch-up pace. H100 resale in 2028 lands near American Compute's conservative residual band (5–7% of list).
- Base = the cascade continues: frontier training moves to Blackwell and Rubin, H100 and A100 shift to inference and fine-tuning in halls that can't host the new racks.
- High = compute scarcity persists: power, not chips, is the constraint through 2029, and old capacity stays fully booked, as in 2026.

**F. What the rates mean for financing.** Dilikoglu's one-megawatt model finds that, after a 3-year contract, the market rent can fall 28% a year (6-year book life), 31% (5-year) or 37% (4-year) before post-contract value drops below book value. Our base case is well inside all three; our low case crosses the 6- and 5-year thresholds. So the depreciation fight (hyperscalers and CoreWeave at 6 years, Nebius at 5, Burry at 2–3) is really a fight about which of our scenarios happens. The retirement record supports long lives: Azure's K80, P100 and P40 each ran 7–9 years, and the V100 about 7.5.

## 5. What would change the view

| Signal | Moves us toward | Where to watch |
|---|---|---|
| Rubin rentals listed widely below about $1 per A100-unit of work | low | GetDeploying, our collectors |
| H100 1-yr contract midpoint below $2.00 for a quarter | low | SemiAnalysis, Ornn OCPI |
| Ornn's transacted A100 index catching up with posted prices, or posted prices falling to it | H4 resolved, A100 base holds or low | Ornn OCPI, our collectors |
| Silicon Data 36-month forward moving below -25% for H100 | low | Silicon Data term structure |
| Kalshi H100 monthly markets (Ornn-settled, listed through Aug 2027) pricing well above or below $3 | high / low | Kalshi KXH100MS (pointer only, not copied) |
| Large A100 or H100 contracts renewed at or above previous prices | high | CoreWeave, Nebius earnings calls |
| American Compute resale index falling faster than 35%/yr | low (resale) | Rack Report |
| Hyperscalers shortening GPU useful lives again | low (resale) | 10-K filings |
| Grid and data-centre power delays worsening | high | utility interconnection queues |

## 6. Limits

- This is a scenario argument, not a fitted forecast; it cannot be backtested on a 13-week panel.
- The capability units are composite, unverified ratios built from MLPerf results; the A100 → H100 step uses 2023 rounds with early H100 software.
- Resale data is thin (American Compute flags limited samples, liquidity grade B–C), and the resale index is restatable.
- Hypothesis tests on the pack use one year of weekly medians; reserved and spot medians rest on 5–14 providers, so their year-on-year changes are noisy. On-demand medians use 39–46 providers.
- The age curve uses approximate ages (A100 5.9, H100 3.9, H200 2.3, B200 1.6 years) and mixes the capability differences that make newer chips dearer.
- Several sources (ComputeLabs, CCIR, Ornn) have commercial interests in GPU financing or price data; company statements are not independently verified.
- "Market midpoint" rent hides the spread between spot and on-demand, which is itself 1.3–1.6× today.

## Sources

- GetDeploying weekly GPU price medians (CC BY 4.0), in our pack as `aggregator_medians.csv`; capability units from the pack's `capability/capability_units.csv` (MLPerf results, Apache-2.0 repositories).
- [American Compute, H100 appraisal](https://www.amcompute.com/appraisals/h100), [A100 appraisal](https://www.amcompute.com/appraisals/a100), [A100 SXM4 80GB](https://www.amcompute.com/appraisals/a100-sxm4-80gb) (October 2026 Rack Report).
- [Dilikoglu Research, what an old GPU is worth (29 Oct 2026)](https://dilikogluresearch.com/reports/old-gpu-worth-2026-10-29); [CCIR, GPU age curve (Sep 2026)](https://ccir.io/research/gpu-age-curve); [ComputeLabs, nine years of A100s](https://www.computelabs.ai/research/nine-years-of-a100s-a-review-of-how-long-gpus-earn); [Compute and LLM dashboard, rental prices and forward curves](https://kadentato.github.io/Compute-and-LLM-Dashboard/compute/prices-full.html); [Ornn GPU indices](https://data.ornn.com/analytics/gpu).
- [CloudZero, H100 cost (Ornn OCPI, B200 spot)](https://www.cloudzero.com/blog/h100-gpu-cost); IntuitionLabs articles on data-center GPU prices and H100 rental prices (2026).
- [Akash, A100 guide (Aug 2026)](https://akash.network/bits/nvidia-a100-gpu-guide-2026-specs-benchmarks-pricing/); [GPUNex, buying and selling GPUs 2026](https://www.gpunex.com/blog/buying-selling-gpus-2026); [Hashrate Index, used GPU market](https://hashrateindex.com/blog/used-gpu-market-pricing-deprecation-secondary-ai/).
- [Tom's Hardware, CoreWeave A100 contract into 2029](https://www.tomshardware.com/tech-industry/coreweave-ceo-mike-intrator-says-it-has-signed-an-a100-contract-running-into-2029); [Benzinga](https://www.benzinga.com/node/61145901).
- NVIDIA roadmap (Rubin, Rubin Ultra, Feynman), as reported from GTC 2026 by Network World and Tom's Hardware.
- Depreciation schedules and the Burry critique, as reported by SiliconANGLE and Tom's Hardware.
