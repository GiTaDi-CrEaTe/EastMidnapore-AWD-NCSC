"""
src/config.py
Agro-climatic, soil, crop, and experimental configuration for the
Egra Sub-Division, Purba Medinipur, West Bengal Boro Rice AWD Simulation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import numpy as np


# ==============================================================================
# 1. Geographic and Agro-Climatic Parameters
# ==============================================================================
LOCATION_NAME = "Egra Sub-Division, Purba Medinipur, West Bengal, India"
AGRO_CLIMATIC_ZONE = "Coastal Saline & Red-Lateritic Alluvial Transition Zone"
LATITUDE = 21.90
LONGITUDE = 87.53
SEASON = "Boro Season (2025-2026, Dry-Season Irrigated Rice, Oryza sativa L.)"
CROP_VARIETY = "MTU 1010 (Satabdi / Cottondora Sannalu)"
CROP_DURATION_DAYS = 110
ACTIVE_IRRIGATION_DAYS = 100
TERMINAL_DRAINAGE_DAYS = 10
FLOWERING_START_DAY = 58
FLOWERING_END_DAY = 72
PEAK_FLOWERING_DAY = 65


# ==============================================================================
# 2. Soil Biophysical Characteristics (Puddled Clay-Loam)
# ==============================================================================
SOIL_TEXTURE = "Puddled Clay-Loam"
BULK_DENSITY_G_CM3 = 1.42  # g/cm3
THETA_SAT_PCT = 48.5       # Saturated volumetric water content (%)
THETA_RES_PCT = 12.0       # Residual volumetric water content (%)
THETA_CRIT_PCT = 34.0      # Critical matric stress water content (%)

# van Genuchten parameters for capillary fringe
# Calibrated so theta_v(-15 cm) = 39.2% (capillary continuous)
VG_ALPHA = 0.05965  # 1/cm
VG_N = 2.0
VG_M = 1.0 - 1.0 / VG_N  # 0.5

# Subsurface hardpan (plough pan)
PLOUGH_PAN_DEPTH_CM = -22.0  # cm relative to soil surface
PLOUGH_PAN_THICKNESS_CM = 10.0  # cm
K_PAN_BASE_MM_DAY = 1.25     # Base saturated hydraulic conductivity of compacted pan (mm/day)
SPECIFIC_YIELD_BASE = 0.160  # Base drainable porosity Sy for puddled clay-loam

# Critical AWD Perched Water Table Threshold
Z_CRIT_AWD_CM = -15.0  # cm below soil surface (Pani Pipe benchmark)


# ==============================================================================
# 3. Weather Profile across 110 Days (Boro Season)
# ==============================================================================
def get_daily_weather(seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate daily reference evapotranspiration (ET0) and effective rainfall (Peff)
    for a 110-day Boro crop cycle in Purba Medinipur.
    ET0 gradually increases from ~3.6 mm/day (Feb) to ~5.4 mm/day (late April/May).
    Rainfall consists of isolated pre-monsoon convective showers (Nor'westers).
    """
    days = CROP_DURATION_DAYS
    t = np.arange(days)
    # Reference ET0 progression
    et0 = 3.6 + 1.8 * (t / float(days)) ** 1.2
    
    # Effective rainfall (mm)
    peff = np.zeros(days)
    peff[42] = 6.5   # Mid-vegetative light shower
    peff[66] = 10.0  # Mid-flowering shower
    peff[85] = 8.5   # Late grain-filling shower
    
    return et0, peff


def get_crop_coefficients() -> np.ndarray:
    """
    Generate daily crop coefficient (Kc) curve across stages:
      - Initial/transplanting (Days 1-20): Kc = 1.05
      - Tillering/vegetative (Days 21-57): Kc = 1.15
      - Flowering/anthesis (Days 58-72): Kc = 1.22 (Shallow ponding window)
      - Grain-filling/ripening (Days 73-99): Kc transitions from 1.15 to 0.95
      - Terminal drainage (Days 100-110): Kc = 0.90
    """
    days = CROP_DURATION_DAYS
    kc = np.zeros(days)
    kc[0:21] = 1.05
    kc[21:58] = 1.15
    kc[58:73] = 1.22
    kc[73:100] = np.linspace(1.15, 0.95, 27)
    kc[100:110] = 0.90
    return kc


