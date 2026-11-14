"""
src/statistics_ncsc.py
ICAR & NCSC Two-Way Randomized Complete Block Design (RCBD) ANOVA solver,
SEm±, SEd±, CD(0.05), CV%, and Tukey HSD groupings.
"""

from typing import Dict, List, Any, Tuple
import numpy as np
import pandas as pd
from scipy import stats


def calculate_two_way_rcbd_anova(df: pd.DataFrame, var_col: str) -> Dict[str, Any]:
    """
    Perform exact Two-Way RCBD ANOVA partitioning variance into:
      Total SS = Treatment SS + Block SS + Error SS
    Degrees of freedom:
      df_Trt = t - 1 = 3
      df_Block = r - 1 = 4
      df_Error = (t - 1) * (r - 1) = 12
      df_Total = t * r - 1 = 19
      
    Returns a dictionary of treatment means, ANOVA table, SEm, CD(0.05), CV%, and significance flag.
    """
    # Filter to the 4 RCBD treatments
    sub_df = df[df["treatment"].isin(["T1", "T2", "T3", "T4"])].copy()
    
    grand_mean = float(sub_df[var_col].mean())
    n_total = len(sub_df)
    r = sub_df["block"].nunique()       # 5 replications
    t = sub_df["treatment"].nunique()   # 4 treatments
    
    # Treatment means
    trt_means = sub_df.groupby("treatment")[var_col].mean()
    trt_dict = trt_means.to_dict()
    
    # Block means
    block_means = sub_df.groupby("block")[var_col].mean()
    
    # Sums of Squares
    ss_total = float(np.sum((sub_df[var_col] - grand_mean) ** 2))
    ss_trt = float(r * np.sum((trt_means - grand_mean) ** 2))
    ss_block = float(t * np.sum((block_means - grand_mean) ** 2))
    ss_error = max(0.0, ss_total - ss_trt - ss_block)
    
    # Degrees of freedom
    df_trt = t - 1          # 3
    df_block = r - 1        # 4
    df_error = (t - 1) * (r - 1)  # 12
    df_total = n_total - 1  # 19
    
    # Mean Squares
    ms_trt = ss_trt / df_trt if df_trt > 0 else 0.0
    ms_block = ss_block / df_block if df_block > 0 else 0.0
    ems = ss_error / df_error if df_error > 0 else 1e-12
    
    # F-statistics and P-values
    f_trt = ms_trt / ems if ems > 0 else 0.0
    p_trt = float(stats.f.sf(f_trt, df_trt, df_error))
    
    f_block = ms_block / ems if ems > 0 else 0.0
    p_block = float(stats.f.sf(f_block, df_block, df_error))
    
    # Standard Errors
    sem = float(np.sqrt(ems / r))
    sed = float(np.sqrt(2.0 * ems / r))
    
    # Critical Difference (CD at 5% / LSD)
    # Student's t critical value for df_error = 12 at alpha = 0.05 two-tailed
    t_crit_05 = float(stats.t.ppf(0.975, df_error))
    cd_05 = float(sed * t_crit_05)
    
    # Coefficient of Variation (CV %)
    cv_pct = float((np.sqrt(ems) / grand_mean) * 100.0) if grand_mean != 0 else 0.0
    
    # Significance flag
    if p_trt <= 0.01:
        sig_flag = "**"
    elif p_trt <= 0.05:
        sig_flag = "*"
    else:
        sig_flag = "NS"
        
    # Critical Difference (CD 0.05 / Fisher's LSD) post-hoc letter grouping
    sorted_trts = sorted(trt_dict.keys(), key=lambda k: trt_dict[k], reverse=True)
    letters = {}
    if sig_flag == "NS":
        # All statistically identical
        for k in sorted_trts:
            letters[k] = "a"
    else:
        # Group according to CD(0.05) threshold
        current_letter_idx = 0
        letter_chars = ["a", "b", "c", "d"]
        group_ref = trt_dict[sorted_trts[0]]
        letters[sorted_trts[0]] = letter_chars[current_letter_idx]
        for trt in sorted_trts[1:]:
            diff = abs(group_ref - trt_dict[trt])
            if diff >= cd_05:
                current_letter_idx = min(current_letter_idx + 1, len(letter_chars) - 1)
                group_ref = trt_dict[trt]
            letters[trt] = letter_chars[current_letter_idx]

    return {
        "variable": var_col,
        "grand_mean": grand_mean,
        "t1_mean": trt_dict.get("T1", 0.0),
        "t2_mean": trt_dict.get("T2", 0.0),
        "t3_mean": trt_dict.get("T3", 0.0),
        "t4_mean": trt_dict.get("T4", 0.0),
        "df_trt": df_trt,
        "df_block": df_block,
        "df_error": df_error,
        "ss_trt": ss_trt,
        "ss_block": ss_block,
        "ss_error": ss_error,
        "ms_trt": ms_trt,
        "ms_block": ms_block,
        "ems": ems,
        "f_trt": f_trt,
        "p_trt": p_trt,
        "sem": sem,
        "sed": sed,
        "cd_05": cd_05,
        "cv_pct": cv_pct,
        "significance": sig_flag,
        "letters": letters
    }


