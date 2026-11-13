# AGENTS.md — Autonomous Build Specification for Google Antigravity (NCSC & Research Edition)

## 1. Project Identity & Scientific Context

* **Repository Name:** `Purba-Medinipur-Rice-AWD-Simulation`
* **Full Study Title:** Integrated Soil-Water-Plant Dynamics Under Reduced Irrigation in Rice: A Field Investigation of Alternate Wetting-Drying and Sensor-Guided Irrigation in Purba Medinipur, West Bengal
* **Target Venue & Standards:** National Children's Science Congress (NCSC) Technical Report, Oral Defense, & Scientific Poster + Undergraduate Research Portfolio (GitHub Pages Live Executable)
* **Location & Agro-Climatic Zone:** Farmer's Field, Egra Sub-Division, Purba Medinipur, West Bengal, India (Coastal Saline & Red-Lateritic Alluvial Transition Zone; Puddled Clay-Loam Lowland Paddy Soil)
* **Season:** Boro Season ($2025\text{--}2026$, Dry-Season Irrigated Rice, *Oryza sativa* L.)
* **Experimental Design:** Randomized Complete Block Design (RCBD) with $4$ irrigation treatments ($T_1, T_2, T_3, T_4$) and $5$ replications ($R_1\text{--}R_5$) across $20$ field plots, plus $1$ independent validation plot (Plot $21$) tested under the calibrated $-15\text{ cm}$ threshold.

---

## 2. One-Line Kickoff Prompt for Antigravity

When starting the agent in Google Antigravity, paste:

> `Read AGENTS.md and autonomously execute Phases 1 through 6 without stopping: build the Python agro-hydrological and physiological simulation engine, generate all NCSC RCBD datasets and ANOVA/CD statistical tables, render all 6 publication-grade 300-DPI figures, build the standalone interactive HTML5 Digital Twin & Farmer Extension Web App in docs/index.html, pass 100% of pytest checks, and write the comprehensive README.md.`

---

## 3. Empirical Field Findings (Mandatory Invariants)

The simulation engine, statistical tables, interactive web app, and `pytest` suite **must** strictly reproduce the empirical field observations from Egra:

1. **Four Irrigation Treatments ($4 \times 5 = 20$ RCBD Plots):**
   * $T_1$ (**Local Conventional Practice**): Unstructured farmer irrigation; heavy reflooding to $+6.5\text{ cm}$ whenever standing water thins to $+1.5\text{ cm}$.
   * $T_2$ (**Standardized Continuous Irrigation**): Scientific continuous submergence maintaining $+1.0\text{ cm}$ to $+5.0\text{ cm}$ standing water depth from transplanting to $10\text{ days}$ before harvest.
   * $T_3$ (**Manual AWD**): Alternate Wetting and Drying monitored via a perforated PVC field water tube (*Pani Pipe*, $15\text{ cm}$ perforated subsurface section); reflooded to $+5.0\text{ cm}$ once the perched water table drops to $-15.0\text{ cm}$ below the soil surface (except during flowering when shallow ponding is maintained).
   * $T_4$ (**Sensor-Guided Adaptive AWD**): Calibrated capacitance/tensiometer soil moisture and water-level sensor network coupled to stage-aware physiological demand, triggering precision reflooding to $+4.2\text{ cm}$ at the exact $-15.0\text{ cm}$ perched water table threshold (roughly $-15\text{ to }-18\text{ kPa}$ matric potential).

2. **Irrigation Water Savings vs. $T_1$:**
   * $T_3$ uses $\approx 24\%$ less irrigation water than $T_1$ (target test range: $23.0\% \text{ to } 25.0\%$).
   * $T_4$ uses $\approx 28\%$ less irrigation water than $T_1$ (target test range: $27.0\% \text{ to } 29.0\%$).

3. **Grain Yield Stability:**
   * Grain yield differs by $< 5\%$ across all four treatments ($T_1, T_2, T_3, T_4$), with treatment differences either statistically non-significant or within narrow agronomic parity ($\approx 6.45 \text{ to } 6.70\text{ t/ha}$).

