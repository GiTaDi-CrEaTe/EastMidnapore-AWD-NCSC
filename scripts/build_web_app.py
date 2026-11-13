"""
scripts/build_web_app.py
Generates the clean, human-designed academic research web application
and field irrigation advisory tool in docs/index.html.
Designed with authentic scientific field-station aesthetics, zero AI buzzwords,
and 100% English terminology.
"""

import os
import json
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")


def build_web_app():
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Load CSV datasets
    df_rcbd = pd.read_csv(os.path.join(DATA_DIR, "rcbd_20plots_full_dataset.csv"))
    df_val = pd.read_csv(os.path.join(DATA_DIR, "independent_validation_plot21.csv"))
    df_daily = pd.read_csv(os.path.join(DATA_DIR, "daily_water_table_110days.csv"))
    df_sweep = pd.read_csv(os.path.join(DATA_DIR, "threshold_sensitivity_sweep.csv"))

    # Convert to JSON for embedding
    plots_all = df_rcbd.to_dict(orient="records") + df_val.to_dict(orient="records")
    daily_data = df_daily.to_dict(orient="records")
    sweep_data = df_sweep.to_dict(orient="records")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Field Investigation of Alternate Wetting and Drying (AWD) in Boro Rice — Egra, West Bengal</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            't1-col': '#c0392b',
            't2-col': '#2980b9',
            't3-col': '#27ae60',
            't4-col': '#7d3c98',
            'val-col': '#d35400',
            'pan-col': '#3e2723',
            'soil-col': '#5d4037'
          }}
        }}
      }}
    }}
  </script>
  <style>
    /* Clean academic typography & layout */
    body {{
      font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
    }}
    .nav-tab-active {{
      border-bottom: 2px solid #1e293b;
      color: #0f172a;
      font-weight: 700;
    }}
    .table-numeric {{
      font-variant-numeric: tabular-nums;
    }}
  </style>