def build_ncsc_summary_table(df_rcbd: pd.DataFrame) -> pd.DataFrame:
    """
    Generate the official ICAR / NCSC championship summary table
    covering all agro-hydrological, physiological, and yield parameters.
    """
    parameters = [
        ("irrigation_mm", "Seasonal Irrigation Water (mm)"),
        ("water_savings_pct", "Irrigation Water Savings (%)"),
        ("grain_yield_tha", "Grain Yield (t/ha)"),
        ("water_productivity_kg_m3", "Irrigation Water Productivity (kg/m3)"),
        ("rwc_pct", "Leaf Relative Water Content (RWC %)"),
        ("spad", "Leaf Chlorophyll Index (SPAD)"),
        ("total_chlorophyll_mg_g", "Total Chlorophyll (mg/g FW)"),
        ("proline_umol_g", "Leaf Free Proline (umol/g FW)"),
        ("effective_tillers_hill", "Effective Tillers per Hill"),
        ("plant_height_cm", "Plant Height at Harvest (cm)"),
        ("panicle_length_cm", "Panicle Length (cm)"),
        ("filled_grains_per_panicle", "Filled Grains per Panicle"),
        ("test_weight_1000_g", "1000-Grain Test Weight (g)"),
        ("straw_yield_tha", "Straw Yield (t/ha)"),
        ("harvest_index_pct", "Harvest Index (HI %)"),
    ]
    
    rows = []
    for col_key, display_name in parameters:
        res = calculate_two_way_rcbd_anova(df_rcbd, col_key)
        
        # Format means with Tukey letters
        t1_str = f"{res['t1_mean']:.2f}{res['letters']['T1']}"
        t2_str = f"{res['t2_mean']:.2f}{res['letters']['T2']}"
        t3_str = f"{res['t3_mean']:.2f}{res['letters']['T3']}"
        t4_str = f"{res['t4_mean']:.2f}{res['letters']['T4']}"
        
        cd_str = f"{res['cd_05']:.2f}" if res["significance"] != "NS" else "NS"
        
        row = {
            "Parameter": display_name,
            "T1 (Local Farmer)": t1_str,
            "T2 (Continuous)": t2_str,
            "T3 (Manual AWD)": t3_str,
            "T4 (Sensor AWD)": t4_str,
            "SEm±": f"{res['sem']:.3f}",
            "CD (P=0.05)": cd_str,
            "CV (%)": f"{res['cv_pct']:.2f}%",
            "F-value": f"{res['f_trt']:.2f}",
            "P-value": f"{res['p_trt']:.4e}",
            "Significance": res["significance"]
        }
        rows.append(row)
        
    df_summary = pd.DataFrame(rows)
    return df_summary
