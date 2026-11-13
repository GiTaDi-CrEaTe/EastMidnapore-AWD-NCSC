"""
src/physiology.py
Plant physiological, biochemical, and agronomic yield component model
for rice under AWD and continuous irrigation in Purba Medinipur, West Bengal.
"""

from typing import Dict, Any, Tuple
import numpy as np


def compute_capillary_stress_index(z_cm_series: np.ndarray, crit_depth_cm: float = -15.0) -> Tuple[np.ndarray, float]:
    """
    Compute daily capillary stress index S(t) and seasonal mean stress S_bar:
      S(t) = max(0, (-15.0 - z(t)) / 15.0)
      S_bar = (1 / D) * sum(S(t))
    """
    s_daily = np.maximum(0.0, (-crit_depth_cm - z_cm_series) / 15.0)
    s_bar = float(np.mean(s_daily))
    return s_daily, s_bar


def compute_physiology_and_yield(
    treatment_key: str,
    block_id: str,
    mean_stress_index: float,
    total_irrigation_mm: float,
    block_effects: Dict[str, float] = None,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Compute physiological assays (RWC, SPAD, Proline) and agronomic yield components.
    
    Parameters:
      treatment_key: 'T1', 'T2', 'T3', 'T4', or 'Plot21'
      block_id: 'R1'..'R5' (or 'Validation')
      mean_stress_index: S_bar across the season
      total_irrigation_mm: Total seasonal irrigation applied (mm)
      block_effects: Dictionary of block deltas for fertility / biometrics
      seed: Random seed for residual plot noise
    """
    rng = np.random.default_rng(seed)
    
    b_eff = block_effects if block_effects is not None else {
        "yield_delta": 0.0, "rwc_delta": 0.0, "proline_delta": 0.0
    }
    
    s_bar = float(mean_stress_index)
    
    # --------------------------------------------------------------------------
    # 1. Physiological and Biochemical Assays (at 50% flowering)
    # --------------------------------------------------------------------------
    # Relative Water Content (RWC %)
    # Base 84.4%, target parity window 83.8 - 84.9% when S_bar = 0
    eps_rwc = float(rng.normal(0.0, 0.18))
    rwc_pct = 84.4 - 14.5 * s_bar + b_eff.get("rwc_delta", 0.0) + eps_rwc
    rwc_pct = float(np.clip(rwc_pct, 65.0, 88.0))
    
    # Chlorophyll (SPAD)
    # Base 40.2, target parity window 39.7 - 40.7 when S_bar = 0
    eps_spad = float(rng.normal(0.0, 0.16))
    spad = 40.2 - 9.0 * s_bar + 0.4 * b_eff.get("yield_delta", 0.0) + eps_spad
    spad = float(np.clip(spad, 25.0, 45.0))
    
    # Total Chlorophyll (mg/g Fresh Weight)
    # Target window 2.65 - 2.78 mg/g FW
    eps_tchl = float(rng.normal(0.0, 0.015))
    total_chlorophyll_mg_g = float(np.clip(0.067 * spad + eps_tchl, 1.2, 3.2))
    
    # Free Proline (umol/g Fresh Weight) - Bates Acid Ninhydrin Assay
    # Base 1.94 umol/g FW, target parity window 1.88 - 2.04 umol/g FW when S_bar = 0.
    # Exponential surge under deeper drying (S_bar > 0)
    eps_pro = float(rng.normal(0.0, 0.025))
    proline_surge = 6.5 * (np.exp(2.2 * s_bar) - 1.0)
    proline_umol_g = 1.94 + proline_surge + b_eff.get("proline_delta", 0.0) + eps_pro
    proline_umol_g = float(np.clip(proline_umol_g, 1.70, 15.0))

    # --------------------------------------------------------------------------
    # 2. Agronomic Growth & Yield Components
    # --------------------------------------------------------------------------
    # Plant height at harvest (cm, ~98-102 cm)
    eps_ht = float(rng.normal(0.0, 0.6))
    plant_height_cm = float(np.clip(100.4 - 12.0 * s_bar + 2.0 * b_eff.get("yield_delta", 0.0) + eps_ht, 75.0, 115.0))
    
    # Effective panicle-bearing tillers per hill (~13.5 - 14.8)
    # In AWD (T3, T4), root oxygenation and phyllochron stimulation promote tiller survival!
    tiller_bonus = 0.7 if treatment_key in ["T3", "T4", "Plot21"] else 0.0
    eps_tillers = float(rng.normal(0.0, 0.15))
    effective_tillers = float(np.clip(13.9 + tiller_bonus - 3.5 * s_bar + b_eff.get("yield_delta", 0.0) + eps_tillers, 8.0, 20.0))
    
    # Panicle length (cm, ~22.8 - 23.6 cm)
    eps_pan = float(rng.normal(0.0, 0.12))
    panicle_length_cm = float(np.clip(23.2 - 2.5 * s_bar + 0.5 * b_eff.get("yield_delta", 0.0) + eps_pan, 16.0, 28.0))
    
    # Filled grains per panicle (~128 - 136)
    eps_grains = float(rng.normal(0.0, 1.2))
    filled_grains_per_panicle = float(np.clip(132.5 - 28.0 * s_bar + 4.0 * b_eff.get("yield_delta", 0.0) + eps_grains, 60.0, 160.0))
    
    # 1000-grain test weight (g, ~23.8 - 24.2 g)
    eps_gw = float(rng.normal(0.0, 0.06))
    test_weight_1000_g = float(np.clip(24.02 - 1.8 * s_bar + 0.2 * b_eff.get("yield_delta", 0.0) + eps_gw, 18.0, 27.0))
    
    # --------------------------------------------------------------------------
    # 3. Grain Yield, Straw Yield, and Harvest Index
    # --------------------------------------------------------------------------
    # Baseline grain yield targets (t/ha):
    # T1: 6.58, T2: 6.62, T3: 6.56, T4: 6.60, Plot21: 6.57
    base_yield_map = {
        "T1": 6.58,
        "T2": 6.62,
        "T3": 6.56,
        "T4": 6.60,
        "Plot21": 6.57
    }
    y_base = base_yield_map.get(treatment_key, 6.58)
    
    # Stress reduction factor (if capillary fringe broken, S_bar > 0)
    stress_yield_factor = max(0.40, 1.0 - 1.85 * (s_bar ** 1.15)) if s_bar > 0 else 1.0
    
    eps_yld = float(rng.normal(0.0, 0.015))
    grain_yield_tha = (y_base + b_eff.get("yield_delta", 0.0) + eps_yld) * stress_yield_factor
    grain_yield_tha = float(np.round(grain_yield_tha, 3))
    grain_yield_kgha = float(np.round(grain_yield_tha * 1000.0, 1))
    
    # Straw yield (t/ha, ~7.2 - 7.8 t/ha)
    eps_straw = float(rng.normal(0.0, 0.04))
    straw_yield_tha = float(np.round(7.48 + 1.2 * b_eff.get("yield_delta", 0.0) + eps_straw, 3))
    
    # Harvest Index (HI %) = Grain / (Grain + Straw) * 100
    harvest_index_pct = float(np.round((grain_yield_tha / (grain_yield_tha + straw_yield_tha)) * 100.0, 2))
    
    # --------------------------------------------------------------------------
    # 4. Irrigation Water Productivity (WP, kg grain per m3 irrigation water)
    # --------------------------------------------------------------------------
    # WP = Grain Yield (kg/ha) / [Irrigation (mm) * 10 m3/mm/ha]
    if total_irrigation_mm > 0:
        water_productivity_kg_m3 = float(np.round(grain_yield_kgha / (total_irrigation_mm * 10.0), 3))
    else:
        water_productivity_kg_m3 = 0.0
        
    return {
        "treatment": treatment_key,
        "block": block_id,
        "mean_stress_index": round(s_bar, 4),
        "rwc_pct": round(rwc_pct, 2),
        "spad": round(spad, 2),
        "total_chlorophyll_mg_g": round(total_chlorophyll_mg_g, 3),
        "proline_umol_g": round(proline_umol_g, 3),
        "plant_height_cm": round(plant_height_cm, 1),
        "effective_tillers_hill": round(effective_tillers, 1),
        "panicle_length_cm": round(panicle_length_cm, 2),
        "filled_grains_per_panicle": round(filled_grains_per_panicle, 1),
        "test_weight_1000_g": round(test_weight_1000_g, 2),
        "grain_yield_tha": grain_yield_tha,
        "grain_yield_kgha": grain_yield_kgha,
        "straw_yield_tha": straw_yield_tha,
        "harvest_index_pct": harvest_index_pct,
        "irrigation_mm": round(total_irrigation_mm, 1),
        "water_productivity_kg_m3": water_productivity_kg_m3
    }
