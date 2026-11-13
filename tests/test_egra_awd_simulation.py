"""
tests/test_egra_awd_simulation.py
Automated verification suite validating all empirical invariants,
statistical significance criteria, threshold sensitivity physics,
and generated artifacts for the Purba Medinipur Rice AWD simulation.
"""

import os
import pytest
import pandas as pd
import numpy as np

from src.rcbd_experiment import run_full_rcbd_experiment
from src.statistics_ncsc import calculate_two_way_rcbd_anova
from src.threshold_calibration import run_threshold_sensitivity_sweep

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
FIGURES_DIR = os.path.join(PROJECT_ROOT, "figures")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")


@pytest.fixture(scope="module")
def experiment_data():
    """Load or run full RCBD experiment data."""
    df_rcbd, df_val, df_daily = run_full_rcbd_experiment(seed=101)
    df_sweep = run_threshold_sensitivity_sweep()
    return {
        "rcbd": df_rcbd,
        "validation": df_val,
        "daily": df_daily,
        "sweep": df_sweep
    }


def test_rcbd_20_plots_completeness(experiment_data):
    """
    Asserts 20 RCBD plots (4 treatments x 5 blocks) + Plot 21 exist with
    all required hydrological, physiological, biochemical, and yield component columns populated.
    """
    df_rcbd = experiment_data["rcbd"]
    df_val = experiment_data["validation"]
    
    # Check 20 plots in RCBD + 1 validation plot
    assert len(df_rcbd) == 20, f"Expected 20 RCBD plots, found {len(df_rcbd)}"
    assert len(df_val) == 1, f"Expected 1 validation plot, found {len(df_val)}"
    
    # Check 4 treatments and 5 blocks
    assert set(df_rcbd["treatment"].unique()) == {"T1", "T2", "T3", "T4"}
    assert set(df_rcbd["block"].unique()) == {"R1", "R2", "R3", "R4", "R5"}
    
    # Check required columns
    required_cols = [
        "plot_id", "block", "treatment", "irrigation_mm", "peff_mm", "eta_mm",
        "dp_mm", "seep_mm", "water_savings_pct", "water_productivity_kg_m3",
        "rwc_pct", "spad", "total_chlorophyll_mg_g", "proline_umol_g",
        "effective_tillers_hill", "grain_yield_tha", "grain_yield_kgha"
    ]
    for col in required_cols:
        assert col in df_rcbd.columns, f"Missing required column in RCBD: {col}"
        assert not df_rcbd[col].isnull().any(), f"Found NaN values in column: {col}"
        assert col in df_val.columns, f"Missing required column in Validation: {col}"
        assert not df_val[col].isnull().any(), f"Found NaN in validation column: {col}"


def test_irrigation_water_savings(experiment_data):
    """
    Asserts T3 saves 24.0% ± 1.5% and T4 saves 28.0% ± 1.5% water relative to T1.
    """
    df_rcbd = experiment_data["rcbd"]
    means = df_rcbd.groupby("treatment")["irrigation_mm"].mean()
    t1_mean = means["T1"]
    t3_mean = means["T3"]
    t4_mean = means["T4"]
    
    t3_savings = (t1_mean - t3_mean) / t1_mean * 100.0
    t4_savings = (t1_mean - t4_mean) / t1_mean * 100.0
    
    print(f"\nT1 Mean Irrigation: {t1_mean:.1f} mm")
    print(f"T3 Savings: {t3_savings:.2f}% (Target: 24.0% ± 1.5%)")
    print(f"T4 Savings: {t4_savings:.2f}% (Target: 28.0% ± 1.5%)")
    
    assert 22.5 <= t3_savings <= 25.5, f"T3 savings {t3_savings:.2f}% out of range [22.5, 25.5]%"
    assert 26.5 <= t4_savings <= 29.5, f"T4 savings {t4_savings:.2f}% out of range [26.5, 29.5]%"


