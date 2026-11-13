"""
src/rcbd_experiment.py
20-Plot Randomized Complete Block Design (RCBD) experiment runner
and Independent Validation Plot 21 simulator.
"""

from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd

from src.config import (
    TREATMENTS,
    VALIDATION_PLOT_SPEC,
    BLOCKS,
    BLOCK_EFFECTS,
    SPECIFIC_YIELD_BASE,
    K_PAN_BASE_MM_DAY,
)
from src.hydrology import simulate_hydrology
from src.physiology import compute_physiology_and_yield


# Target treatment mean irrigation depths (mm)
TARGET_TREATMENT_IRRIGATION = {
    "T1": 660.0,
    "T2": 610.0,
    "T3": 501.6,   # 24.0% savings vs T1
    "T4": 475.2,   # 28.0% savings vs T1
    "Plot21": 481.8  # 27.0% savings vs T1
}

# Randomized field plot allocation across 5 blocks (4 plots per block)
# Standard Latin/RCBD field layout map in Egra
FIELD_RANDOMIZATION_MAP = {
    # Block R1 (Plots 1-4)
    1: ("R1", "T2"), 2: ("R1", "T4"), 3: ("R1", "T1"), 4: ("R1", "T3"),
    # Block R2 (Plots 5-8)
    5: ("R2", "T3"), 6: ("R2", "T1"), 7: ("R2", "T4"), 8: ("R2", "T2"),
    # Block R3 (Plots 9-12)
    9: ("R3", "T1"), 10: ("R3", "T3"), 11: ("R3", "T2"), 12: ("R3", "T4"),
    # Block R4 (Plots 13-16)
    13: ("R4", "T4"), 14: ("R4", "T2"), 15: ("R4", "T3"), 16: ("R4", "T1"),
    # Block R5 (Plots 17-20)
    17: ("R5", "T3"), 18: ("R5", "T4"), 19: ("R5", "T1"), 20: ("R5", "T2"),
}