4. **Primary Outcome — Water Productivity ($\text{WP}$, in $\text{kg grain per m}^3$ of irrigation water):**
   * $T_1$: $\text{WP} \approx 1.00\text{ kg/m}^3$ (acceptable window: $0.96 \text{ to } 1.04\text{ kg/m}^3$).
   * $T_2$: $\text{WP} \approx 1.08\text{ kg/m}^3$ (acceptable window: $1.05 \text{ to } 1.14\text{ kg/m}^3$).
   * $T_3$: $\text{WP} \approx 1.31\text{ kg/m}^3$ (acceptable window: $1.28 \text{ to } 1.35\text{ kg/m}^3$).
   * $T_4$: $\text{WP} \approx 1.39\text{ kg/m}^3$ (acceptable window: $1.35 \text{ to } 1.42\text{ kg/m}^3$).

5. **Physiological & Biochemical Parity (Zero Stress at $-15\text{ cm}$):**
   * At the $-15\text{ cm}$ threshold, leaf **Relative Water Content** ($\text{RWC} \approx 83.8\text{--}84.9\%$), **Chlorophyll Content** ($\text{SPAD} \approx 39.7\text{--}40.7$, total chlorophyll $\approx 2.65\text{--}2.78\text{ mg/g FW}$), and **Free Proline Content** ($\approx 1.88\text{--}2.04\text{ }\mu\text{mol/g FW}$) remain statistically comparable across $T_1, T_2, T_3, T_4$ (Two-way RCBD ANOVA treatment $P > 0.05$, marked $\text{NS}$).

6. **Threshold Calibration & Independent Validation Plot (Plot $21$):**
   * Sweeping the reflood depth from $0\text{ cm}$ to $-30\text{ cm}$ proves that $z_{\text{crit}} = -15.0\text{ cm}$ sits at the capillary fringe limit of puddled clay-loam soil: deeper drying ($-18\text{ cm}$ to $-30\text{ cm}$) breaks hydraulic continuity, triggering an exponential surge in osmoregulatory proline ($> 3.8\text{ }\mu\text{mol/g FW}$), a drop in $\text{RWC}$ ($< 75\%$), and spikelet sterility / grain yield loss ($> 12\%$).
   * Independent Validation Plot (Plot $21$) managed under the derived $-15.0\text{ cm}$ threshold achieves $\approx 26.5\text{--}28.0\%$ water savings, $\text{WP} \approx 1.36\text{ kg/m}^3$, grain yield within $2\%$ of $T_1$, and baseline proline ($\approx 1.97\text{ }\mu\text{mol/g FW}$).

---

## 4. Target Repository Architecture

Generate all files in the following layout:

```
.
├── AGENTS.md
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── config.py                  # Egra soil, weather, crop stage, & RCBD constants
│   ├── hydrology.py               # Daily perched water table, sensor moisture, ETa, & percolation
│   ├── physiology.py              # RWC, SPAD chlorophyll, Bates proline, growth & yield components
│   ├── rcbd_experiment.py         # 20-plot RCBD simulator + Plot 21 independent validation
│   ├── statistics_ncsc.py         # Two-way RCBD ANOVA, SEm, CD(0.05), CV%, & Tukey HSD groupings
│   └── threshold_calibration.py   # Pareto sensitivity sweep (0 cm to -30 cm) & extension impact
├── scripts/
│   ├── run_all.py                 # Master orchestrator: runs model, stats, CSVs, & 6 figures
│   └── generate_figures.py        # 6 NCSC poster & report figures (300 DPI PNG + vector PDF)
├── data/
│   ├── rcbd_20plots_full_dataset.csv
│   ├── daily_water_table_110days.csv
│   ├── ncsc_anova_cd_summary_table.csv
│   ├── threshold_sensitivity_sweep.csv
│   ├── independent_validation_plot21.csv
│   └── egra_extension_advisory_table.csv
├── reports/
│   └── NCSC_Statistical_and_Field_Report.md
├── figures/
│   ├── fig1_rcbd_layout_and_water_balance.png
│   ├── fig2_daily_perched_water_table_sawtooth.png
│   ├── fig3_water_use_yield_and_productivity.png
│   ├── fig4_physiological_biochemical_parity.png
│   ├── fig5_threshold_calibration_pareto_curve.png
│   └── fig6_farmer_extension_savings_impact.png
├── docs/
│   └── index.html                 # Standalone interactive HTML5/JS Digital Twin & Advisory App
└── tests/
    └── test_egra_awd_simulation.py
```

---

## 5. First-Principles Biophysical & Statistical Formulation

### 5.1 Daily Agro-Hydrological State-Space Model (`src/hydrology.py`)

Simulate a $110\text{-day}$ Boro season crop cycle ($100\text{ days}$ active irrigation window + $10\text{ days}$ terminal ripening drainage) across plot $(i, b)$ where $i \in \{T_1, T_2, T_3, T_4\}$ and block $b \in \{1..5\}$:

1. **Daily Water Flux Balance ($\text{mm/day}$):**
   $$\Delta W_{i,b}(t) = I_{i,b}(t) + P_{\text{eff}}(t) - ET_{a,i,b}(t) - DP_{i,b}(t) - S_{\text{bund},i,b}(t)$$
   where $ET_{a,i,b}(t) = K_s(t) \cdot K_c(t) \cdot ET_0(t)$, with crop coefficient $K_c(t)$ transitioning across initial ($1.05$), vegetative/tillering ($1.15$), reproductive/flowering ($1.22$), and maturity ($0.90$) stages.

2. **Perched Water Table Depth $z_{i,b}(t)$ ($\text{cm}$ relative to soil surface):**
   Using subsurface specific yield (drainable porosity) $S_{y,b} = 0.15 + \delta_b$ for Purba Medinipur puddled clay-loam above a compacted plough pan at $-22\text{ cm}$:
   $$z_{i,b}(t+1) = \begin{cases} z_{i,b}(t) + \frac{\Delta W_{i,b}(t)}{10.0} & \text{if } z_{i,b}(t) \ge 0 \text{ (standing ponded water)} \\ z_{i,b}(t) + \frac{\Delta W_{i,b}(t)}{10.0 \cdot S_{y,b}} & \text{if } z_{i,b}(t) < 0 \text{ (subsurface perched water table)} \end{cases}$$
   Handle exact piecewise flux integration when $\Delta W_{i,b}(t)$ crosses the $z = 0$ boundary on any day.

3. **Calibrated Sensor Volumetric Soil Moisture $\theta_{v,i,b}(t)$ ($\%$):**
   Map perched water table depth $z(t)$ to root-zone volumetric water content ($\theta_s = 48.5\%$ saturated when $z \ge 0$) via the van Genuchten capillary fringe relation:
   $$\theta_{v,i,b}(t) = \begin{cases} \theta_s & \text{if } z_{i,b}(t) \ge 0 \\ \theta_r + \frac{\theta_s - \theta_r}{\left(1 + \left|\alpha_{\text{vg}} \cdot z_{i,b}(t)\right|^{n_{\text{vg}}}\right)^{1 - 1/n_{\text{vg}}}} & \text{if } z_{i,b}(t) < 0 \end{cases}$$
   At $z = -15.0\text{ cm}$, $\theta_v \approx 39.2\%$ (well above the critical stress point $\theta_{\text{crit}} \approx 34.0\%$).

4. **Darcy Hydrostatic Deep Percolation $DP_{i,b}(t)$ ($\text{mm/day}$):**
   $$DP_{i,b}(t) = \begin{cases} K_{\text{pan},b}\left(1 + \frac{z_{i,b}(t)}{L_{\text{pan}}}\right) & \text{if } z_{i,b}(t) > 0 \\ K_{\text{pan},b} \cdot 0.18 \left(\frac{z_{i,b}(t) + 8.0}{8.0}\right) & \text{if } -8.0 < z_{i,b}(t) \le 0 \\ 0 & \text{if } z_{i,b}(t) \le -8.0 \end{cases}$$

### 5.2 Plant Growth, Physiological, Biochemical & Yield Component Model (`src/physiology.py`)

For every plot $(i, b)$, compute and export both the **core physiological markers** and **agronomic yield components**:

* **Capillary Stress Index:**
  $$S_{i,b}(t) = \max\left(0, \frac{-15.0 - z_{i,b}(t)}{15.0}\right), \qquad \bar{S}_{i,b} = \frac{1}{D}\sum_{t=0}^{D-1} S_{i,b}(t)$$
* **Physiological & Biochemical Assays (at $50\%$ flowering):**
  * $\text{RWC}_{i,b}\text{ (\%)} = \frac{\text{FW} - \text{DW}}{\text{TW} - \text{DW}} \times 100 = 84.4 - 14.5 \bar{S}_{i,b} + \eta_b + \varepsilon_{\text{rwc}}$
  * $\text{Chlorophyll}_{i,b}\text{ (SPAD)} = 40.2 - 9.0 \bar{S}_{i,b} + 0.4\eta_b + \varepsilon_{\text{chl}}$
  * $\text{Total Chlorophyll}_{i,b}\text{ (mg/g FW)} = 0.067 \cdot \text{SPAD}_{i,b} + \varepsilon_{\text{tchl}}$
  * $\text{Free Proline}_{i,b}\text{ (}\mu\text{mol/g FW)} = 1.94 + 6.5\left(\exp(2.2\bar{S}_{i,b}) - 1\right) + \varepsilon_{\text{pro}}$