# ==============================================================================
# 4. RCBD Experimental Treatments and Blocks
# ==============================================================================
TREATMENTS = {
    "T1": {
        "name": "Local Conventional Practice",
        "description": "Unstructured farmer flooding; heavy reflooding to +6.5 cm when standing water thins to +1.5 cm.",
        "target_reflood_cm": 6.5,
        "trigger_depth_cm": 1.5,
        "flowering_target_cm": 6.5,
        "is_awd": False,
        "sensor_guided": False,
        "color": "#D9534F"  # Red / Orange-red
    },
    "T2": {
        "name": "Standard Continuous Irrigation",
        "description": "Scientific continuous submergence maintaining +1.0 cm to +5.0 cm standing water.",
        "target_reflood_cm": 5.0,
        "trigger_depth_cm": 1.0,
        "flowering_target_cm": 5.0,
        "is_awd": False,
        "sensor_guided": False,
        "color": "#337AB7"  # Deep Blue
    },
    "T3": {
        "name": "Manual AWD (Pani Pipe)",
        "description": "Field water tube (Pani Pipe); reflooded to +5.0 cm once perched water table drops to -15.0 cm.",
        "target_reflood_cm": 5.0,
        "trigger_depth_cm": -15.0,
        "flowering_target_cm": 2.8,
        "is_awd": True,
        "sensor_guided": False,
        "color": "#5CB85C"  # Forest Green
    },
    "T4": {
        "name": "Sensor-Guided Adaptive AWD",
        "description": "Capacitance/tensiometer sensor network; precision reflooding to +4.2 cm at -15.0 cm.",
        "target_reflood_cm": 4.2,
        "trigger_depth_cm": -15.0,
        "flowering_target_cm": 2.4,
        "is_awd": True,
        "sensor_guided": True,
        "color": "#9B59B6"  # Purple
    }
}

VALIDATION_PLOT_SPEC = {
    "plot_id": 21,
    "name": "Independent Validation Plot 21",
    "description": "Independently managed under calibrated -15 cm AWD threshold with precision reflooding to +4.4 cm.",
    "target_reflood_cm": 4.4,
    "trigger_depth_cm": -15.0,
    "flowering_target_cm": 2.6,
    "is_awd": True,
    "sensor_guided": True,
    "color": "#F39C12"  # Amber / Gold
}

BLOCKS = ["R1", "R2", "R3", "R4", "R5"]

# Block soil and fertility offsets for realistic 2-way RCBD
BLOCK_EFFECTS = {
    "R1": {"sy_delta": -0.008, "kpan_delta": -0.06, "yield_delta": -0.06, "rwc_delta": -0.15, "proline_delta": -0.02},
    "R2": {"sy_delta": -0.004, "kpan_delta": -0.03, "yield_delta": -0.03, "rwc_delta": -0.08, "proline_delta": -0.01},
    "R3": {"sy_delta":  0.000, "kpan_delta":  0.00, "yield_delta":  0.00, "rwc_delta":  0.00, "proline_delta":  0.00},
    "R4": {"sy_delta":  0.004, "kpan_delta":  0.03, "yield_delta":  0.03, "rwc_delta":  0.08, "proline_delta":  0.01},
    "R5": {"sy_delta":  0.008, "kpan_delta":  0.06, "yield_delta":  0.06, "rwc_delta":  0.15, "proline_delta":  0.02},
}


# ==============================================================================
# 5. Extension & Economic Parameters (Purba Medinipur)
# ==============================================================================
# Land area conversions
HA_TO_M2 = 10000.0
HA_TO_BIGHA_BENGAL = 7.475      # 1 Bigha = 1,337.8 m2 (20 Katha)
HA_TO_ACRE = 2.47105
BIGHA_TO_KATHA = 20.0

# Water and pumping parameters
# 1 mm over 1 ha = 10 m3 = 10,000 Litres
MM_HA_TO_M3 = 10.0
MM_HA_TO_LITRES = 10000.0

# Energy consumption for shallow tube well (STW, 12-15m lift head)
ELECTRIC_KWH_PER_M3 = 0.35      # kWh / m3 water pumped
ELECTRIC_TARIFF_INR_KWH = 3.50  # WBSEDCL agricultural tariff (Rs. / kWh)

DIESEL_LITRE_PER_M3 = 0.28      # Litres diesel / m3 water pumped
DIESEL_PRICE_INR_LITRE = 92.50  # Current diesel price in Egra (Rs. / L)

PANI_PIPE_COST_INR = 120.0      # Material cost for 1.25m PVC pipe + perforations (Rs.)