def test_grain_yield_parity(experiment_data):
    """
    Asserts grain yield across all four treatments (T1-T4) varies by < 5.0%,
    demonstrating narrow agronomic parity (~6.45 to 6.70 t/ha).
    """
    df_rcbd = experiment_data["rcbd"]
    yield_means = df_rcbd.groupby("treatment")["grain_yield_tha"].mean()
    
    y_min = yield_means.min()
    y_max = yield_means.max()
    max_diff_pct = (y_max - y_min) / y_min * 100.0
    
    print(f"\nYield Means: T1={yield_means['T1']:.2f}, T2={yield_means['T2']:.2f}, T3={yield_means['T3']:.2f}, T4={yield_means['T4']:.2f} t/ha")
    print(f"Max Yield Difference: {max_diff_pct:.2f}% (Target: < 5.0%)")
    
    assert max_diff_pct < 5.0, f"Yield difference {max_diff_pct:.2f}% exceeds 5.0%"
    for t, ym in yield_means.items():
        assert 6.45 <= ym <= 6.70, f"Treatment {t} yield {ym:.2f} t/ha outside expected agronomic window [6.45, 6.70] t/ha"


def test_water_productivity_targets(experiment_data):
    """
    Asserts Water Productivity (WP) targets:
      - T1: WP in [0.96, 1.04] kg/m3
      - T2: WP in [1.05, 1.14] kg/m3
      - T3: WP in [1.28, 1.36] kg/m3
      - T4: WP in [1.34, 1.42] kg/m3
    """
    df_rcbd = experiment_data["rcbd"]
    wp_means = df_rcbd.groupby("treatment")["water_productivity_kg_m3"].mean()
    
    wp1 = wp_means["T1"]
    wp2 = wp_means["T2"]
    wp3 = wp_means["T3"]
    wp4 = wp_means["T4"]
    
    print(f"\nWater Productivity: T1={wp1:.3f}, T2={wp2:.3f}, T3={wp3:.3f}, T4={wp4:.3f} kg/m3")
    
    assert 0.96 <= wp1 <= 1.04, f"T1 WP {wp1:.3f} outside [0.96, 1.04]"
    assert 1.05 <= wp2 <= 1.14, f"T2 WP {wp2:.3f} outside [1.05, 1.14]"
    assert 1.28 <= wp3 <= 1.36, f"T3 WP {wp3:.3f} outside [1.28, 1.36]"
    assert 1.34 <= wp4 <= 1.42, f"T4 WP {wp4:.3f} outside [1.34, 1.42]"


def test_physiological_parity_anova(experiment_data):
    """
    Asserts Two-Way RCBD ANOVA treatment P > 0.05 for RWC, Chlorophyll (SPAD), and Free Proline
    at the -15 cm threshold (zero stress parity), while P < 0.001 for Irrigation Water and Water Productivity.
    """
    df_rcbd = experiment_data["rcbd"]
    
    # 1. Physiological assays: must be statistically non-significant (P > 0.05)
    for var in ["rwc_pct", "spad", "proline_umol_g"]:
        res = calculate_two_way_rcbd_anova(df_rcbd, var)
        print(f"ANOVA {var:15s}: F={res['f_trt']:.2f}, P={res['p_trt']:.4f}, Sig={res['significance']}")
        assert res["p_trt"] > 0.05, f"Expected NS (P > 0.05) for {var}, got P = {res['p_trt']}"
        assert res["significance"] == "NS", f"Expected significance NS for {var}, got {res['significance']}"

    # Verify baseline assay ranges
    rwc_mean = df_rcbd["rwc_pct"].mean()
    spad_mean = df_rcbd["spad"].mean()
    pro_mean = df_rcbd["proline_umol_g"].mean()
    assert 83.8 <= rwc_mean <= 84.9, f"Mean RWC {rwc_mean:.2f}% outside [83.8, 84.9]%"
    assert 39.7 <= spad_mean <= 40.7, f"Mean SPAD {spad_mean:.2f} outside [39.7, 40.7]"
    assert 1.88 <= pro_mean <= 2.04, f"Mean Proline {pro_mean:.2f} outside [1.88, 2.04] µmol/g"

    # 2. Water and Productivity: must be highly significant (P < 0.001)
    for var in ["irrigation_mm", "water_productivity_kg_m3"]:
        res = calculate_two_way_rcbd_anova(df_rcbd, var)
        print(f"ANOVA {var:15s}: F={res['f_trt']:.2f}, P={res['p_trt']:.4e}, Sig={res['significance']}")
        assert res["p_trt"] < 0.001, f"Expected P < 0.001 for {var}, got P = {res['p_trt']}"
        assert res["significance"] == "**", f"Expected ** for {var}, got {res['significance']}"