* **Agronomic Growth & Yield Components:**
  * Plant height at harvest ($\text{cm}$, $\approx 98\text{--}102\text{ cm}$)
  * Effective panicle-bearing tillers per hill ($\approx 13.5\text{--}14.8$, slightly higher in AWD due to root oxygenation and phyllochron stimulation!)
  * Panicle length ($\text{cm}$, $\approx 22.8\text{--}23.6\text{ cm}$)
  * Filled grains per panicle ($\approx 128\text{--}136$)
  * $1000\text{-grain}$ test weight ($\text{g}$, $\approx 23.8\text{--}24.2\text{ g}$)
  * Grain yield ($\text{kg/ha}$ and $\text{t/ha}$), Straw yield ($\text{t/ha}$), and Harvest Index ($\text{HI}$, $\%$).

### 5.3 NCSC Agricultural Biometrics Engine (`src/statistics_ncsc.py`)

Implement an exact **Two-Way RCBD ANOVA** solver partitioning total variance across $t = 4$ treatments and $r = 5$ blocks ($N = 20$):
* Degrees of freedom: $df_{\text{Block}} = r - 1 = 4$, $df_{\text{Trt}} = t - 1 = 3$, $df_{\text{Error}} = (r-1)(t-1) = 12$, $df_{\text{Total}} = 19$.
* Compute Error Mean Square ($\text{EMS}$), Treatment $F\text{-ratio}$, $P\text{-value}$, Standard Error of Mean:
  $$\text{SEm}\pm = \sqrt{\frac{\text{EMS}}{r}}$$
* Compute Critical Difference at the $5\%$ significance level ($\alpha = 0.05$):
  $$\text{CD}_{0.05} = \text{SEm}\pm \times \sqrt{2} \times t_{0.05, df=12}$$
* Export `data/ncsc_anova_cd_summary_table.csv` and `reports/NCSC_Statistical_and_Field_Report.md` formatted exactly like an Indian Council of Agricultural Research (ICAR) / NCSC championship logbook table (showing Treatment Means, $\text{SEm}\pm$, $\text{CD}$ at $5\%$, $\text{CV }\%$, and significance flags `*`, `**`, or $\text{NS}$).

---

## 6. Standalone Interactive HTML5 Digital Twin (`docs/index.html`)

Build a single-file, zero-backend, responsive HTML5 + Tailwind CSS + Canvas/SVG interactive web application in `docs/index.html` (ready to open locally in a browser during an NCSC live presentation or host on GitHub Pages) containing **four interactive modules**:

1. **Interactive Perched Water Table ("Pani Pipe") & Sensor Simulator:**
   * Live animated cross-section of a Purba Medinipur rice paddy showing standing water ($z > 0$), soil surface ($z = 0$), root zone, perforated PVC AWD tube, capacitance moisture sensor, and the $-22\text{ cm}$ plough pan.
   * Sliders for **AWD Reflood Threshold** ($0\text{ cm}$ to $-30\text{ cm}$, default $-15\text{ cm}$), **Soil Drainable Porosity $S_y$** ($0.10$ to $0.22$), and **Treatment Selector** ($T_1, T_2, T_3, T_4$).
2. **20-Plot Egra RCBD Field Map & Live Telemetry:**
   * Interactive $4 \times 5$ randomized plot layout grid where clicking any of the $20$ plots (or Plot $21$ Validation Plot) displays its seasonal irrigation volume, minimum water depth, $\text{RWC}$, $\text{SPAD}$ chlorophyll, proline level, grain yield, and water productivity.
3. **Multi-Chart Comparative Analytics:**
   * Interactive charts for the $110\text{-day}$ sawtooth water depth trajectory, treatment comparison bars, and the Pareto threshold calibration curve showing the $-15\text{ cm}$ physiological safety cliff.
4. **Egra Sub-Division Farmer Extension Advisory Calculator (English + Bengali Toggle):**
   * Allows a local farmer or NCSC judge to input land area in **Bigha**, **Katha**, **Acre**, or **Hectare** and pump type (electric submersible vs. diesel pump), and outputs:
     * Recommended PVC Pani Pipe installation & $-15\text{ cm}$ reflood schedule (with flowering stage safety warning).
     * Exact litres / $\text{m}^3$ of groundwater saved, pump electricity ($\text{kWh}$) or diesel ($\text{L}$) saved, and net cost savings in $\text{INR}$ ($\text{Rs.}$).

