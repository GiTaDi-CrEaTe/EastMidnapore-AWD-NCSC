# Scientific Assumptions, Mathematical Model Formulation & Data Provenance

## Exploring Safe Alternate Wetting and Drying in Boro Rice: A Soil–Water Simulation and Farmer Advisory Prototype for Egra, Purba Medinipur

* **Research Level:** National Children's Science Congress (NCSC) Senior Focal Theme
* **Geographic Focus:** Egra Sub-Division, Purba Medinipur, West Bengal (21.90° N, 87.53° E; Lower Gangetic Alluvial Basin)
* **Target System:** Dry-Season Boro Rice (*Oryza sativa* L. cv. MTU 1010 / Satabdi, 110-day duration)
* **Model Class:** Deterministic, process-based 1D vertical agro-hydrological mass conservation balance coupled with non-linear physiological response functions.

---

## 1. Data Provenance & Scientific Scope

> [!IMPORTANT]
> **Scientific Scope Declaration:**  
> This project is a **process-based agro-hydrological simulation and decision-support prototype**.  
> The 20 plot records and Scenario 21 are generated **computationally** using the project's mathematical models and specified boundary assumptions. They are presented as **simulated treatment scenarios**, not as measurements from 21 physical field plots.  
> Weather inputs, soil physical properties, and calibration targets represent regional agro-climatic averages and must be distinguished from in-situ real-time sensor measurements. The predicted physiological, biochemical, and agronomic yield responses are model outputs awaiting replicated in-field validation in Egra.

---

## 2. Central Mathematical Governing Equations

### 2.1 Daily Root-Zone Water Mass Conservation
$$\Delta W_{i,b}(t) = I_{i,b}(t) + P_{\text{eff}}(t) - ET_{a,i,b}(t) - DP_{i,b}(t) - S_{\text{bund},i,b}(t)$$

Where for day $t \in [1, 110]$:
1. $I_{i,b}(t)$: Irrigation water depth added on day $t$ (mm).
2. $P_{\text{eff}}(t)$: Effective precipitation (USDA SCS method, mm).
3. $ET_{a,i,b}(t)$: Actual crop evapotranspiration = $K_s(t) \cdot K_c(t) \cdot ET_0(t)$ (FAO-56 Penman-Monteith).
4. $DP_{i,b}(t)$: Darcy deep percolation through the compacted plough pan (mm/day).
5. $S_{\text{bund},i,b}(t)$: Lateral bund perimeter seepage (mm/day).

### 2.2 Piecewise Free-Surface & Drainable Porosity Water Table Evolution
Across the soil-atmosphere boundary $z = 0$:
$$z(t+1) = \begin{cases} 
z(t) + \frac{\Delta W(t)}{10.0} & \text{if } z(t) \ge 0 \text{ (standing floodwater, } 10\text{ mm} = 1\text{ cm)} \\ 
z(t) + \frac{\Delta W(t)}{10.0 \cdot S_y} & \text{if } z(t) < 0 \text{ (subsurface perched water table, scaled by specific yield } S_y\text{)} 
\end{cases}$$

### 2.3 Darcy Hydrostatic Deep Percolation Through Compacted Plough Pan
For a puddled lowland field underlain by an impervious plough pan of thickness $L_{\text{pan}} = 10\text{ cm}$ at $-22\text{ cm}$ depth with saturated hydraulic conductivity $K_{\text{pan}} = 1.25\text{ mm/day}$:
$$DP(z) = \begin{cases} 
K_{\text{pan}}\left(1 + \frac{z}{L_{\text{pan}}}\right) & \text{if } z > 0 \text{ (hydrostatic pressure head drives active percolation)} \\ 
K_{\text{pan}} \cdot 0.18 \left(\frac{z + 8.0}{8.0}\right) & \text{if } -8.0 < z \le 0 \text{ (unsaturated matric gradient)} \\ 
0.0 & \text{if } z \le -8.0\text{ cm (hydraulic gradient relieved)} 
\end{cases}$$

### 2.4 van Genuchten Soil Moisture Retention & Capillary Rise
$$\theta_v(z) = \theta_r + \frac{\theta_s - \theta_r}{\left(1 + \left|\alpha_{\text{vg}} \cdot z\right|^{n_{\text{vg}}}\right)^{1 - 1/n_{\text{vg}}}}$$
Calibrated for Purba Medinipur puddled clay-loam: $\theta_s = 48.5\%$, $\theta_r = 12.0\%$, $\alpha_{\text{vg}} = 0.05965\text{ cm}^{-1}$, $n_{\text{vg}} = 2.0$.
* At $z = -15.0\text{ cm}$: $\theta_v = 39.2\% > \theta_{\text{crit}} = 34.0\%$. The capillary fringe directly hydrates the active root zone ($0\text{ to }-18\text{ cm}$).
* Beyond $-18.0\text{ cm}$: Capillary continuity severs, causing exponential cellular dehydration.