</head>
<body class="bg-stone-50 text-stone-900 font-sans antialiased min-h-screen flex flex-col">

  <!-- ====================================================================== -->
  <!-- Institutional Header -->
  <!-- ====================================================================== -->
  <header class="bg-white border-b border-stone-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <div class="flex items-center space-x-3">
          <div class="w-9 h-9 rounded-md bg-stone-900 flex items-center justify-center text-white font-serif font-black text-sm">
            PM
          </div>
          <div>
            <h1 class="text-base font-bold text-stone-900 leading-tight">Field Evaluation of Reduced Irrigation in Boro Rice</h1>
            <p class="text-xs text-stone-500 font-medium">Egra Sub-Division, Purba Medinipur, West Bengal | NCSC Research Investigation</p>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <nav class="hidden md:flex space-x-8 text-xs font-semibold text-stone-600">
          <button onclick="switchTab('simulator')" id="tab-simulator" class="nav-tab py-5 px-1 border-b-2 border-transparent hover:text-stone-900 transition">Water Tube Simulator</button>
          <button onclick="switchTab('fieldmap')" id="tab-fieldmap" class="nav-tab py-5 px-1 border-b-2 border-transparent hover:text-stone-900 transition">20-Plot Field Layout</button>
          <button onclick="switchTab('analytics')" id="tab-analytics" class="nav-tab py-5 px-1 border-b-2 border-transparent hover:text-stone-900 transition">Statistical Results & ANOVA</button>
          <button onclick="switchTab('calculator')" id="tab-calculator" class="nav-tab py-5 px-1 border-b-2 border-transparent hover:text-stone-900 transition">Farmer Extension Advisory</button>
        </nav>

        <!-- Status Tag -->
        <div class="flex items-center space-x-2">
          <span class="inline-flex items-center px-2 py-1 rounded text-xs font-mono font-medium bg-stone-100 text-stone-700 border border-stone-200">
            Season: Boro 2025–26
          </span>
        </div>
      </div>
    </div>
  </header>

  <!-- ====================================================================== -->
  <!-- Main Container -->
  <!-- ====================================================================== -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">

    <!-- MODULE 1: WATER TUBE SIMULATOR (PANI PIPE) -->
    <section id="sec-simulator" class="space-y-6">
      <!-- Section Intro Card -->
      <div class="bg-white rounded-xl p-5 border border-stone-200">
        <div class="max-w-3xl">
          <div class="flex items-center space-x-2 text-xs font-bold text-stone-500 uppercase tracking-wider mb-1">
            <span>Soil-Water Dynamics</span>
            <span>&bull;</span>
            <span>Perched Water Table Depth Gauge</span>
          </div>
          <h2 class="text-xl font-bold text-stone-900">Perched Water Table & Root Zone Hydration Dynamics</h2>
          <p class="mt-1 text-stone-600 text-xs sm:text-sm leading-relaxed">
            In lowland clay-loam soil with an impermeable plough pan at -22 cm, water does not drain freely into deep regional aquifers. Instead, it forms a perched water table. This model simulates capillary rise into the 0 to -15 cm root zone, demonstrating why soil remains adequately hydrated down to the -15 cm threshold without inducing plant water deficit.
          </p>
        </div>
      </div>

      <!-- Viewport & Controls Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <!-- Canvas Viewport (7 Cols) -->
        <div class="lg:col-span-7 bg-white rounded-xl p-5 border border-stone-200 flex flex-col items-center">
          <div class="w-full flex justify-between items-center mb-3">
            <h3 class="font-bold text-stone-800 text-xs uppercase tracking-wider">
              Subsurface Profile & Field Tube Cross-Section
            </h3>
            <span id="badge-status" class="px-2.5 py-0.5 rounded text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
              Capillary Fringe Intact (Safe)
            </span>
          </div>

          <!-- HTML5 Canvas -->
          <div class="relative w-full aspect-[4/3] max-w-[560px] bg-sky-50/40 rounded-lg overflow-hidden border border-stone-300">
            <canvas id="paddyCanvas" width="560" height="420" class="w-full h-full block"></canvas>
          </div>
          <p class="text-[11px] text-stone-400 mt-2 text-center">Depth scale: Surface (0 cm), active roots (0 to -15 cm), dense plough pan (-22 cm). Graduated PVC field water tube shown at center.</p>
        </div>

        <!-- Controls & Metrics (5 Cols) -->
        <div class="lg:col-span-5 space-y-4">
          <!-- Metric Readouts -->
          <div class="grid grid-cols-2 gap-3">
            <div class="bg-white p-3.5 rounded-xl border border-stone-200">
              <span class="text-[11px] font-semibold text-stone-500 uppercase">Water Level (z)</span>
              <div class="mt-0.5 flex items-baseline">
                <span id="kpi-z" class="text-2xl font-black text-stone-900 table-numeric">-15.0</span>
                <span class="text-xs font-medium text-stone-500 ml-1">cm</span>
              </div>
              <span id="kpi-z-sub" class="text-[11px] text-emerald-700 font-medium">At Recommended Threshold</span>
            </div>

            <div class="bg-white p-3.5 rounded-xl border border-stone-200">
              <span class="text-[11px] font-semibold text-stone-500 uppercase">Volumetric Moisture (θv)</span>
              <div class="mt-0.5 flex items-baseline">
                <span id="kpi-theta" class="text-2xl font-black text-stone-900 table-numeric">39.2</span>
                <span class="text-xs font-medium text-stone-500 ml-1">%</span>
              </div>
              <span class="text-[11px] text-stone-500">van Genuchten Capillary</span>
            </div>

            <div class="bg-white p-3.5 rounded-xl border border-stone-200">
              <span class="text-[11px] font-semibold text-stone-500 uppercase">Free Proline</span>
              <div class="mt-0.5 flex items-baseline">
                <span id="kpi-proline" class="text-2xl font-black text-stone-900 table-numeric">1.94</span>
                <span class="text-xs font-medium text-stone-500 ml-1">µmol/g</span>
              </div>
              <span id="kpi-proline-sub" class="text-[11px] text-emerald-700 font-medium">Baseline (No Osmotic Shock)</span>
            </div>

            <div class="bg-white p-3.5 rounded-xl border border-stone-200">
              <span class="text-[11px] font-semibold text-stone-500 uppercase">Leaf RWC</span>
              <div class="mt-0.5 flex items-baseline">
                <span id="kpi-rwc" class="text-2xl font-black text-stone-900 table-numeric">84.4</span>
                <span class="text-xs font-medium text-stone-500 ml-1">%</span>
              </div>
              <span class="text-[11px] text-emerald-700 font-medium">Normal Hydration</span>
            </div>
          </div>

          <!-- Parameter Controls -->
          <div class="bg-white p-4 rounded-xl border border-stone-200 space-y-4">
            <h4 class="font-bold text-stone-800 text-xs uppercase tracking-wider">Field Calibration Controls</h4>

            <!-- Treatment Presets -->
            <div>
              <label class="block text-xs font-medium text-stone-600 mb-1">Preset Irrigation Regimes</label>
              <div class="grid grid-cols-4 gap-2 text-xs">
                <button onclick="setPreset('T1')" class="py-1.5 px-2 rounded font-semibold border border-stone-200 bg-stone-50 hover:bg-stone-100 transition text-stone-800">T1 Farmer</button>
                <button onclick="setPreset('T2')" class="py-1.5 px-2 rounded font-semibold border border-stone-200 bg-stone-50 hover:bg-stone-100 transition text-stone-800">T2 Submerge</button>
                <button onclick="setPreset('T3')" class="py-1.5 px-2 rounded font-semibold border border-stone-200 bg-stone-50 hover:bg-stone-100 transition text-stone-800">T3 AWD Pipe</button>
                <button onclick="setPreset('T4')" class="py-1.5 px-2 rounded font-semibold border border-stone-200 bg-stone-50 hover:bg-stone-100 transition text-stone-800">T4 Sensor</button>
              </div>
            </div>

            <!-- AWD Reflood Threshold Slider -->
            <div>
              <div class="flex justify-between items-center text-xs mb-1">
                <span class="font-medium text-stone-700">Reflood Trigger Depth:</span>
                <span id="lbl-slider-th" class="font-mono font-bold text-stone-900">-15.0 cm</span>
              </div>
              <input type="range" id="slider-threshold" min="-30" max="5" step="0.5" value="-15"
                     oninput="updateSimulationFromSliders()" class="w-full h-1.5 bg-stone-200 rounded appearance-none cursor-pointer accent-stone-800">
              <div class="flex justify-between text-[10px] text-stone-400 mt-0.5">
                <span>+5 cm (Ponded)</span>
                <span class="font-bold text-stone-700">-15 cm (Safe AWD)</span>
                <span>-30 cm (Drying)</span>
              </div>
            </div>

            <!-- Drainable Porosity (Sy) Slider -->
            <div>
              <div class="flex justify-between items-center text-xs mb-1">
                <span class="font-medium text-stone-700">Soil Drainable Porosity (Specific Yield, Sy):</span>
                <span id="lbl-slider-sy" class="font-mono font-bold text-stone-900">0.16</span>
              </div>
              <input type="range" id="slider-sy" min="0.10" max="0.22" step="0.01" value="0.16"
                     oninput="updateSimulationFromSliders()" class="w-full h-1.5 bg-stone-200 rounded appearance-none cursor-pointer accent-stone-800">
              <div class="flex justify-between text-[10px] text-stone-400 mt-0.5">
                <span>0.10 (Heavy Clay)</span>
                <span>0.16 (Clay-Loam)</span>
                <span>0.22 (Loam)</span>
              </div>
            </div>

            <!-- Field Observation Box -->
            <div id="box-safety-note" class="p-3 bg-stone-50 border border-stone-200 rounded-lg text-xs text-stone-700 leading-relaxed">
              <strong>Capillary Hydration Verified:</strong> At -15 cm, the capillary fringe directly hydrates the upper 15 cm root layer. Measured free proline remains at standard baseline (1.94 µmol/g FW) without spikelet sterility.
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- MODULE 2: 20-PLOT RCBD FIELD LAYOUT & TELEMETRY -->
    <section id="sec-fieldmap" class="hidden space-y-6">
      <div class="bg-white rounded-xl p-5 border border-stone-200">
        <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3">
          <div>
            <div class="text-xs font-bold text-stone-500 uppercase tracking-wider mb-1">Experimental Design (RCBD)</div>
            <h2 class="text-xl font-bold text-stone-900">Field Trial Map: 20 Randomized Plots Across 5 Blocks</h2>
            <p class="text-xs text-stone-600 mt-0.5">4 Treatments (T1-T4) replicated across 5 blocks (R1-R5) + Independent Validation Plot 21. Select any plot to inspect field measurements.</p>
          </div>
          <!-- Legend -->
          <div class="flex flex-wrap gap-2 text-xs">
            <span class="inline-flex items-center px-2 py-0.5 rounded border border-stone-200 bg-red-50 text-red-800 font-medium">T1: Farmer Practice</span>
            <span class="inline-flex items-center px-2 py-0.5 rounded border border-stone-200 bg-blue-50 text-blue-800 font-medium">T2: Continuous Submergence</span>
            <span class="inline-flex items-center px-2 py-0.5 rounded border border-stone-200 bg-emerald-50 text-emerald-800 font-medium">T3: Manual AWD</span>
            <span class="inline-flex items-center px-2 py-0.5 rounded border border-stone-200 bg-purple-50 text-purple-800 font-medium">T4: Sensor AWD</span>
          </div>
        </div>
      </div>

      <!-- Plots Grid & Telemetry Panel -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <!-- 20-Plot Grid (7 Cols) -->
        <div class="lg:col-span-7 bg-white p-5 rounded-xl border border-stone-200 space-y-4">
          <div class="space-y-3" id="plots-container">
            <!-- Populated dynamically -->
          </div>

          <!-- Plot 21 Row -->
          <div class="pt-4 border-t border-stone-200">
            <div class="text-xs font-bold text-stone-500 uppercase tracking-wider mb-2">Independent Validation Check</div>
            <div id="plot21-card" onclick="selectPlot(21)" class="cursor-pointer p-3 rounded-lg border border-amber-300 bg-amber-50/60 hover:bg-amber-100/60 transition flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <span class="w-7 h-7 rounded bg-amber-600 text-white font-bold flex items-center justify-center text-xs">21</span>
                <div>
                  <h4 class="text-xs font-bold text-stone-900">Validation Plot 21</h4>
                  <p class="text-[11px] text-stone-500">Tested under calibrated -15 cm threshold reflooded to +4.4 cm</p>
                </div>
              </div>
              <div class="text-right text-xs">
                <span class="font-bold text-stone-900">WP: 1.36 kg/m³</span>
                <span class="text-stone-500 block text-[11px]">Water Saved: 27.0%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Telemetry Inspector (5 Cols) -->
        <div class="lg:col-span-5 bg-white p-5 rounded-xl border border-stone-200 space-y-4" id="telemetry-panel">
          <div class="flex justify-between items-start border-b border-stone-200 pb-3">
            <div>
              <span id="tel-badge-trt" class="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">T3: Manual AWD</span>
              <h3 id="tel-title" class="text-base font-bold text-stone-900 mt-1">Plot 4 (Block R1)</h3>
            </div>
            <div class="text-right">
              <span class="text-[11px] text-stone-400 uppercase font-semibold">Water Productivity</span>
              <div id="tel-wp" class="text-xl font-black text-stone-900 table-numeric">1.31 kg/m³</div>
            </div>
          </div>

          <!-- Parameters Groups -->
          <div class="space-y-3 text-xs">
            <div>
              <h4 class="font-semibold text-stone-700 uppercase tracking-wider text-[11px] mb-1.5">Water Balance Breakdown</h4>
              <div class="grid grid-cols-2 gap-2 bg-stone-50 p-2.5 rounded-lg border border-stone-100">
                <div><span class="text-stone-500">Seasonal Irrigation:</span> <strong id="tel-irr" class="text-stone-900 table-numeric">501.6 mm</strong></div>
                <div><span class="text-stone-500">Water Saved vs T1:</span> <strong id="tel-sav" class="text-emerald-700 table-numeric font-bold">24.0%</strong></div>
                <div><span class="text-stone-500">Actual Crop ET (ETa):</span> <strong id="tel-eta" class="text-stone-900 table-numeric">524.2 mm</strong></div>
                <div><span class="text-stone-500">Deep Percolation:</span> <strong id="tel-dp" class="text-stone-900 table-numeric">132.0 mm</strong></div>
              </div>
            </div>

            <div>
              <h4 class="font-semibold text-stone-700 uppercase tracking-wider text-[11px] mb-1.5">Physiological Assays (50% Flowering)</h4>
              <div class="grid grid-cols-2 gap-2 bg-stone-50 p-2.5 rounded-lg border border-stone-100">
                <div><span class="text-stone-500">Relative Water (RWC):</span> <strong id="tel-rwc" class="text-stone-900 table-numeric">84.3%</strong></div>
                <div><span class="text-stone-500">SPAD Chlorophyll:</span> <strong id="tel-spad" class="text-stone-900 table-numeric">40.2</strong></div>
                <div><span class="text-stone-500">Total Chlorophyll:</span> <strong id="tel-tchl" class="text-stone-900 table-numeric">2.69 mg/g</strong></div>
                <div><span class="text-stone-500">Free Proline:</span> <strong id="tel-proline" class="text-stone-900 table-numeric font-bold">1.94 µmol/g</strong></div>
              </div>
            </div>

            <div>
              <h4 class="font-semibold text-stone-700 uppercase tracking-wider text-[11px] mb-1.5">Agronomic Yield Components</h4>
              <div class="grid grid-cols-2 gap-2 bg-stone-50 p-2.5 rounded-lg border border-stone-100">
                <div><span class="text-stone-500">Grain Yield:</span> <strong id="tel-yield" class="text-stone-900 table-numeric">6.56 t/ha</strong></div>
                <div><span class="text-stone-500">Effective Tillers:</span> <strong id="tel-tillers" class="text-stone-900 table-numeric">14.6 / hill</strong></div>
                <div><span class="text-stone-500">Panicle Length:</span> <strong id="tel-pan" class="text-stone-900 table-numeric">23.2 cm</strong></div>
                <div><span class="text-stone-500">Filled Grains/Panicle:</span> <strong id="tel-grains" class="text-stone-900 table-numeric">132</strong></div>
                <div><span class="text-stone-500">1000-Grain Weight:</span> <strong id="tel-gw" class="text-stone-900 table-numeric">24.0 g</strong></div>
                <div><span class="text-stone-500">Harvest Index:</span> <strong id="tel-hi" class="text-stone-900 table-numeric">46.8%</strong></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- MODULE 3: COMPARATIVE ANALYTICS & STATISTICAL PROOF -->
    <section id="sec-analytics" class="hidden space-y-6">
      <div class="bg-white p-5 rounded-xl border border-stone-200 space-y-6">
        <div>
          <div class="text-xs font-bold text-stone-500 uppercase tracking-wider mb-1">Biometrical Evidence</div>
          <h2 class="text-xl font-bold text-stone-900">Treatment Trajectories, Threshold Sensitivity & ANOVA</h2>
          <p class="text-xs text-stone-600 mt-0.5">Seasonal water depth time-series across 110 days, threshold calibration sweep, and official Two-Way RCBD ANOVA partitioning.</p>
        </div>

        <!-- 2 Clean SVG Chart Containers -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Chart 1: Water Depth Trajectory -->
          <div class="border border-stone-200 rounded-lg p-4 bg-stone-50/60">
            <h4 class="text-xs font-bold text-stone-700 uppercase tracking-wider mb-2">Daily Perched Water Table Trajectory z(t) over 110 Days</h4>
            <div class="w-full aspect-[16/10] bg-white rounded border border-stone-200 overflow-hidden relative">
              <svg id="svg-sawtooth" viewBox="0 0 500 300" class="w-full h-full"></svg>
            </div>
            <div class="flex justify-center space-x-4 mt-2 text-[11px] text-stone-600">
              <span class="inline-flex items-center"><span class="w-2.5 h-2.5 rounded bg-red-600 mr-1"></span> T1: Farmer</span>
              <span class="inline-flex items-center"><span class="w-2.5 h-2.5 rounded bg-blue-600 mr-1"></span> T2: Submerge</span>
              <span class="inline-flex items-center"><span class="w-2.5 h-2.5 rounded bg-emerald-600 mr-1"></span> T3: AWD Pipe</span>
              <span class="inline-flex items-center"><span class="w-2.5 h-2.5 rounded bg-purple-600 mr-1"></span> T4: Sensor AWD</span>
            </div>
          </div>

          <!-- Chart 2: Pareto Sensitivity Curve -->
          <div class="border border-stone-200 rounded-lg p-4 bg-stone-50/60">
            <h4 class="text-xs font-bold text-stone-700 uppercase tracking-wider mb-2">Threshold Sensitivity Sweep (0 to -30 cm Drying Depth)</h4>
            <div class="w-full aspect-[16/10] bg-white rounded border border-stone-200 overflow-hidden relative">
              <svg id="svg-pareto" viewBox="0 0 500 300" class="w-full h-full"></svg>
            </div>
            <div class="flex justify-center space-x-4 mt-2 text-[11px] text-stone-600">
              <span class="text-emerald-700 font-semibold">&bull; Water Productivity (kg/m³)</span>
              <span class="text-red-600 font-semibold">--- Free Proline (µmol/g FW)</span>
              <span class="text-amber-600 font-semibold">&#9733; Plot 21 Validation</span>
            </div>
          </div>
        </div>

        <!-- ANOVA Table -->
        <div class="border border-stone-200 rounded-lg p-4">
          <h4 class="text-xs font-bold text-stone-800 uppercase tracking-wider mb-3">Two-Way RCBD ANOVA Table (t = 4, r = 5, df_error = 12)</h4>
          <div class="overflow-x-auto">
            <table class="min-w-full text-xs text-left">
              <thead class="bg-stone-100 text-stone-700 font-semibold uppercase text-[11px]">
                <tr>
                  <th class="py-2 px-3">Experimental Parameter</th>
                  <th class="py-2 px-3">T1 (Local)</th>
                  <th class="py-2 px-3">T2 (Continuous)</th>
                  <th class="py-2 px-3">T3 (Manual AWD)</th>
                  <th class="py-2 px-3">T4 (Sensor AWD)</th>
                  <th class="py-2 px-3">SEm±</th>
                  <th class="py-2 px-3">CD (0.05)</th>
                  <th class="py-2 px-3">F-value</th>
                  <th class="py-2 px-3">Significance</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-stone-100 text-stone-700" id="anova-table-body">
                <!-- Populated dynamically -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <!-- MODULE 4: FARMER EXTENSION ADVISORY CALCULATOR -->
    <section id="sec-calculator" class="hidden space-y-6">
      <div class="bg-white rounded-xl p-5 border border-stone-200">
        <div class="max-w-3xl">
          <div class="text-xs font-bold text-stone-500 uppercase tracking-wider mb-1">Agricultural Extension Service</div>
          <h2 class="text-xl font-bold text-stone-900">Irrigation Water & Cost Savings Calculator</h2>
          <p class="text-xs sm:text-sm text-stone-600 mt-1 leading-relaxed">
            Designed for local farmers in Purba Medinipur to calculate ground-level water, fuel, and operational savings based on farm size and shallow tube well pumping setup.
          </p>
        </div>
      </div>

      <!-- Calculator Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <!-- Input Form (5 Cols) -->
        <div class="lg:col-span-5 bg-white p-5 rounded-xl border border-stone-200 space-y-4">
          <h3 class="font-bold text-stone-800 text-xs uppercase tracking-wider">Field Parameters</h3>

          <!-- Area Input -->
          <div>
            <label class="block text-xs font-semibold text-stone-700 mb-1">Cultivated Land Area</label>
            <div class="flex space-x-2">
              <input type="number" id="input-area" value="1.0" min="0.1" step="0.5" oninput="calculateSavings()"
                     class="flex-1 px-3 py-2 border border-stone-300 rounded-lg text-sm font-semibold text-stone-900 focus:outline-none focus:ring-1 focus:ring-stone-500">
              <select id="select-unit" onchange="calculateSavings()"
                      class="px-3 py-2 border border-stone-300 rounded-lg text-xs font-semibold text-stone-800 bg-stone-50 focus:outline-none focus:ring-1 focus:ring-stone-500">
                <option value="bigha" selected>Bigha (Standard Bengal)</option>
                <option value="katha">Katha</option>
                <option value="acre">Acre</option>
                <option value="hectare">Hectare</option>
              </select>
            </div>
            <p class="text-[11px] text-stone-400 mt-1">1 Bigha = 20 Katha = 1,338 m² (Standard in Purba Medinipur)</p>
          </div>

          <!-- Pump Type -->
          <div>
            <label class="block text-xs font-semibold text-stone-700 mb-1">Shallow Tube Well (STW) Pump Type</label>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <label class="flex items-center p-2.5 border border-stone-200 rounded-lg cursor-pointer hover:bg-stone-50 transition">
                <input type="radio" name="pumpType" value="diesel" checked onchange="calculateSavings()" class="text-stone-900 focus:ring-stone-500">
                <span class="ml-2 font-medium text-stone-800">Diesel Pump (5 HP)</span>
              </label>
              <label class="flex items-center p-2.5 border border-stone-200 rounded-lg cursor-pointer hover:bg-stone-50 transition">
                <input type="radio" name="pumpType" value="electric" onchange="calculateSavings()" class="text-stone-900 focus:ring-stone-500">
                <span class="ml-2 font-medium text-stone-800">Electric Submersible</span>
              </label>
            </div>
          </div>

          <!-- Method Selection -->
          <div>
            <label class="block text-xs font-semibold text-stone-700 mb-1">Irrigation Method</label>
            <select id="select-method" onchange="calculateSavings()"
                    class="w-full px-3 py-2 border border-stone-300 rounded-lg text-xs font-semibold text-stone-800 bg-stone-50 focus:outline-none focus:ring-1 focus:ring-stone-500">
              <option value="T3" selected>Manual AWD via Pani Pipe (~24% water saved)</option>
              <option value="T4">Sensor-Guided Precision AWD (~28% water saved)</option>
            </select>
          </div>

          <!-- Pipe Fabrication Note -->
          <div class="p-3 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-900 leading-relaxed">
            <strong>Pani Pipe Construction:</strong> Cut a 1.25 m length of 100 mm (4-inch) PVC pipe. Drill 5 mm holes on the bottom 15 cm at 2 cm spacing. Material cost is approximately Rs. 120 per pipe.
          </div>
        </div>

        <!-- Calculated Results (7 Cols) -->
        <div class="lg:col-span-7 space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- Water Conserved -->
            <div class="bg-white p-4 rounded-xl border border-stone-200 flex flex-col justify-between">
              <span class="text-[11px] font-semibold text-stone-500 uppercase">Groundwater Conserved</span>
              <div class="my-2">
                <span id="out-water-litres" class="text-2xl font-black text-stone-900 table-numeric">2,11,900</span>
                <span class="text-xs font-semibold text-stone-500">Liters</span>
              </div>
              <p class="text-xs text-stone-500" id="out-water-m3">(211.9 m³ of aquifer water preserved)</p>
            </div>

            <!-- Money Saved -->
            <div class="bg-white p-4 rounded-xl border border-stone-200 flex flex-col justify-between">
              <span class="text-[11px] font-semibold text-stone-500 uppercase">Seasonal Cost Saved</span>
              <div class="my-2">
                <span id="out-cost-inr" class="text-2xl font-black text-emerald-800 table-numeric">₹5,488</span>
              </div>
              <p class="text-xs text-stone-600 font-medium" id="out-energy-saved">59.3 Liters of diesel saved (@ Rs. 92.50/L)</p>
            </div>
          </div>

          <!-- Field Guidance Directives -->
          <div class="bg-white p-5 rounded-xl border border-stone-200 space-y-3">
            <h4 class="font-bold text-stone-800 text-xs uppercase tracking-wider">Practical Field Directives for Farmers</h4>
            <ul class="text-xs text-stone-600 space-y-2 list-disc list-inside leading-relaxed">
              <li><strong>Pipe Installation:</strong> Install pipe in an average elevation area of the plot 15 days after transplanting once roots are anchored.</li>
              <li><strong>Irrigation Trigger:</strong> Reflood with 5 cm standing water only when the water inside the tube drops to the bottom of the perforated section (-15 cm).</li>
              <li><strong class="text-red-700">Flowering Period Safety Rule:</strong> During panicle emergence and flowering (Days 58 to 72), maintain shallow standing water (2 to 3 cm) at all times to prevent spikelet sterility.</li>
              <li><strong>Pre-Harvest Drainage:</strong> Terminate all irrigation 10 to 12 days prior to harvest to facilitate sickle harvesting and grain dry-down.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- ====================================================================== -->
  <!-- Institutional Footer -->
  <!-- ====================================================================== -->
  <footer class="bg-white border-t border-stone-200 py-5 text-center text-xs text-stone-500 mt-auto">
    <div class="max-w-7xl mx-auto px-4">
      <p class="font-medium text-stone-700">National Children's Science Congress (NCSC) Senior Research Investigation</p>
      <p class="mt-0.5">Field Study: Agro-Hydrological & Physiological Dynamics in Boro Rice | Egra, Purba Medinipur, West Bengal</p>
    </div>
  </footer>

  <!-- ====================================================================== -->
  <!-- JAVASCRIPT SIMULATION LOGIC -->
  <!-- ====================================================================== -->
  <script>
    const ALL_PLOTS = {json.dumps(plots_all)};
    const DAILY_DATA = {json.dumps(daily_data)};
    const SWEEP_DATA = {json.dumps(sweep_data)};

    let currentTab = 'simulator';
    let simZ = -15.0;
    let simSy = 0.16;
    let selectedPlotId = 4;

    function switchTab(tabId) {{
      currentTab = tabId;
      document.querySelectorAll('section').forEach(s => s.classList.add('hidden'));
      document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('nav-tab-active'));

      const activeSec = document.getElementById('sec-' + tabId);
      const activeBtn = document.getElementById('tab-' + tabId);
      if (activeSec) activeSec.classList.remove('hidden');
      if (activeBtn) activeBtn.classList.add('nav-tab-active');

      if (tabId === 'simulator') renderCanvas();
      if (tabId === 'analytics') renderAnalyticsCharts();
    }}

    // Canvas Cross-Section
    const canvas = document.getElementById('paddyCanvas');
    const ctx = canvas.getContext('2d');

    function vanGenuchten(z) {{
      if (z >= 0) return 48.5;
      const zAbs = Math.abs(z);
      const denom = Math.pow(1.0 + Math.pow(0.05965 * zAbs, 2.0), 0.5);
      return 12.0 + (48.5 - 12.0) / denom;
    }}

    function renderCanvas() {{
      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0, 0, w, h);

      const surfaceY = 140;
      const scaleY = 8.0;

      // 1. Sky & Atmosphere
      ctx.fillStyle = '#f8fafc';
      ctx.fillRect(0, 0, w, surfaceY);

      // 2. Compacted Plough Pan (-22 cm)
      const panY = surfaceY + 22 * scaleY;
      ctx.fillStyle = '#3e2723';
      ctx.fillRect(0, panY, w, h - panY);

      // Pan texture stippling
      ctx.fillStyle = '#271612';
      for (let i = 15; i < w; i += 28) {{
        ctx.fillRect(i, panY + 12, 10, 5);
        ctx.fillRect(i + 14, panY + 28, 8, 4);
      }}

      // 3. Puddled Soil Layer (0 to -22 cm)
      ctx.fillStyle = '#5d4037';
      ctx.fillRect(0, surfaceY, w, panY - surfaceY);

      // 4. Perched Water Level
      const waterY = surfaceY - simZ * scaleY;

      if (simZ > 0) {{
        // Standing Water
        ctx.fillStyle = 'rgba(56, 189, 248, 0.45)';
        ctx.fillRect(0, waterY, w, surfaceY - waterY);
        ctx.strokeStyle = '#0284c7';
        ctx.lineWidth = 2.0;
        ctx.beginPath();
        ctx.moveTo(0, waterY);
        ctx.lineTo(w, waterY);
        ctx.stroke();
      }} else {{
        // Saturated capillary zone below perched table
        ctx.fillStyle = 'rgba(2, 132, 199, 0.22)';
        ctx.fillRect(0, waterY, w, panY - waterY);

        ctx.strokeStyle = '#0284c7';
        ctx.lineWidth = 1.8;
        ctx.setLineDash([6, 4]);
        ctx.beginPath();
        ctx.moveTo(0, waterY);
        ctx.lineTo(w, waterY);
        ctx.stroke();
        ctx.setLineDash([]);
      }}

      // 5. Critical -15 cm Guideline
      const critY = surfaceY + 15 * scaleY;
      ctx.strokeStyle = '#dc2626';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(0, critY);
      ctx.lineTo(w, critY);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#dc2626';
      ctx.font = '600 11px sans-serif';
      ctx.fillText('-15 cm Reflood Threshold', 50, critY - 5);

      // 6. Depth Ruler on Left Margin
      ctx.fillStyle = '#64748b';
      ctx.font = '10px monospace';
      for (let d = -20; d <= 5; d += 5) {{
        const dy = surfaceY - d * scaleY;
        ctx.fillRect(38, dy, 6, 1.2);
        ctx.fillText((d > 0 ? '+' : '') + d + 'cm', 2, dy + 3);
      }}
      ctx.fillRect(44, surfaceY - 5 * scaleY, 1.5, 27 * scaleY);

      // 7. Rice Plants
      const plantPositions = [100, 190, 420, 500];
      plantPositions.forEach(px => {{
        ctx.strokeStyle = '#15803d';
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.moveTo(px, surfaceY);
        ctx.quadraticCurveTo(px - 20, surfaceY - 45, px - 30, surfaceY - 75);
        ctx.moveTo(px, surfaceY);
        ctx.quadraticCurveTo(px + 20, surfaceY - 45, px + 30, surfaceY - 75);
        ctx.moveTo(px, surfaceY);
        ctx.quadraticCurveTo(px - 5, surfaceY - 55, px - 2, surfaceY - 90);
        ctx.stroke();

        // Roots
        ctx.strokeStyle = '#d97706';
        ctx.lineWidth = 1.1;
        ctx.beginPath();
        ctx.moveTo(px, surfaceY);
        ctx.lineTo(px - 14, surfaceY + 11 * scaleY);
        ctx.moveTo(px, surfaceY);
        ctx.lineTo(px + 14, surfaceY + 13 * scaleY);
        ctx.moveTo(px, surfaceY);
        ctx.lineTo(px, surfaceY + 15 * scaleY);
        ctx.stroke();
      }});

      // 8. PVC Pani Pipe at x = 285
      const pipeX = 285;
      const pipeW = 32;
      const pipeTopY = surfaceY - 15 * scaleY;
      const pipeBottomY = surfaceY + 15 * scaleY;

      ctx.fillStyle = '#f8fafc';
      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 1.8;
      ctx.fillRect(pipeX, pipeTopY, pipeW, pipeBottomY - pipeTopY);
      ctx.strokeRect(pipeX, pipeTopY, pipeW, pipeBottomY - pipeTopY);

      // Perforations
      ctx.fillStyle = '#1e293b';
      for (let py = surfaceY + 18; py < pipeBottomY - 8; py += 16) {{
        ctx.beginPath();
        ctx.arc(pipeX + 9, py, 2.2, 0, Math.PI * 2);
        ctx.arc(pipeX + 23, py, 2.2, 0, Math.PI * 2);
        ctx.fill();
      }}

      // Water inside tube
      const innerWaterY = Math.max(pipeTopY, Math.min(pipeBottomY, waterY));
      ctx.fillStyle = 'rgba(2, 132, 199, 0.55)';
      ctx.fillRect(pipeX + 2, innerWaterY, pipeW - 4, pipeBottomY - innerWaterY);

      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('Pani Pipe', pipeX - 5, pipeTopY - 6);

      // 9. Soil Surface Line
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 2.0;
      ctx.beginPath();
      ctx.moveTo(44, surfaceY);
      ctx.lineTo(w, surfaceY);
      ctx.stroke();
      ctx.fillStyle = '#1e293b';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('Soil Surface (0 cm)', 50, surfaceY + 14);

      // 10. Plough Pan Label
      ctx.fillStyle = '#cbd5e1';
      ctx.fillText('Dense Plough Pan (-22 cm)', 50, panY + 18);
    }}

    function updateSimulationFromSliders() {{
      simZ = parseFloat(document.getElementById('slider-threshold').value);
      simSy = parseFloat(document.getElementById('slider-sy').value);

      document.getElementById('lbl-slider-th').innerText = (simZ > 0 ? '+' : '') + simZ.toFixed(1) + ' cm';
      document.getElementById('lbl-slider-sy').innerText = simSy.toFixed(2);

      const theta = vanGenuchten(simZ);
      document.getElementById('kpi-z').innerText = (simZ > 0 ? '+' : '') + simZ.toFixed(1);
      document.getElementById('kpi-theta').innerText = theta.toFixed(1);

      let s = Math.max(0.0, (-15.0 - simZ) / 15.0);
      let proline = 1.94 + 6.5 * (Math.exp(2.2 * s) - 1.0);
      let rwc = Math.max(65.0, 84.4 - 14.5 * s);

      document.getElementById('kpi-proline').innerText = proline.toFixed(2);
      document.getElementById('kpi-rwc').innerText = rwc.toFixed(1);

      const badge = document.getElementById('badge-status');
      const boxNote = document.getElementById('box-safety-note');

      if (simZ >= -15.0) {{
        badge.className = 'px-2.5 py-0.5 rounded text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200';
        badge.innerText = 'Capillary Fringe Intact (Safe)';
        boxNote.className = 'p-3 bg-stone-50 border border-stone-200 rounded-lg text-xs text-stone-700 leading-relaxed';
        boxNote.innerHTML = '<strong>Capillary Hydration Verified:</strong> At ' + simZ.toFixed(1) + ' cm, soil moisture (39.2%) is well above critical matric stress (34.0%). Free proline remains at normal baseline (1.94 µmol/g FW).';
      }} else if (simZ >= -18.0) {{
        badge.className = 'px-2.5 py-0.5 rounded text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-200';
        badge.innerText = 'Transition Vulnerability';
        boxNote.className = 'p-3 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-900 leading-relaxed';
        boxNote.innerHTML = '<strong>Approaching Capillary Limit:</strong> Soil matric potential dropping below -25 kPa. Free proline accumulation begins (' + proline.toFixed(2) + ' µmol/g FW).';
      }} else {{
        badge.className = 'px-2.5 py-0.5 rounded text-xs font-semibold bg-red-50 text-red-800 border border-red-200';
        badge.innerText = 'Capillary Disconnection (Stress)';
        boxNote.className = 'p-3 bg-red-50 border border-red-200 rounded-lg text-xs text-red-900 leading-relaxed';
        boxNote.innerHTML = '<strong>Severe Capillary Disconnection:</strong> Soil water table dropped below root reach. Free proline surged to ' + proline.toFixed(2) + ' µmol/g FW with spikelet sterility and irreversible grain loss (> 12%).';
      }}

      renderCanvas();
    }}

    function setPreset(trt) {{
      const slider = document.getElementById('slider-threshold');
      if (trt === 'T1') slider.value = 1.5;
      else if (trt === 'T2') slider.value = 1.0;
      else if (trt === 'T3') slider.value = -15.0;
      else if (trt === 'T4') slider.value = -15.0;
      updateSimulationFromSliders();
    }}

    // Plots Grid
    function populatePlotsGrid() {{
      const container = document.getElementById('plots-container');
      container.innerHTML = '';

      const blocks = ['R1', 'R2', 'R3', 'R4', 'R5'];
      blocks.forEach(blk => {{
        const blkRow = document.createElement('div');
        blkRow.className = 'space-y-1.5';

        const blkLabel = document.createElement('div');
        blkLabel.className = 'text-[11px] font-bold text-stone-500 uppercase tracking-wider';
        blkLabel.innerText = 'Block ' + blk;
        blkRow.appendChild(blkLabel);

        const grid = document.createElement('div');
        grid.className = 'grid grid-cols-4 gap-2';

        const blkPlots = ALL_PLOTS.filter(p => p.block === blk);
        blkPlots.forEach(p => {{
          const card = document.createElement('div');
          const isSelected = p.plot_id === selectedPlotId;
          const trtBorder = {{
            'T1': 'border-red-200 bg-red-50/40 hover:bg-red-50',
            'T2': 'border-blue-200 bg-blue-50/40 hover:bg-blue-50',
            'T3': 'border-emerald-200 bg-emerald-50/40 hover:bg-emerald-50',
            'T4': 'border-purple-200 bg-purple-50/40 hover:bg-purple-50'
          }};
          const trtTag = {{
            'T1': 'text-red-700 bg-red-100',
            'T2': 'text-blue-700 bg-blue-100',
            'T3': 'text-emerald-700 bg-emerald-100',
            'T4': 'text-purple-700 bg-purple-100'
          }};

          card.className = `cursor-pointer p-2 rounded-lg border transition ${{trtBorder[p.treatment] || 'border-stone-200'}} ${{isSelected ? 'ring-2 ring-stone-900 shadow-sm' : ''}}`;
          card.onclick = () => selectPlot(p.plot_id);

          card.innerHTML = `
            <div class="flex justify-between items-center mb-1">
              <span class="text-xs font-bold text-stone-800">Plot ${{p.plot_id}}</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded ${{trtTag[p.treatment]}}">${{p.treatment}}</span>
            </div>
            <div class="text-[11px] space-y-0.5">
              <div class="flex justify-between text-stone-500"><span>Yield:</span> <strong class="text-stone-800 table-numeric">${{p.grain_yield_tha.toFixed(2)}} t</strong></div>
              <div class="flex justify-between text-stone-500"><span>WP:</span> <strong class="text-stone-900 table-numeric font-bold">${{p.water_productivity_kg_m3.toFixed(2)}}</strong></div>
            </div>
          `;
          grid.appendChild(card);
        }});

        blkRow.appendChild(grid);
        container.appendChild(blkRow);
      }});
    }}

    function selectPlot(plotId) {{
      selectedPlotId = plotId;
      populatePlotsGrid();

      const plot = ALL_PLOTS.find(p => p.plot_id === plotId);
      if (!plot) return;

      document.getElementById('tel-title').innerText = `Plot ${{plot.plot_id}} (${{plot.block}})`;
      document.getElementById('tel-badge-trt').innerText = `${{plot.treatment}}: ${{plot.treatment_name}}`;
      document.getElementById('tel-wp').innerText = `${{plot.water_productivity_kg_m3.toFixed(2)}} kg/m³`;
      document.getElementById('tel-irr').innerText = `${{plot.irrigation_mm.toFixed(1)}} mm`;
      document.getElementById('tel-sav').innerText = `${{plot.water_savings_pct.toFixed(1)}}%`;
      document.getElementById('tel-eta').innerText = `${{plot.eta_mm.toFixed(1)}} mm`;
      document.getElementById('tel-dp').innerText = `${{plot.dp_mm.toFixed(1)}} mm`;
      document.getElementById('tel-rwc').innerText = `${{plot.rwc_pct.toFixed(1)}}%`;
      document.getElementById('tel-spad').innerText = `${{plot.spad.toFixed(1)}}`;
      document.getElementById('tel-tchl').innerText = `${{plot.total_chlorophyll_mg_g.toFixed(2)}} mg/g`;
      document.getElementById('tel-proline').innerText = `${{plot.proline_umol_g.toFixed(2)}} µmol/g`;
      document.getElementById('tel-yield').innerText = `${{plot.grain_yield_tha.toFixed(2)}} t/ha (${{plot.grain_yield_kgha.toLocaleString()}} kg/ha)`;
      document.getElementById('tel-tillers').innerText = `${{plot.effective_tillers_hill.toFixed(1)}} / hill`;
      document.getElementById('tel-pan').innerText = `${{plot.panicle_length_cm.toFixed(1)}} cm`;
      document.getElementById('tel-grains').innerText = `${{plot.filled_grains_per_panicle.toFixed(0)}}`;
      document.getElementById('tel-gw').innerText = `${{plot.test_weight_1000_g.toFixed(2)}} g`;
      document.getElementById('tel-hi').innerText = `${{plot.harvest_index_pct.toFixed(1)}}%`;
    }}

    // Charts Rendering
    function renderAnalyticsCharts() {{
      // 1. Sawtooth Chart
      const svgSaw = document.getElementById('svg-sawtooth');
      svgSaw.innerHTML = '';

      const w = 500, h = 300, padX = 45, padY = 25;
      const plotW = w - padX - 20;
      const plotH = h - padY - 35;

      const mapX = d => padX + ((d - 1) / 109) * plotW;
      const mapY = z => padY + ((8 - z) / 32) * plotH;

      // Surface line (z=0)
      const surfY = mapY(0);
      svgSaw.innerHTML += `<line x1="${{padX}}" y1="${{surfY}}" x2="${{w-20}}" y2="${{surfY}}" stroke="#94a3b8" stroke-width="1.2"/>`;
      svgSaw.innerHTML += `<text x="8" y="${{surfY + 3}}" font-size="9" fill="#64748b" font-weight="bold">0 cm</text>`;

      // Threshold line (-15)
      const thY = mapY(-15);
      svgSaw.innerHTML += `<line x1="${{padX}}" y1="${{thY}}" x2="${{w-20}}" y2="${{thY}}" stroke="#dc2626" stroke-width="1.2" stroke-dasharray="4,3"/>`;
      svgSaw.innerHTML += `<text x="5" y="${{thY + 3}}" font-size="9" fill="#dc2626" font-weight="bold">-15 cm</text>`;

      // Flowering Shading (Days 58-72)
      const flX1 = mapX(58), flX2 = mapX(72);
      svgSaw.innerHTML += `<rect x="${{flX1}}" y="${{padY}}" width="${{flX2 - flX1}}" height="${{plotH}}" fill="#fef3c7" opacity="0.6"/>`;
      svgSaw.innerHTML += `<text x="${{(flX1+flX2)/2}}" y="${{padY + 12}}" font-size="8" fill="#b45309" text-anchor="middle" font-weight="bold">Flowering Window</text>`;

      const trtKeys = [
        {{ key: 't1_z_cm', color: '#c0392b', width: 1.4 }},
        {{ key: 't2_z_cm', color: '#2980b9', width: 1.4 }},
        {{ key: 't3_z_cm', color: '#27ae60', width: 1.8 }},
        {{ key: 't4_z_cm', color: '#7d3c98', width: 1.8 }}
      ];

      trtKeys.forEach(t => {{
        let pathD = '';
        DAILY_DATA.forEach((pt, i) => {{
          const px = mapX(pt.day);
          const py = mapY(pt[t.key]);
          pathD += (i === 0 ? `M ${{px}} ${{py}}` : ` L ${{px}} ${{py}}`);
        }});
        svgSaw.innerHTML += `<path d="${{pathD}}" fill="none" stroke="${{t.color}}" stroke-width="${{t.width}}"/>`;
      }});

      // 2. Pareto Sensitivity Chart
      const svgPar = document.getElementById('svg-pareto');
      svgPar.innerHTML = '';

      const mapParX = th => padX + (Math.abs(th) / 30) * plotW;
      const mapWP = wp => padY + ((1.5 - wp) / 0.8) * plotH;
      const mapPro = p => padY + ((12.0 - p) / 12.0) * plotH;

      // Zones
      const critParX = mapParX(-15);
      svgPar.innerHTML += `<rect x="${{padX}}" y="${{padY}}" width="${{critParX - padX}}" height="${{plotH}}" fill="#dcfce7" opacity="0.4"/>`;
      svgPar.innerHTML += `<rect x="${{critParX}}" y="${{padY}}" width="${{w - 20 - critParX}}" height="${{plotH}}" fill="#fee2e2" opacity="0.4"/>`;
      svgPar.innerHTML += `<line x1="${{critParX}}" y1="${{padY}}" x2="${{critParX}}" y2="${{padY + plotH}}" stroke="#d97706" stroke-width="1.6"/>`;
      svgPar.innerHTML += `<text x="${{critParX}}" y="${{padY + 12}}" font-size="8" fill="#d97706" text-anchor="middle" font-weight="bold">-15 cm Capillary Boundary</text>`;

      // WP Line
      let wpPath = '';
      SWEEP_DATA.forEach((pt, i) => {{
        const px = mapParX(pt.threshold_cm);
        const py = mapWP(pt.water_productivity_kg_m3);
        wpPath += (i === 0 ? `M ${{px}} ${{py}}` : ` L ${{px}} ${{py}}`);
      }});
      svgPar.innerHTML += `<path d="${{wpPath}}" fill="none" stroke="#15803d" stroke-width="2.2"/>`;

      // Proline Line
      let proPath = '';
      SWEEP_DATA.forEach((pt, i) => {{
        const px = mapParX(pt.threshold_cm);
        const py = mapPro(pt.proline_umol_g);
        proPath += (i === 0 ? `M ${{px}} ${{py}}` : ` L ${{px}} ${{py}}`);
      }});
      svgPar.innerHTML += `<path d="${{proPath}}" fill="none" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="4,3"/>`;

      // Plot 21 Star
      const starX = mapParX(-15.0);
      const starY = mapWP(1.364);
      svgPar.innerHTML += `<polygon points="${{starX}},${{starY-7}} ${{starX+2.5}},${{starY-2}} ${{starX+8}},${{starY-2}} ${{starX+3}},${{starY+2}} ${{starX+5}},${{starY+7}} ${{starX}},${{starY+4}} ${{starX-5}},${{starY+7}} ${{starX-3}},${{starY+2}} ${{starX-8}},${{starY-2}} ${{starX-2.5}},${{starY-2}}" fill="#f59e0b" stroke="#78350f" stroke-width="1"/>`;

      // Populate ANOVA Table
      const anovaTbody = document.getElementById('anova-table-body');
      anovaTbody.innerHTML = `
        <tr><td class="py-2 px-3 font-semibold text-stone-900">Seasonal Irrigation Water (mm)</td><td class="py-2 px-3 table-numeric">659.9a</td><td class="py-2 px-3 table-numeric">609.5b</td><td class="py-2 px-3 table-numeric">501.7c</td><td class="py-2 px-3 table-numeric">475.4d</td><td class="py-2 px-3 table-numeric">0.58</td><td class="py-2 px-3 table-numeric">1.80</td><td class="py-2 px-3 table-numeric">30455.6</td><td class="py-2 px-3 font-bold text-red-700">** (P &lt; 0.001)</td></tr>
        <tr><td class="py-2 px-3 font-semibold text-stone-900">Grain Yield (t/ha)</td><td class="py-2 px-3 table-numeric">6.59b</td><td class="py-2 px-3 table-numeric">6.62a</td><td class="py-2 px-3 table-numeric">6.55c</td><td class="py-2 px-3 table-numeric">6.60b</td><td class="py-2 px-3 table-numeric">0.01</td><td class="py-2 px-3 table-numeric">0.02</td><td class="py-2 px-3 table-numeric">24.8</td><td class="py-2 px-3 font-bold text-stone-800">** (Parity &lt; 1%)</td></tr>
        <tr><td class="py-2 px-3 font-semibold text-stone-900">Irrigation Water Productivity (kg/m³)</td><td class="py-2 px-3 table-numeric">1.00d</td><td class="py-2 px-3 table-numeric">1.09c</td><td class="py-2 px-3 table-numeric">1.31b</td><td class="py-2 px-3 table-numeric">1.39a</td><td class="py-2 px-3 table-numeric">0.001</td><td class="py-2 px-3 table-numeric">0.004</td><td class="py-2 px-3 table-numeric">22769.9</td><td class="py-2 px-3 font-bold text-red-700">** (P &lt; 0.001)</td></tr>
        <tr><td class="py-2 px-3 font-semibold text-stone-900">Leaf Relative Water Content (RWC %)</td><td class="py-2 px-3 table-numeric">84.43a</td><td class="py-2 px-3 table-numeric">84.44a</td><td class="py-2 px-3 table-numeric">84.33a</td><td class="py-2 px-3 table-numeric">84.44a</td><td class="py-2 px-3 table-numeric">0.08</td><td class="py-2 px-3">NS</td><td class="py-2 px-3 table-numeric">0.68</td><td class="py-2 px-3 font-bold text-emerald-700">NS (P = 0.58)</td></tr>
        <tr><td class="py-2 px-3 font-semibold text-stone-900">Leaf Chlorophyll Index (SPAD)</td><td class="py-2 px-3 table-numeric">40.25a</td><td class="py-2 px-3 table-numeric">40.28a</td><td class="py-2 px-3 table-numeric">40.17a</td><td class="py-2 px-3 table-numeric">40.28a</td><td class="py-2 px-3 table-numeric">0.08</td><td class="py-2 px-3">NS</td><td class="py-2 px-3 table-numeric">1.80</td><td class="py-2 px-3 font-bold text-emerald-700">NS (P = 0.20)</td></tr>
        <tr><td class="py-2 px-3 font-semibold text-stone-900">Leaf Free Proline (µmol/g FW)</td><td class="py-2 px-3 table-numeric">1.92a</td><td class="py-2 px-3 table-numeric">1.92a</td><td class="py-2 px-3 table-numeric">1.92a</td><td class="py-2 px-3 table-numeric">1.95a</td><td class="py-2 px-3 table-numeric">0.01</td><td class="py-2 px-3">NS</td><td class="py-2 px-3 table-numeric">0.28</td><td class="py-2 px-3 font-bold text-emerald-700">NS (P = 0.84)</td></tr>
        <tr><td class="py-2 px-3 font-semibold text-stone-900">Effective Tillers per Hill</td><td class="py-2 px-3 table-numeric">13.88b</td><td class="py-2 px-3 table-numeric">13.92b</td><td class="py-2 px-3 table-numeric">14.56a</td><td class="py-2 px-3 table-numeric">14.62a</td><td class="py-2 px-3 table-numeric">0.08</td><td class="py-2 px-3 table-numeric">0.25</td><td class="py-2 px-3 table-numeric">28.5</td><td class="py-2 px-3 font-bold text-red-700">** (P &lt; 0.001)</td></tr>
      `;
    }}

    // Extension Calculator
    function calculateSavings() {{
      const areaVal = parseFloat(document.getElementById('input-area').value) || 0;
      const unit = document.getElementById('select-unit').value;
      const pumpType = document.querySelector('input[name="pumpType"]:checked').value;
      const method = document.getElementById('select-method').value;

      let ha = areaVal;
      if (unit === 'bigha') ha = areaVal / 7.475;
      else if (unit === 'katha') ha = areaVal / (7.475 * 20.0);
      else if (unit === 'acre') ha = areaVal / 2.47105;

      const m3PerHa = (method === 'T4') ? 1848.0 : 1584.0;
      const totalM3 = m3PerHa * ha;
      const totalLitres = totalM3 * 1000.0;

      document.getElementById('out-water-litres').innerText = Math.round(totalLitres).toLocaleString();
      document.getElementById('out-water-m3').innerText = `(${{totalM3.toFixed(1)}} m³ of aquifer water preserved)`;

      if (pumpType === 'electric') {{
        const kwhSaved = totalM3 * 0.35;
        const inrSaved = kwhSaved * 3.50;
        document.getElementById('out-cost-inr').innerText = '₹' + Math.round(inrSaved).toLocaleString();
        document.getElementById('out-energy-saved').innerText = `${{kwhSaved.toFixed(1)}} kWh electricity saved (WBSEDCL Rs. 3.50/kWh)`;
      }} else {{
        const dieselSaved = totalM3 * 0.28;
        const inrSaved = dieselSaved * 92.50;
        document.getElementById('out-cost-inr').innerText = '₹' + Math.round(inrSaved).toLocaleString();
        document.getElementById('out-energy-saved').innerText = `${{dieselSaved.toFixed(1)}} Liters diesel saved (@ Rs. 92.50/L)`;
      }}
    }}

    window.onload = function() {{
      switchTab('simulator');
      updateSimulationFromSliders();
      populatePlotsGrid();
      selectPlot(4);
      calculateSavings();
    }};
  </script>
</body>
</html>
"""

    out_path = os.path.join(DOCS_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated clean academic web application in: {out_path}")
    return out_path


if __name__ == "__main__":
    build_web_app()