---

## 7. Six High-Resolution NCSC Poster & Report Figures (`scripts/generate_figures.py`)

Generate all $6$ figures at $300\text{ DPI}$ in `figures/` with clean typography, error bars, and statistical annotations:

1. `fig1_rcbd_layout_and_water_balance.png`: Panel A shows the $20\text{-plot}$ RCBD field randomization map + Independent Validation Plot $21$; Panel B shows stacked seasonal water balance components ($ET_a$, Deep Percolation, Surface Ponding/Seepage) across $T_1\text{--}T_4$.
2. `fig2_daily_perched_water_table_sawtooth.png`: $4\text{-panel}$ daily perched water table trajectories $z(t)$ ($\text{cm}$) over $110\text{ days}$ for $T_1\text{--}T_4$, highlighting the $-15\text{ cm}$ critical threshold dashed line and the shaded reproductive ponding window (Days $58\text{--}72$).
3. `fig3_water_use_yield_and_productivity.png`: $3\text{-panel}$ bar chart (with $\pm \text{SEm}$, $\text{CD}_{0.05}$ whiskers, and Tukey HSD letters) for Seasonal Irrigation Input ($\text{mm}$), Grain Yield ($\text{t/ha}$), and Irrigation Water Productivity ($\text{kg/m}^3$).
4. `fig4_physiological_biochemical_parity.png`: $3\text{-panel}$ combined boxplot + individual replicate scatter ($n=5$ per treatment) for Relative Water Content ($\text{RWC }\%$), Leaf Chlorophyll ($\text{SPAD}$), and Free Proline ($\mu\text{mol/g FW}$), annotated with ANOVA $F\text{-values}$ and $P > 0.05\text{ (NS)}$.
5. `fig5_threshold_calibration_pareto_curve.png`: Dual-axis threshold calibration curve sweeping reflood depth from $0\text{ cm}$ to $-30\text{ cm}$, marking the $-15\text{ cm}$ threshold where Water Productivity peaks ($\approx 1.39\text{ kg/m}^3$) right before capillary rupture triggers exponential proline accumulation and yield loss, with Validation Plot $21$ plotted as a gold star.
6. `fig6_farmer_extension_savings_impact.png`: Sub-division extension impact visual comparing groundwater saved ($\text{m}^3\text{/ha}$), pumping energy saved ($\text{kWh/ha}$), and effective tillers/yield components across $T_1\text{--}T_4$.

---

## 8. Automated Verification Suite (`tests/test_egra_awd_simulation.py`)

Run `pytest -v` and ensure $100\%$ pass rate on:
* `test_rcbd_20_plots_completeness`: Asserts $20$ RCBD plots ($4 \times 5$) + Plot $21$ exist with all hydrological, physiological, biochemical, and yield component columns populated.
* `test_irrigation_water_savings`: Asserts $T_3$ saves $24.0\% \pm 1.5\%$ and $T_4$ saves $28.0\% \pm 1.5\%$ water relative to $T_1$.
* `test_grain_yield_parity`: Asserts grain yield across $T_1\text{--}T_4$ varies by $< 5.0\%$.
* `test_water_productivity_targets`: Asserts $\text{WP}_{T_1} \in [0.96, 1.04]\text{ kg/m}^3$, $\text{WP}_{T_3} \in [1.28, 1.36]\text{ kg/m}^3$, and $\text{WP}_{T_4} \in [1.34, 1.42]\text{ kg/m}^3$.
* `test_physiological_parity_anova`: Asserts Two-Way RCBD ANOVA treatment $P > 0.05$ for $\text{RWC}$, $\text{Chlorophyll (SPAD)}$, and $\text{Free Proline}$ at the $-15\text{ cm}$ threshold, while $P < 0.001$ for Irrigation Water and Water Productivity.
* `test_threshold_capillary_break`: Asserts that shifting the threshold deeper to $-25\text{ cm}$ spikes proline above $3.5\text{ }\mu\text{mol/g FW}$ and drops grain yield by $> 12\%$.
* `test_validation_plot_and_artifacts`: Asserts Plot $21$ matches $T_3/T_4$ performance and verifies all $6$ PNG figures, $6$ CSV datasets, `reports/NCSC_Statistical_and_Field_Report.md`, and `docs/index.html` exist and are non-empty.