def test_threshold_capillary_break(experiment_data):
    """
    Asserts that shifting the threshold deeper to -25 cm breaks capillary continuity,
    spiking proline above 3.5 umol/g FW and dropping grain yield by > 12%.
    """
    df_sweep = experiment_data["sweep"]
    
    # Check at -15 cm (Optimal Pareto peak)
    row_15 = df_sweep[df_sweep["threshold_cm"] == -15.0].iloc[0]
    assert row_15["water_productivity_kg_m3"] >= 1.35, "WP at -15 cm should peak >= 1.35 kg/m3"
    assert row_15["proline_umol_g"] < 2.05, "Proline at -15 cm should be baseline < 2.05 µmol/g"
    assert row_15["yield_loss_pct"] == 0.0, "Yield loss at -15 cm should be 0.0%"
    
    # Check at -25 cm (Severe Capillary Break)
    row_25 = df_sweep[df_sweep["threshold_cm"] == -25.0].iloc[0]
    print(f"\nThreshold -25 cm: Proline={row_25['proline_umol_g']:.2f} µmol/g, Yield Loss={row_25['yield_loss_pct']:.1f}%")
    assert row_25["proline_umol_g"] > 3.5, f"Expected Proline > 3.5 µmol/g at -25 cm, got {row_25['proline_umol_g']:.2f}"
    assert row_25["yield_loss_pct"] > 12.0, f"Expected Yield Loss > 12.0% at -25 cm, got {row_25['yield_loss_pct']:.1f}%"


def test_validation_plot_and_artifacts(experiment_data):
    """
    Asserts Plot 21 matches T3/T4 performance and verifies all 6 PNG figures,
    6 CSV datasets, reports/NCSC_Statistical_and_Field_Report.md, and docs/index.html exist and are non-empty.
    """
    df_val = experiment_data["validation"]
    row_val = df_val.iloc[0]
    
    # Plot 21 performance checks
    assert 26.0 <= row_val["water_savings_pct"] <= 28.5, f"Plot 21 savings {row_val['water_savings_pct']}% outside [26.0, 28.5]%"
    assert 1.32 <= row_val["water_productivity_kg_m3"] <= 1.40, f"Plot 21 WP {row_val['water_productivity_kg_m3']} outside [1.32, 1.40]"
    assert 1.88 <= row_val["proline_umol_g"] <= 2.05, f"Plot 21 Proline {row_val['proline_umol_g']} outside baseline"
    assert 6.45 <= row_val["grain_yield_tha"] <= 6.70, f"Plot 21 yield {row_val['grain_yield_tha']} outside expected parity"
    
    # Check 6 CSV datasets
    csv_files = [
        "rcbd_20plots_full_dataset.csv",
        "daily_water_table_110days.csv",
        "ncsc_anova_cd_summary_table.csv",
        "threshold_sensitivity_sweep.csv",
        "independent_validation_plot21.csv",
        "egra_extension_advisory_table.csv"
    ]
    for cf in csv_files:
        p = os.path.join(DATA_DIR, cf)
        assert os.path.isfile(p), f"Missing CSV file: {p}"
        assert os.path.getsize(p) > 100, f"CSV file is empty or too small: {p}"
        
    # Check 6 PNG Figures (300 DPI)
    fig_files = [
        "fig1_rcbd_layout_and_water_balance.png",
        "fig2_daily_perched_water_table_sawtooth.png",
        "fig3_water_use_yield_and_productivity.png",
        "fig4_physiological_biochemical_parity.png",
        "fig5_threshold_calibration_pareto_curve.png",
        "fig6_farmer_extension_savings_impact.png"
    ]
    for ff in fig_files:
        p = os.path.join(FIGURES_DIR, ff)
        assert os.path.isfile(p), f"Missing figure file: {p}"
        assert os.path.getsize(p) > 50000, f"Figure file is suspiciously small (<50KB): {p}"
        
    # Check NCSC Technical Report
    report_file = os.path.join(REPORTS_DIR, "NCSC_Statistical_and_Field_Report.md")
    assert os.path.isfile(report_file), f"Missing report: {report_file}"
    assert os.path.getsize(report_file) > 2000, "Report is too short"
    
    # Check docs/index.html
    html_file = os.path.join(DOCS_DIR, "index.html")
    assert os.path.isfile(html_file), f"Missing HTML5 Digital Twin: {html_file}"
    assert os.path.getsize(html_file) > 10000, "docs/index.html is too small"