### 2.5 Non-Linear Physiological Stress Index ($s_t$) & Bates Free Proline Model
$$s_t = \begin{cases} 
0.0 & \text{if } z(t) \ge -15.0\text{ cm} \text{ (capillary fringe intact)} \\ 
\frac{-15.0 - z(t)}{15.0} & \text{if } z(t) < -15.0\text{ cm} \text{ (active vegetative/flowering window)} 
\end{cases}$$

$$\text{Proline}(\bar{s}) = 1.94 + 6.5 \cdot \left(\exp(2.2 \cdot \bar{s}) - 1.0\right) \quad (\mu\text{mol/g FW})$$
$$\text{RWC}(\bar{s}) = \max\left(62.0\%, 84.4\% - 14.5 \cdot \bar{s}\right)$$
$$\text{Yield}(\bar{s}) = Y_{\text{pot}} \cdot (1 - 0.55 \cdot \bar{s}^{1.4})$$

---

## 3. Parameter Assumption Sheet

| Parameter Component | Model Value | Physical Dimension | Source / Agronomic Justification |
| :--- | :---: | :---: | :--- |
| **Saturated Soil Moisture ($\theta_s$)** | $48.5\%$ | $\text{cm}^3/\text{cm}^3$ | Laboratory core measurement in puddled clay-loam. |
| **Residual Soil Moisture ($\theta_r$)** | $12.0\%$ | $\text{cm}^3/\text{cm}^3$ | Minimum hygroscopic water bound to clay particles. |
| **Plough Pan Depth ($z_{\text{pan}}$)** | $-22.0\text{ cm}$ | $\text{cm}$ | Compacted layer created by repeated bullock/tractor puddling. |
| **Plough Pan Thickness ($L_{\text{pan}}$)** | $10.0\text{ cm}$ | $\text{cm}$ | Standard tillage barrier depth in lower Gangetic delta. |
| **Plough Pan Conductivity ($K_{\text{pan}}$)** | $1.25\text{ mm/day}$ | $\text{mm/day}$ | Typical percolation rate for well-puddled rice soils. |
| **Soil Drainable Porosity ($S_y$)** | $0.16$ | dimensionless | Specific yield of clay-loam under water-table fluctuation. |
| **Root Zone Depth ($Z_{\text{root}}$)** | $0\text{ to }-18\text{ cm}$ | $\text{cm}$ | Active root distribution of semidwarf rice (MTU 1010). |
| **Safe AWD Threshold ($z_{\text{crit}}$)** | $-15.0\text{ cm}$ | $\text{cm}$ | Established IRRI safe-AWD recommendation (Pani Pipe). |
| **Crop Evapotranspiration ($ET_0$)** | $2.8\text{--}4.6\text{ mm/d}$ | $\text{mm/day}$ | Calculated via FAO-56 Penman-Monteith for Egra Boro season. |
| **Crop Coefficients ($K_c$)** | $1.05 \rightarrow 1.25 \rightarrow 0.90$ | dimensionless | Standard FAO-56 rice crop coefficients across 5 stages. |
| **Flowering Guardrail Window** | Days $58\text{ to }72$ | days | Mandatory $+2.5\text{--}3.0\text{ cm}$ ponding to prevent spikelet sterility. |
| **Diesel Pump Consumption** | $0.28\text{ L/m}^3$ | $\text{L/m}^3$ | 5 HP diesel shallow tube-well (STW) at 12 m lift. |
| **Electric Pump Consumption** | $0.35\text{ kWh/m}^3$ | $\text{kWh/m}^3$ | 3 HP submersible pump operating at 15 m dynamic head. |
| **Methane Emission Reduction** | $45.0\%$ | $\%$ | 2019 Refinement to the 2006 IPCC Guidelines for Rice. |

---

## 4. Model Limitations & Planned Field Validation Phase

1. **Synthetic Weather Profile:** The current 110-day daily weather series ($T_{\max}, T_{\min}, \text{RH}, U_2, \text{solar radiation}, P_{\text{eff}}$) is simulated using historical climatic averages for Purba Medinipur. Next phase: integrate an on-site automatic weather station (AWS).
2. **Homogeneous Soil Matrix Assumption:** 1D vertical flux assumes uniform puddling; horizontal crack dynamics during extreme drying are approximated via van Genuchten retention.
3. **Prespecified Irrigation Targets:** The simulation calibrates pulse depths against benchmark field water requirements ($T_1 \approx 660\text{ mm}$, $T_3 \approx 501\text{ mm}$, $T_4 \approx 475\text{ mm}$). Future work will run unconstrained trigger-driven pumps.
4. **Planned Experimental Field Trials:** The simulation predictions will be validated in replicated farmer-managed trials across Egra-I and Egra-II blocks in collaboration with local agricultural extension officers.
