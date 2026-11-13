"""
src/hydrology.py
First-principles biophysical daily agro-hydrological state-space engine for
puddled clay-loam rice paddies in Purba Medinipur, West Bengal.
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd

from src.config import (
    CROP_DURATION_DAYS,
    ACTIVE_IRRIGATION_DAYS,
    FLOWERING_START_DAY,
    FLOWERING_END_DAY,
    THETA_SAT_PCT,
    THETA_RES_PCT,
    VG_ALPHA,
    VG_N,
    VG_M,
    PLOUGH_PAN_DEPTH_CM,
    PLOUGH_PAN_THICKNESS_CM,
    K_PAN_BASE_MM_DAY,
    SPECIFIC_YIELD_BASE,
    Z_CRIT_AWD_CM,
    TREATMENTS,
    VALIDATION_PLOT_SPEC,
    get_daily_weather,
    get_crop_coefficients,
)


def van_genuchten_moisture(z_cm: float) -> float:
    """
    Compute root-zone volumetric soil moisture theta_v (%) from perched water table depth z (cm)
    using the van Genuchten capillary fringe model:
      theta_v(z) = theta_s                             if z >= 0 (ponded water)
      theta_v(z) = theta_r + (theta_s - theta_r) / [1 + |alpha * z|^n]^m   if z < 0
    """
    if z_cm >= 0.0:
        return float(THETA_SAT_PCT)
    z_abs = abs(float(z_cm))
    denom = (1.0 + (VG_ALPHA * z_abs) ** VG_N) ** VG_M
    theta_v = THETA_RES_PCT + (THETA_SAT_PCT - THETA_RES_PCT) / denom
    return float(theta_v)


def darcy_deep_percolation(z_cm: float, k_pan: float = K_PAN_BASE_MM_DAY, l_pan: float = PLOUGH_PAN_THICKNESS_CM) -> float:
    """
    Compute hydrostatic deep percolation DP (mm/day) across the compacted plough pan:
      DP = K_pan * (1 + z / L_pan)               if z > 0 (hydrostatic ponding pressure)
      DP = K_pan * 0.18 * ((z + 8.0) / 8.0)      if -8.0 < z <= 0 (unsaturated capillary transmission)
      DP = 0.0                                   if z <= -8.0 (negligible unsaturated flux)
    """
    if z_cm > 0.0:
        return float(k_pan * (1.0 + z_cm / l_pan))
    elif -8.0 < z_cm <= 0.0:
        return float(k_pan * 0.18 * ((z_cm + 8.0) / 8.0))
    else:
        return 0.0


def bund_lateral_seepage(z_cm: float) -> float:
    """
    Compute small lateral bund seepage loss S_bund (mm/day):
      S_bund = 0.20 mm/day if z > 0 (standing water above bund toe)
      S_bund = 0.0 mm/day if z <= 0
    """
    return 0.20 if z_cm > 0.0 else 0.0


def update_water_table_step(z_curr: float, delta_w_mm: float, sy: float) -> float:
    """
    Piecewise analytical water flux integration updating perched water table depth z (cm)
    across the z = 0 boundary:
      - Standing water (z >= 0): 10.0 mm of water flux = 1.0 cm of water level change.
      - Subsurface perched table (z < 0): 10.0 * Sy mm of water flux = 1.0 cm of water level change.
    Bounded below at the impermeable plough pan (-22.0 cm).
    """
    z = float(z_curr)
    dw = float(delta_w_mm)
    s_y = float(sy)
    
    if dw < 0.0:
        # Water loss (ETa + percolation + seepage > rainfall)
        loss = -dw
        if z > 0.0:
            water_above_surface = z * 10.0  # mm
            if loss <= water_above_surface:
                z -= loss / 10.0
            else:
                rem_loss = loss - water_above_surface
                z = -rem_loss / (10.0 * s_y)
        else:
            z -= loss / (10.0 * s_y)
    else:
        # Water gain (Rainfall + Irrigation > ETa + percolation + seepage)
        gain = dw
        if z < 0.0:
            deficit_to_surface = -z * 10.0 * s_y  # mm
            if gain <= deficit_to_surface:
                z += gain / (10.0 * s_y)
            else:
                rem_gain = gain - deficit_to_surface
                z = rem_gain / 10.0
        else:
            z += gain / 10.0

    # Physical boundary limit at dense plough pan (-22.0 cm)
    if z < PLOUGH_PAN_DEPTH_CM:
        z = PLOUGH_PAN_DEPTH_CM
        
    return float(z)


def simulate_hydrology(
    treatment_key: str,
    sy: float = SPECIFIC_YIELD_BASE,
    k_pan: float = K_PAN_BASE_MM_DAY,
    initial_ponding_cm: float = 4.0,
    seed: int = 42,
    target_irrigation_sum: float = None
) -> Dict[str, Any]:
    """
    Run 110-day daily state-space simulation for a single paddy plot.
    
    Parameters:
      treatment_key: 'T1', 'T2', 'T3', 'T4', or 'Plot21'
      sy: Subsurface specific yield (drainable porosity)
      k_pan: Saturated conductivity of plough pan (mm/day)
      initial_ponding_cm: Standing ponding at transplanting (cm)
      seed: Random seed for micro-weather variability
      target_irrigation_sum: Optional target seasonal irrigation (mm) for exact calibration
      
    Returns:
      Dictionary with daily trajectories (DataFrame), seasonal totals, and stress indices.
    """
    days = CROP_DURATION_DAYS
    et0_series, peff_series = get_daily_weather(seed=seed)
    kc_series = get_crop_coefficients()
    
    # Treatment specifications
    if treatment_key in TREATMENTS:
        trt_spec = TREATMENTS[treatment_key]
    elif treatment_key == "Plot21":
        trt_spec = VALIDATION_PLOT_SPEC
    else:
        raise ValueError(f"Unknown treatment key: {treatment_key}")
        
    target_reflood = trt_spec["target_reflood_cm"]
    trigger_depth = trt_spec["trigger_depth_cm"]
    flowering_target = trt_spec["flowering_target_cm"]
    is_awd = trt_spec["is_awd"]
    
    # State tracking
    z = float(initial_ponding_cm)
    
    z_hist = []
    theta_hist = []
    irr_hist = []
    eta_hist = []
    dp_hist = []
    seep_hist = []
    stress_hist = []
    
    # Pass 1: Raw biophysical simulation
    for t in range(days):
        irr = 0.0
        # Active irrigation window (Days 0 to 99)
        if t < ACTIVE_IRRIGATION_DAYS:
            is_flowering = (FLOWERING_START_DAY <= t <= FLOWERING_END_DAY)
            
            if is_flowering and is_awd:
                # Critical reproductive ponding window: keep shallow standing water
                if z <= 0.8:
                    needed = (flowering_target - z) * 10.0 if z >= 0 else (-z * sy + flowering_target) * 10.0
                    irr = needed
            else:
                # Normal vegetative / ripening AWD or continuous submergence
                if z <= trigger_depth:
                    needed = (target_reflood - z) * 10.0 if z >= 0 else (-z * sy + target_reflood) * 10.0
                    irr = needed
                    
        # Apply irrigation
        if irr > 0.0:
            if z < 0.0:
                needed_to_surface = -z * sy * 10.0
                if irr <= needed_to_surface:
                    z += irr / (10.0 * sy)
                else:
                    z = (irr - needed_to_surface) / 10.0
            else:
                z += irr / 10.0
                
        irr_hist.append(irr)
        
        # Crop ETa with capillary stress factor Ks
        if z >= Z_CRIT_AWD_CM:
            ks = 1.0
        else:
            ks = max(0.60, 1.0 - 0.04 * (Z_CRIT_AWD_CM - z))
        eta = ks * kc_series[t] * et0_series[t]
        eta_hist.append(eta)
        
        # Deep percolation and bund seepage
        dp = darcy_deep_percolation(z, k_pan=k_pan)
        seep = bund_lateral_seepage(z)
        dp_hist.append(dp)
        seep_hist.append(seep)
        
        # Net flux update (rainfall - losses)
        delta_w = peff_series[t] - eta - dp - seep
        z = update_water_table_step(z, delta_w, sy=sy)
        
        z_hist.append(z)
        theta_hist.append(van_genuchten_moisture(z))
        
        # Capillary stress index (active growth season only)
        s_t = max(0.0, (Z_CRIT_AWD_CM - z) / 15.0) if t < ACTIVE_IRRIGATION_DAYS else 0.0
        stress_hist.append(s_t)
        
    irr_arr = np.array(irr_hist, dtype=float)
    
    # If a specific calibration target was requested, adjust irrigation pulses proportionally
    if target_irrigation_sum is not None and np.sum(irr_arr) > 0:
        scale_factor = target_irrigation_sum / np.sum(irr_arr)
        irr_arr = irr_arr * scale_factor
        
        # Re-run water table with calibrated irrigation pulses for complete conservation
        z = float(initial_ponding_cm)
        z_hist = []
        theta_hist = []
        eta_hist = []
        dp_hist = []
        seep_hist = []
        stress_hist = []
        
        for t in range(days):
            irr = irr_arr[t]
            if irr > 0.0:
                if z < 0.0:
                    needed_to_surface = -z * sy * 10.0
                    if irr <= needed_to_surface:
                        z += irr / (10.0 * sy)
                    else:
                        z = (irr - needed_to_surface) / 10.0
                else:
                    z += irr / 10.0
                    
            if z >= Z_CRIT_AWD_CM:
                ks = 1.0
            else:
                ks = max(0.60, 1.0 - 0.04 * (Z_CRIT_AWD_CM - z))
            eta = ks * kc_series[t] * et0_series[t]
            eta_hist.append(eta)
            
            dp = darcy_deep_percolation(z, k_pan=k_pan)
            seep = bund_lateral_seepage(z)
            dp_hist.append(dp)
            seep_hist.append(seep)
            
            delta_w = peff_series[t] - eta - dp - seep
            z = update_water_table_step(z, delta_w, sy=sy)
            
            z_hist.append(z)
            theta_hist.append(van_genuchten_moisture(z))
            s_t = max(0.0, (Z_CRIT_AWD_CM - z) / 15.0) if t < ACTIVE_IRRIGATION_DAYS else 0.0
            stress_hist.append(s_t)

    df_daily = pd.DataFrame({
        "day": np.arange(1, days + 1),
        "z_cm": np.round(z_hist, 2),
        "theta_v_pct": np.round(theta_hist, 2),
        "irrigation_mm": np.round(irr_arr, 2),
        "peff_mm": np.round(peff_series, 2),
        "eta_mm": np.round(eta_hist, 2),
        "dp_mm": np.round(dp_hist, 2),
        "seep_mm": np.round(seep_hist, 2),
        "stress_index": np.round(stress_hist, 4)
    })
    
    return {
        "treatment": treatment_key,
        "daily_df": df_daily,
        "total_irrigation_mm": float(np.sum(irr_arr)),
        "total_peff_mm": float(np.sum(peff_series)),
        "total_eta_mm": float(np.sum(eta_hist)),
        "total_dp_mm": float(np.sum(dp_hist)),
        "total_seep_mm": float(np.sum(seep_hist)),
        "min_water_table_cm": float(np.min(z_hist)),
        "mean_stress_index": float(np.mean(stress_hist)),
    }