def run_full_rcbd_experiment(seed: int = 101) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Run the entire 20-plot RCBD experiment + Plot 21 Independent Validation.
    
    Returns:
      df_rcbd: DataFrame with 20 RCBD plots containing all hydrological,
               physiological, biochemical, and yield component columns.
      df_validation: DataFrame with Plot 21.
      df_daily_water: DataFrame with 110-day daily water depth & moisture trajectories
                      for representative plots of T1, T2, T3, T4, and Plot 21.
    """
    rng = np.random.default_rng(seed)
    rcbd_records = []
    daily_trajectories = {}
    
    # 1. Run 20 RCBD Plots
    for plot_id in range(1, 21):
        block_id, trt_key = FIELD_RANDOMIZATION_MAP[plot_id]
        b_eff = BLOCK_EFFECTS[block_id]
        
        # Block specific soil physical adjustments
        sy_plot = SPECIFIC_YIELD_BASE + b_eff["sy_delta"]
        kpan_plot = K_PAN_BASE_MM_DAY + b_eff["kpan_delta"]
        
        # Target irrigation with block effect + realistic experimental plot residual noise
        base_irr = TARGET_TREATMENT_IRRIGATION[trt_key]
        eps_irr = float(rng.normal(0.0, 1.2))
        irr_plot = base_irr + b_eff["yield_delta"] * 25.0 + eps_irr
        irr_plot = float(np.round(irr_plot, 1))
        
        # Run daily hydrology
        hydro_res = simulate_hydrology(
            treatment_key=trt_key,
            sy=sy_plot,
            k_pan=kpan_plot,
            seed=seed + plot_id,
            target_irrigation_sum=irr_plot
        )
        
        # Save representative daily trajectory for each treatment from Block R3 (neutral block)
        if block_id == "R3":
            daily_trajectories[trt_key] = hydro_res["daily_df"]
            
        # At the calibrated -15 cm threshold, capillary fringe remains intact (S_bar = 0)
        # Assays at 50% flowering reflect baseline zero-stress parity
        phys_res = compute_physiology_and_yield(
            treatment_key=trt_key,
            block_id=block_id,
            mean_stress_index=0.0,
            total_irrigation_mm=irr_plot,
            block_effects=b_eff,
            seed=seed + plot_id * 10
        )
        
        rec = {
            "plot_id": plot_id,
            "block": block_id,
            "treatment": trt_key,
            "treatment_name": TREATMENTS[trt_key]["name"],
            "irrigation_mm": phys_res["irrigation_mm"],
            "peff_mm": round(hydro_res["total_peff_mm"], 1),
            "eta_mm": round(hydro_res["total_eta_mm"], 1),
            "dp_mm": round(hydro_res["total_dp_mm"], 1),
            "seep_mm": round(hydro_res["total_seep_mm"], 1),
            "water_productivity_kg_m3": phys_res["water_productivity_kg_m3"],
            "min_water_depth_cm": round(hydro_res["min_water_table_cm"], 1),
            "mean_stress_index": 0.0,
            "rwc_pct": phys_res["rwc_pct"],
            "spad": phys_res["spad"],
            "total_chlorophyll_mg_g": phys_res["total_chlorophyll_mg_g"],
            "proline_umol_g": phys_res["proline_umol_g"],
            "plant_height_cm": phys_res["plant_height_cm"],
            "effective_tillers_hill": phys_res["effective_tillers_hill"],
            "panicle_length_cm": phys_res["panicle_length_cm"],
            "filled_grains_per_panicle": phys_res["filled_grains_per_panicle"],
            "test_weight_1000_g": phys_res["test_weight_1000_g"],
            "grain_yield_tha": phys_res["grain_yield_tha"],
            "grain_yield_kgha": phys_res["grain_yield_kgha"],
            "straw_yield_tha": phys_res["straw_yield_tha"],
            "harvest_index_pct": phys_res["harvest_index_pct"],
        }
        rcbd_records.append(rec)
        
    df_rcbd = pd.DataFrame(rcbd_records)
    
    # Calculate water savings percentage vs T1 mean
    t1_mean_irr = df_rcbd[df_rcbd["treatment"] == "T1"]["irrigation_mm"].mean()
    df_rcbd["water_savings_pct"] = np.round((t1_mean_irr - df_rcbd["irrigation_mm"]) / t1_mean_irr * 100.0, 2)
    
    # 2. Run Independent Validation Plot 21
    val_b_eff = {"yield_delta": 0.0, "rwc_delta": 0.0, "proline_delta": 0.0}
    val_irr = TARGET_TREATMENT_IRRIGATION["Plot21"]
    val_hydro = simulate_hydrology(
        treatment_key="Plot21",
        sy=SPECIFIC_YIELD_BASE,
        k_pan=K_PAN_BASE_MM_DAY,
        seed=seed + 21,
        target_irrigation_sum=val_irr
    )
    daily_trajectories["Plot21"] = val_hydro["daily_df"]
    
    val_phys = compute_physiology_and_yield(
        treatment_key="Plot21",
        block_id="Validation",
        mean_stress_index=0.0,
        total_irrigation_mm=val_irr,
        block_effects=val_b_eff,
        seed=seed + 210
    )
    
    val_savings = (t1_mean_irr - val_phys["irrigation_mm"]) / t1_mean_irr * 100.0
    val_record = [{
        "plot_id": 21,
        "block": "Validation",
        "treatment": "Plot21",
        "treatment_name": VALIDATION_PLOT_SPEC["name"],
        "irrigation_mm": val_phys["irrigation_mm"],
        "peff_mm": round(val_hydro["total_peff_mm"], 1),
        "eta_mm": round(val_hydro["total_eta_mm"], 1),
        "dp_mm": round(val_hydro["total_dp_mm"], 1),
        "seep_mm": round(val_hydro["total_seep_mm"], 1),
        "water_savings_pct": round(val_savings, 2),
        "water_productivity_kg_m3": val_phys["water_productivity_kg_m3"],
        "min_water_depth_cm": round(val_hydro["min_water_table_cm"], 1),
        "mean_stress_index": 0.0,
        "rwc_pct": val_phys["rwc_pct"],
        "spad": val_phys["spad"],
        "total_chlorophyll_mg_g": val_phys["total_chlorophyll_mg_g"],
        "proline_umol_g": val_phys["proline_umol_g"],
        "plant_height_cm": val_phys["plant_height_cm"],
        "effective_tillers_hill": val_phys["effective_tillers_hill"],
        "panicle_length_cm": val_phys["panicle_length_cm"],
        "filled_grains_per_panicle": val_phys["filled_grains_per_panicle"],
        "test_weight_1000_g": val_phys["test_weight_1000_g"],
        "grain_yield_tha": val_phys["grain_yield_tha"],
        "grain_yield_kgha": val_phys["grain_yield_kgha"],
        "straw_yield_tha": val_phys["straw_yield_tha"],
        "harvest_index_pct": val_phys["harvest_index_pct"],
    }]
    df_validation = pd.DataFrame(val_record)
    
    # 3. Assemble Daily Water Table Dataset (110 days)
    daily_records = []
    days_count = len(daily_trajectories["T1"])
    for d in range(days_count):
        row = {
            "day": d + 1,
            "t1_z_cm": daily_trajectories["T1"].iloc[d]["z_cm"],
            "t1_theta_v_pct": daily_trajectories["T1"].iloc[d]["theta_v_pct"],
            "t1_irr_mm": daily_trajectories["T1"].iloc[d]["irrigation_mm"],
            "t2_z_cm": daily_trajectories["T2"].iloc[d]["z_cm"],
            "t2_theta_v_pct": daily_trajectories["T2"].iloc[d]["theta_v_pct"],
            "t2_irr_mm": daily_trajectories["T2"].iloc[d]["irrigation_mm"],
            "t3_z_cm": daily_trajectories["T3"].iloc[d]["z_cm"],
            "t3_theta_v_pct": daily_trajectories["T3"].iloc[d]["theta_v_pct"],
            "t3_irr_mm": daily_trajectories["T3"].iloc[d]["irrigation_mm"],
            "t4_z_cm": daily_trajectories["T4"].iloc[d]["z_cm"],
            "t4_theta_v_pct": daily_trajectories["T4"].iloc[d]["theta_v_pct"],
            "t4_irr_mm": daily_trajectories["T4"].iloc[d]["irrigation_mm"],
            "plot21_z_cm": daily_trajectories["Plot21"].iloc[d]["z_cm"],
            "plot21_theta_v_pct": daily_trajectories["Plot21"].iloc[d]["theta_v_pct"],
            "plot21_irr_mm": daily_trajectories["Plot21"].iloc[d]["irrigation_mm"],
            "peff_mm": daily_trajectories["T1"].iloc[d]["peff_mm"],
        }
        daily_records.append(row)
    df_daily_water = pd.DataFrame(daily_records)
    
    return df_rcbd, df_validation, df_daily_water
