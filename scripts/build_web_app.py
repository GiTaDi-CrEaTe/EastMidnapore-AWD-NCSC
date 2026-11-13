"""
scripts/build_web_app.py
Generates the standalone, single-file interactive HTML5 Digital Twin
and Farmer Extension Web App in docs/index.html.
"""

import os
import json
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
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
  <title>Purba Medinipur Rice AWD Digital Twin & Farmer Advisory</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            't1-red': '#D9534F',
            't2-blue': '#337AB7',
            't3-green': '#5CB85C',
            't4-purple': '#8E44AD',
            'val-gold': '#F39C12',
            'soil-dark': '#5D4037',
            'soil-pan': '#3E2723'
          }}
        }}
      }}
    }}
  </script>
  <style>
    /* Custom clean styling */
    .tab-active {{
      border-bottom: 3px solid #16a34a;
      color: #16a34a;
      font-weight: 700;
    }}
    .custom-scrollbar::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{
      background: #cbd5e1;
      border-radius: 4px;
    }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 font-sans antialiased min-h-screen flex flex-col">

  <!-- ====================================================================== -->
  <!-- Header / Navigation Bar -->
  <!-- ====================================================================== -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-700 flex items-center justify-center text-white shadow-md">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
          <div>
            <h1 class="text-lg font-bold text-slate-900 leading-tight">Purba Medinipur Rice AWD Digital Twin</h1>
            <p class="text-xs text-slate-500">Egra Sub-Division | NCSC 2025–2026 Research Investigation</p>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <nav class="hidden md:flex space-x-6 text-sm font-medium">
          <button onclick="switchTab('simulator')" id="tab-simulator" class="tab-link py-5 px-1 border-b-2 border-transparent text-slate-600 hover:text-green-600 transition">Pani Pipe Simulator</button>
          <button onclick="switchTab('fieldmap')" id="tab-fieldmap" class="tab-link py-5 px-1 border-b-2 border-transparent text-slate-600 hover:text-green-600 transition">20-Plot Field Map</button>
          <button onclick="switchTab('analytics')" id="tab-analytics" class="tab-link py-5 px-1 border-b-2 border-transparent text-slate-600 hover:text-green-600 transition">Comparative Analytics</button>
          <button onclick="switchTab('calculator')" id="tab-calculator" class="tab-link py-5 px-1 border-b-2 border-transparent text-slate-600 hover:text-green-600 transition">Farmer Advisory (কৃষক পরামর্শ)</button>
        </nav>

        <!-- Right Quick Badge -->
        <div class="flex items-center space-x-2">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5 animate-pulse"></span> Live Simulation
          </span>
        </div>
      </div>
    </div>
  </header>

  <!-- ====================================================================== -->
  <!-- Main Container -->
  <!-- ====================================================================== -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">

    <!-- TAB 1: PANI PIPE CROSS-SECTION SIMULATOR -->
    <section id="sec-simulator" class="space-y-6">
      <!-- Overview Banner -->
      <div class="bg-gradient-to-r from-emerald-800 to-teal-900 text-white rounded-2xl p-6 shadow-md">
        <div class="max-w-3xl">
          <span class="text-emerald-300 font-semibold text-xs tracking-wider uppercase">Interactive Biophysical Digital Twin</span>
          <h2 class="text-2xl font-bold mt-1 text-white">Perched Water Table ("Pani Pipe") & Root-Zone Simulator</h2>
          <p class="mt-2 text-emerald-100 text-sm leading-relaxed">
            Simulate water table recession and root-zone soil moisture dynamics in puddled clay-loam paddy soil.
            Observe why the <strong class="text-white">-15 cm threshold</strong> maintains complete capillary continuity, while deeper drying (> -18 cm) triggers exponential osmoregulatory proline accumulation and yield loss.
          </p>
        </div>
      </div>

      <!-- Simulator Canvas & Controls Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <!-- Canvas Viewport (7 Cols) -->
        <div class="lg:col-span-7 bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col items-center">
          <div class="w-full flex justify-between items-center mb-3">
            <h3 class="font-bold text-slate-800 text-sm flex items-center">
              <svg class="w-4 h-4 text-green-600 mr-1.5" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a8 8 0 100 16 8 8 0 000-16zM9 9a1 1 0 012 0v5a1 1 0 11-2 0V9zm1-4a1 1 0 100 2 1 1 0 000-2z"/></svg>
              Soil-Water-Crop Cross-Section Viewport
            </h3>
            <span id="badge-status" class="px-2.5 py-1 rounded-full text-xs font-bold bg-green-100 text-green-800">
              Capillary Intact (Safety Zone)
            </span>
          </div>

          <!-- The Animated HTML5 Canvas -->
          <div class="relative w-full aspect-[4/3] max-w-[560px] bg-sky-50 rounded-xl overflow-hidden border border-slate-300 shadow-inner">
            <canvas id="paddyCanvas" width="560" height="420" class="w-full h-full block"></canvas>
          </div>
          <p class="text-xs text-slate-400 mt-2 text-center">Puddled clay-loam over compacted plough pan (-22 cm). Perforated PVC Pani Pipe & capacitance moisture sensor shown.</p>
        </div>

        <!-- Interactive Controls & KPI Readouts (5 Cols) -->
        <div class="lg:col-span-5 space-y-4">
          <!-- Real-Time Readout Cards -->
          <div class="grid grid-cols-2 gap-3">
            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <span class="text-xs font-medium text-slate-500 uppercase">Water Level (z)</span>
              <div class="mt-1 flex items-baseline">
                <span id="kpi-z" class="text-2xl font-black text-slate-900">-15.0</span>
                <span class="text-xs font-semibold text-slate-500 ml-1">cm</span>
              </div>
              <span id="kpi-z-sub" class="text-xs text-emerald-600 font-medium">Perched Water Table</span>
            </div>

            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <span class="text-xs font-medium text-slate-500 uppercase">Soil Moisture (θv)</span>
              <div class="mt-1 flex items-baseline">
                <span id="kpi-theta" class="text-2xl font-black text-slate-900">39.2</span>
                <span class="text-xs font-semibold text-slate-500 ml-1">%</span>
              </div>
              <span class="text-xs text-slate-400">van Genuchten Capillary</span>
            </div>

            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <span class="text-xs font-medium text-slate-500 uppercase">Free Proline</span>
              <div class="mt-1 flex items-baseline">
                <span id="kpi-proline" class="text-2xl font-black text-slate-900">1.94</span>
                <span class="text-xs font-semibold text-slate-500 ml-1">µmol/g</span>
              </div>
              <span id="kpi-proline-sub" class="text-xs text-green-600 font-medium">Baseline (Zero Stress)</span>
            </div>

            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <span class="text-xs font-medium text-slate-500 uppercase">Leaf RWC</span>
              <div class="mt-1 flex items-baseline">
                <span id="kpi-rwc" class="text-2xl font-black text-slate-900">84.4</span>
                <span class="text-xs font-semibold text-slate-500 ml-1">%</span>
              </div>
              <span class="text-xs text-emerald-600 font-medium">Full Turgor Pressure</span>
            </div>
          </div>

          <!-- Controls Panel -->
          <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
            <h4 class="font-bold text-slate-900 text-sm">Interactive Parameter Tuning</h4>

            <!-- Treatment Presets -->
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5 uppercase">Treatment Presets</label>
              <div class="grid grid-cols-4 gap-2 text-xs">
                <button onclick="setPreset('T1')" class="py-1.5 px-2 rounded-lg font-bold border border-red-300 text-red-700 bg-red-50 hover:bg-red-100 transition">T1 Farmer</button>
                <button onclick="setPreset('T2')" class="py-1.5 px-2 rounded-lg font-bold border border-blue-300 text-blue-700 bg-blue-50 hover:bg-blue-100 transition">T2 Submerge</button>
                <button onclick="setPreset('T3')" class="py-1.5 px-2 rounded-lg font-bold border border-green-300 text-green-700 bg-green-50 hover:bg-green-100 transition">T3 AWD Pipe</button>
                <button onclick="setPreset('T4')" class="py-1.5 px-2 rounded-lg font-bold border border-purple-300 text-purple-700 bg-purple-50 hover:bg-purple-100 transition">T4 Sensor</button>
              </div>
            </div>

            <!-- AWD Reflood Threshold Slider -->
            <div>
              <div class="flex justify-between items-center text-xs mb-1">
                <span class="font-semibold text-slate-700">AWD Reflood Threshold:</span>
                <span id="lbl-slider-th" class="font-mono font-bold text-emerald-700">-15.0 cm</span>
              </div>
              <input type="range" id="slider-threshold" min="-30" max="5" step="0.5" value="-15"
                     oninput="updateSimulationFromSliders()" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-600">
              <div class="flex justify-between text-[10px] text-slate-400 mt-0.5">
                <span>+5 cm (Ponded)</span>
                <span class="font-bold text-emerald-600">-15 cm (Safe AWD)</span>
                <span>-30 cm (Drought)</span>
              </div>
            </div>

            <!-- Drainable Porosity (Specific Yield Sy) Slider -->
            <div>
              <div class="flex justify-between items-center text-xs mb-1">
                <span class="font-semibold text-slate-700">Drainable Porosity (Sy):</span>
                <span id="lbl-slider-sy" class="font-mono font-bold text-slate-700">0.16</span>
              </div>
              <input type="range" id="slider-sy" min="0.10" max="0.22" step="0.01" value="0.16"
                     oninput="updateSimulationFromSliders()" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-slate-600">
              <div class="flex justify-between text-[10px] text-slate-400 mt-0.5">
                <span>0.10 (Heavy Clay)</span>
                <span>0.16 (Clay-Loam)</span>
                <span>0.22 (Silty Loam)</span>
              </div>
            </div>

            <!-- Capillary Safety Explainer Note -->
            <div id="box-safety-note" class="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-900 leading-relaxed">
              <strong>Capillary Continuity Intact:</strong> At -15 cm, the capillary fringe connects the perched water table directly to the active root zone. Free proline is maintained at baseline (~1.94 µmol/g) with zero spikelet sterility.
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 2: 20-PLOT RCBD FIELD MAP & TELEMETRY -->
    <section id="sec-fieldmap" class="hidden space-y-6">
      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2">
        <div>
          <h2 class="text-xl font-bold text-slate-900">Egra Farmer's Field: 20-Plot RCBD Layout</h2>
          <p class="text-xs text-slate-500">Randomized Complete Block Design (4 Treatments × 5 Replications) + Plot 21 Independent Validation.</p>
        </div>
        <!-- Legend -->
        <div class="flex flex-wrap gap-2 text-xs">
          <span class="inline-flex items-center"><span class="w-3 h-3 rounded-full bg-[#D9534F] mr-1"></span> T1 Local</span>
          <span class="inline-flex items-center"><span class="w-3 h-3 rounded-full bg-[#337AB7] mr-1"></span> T2 Continuous</span>
          <span class="inline-flex items-center"><span class="w-3 h-3 rounded-full bg-[#5CB85C] mr-1"></span> T3 Manual AWD</span>
          <span class="inline-flex items-center"><span class="w-3 h-3 rounded-full bg-[#8E44AD] mr-1"></span> T4 Sensor AWD</span>
          <span class="inline-flex items-center"><span class="w-3 h-3 rounded-full bg-[#F39C12] mr-1"></span> Plot 21 Validation</span>
        </div>
      </div>

      <!-- Main Layout Grid: Plots Grid + Telemetry Inspector -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <!-- Plots Grid (7 Cols) -->
        <div class="lg:col-span-7 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <div class="space-y-3" id="plots-container">
            <!-- Populated dynamically via JS -->
          </div>

          <!-- Validation Plot 21 Row -->
          <div class="pt-4 border-t border-slate-200">
            <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Independent Validation Plot (Calibrated -15 cm Threshold)</h4>
            <div id="plot21-card" onclick="selectPlot(21)" class="cursor-pointer p-3 rounded-xl border-2 border-amber-400 bg-amber-50 hover:bg-amber-100 transition flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <span class="w-8 h-8 rounded-lg bg-amber-500 text-white font-black flex items-center justify-center text-sm shadow">21</span>
                <div>
                  <h5 class="text-sm font-bold text-slate-900">Validation Plot 21 (Independent)</h5>
                  <p class="text-xs text-slate-600">AWD (-15 cm threshold reflooded to +4.4 cm)</p>
                </div>
              </div>
              <div class="text-right">
                <span class="text-xs font-bold text-amber-700">WP: 1.36 kg/m³</span>
                <p class="text-[11px] text-slate-500">Savings: 27.0%</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Live Plot Telemetry Inspector (5 Cols) -->
        <div class="lg:col-span-5 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4" id="telemetry-panel">
          <div class="flex justify-between items-start border-b border-slate-100 pb-3">
            <div>
              <span id="tel-badge-trt" class="px-2 py-0.5 rounded text-xs font-bold bg-green-100 text-green-800">T3: Manual AWD</span>
              <h3 id="tel-title" class="text-lg font-black text-slate-900 mt-1">Plot 4 (Block R1)</h3>
            </div>
            <div class="text-right">
              <span class="text-xs text-slate-400">Seasonal WP</span>
              <div id="tel-wp" class="text-xl font-black text-emerald-600">1.31 kg/m³</div>
            </div>
          </div>

          <!-- Metrics Groups -->
          <div class="space-y-3 text-xs">
            <h4 class="font-bold text-slate-700 uppercase tracking-wider">Hydrological Water Balance</h4>
            <div class="grid grid-cols-2 gap-2 bg-slate-50 p-3 rounded-xl">
              <div><span class="text-slate-500">Irrigation Input:</span> <strong id="tel-irr" class="text-slate-800">501.6 mm</strong></div>
              <div><span class="text-slate-500">Water Savings:</span> <strong id="tel-sav" class="text-emerald-600 font-bold">24.0%</strong></div>
              <div><span class="text-slate-500">Crop ETa:</span> <strong id="tel-eta" class="text-slate-800">524.2 mm</strong></div>
              <div><span class="text-slate-500">Deep Percolation:</span> <strong id="tel-dp" class="text-slate-800">132.0 mm</strong></div>
            </div>

            <h4 class="font-bold text-slate-700 uppercase tracking-wider">Physiological & Biochemical Markers</h4>
            <div class="grid grid-cols-2 gap-2 bg-slate-50 p-3 rounded-xl">
              <div><span class="text-slate-500">Relative Water (RWC):</span> <strong id="tel-rwc" class="text-slate-800">84.3%</strong></div>
              <div><span class="text-slate-500">SPAD Chlorophyll:</span> <strong id="tel-spad" class="text-slate-800">40.2</strong></div>
              <div><span class="text-slate-500">Total Chlorophyll:</span> <strong id="tel-tchl" class="text-slate-800">2.69 mg/g</strong></div>
              <div><span class="text-slate-500">Free Proline:</span> <strong id="tel-proline" class="text-emerald-700 font-bold">1.94 µmol/g</strong></div>
            </div>

            <h4 class="font-bold text-slate-700 uppercase tracking-wider">Agronomic Yield Components</h4>
            <div class="grid grid-cols-2 gap-2 bg-slate-50 p-3 rounded-xl">
              <div><span class="text-slate-500">Grain Yield:</span> <strong id="tel-yield" class="text-slate-800">6.56 t/ha</strong></div>
              <div><span class="text-slate-500">Effective Tillers:</span> <strong id="tel-tillers" class="text-slate-800">14.6 / hill</strong></div>
              <div><span class="text-slate-500">Panicle Length:</span> <strong id="tel-pan" class="text-slate-800">23.2 cm</strong></div>
              <div><span class="text-slate-500">Filled Grains/Panicle:</span> <strong id="tel-grains" class="text-slate-800">132</strong></div>
              <div><span class="text-slate-500">1000-Grain Weight:</span> <strong id="tel-gw" class="text-slate-800">24.0 g</strong></div>
              <div><span class="text-slate-500">Harvest Index:</span> <strong id="tel-hi" class="text-slate-800">46.8%</strong></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 3: COMPARATIVE ANALYTICS -->
    <section id="sec-analytics" class="hidden space-y-6">
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
        <div>
          <h2 class="text-xl font-bold text-slate-900">Multi-Chart Comparative Analytics & Statistical Proof</h2>
          <p class="text-xs text-slate-500">Full 110-day seasonal water table trajectory, treatment comparison bars, and Pareto threshold sensitivity curve.</p>
        </div>

        <!-- 3 Interactive SVG Chart Containers -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Chart 1: Daily Water Table Trajectory -->
          <div class="border border-slate-200 rounded-xl p-4 bg-slate-50">
            <h4 class="text-xs font-bold text-slate-700 uppercase mb-2">110-Day Perched Water Table Trajectory z(t)</h4>
            <div class="w-full aspect-[16/10] bg-white rounded-lg border border-slate-200 overflow-hidden relative">
              <svg id="svg-sawtooth" viewBox="0 0 500 300" class="w-full h-full"></svg>
            </div>
            <div class="flex justify-center space-x-4 mt-2 text-[11px]">
              <span class="inline-flex items-center"><span class="w-2.5 h-2.5 rounded bg-red-500 mr-1"></span> T1</span>
              <span class="inline-flex items-center"><span class="w-2.5 h-2.5 rounded bg-blue-500 mr-1"></span> T2</span>
              <span class="inline-flex items-center"><span class="w-2.5 h-2.5 rounded bg-green-500 mr-1"></span> T3</span>
              <span class="inline-flex items-center"><span class="w-2.5 h-2.5 rounded bg-purple-500 mr-1"></span> T4</span>
            </div>
          </div>

          <!-- Chart 2: Pareto Threshold Sensitivity Curve -->
          <div class="border border-slate-200 rounded-xl p-4 bg-slate-50">
            <h4 class="text-xs font-bold text-slate-700 uppercase mb-2">Pareto Calibration Curve (0 to -30 cm Threshold)</h4>
            <div class="w-full aspect-[16/10] bg-white rounded-lg border border-slate-200 overflow-hidden relative">
              <svg id="svg-pareto" viewBox="0 0 500 300" class="w-full h-full"></svg>
            </div>
            <div class="flex justify-center space-x-4 mt-2 text-[11px]">
              <span class="text-emerald-600 font-bold">● Water Productivity</span>
              <span class="text-red-600 font-bold">--- Leaf Proline (µmol/g)</span>
              <span class="text-amber-500 font-bold">★ Plot 21 Validation</span>
            </div>
          </div>
        </div>

        <!-- ANOVA Summary Table Embed -->
        <div class="border border-slate-200 rounded-xl p-4">
          <h4 class="text-xs font-bold text-slate-700 uppercase mb-3">Two-Way RCBD ANOVA & Critical Difference (CD 0.05) Summary</h4>
          <div class="overflow-x-auto">
            <table class="min-w-full text-xs text-left">
              <thead class="bg-slate-100 text-slate-700 uppercase font-semibold">
                <tr>
                  <th class="py-2 px-3">Parameter</th>
                  <th class="py-2 px-3">T1 (Local)</th>
                  <th class="py-2 px-3">T2 (Submerge)</th>
                  <th class="py-2 px-3">T3 (Manual AWD)</th>
                  <th class="py-2 px-3">T4 (Sensor AWD)</th>
                  <th class="py-2 px-3">SEm±</th>
                  <th class="py-2 px-3">CD(0.05)</th>
                  <th class="py-2 px-3">Sig.</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-slate-600" id="anova-table-body">
                <!-- Dynamically populated from JSON -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 4: FARMER EXTENSION ADVISORY CALCULATOR -->
    <section id="sec-calculator" class="hidden space-y-6">
      <div class="bg-gradient-to-r from-emerald-700 to-green-800 text-white rounded-2xl p-6 shadow-md flex justify-between items-center flex-wrap gap-4">
        <div>
          <span class="text-emerald-200 font-semibold text-xs tracking-wider uppercase" id="calc-badge">Farmer Extension Advisory</span>
          <h2 class="text-2xl font-bold mt-1 text-white" id="calc-title">Egra Sub-Division Rice AWD Water & Cost Savings Calculator</h2>
          <p class="text-xs text-emerald-100 mt-1" id="calc-desc">Calculate exact groundwater, pumping energy, and money saved on your farm in Purba Medinipur.</p>
        </div>

        <!-- Bilingual Toggle Button -->
        <div class="flex items-center bg-white/20 p-1 rounded-xl backdrop-blur-sm border border-white/30">
          <button onclick="setLanguage('en')" id="btn-lang-en" class="px-3 py-1.5 rounded-lg text-xs font-bold transition bg-white text-emerald-900 shadow">English</button>
          <button onclick="setLanguage('bn')" id="btn-lang-bn" class="px-3 py-1.5 rounded-lg text-xs font-bold transition text-white hover:text-emerald-100">বাংলা (Bengali)</button>
        </div>
      </div>

      <!-- Calculator Card -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <!-- Input Form (5 Cols) -->
        <div class="lg:col-span-5 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h3 class="font-bold text-slate-900 text-sm" id="lbl-farm-details">Farm Land & Pumping Setup</h3>

          <!-- Land Area Input -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1" id="lbl-area">Total Cultivated Area</label>
            <div class="flex space-x-2">
              <input type="number" id="input-area" value="1.0" min="0.1" step="0.5" oninput="calculateSavings()"
                     class="flex-1 px-3 py-2 border border-slate-300 rounded-xl text-sm font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <select id="select-unit" onchange="calculateSavings()"
                      class="px-3 py-2 border border-slate-300 rounded-xl text-xs font-bold text-slate-800 bg-slate-50 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                <option value="bigha" selected>Bigha (বিঘা)</option>
                <option value="katha">Katha (কাঠা)</option>
                <option value="acre">Acre (একর)</option>
                <option value="hectare">Hectare (হেক্টর)</option>
              </select>
            </div>
            <p class="text-[11px] text-slate-400 mt-1" id="lbl-unit-note">Standard Bengal Bigha: 1 Bigha = 20 Katha = 1,338 m²</p>
          </div>

          <!-- Pumping Engine Type -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1" id="lbl-pump">Irrigation Pump Type</label>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <label class="flex items-center p-3 border border-slate-200 rounded-xl cursor-pointer hover:bg-slate-50 transition">
                <input type="radio" name="pumpType" value="electric" checked onchange="calculateSavings()" class="text-emerald-600 focus:ring-emerald-500">
                <span class="ml-2 font-semibold text-slate-800" id="lbl-elec-pump">Electric Submersible (STW)</span>
              </label>
              <label class="flex items-center p-3 border border-slate-200 rounded-xl cursor-pointer hover:bg-slate-50 transition">
                <input type="radio" name="pumpType" value="diesel" onchange="calculateSavings()" class="text-emerald-600 focus:ring-emerald-500">
                <span class="ml-2 font-semibold text-slate-800" id="lbl-diesel-pump">Diesel Engine Pump</span>
              </label>
            </div>
          </div>

          <!-- AWD Method -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1" id="lbl-method">AWD Irrigation Technology</label>
            <select id="select-method" onchange="calculateSavings()"
                    class="w-full px-3 py-2 border border-slate-300 rounded-xl text-xs font-bold text-slate-800 bg-slate-50 focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="T3" selected>Manual AWD (Pani Pipe, ~24% Savings)</option>
              <option value="T4">Sensor-Guided Adaptive AWD (~28% Savings)</option>
            </select>
          </div>

          <!-- Pipe Cost / Payback Note -->
          <div class="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 leading-relaxed" id="lbl-pipe-advice">
            <strong>Pani Pipe Fabrication:</strong> 1.25 m long 4-inch PVC pipe with bottom 15 cm perforated. Cost: ~₹120 per pipe. Payback achieved in less than 10 days of pumping!
          </div>
        </div>

        <!-- Calculated Output Cards (7 Cols) -->
        <div class="lg:col-span-7 space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- Groundwater Saved -->
            <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
              <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider" id="out-lbl-water">Groundwater Saved</span>
              <div class="my-2">
                <span id="out-water-litres" class="text-2xl font-black text-emerald-600">2,11,900</span>
                <span class="text-xs font-bold text-slate-500">Litres</span>
              </div>
              <p class="text-xs text-slate-400" id="out-water-m3">(~211.9 m³ of aquifer water preserved)</p>
            </div>

            <!-- Money Saved -->
            <div class="bg-gradient-to-br from-emerald-50 to-teal-50 p-5 rounded-2xl border border-emerald-200 shadow-sm flex flex-col justify-between">
              <span class="text-xs font-semibold text-emerald-700 uppercase tracking-wider" id="out-lbl-cost">Net Money Saved (Season)</span>
              <div class="my-2">
                <span id="out-cost-inr" class="text-3xl font-black text-emerald-800">₹5,488</span>
              </div>
              <p class="text-xs text-emerald-600 font-medium" id="out-energy-saved">59.3 Litres of diesel saved</p>
            </div>
          </div>

          <!-- Step-by-Step Farmer Instruction Box -->
          <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3">
            <h4 class="font-bold text-slate-900 text-sm" id="lbl-guide-title">Key Field Recommendations for Purba Medinipur Farmers</h4>
            <ul class="text-xs text-slate-600 space-y-2 list-disc list-inside leading-relaxed" id="lbl-guide-list">
              <li><strong>Pani Pipe Placement:</strong> Install one Pani Pipe per bigha in an average field spot (avoid depressions and bund edges).</li>
              <li><strong>Reflood Schedule:</strong> Do not irrigate until water drops to the -15 cm bottom mark. Reflood to 5 cm.</li>
              <li><strong class="text-red-600">CRITICAL FLOWERING WARNING:</strong> During panicle emergence & flowering (Days 58 to 72), maintain shallow standing water (2–3 cm) constantly to avoid grain sterility!</li>
              <li><strong>Terminal Ripening Drainage:</strong> Stop all irrigation 10 days before harvest to hasten uniform grain ripening.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- ====================================================================== -->
  <!-- Footer -->
  <!-- ====================================================================== -->
  <footer class="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500 mt-auto">
    <div class="max-w-7xl mx-auto px-4">
      <p class="font-medium text-slate-700">National Children's Science Congress (NCSC) Technical Investigation & Demonstration</p>
      <p class="mt-1">Integrated Soil-Water-Plant Dynamics in Rice under AWD | Egra Sub-Division, Purba Medinipur, West Bengal</p>
    </div>
  </footer>

  <!-- ====================================================================== -->
  <!-- EMBEDDED DATA & DIGITAL TWIN JAVASCRIPT ENGINE -->
  <!-- ====================================================================== -->
  <script>
    // Embedded Datasets from Python Simulator
    const ALL_PLOTS = {json.dumps(plots_all)};
    const DAILY_DATA = {json.dumps(daily_data)};
    const SWEEP_DATA = {json.dumps(sweep_data)};

    // Current State
    let currentTab = 'simulator';
    let simZ = -15.0;
    let simSy = 0.16;
    let currentLang = 'en';
    let selectedPlotId = 4;

    // --- TAB SWITCHING ---
    function switchTab(tabId) {{
      currentTab = tabId;
      document.querySelectorAll('section').forEach(sec => sec.classList.add('hidden'));
      document.querySelectorAll('.tab-link').forEach(btn => btn.classList.remove('tab-active'));
      
      const activeSec = document.getElementById('sec-' + tabId);
      const activeBtn = document.getElementById('tab-' + tabId);
      if (activeSec) activeSec.classList.remove('hidden');
      if (activeBtn) activeBtn.classList.add('tab-active');

      if (tabId === 'simulator') renderCanvas();
      if (tabId === 'analytics') renderAnalyticsCharts();
    }}

    // --- CANVAS DIGITAL TWIN ANIMATION ---
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

      // Coordinates mapping
      // Soil surface z = 0 is at y = 140
      // Scale: 1 cm = 8 pixels
      const surfaceY = 140;
      const scaleY = 8.0;

      // 1. Sky & Atmosphere
      const skyGrad = ctx.createLinearGradient(0, 0, 0, surfaceY);
      skyGrad.addColorStop(0, '#bae6fd');
      skyGrad.addColorStop(1, '#e0f2fe');
      ctx.fillStyle = skyGrad;
      ctx.fillRect(0, 0, w, surfaceY);

      // 2. Compacted Plough Pan (-22 cm) at y = 140 + 22 * 8 = 316
      const panY = surfaceY + 22 * scaleY;
      ctx.fillStyle = '#3e2723';
      ctx.fillRect(0, panY, w, h - panY);
      // Stipples for plough pan
      ctx.fillStyle = '#271612';
      for (let i = 15; i < w; i += 25) {{
        ctx.fillRect(i, panY + 10, 12, 6);
        ctx.fillRect(i + 10, panY + 30, 8, 4);
      }}

      // 3. Puddled Soil Layer (Surface to Plough Pan)
      const soilGrad = ctx.createLinearGradient(0, surfaceY, 0, panY);
      soilGrad.addColorStop(0, '#6d4c41');
      soilGrad.addColorStop(1, '#4e342e');
      ctx.fillStyle = soilGrad;
      ctx.fillRect(0, surfaceY, w, panY - surfaceY);

      // Water Table Level
      const waterY = surfaceY - simZ * scaleY;

      // 4. Perched Water / Saturated Soil Rendering
      if (simZ > 0) {{
        // Standing water above soil surface
        const pondGrad = ctx.createLinearGradient(0, waterY, 0, surfaceY);
        pondGrad.addColorStop(0, 'rgba(56, 189, 248, 0.7)');
        pondGrad.addColorStop(1, 'rgba(14, 165, 233, 0.85)');
        ctx.fillStyle = pondGrad;
        ctx.fillRect(0, waterY, w, surfaceY - waterY);

        // Water surface line with wave effect
        ctx.strokeStyle = '#0284c7';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(0, waterY);
        ctx.lineTo(w, waterY);
        ctx.stroke();
      }} else {{
        // Subsurface saturated capillary zone
        ctx.fillStyle = 'rgba(2, 132, 199, 0.28)';
        ctx.fillRect(0, waterY, w, panY - waterY);
        
        // Dashed perched water table line
        ctx.strokeStyle = '#0284c7';
        ctx.lineWidth = 2;
        ctx.setLineDash([6, 4]);
        ctx.beginPath();
        ctx.moveTo(0, waterY);
        ctx.lineTo(w, waterY);
        ctx.stroke();
        ctx.setLineDash([]);
      }}

      // 5. Critical -15 cm Threshold Line
      const critY = surfaceY + 15 * scaleY;
      ctx.strokeStyle = '#dc2626';
      ctx.lineWidth = 1.8;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(0, critY);
      ctx.lineTo(w, critY);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#dc2626';
      ctx.font = 'bold 11px sans-serif';
      ctx.fillText('Critical AWD Threshold (-15 cm)', 15, critY - 6);

      // 6. Draw Rice Plants (Hills)
      const plantPositions = [80, 180, 420, 500];
      plantPositions.forEach(px => {{
        ctx.strokeStyle = '#15803d';
        ctx.lineWidth = 2.5;
        // Leaves
        ctx.beginPath();
        ctx.moveTo(px, surfaceY);
        ctx.quadraticCurveTo(px - 25, surfaceY - 50, px - 35, surfaceY - 80);
        ctx.moveTo(px, surfaceY);
        ctx.quadraticCurveTo(px + 25, surfaceY - 50, px + 35, surfaceY - 80);
        ctx.moveTo(px, surfaceY);
        ctx.quadraticCurveTo(px, surfaceY - 60, px - 5, surfaceY - 95);
        ctx.stroke();

        // Roots (0 to -15 cm)
        ctx.strokeStyle = '#d97706';
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(px, surfaceY);
        ctx.lineTo(px - 15, surfaceY + 12 * scaleY);
        ctx.moveTo(px, surfaceY);
        ctx.lineTo(px + 15, surfaceY + 14 * scaleY);
        ctx.moveTo(px, surfaceY);
        ctx.lineTo(px, surfaceY + 15 * scaleY);
        ctx.stroke();
      }});

      // 7. Draw PVC Pani Pipe (Field Water Tube) at x = 280
      const pipeX = 280;
      const pipeW = 34;
      const pipeTopY = surfaceY - 15 * scaleY; // 15 cm above surface
      const pipeBottomY = surfaceY + 15 * scaleY; // 15 cm subsurface

      // Pipe body
      ctx.fillStyle = '#f1f5f9';
      ctx.strokeStyle = '#64748b';
      ctx.lineWidth = 2;
      ctx.fillRect(pipeX, pipeTopY, pipeW, pipeBottomY - pipeTopY);
      ctx.strokeRect(pipeX, pipeTopY, pipeW, pipeBottomY - pipeTopY);

      // Perforations on bottom 15 cm (subsurface section)
      ctx.fillStyle = '#334155';
      for (let py = surfaceY + 20; py < pipeBottomY - 10; py += 16) {{
        ctx.beginPath();
        ctx.arc(pipeX + 10, py, 2.5, 0, Math.PI * 2);
        ctx.arc(pipeX + 24, py, 2.5, 0, Math.PI * 2);
        ctx.fill();
      }}

      // Water level inside pipe
      const innerWaterY = Math.max(pipeTopY, Math.min(pipeBottomY, waterY));
      ctx.fillStyle = 'rgba(14, 165, 233, 0.7)';
      ctx.fillRect(pipeX + 2, innerWaterY, pipeW - 4, pipeBottomY - innerWaterY);

      // Pipe Label
      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('Pani Pipe', pipeX - 6, pipeTopY - 6);

      // 8. Capacitance Moisture Sensor Probe at x = 350
      const probeX = 350;
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      ctx.moveTo(probeX, surfaceY - 40);
      ctx.lineTo(probeX, surfaceY + 16 * scaleY);
      ctx.stroke();
      // Sensor Head with LED
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(probeX - 8, surfaceY - 45, 16, 20);
      ctx.fillStyle = (simZ >= -15.0) ? '#22c55e' : '#ef4444';
      ctx.beginPath();
      ctx.arc(probeX, surfaceY - 35, 3.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#475569';
      ctx.font = '9px sans-serif';
      ctx.fillText('Sensor', probeX - 8, surfaceY - 50);

      // 9. Soil Surface Boundary Line
      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 2.0;
      ctx.beginPath();
      ctx.moveTo(0, surfaceY);
      ctx.lineTo(w, surfaceY);
      ctx.stroke();
      ctx.fillStyle = '#334155';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('Soil Surface (z = 0 cm)', 15, surfaceY + 14);

      // 10. Plough Pan Label
      ctx.fillStyle = '#cbd5e1';
      ctx.fillText('Compacted Plough Pan (-22 cm)', 15, panY + 18);
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
        badge.className = 'px-2.5 py-1 rounded-full text-xs font-bold bg-green-100 text-green-800';
        badge.innerText = 'Capillary Intact (Safety Zone)';
        boxNote.className = 'p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-900 leading-relaxed';
        boxNote.innerHTML = '<strong>Capillary Continuity Intact:</strong> At ' + simZ.toFixed(1) + ' cm, the capillary fringe directly hydrates the active root zone. Free proline is baseline (~1.94 µmol/g) with zero yield loss.';
      }} else if (simZ >= -18.0) {{
        badge.className = 'px-2.5 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800';
        badge.innerText = 'Transition Vulnerability';
        boxNote.className = 'p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 leading-relaxed';
        boxNote.innerHTML = '<strong>Warning — Approaching Capillary Break:</strong> Soil matric potential dropping below -25 kPa. Free proline starting to accumulate (' + proline.toFixed(2) + ' µmol/g).';
      }} else {{
        badge.className = 'px-2.5 py-1 rounded-full text-xs font-bold bg-red-100 text-red-800';
        badge.innerText = 'Capillary Rupture / Severe Stress';
        boxNote.className = 'p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-900 leading-relaxed';
        boxNote.innerHTML = '<strong>CRITICAL HYDRAULIC DISCONNECTION:</strong> Capillary fringe ruptured! Proline surged to ' + proline.toFixed(2) + ' µmol/g. Severe spikelet sterility & irreversible grain yield collapse (> 12%).';
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

    // --- POPULATE PLOTS GRID ---
    function populatePlotsGrid() {{
      const container = document.getElementById('plots-container');
      container.innerHTML = '';

      const blocks = ['R1', 'R2', 'R3', 'R4', 'R5'];
      blocks.forEach(blk => {{
        const blkRow = document.createElement('div');
        blkRow.className = 'space-y-1.5';
        
        const blkLabel = document.createElement('div');
        blkLabel.className = 'text-[11px] font-bold text-slate-400 uppercase tracking-wider';
        blkLabel.innerText = 'Block ' + blk;
        blkRow.appendChild(blkLabel);
        
        const grid = document.createElement('div');
        grid.className = 'grid grid-cols-4 gap-2';
        
        const blkPlots = ALL_PLOTS.filter(p => p.block === blk);
        blkPlots.forEach(p => {{
          const card = document.createElement('div');
          const isSelected = p.plot_id === selectedPlotId;
          const trtColors = {{
            'T1': 'border-red-300 hover:border-red-500 bg-red-50/50',
            'T2': 'border-blue-300 hover:border-blue-500 bg-blue-50/50',
            'T3': 'border-green-300 hover:border-green-500 bg-green-50/50',
            'T4': 'border-purple-300 hover:border-purple-500 bg-purple-50/50'
          }};
          const trtBadge = {{
            'T1': 'bg-red-500', 'T2': 'bg-blue-500', 'T3': 'bg-green-600', 'T4': 'bg-purple-600'
          }};

          card.className = `cursor-pointer p-2 rounded-xl border-2 transition ${{trtColors[p.treatment] || 'border-slate-200'}} ${{isSelected ? 'ring-2 ring-slate-900 shadow-md' : ''}}`;
          card.onclick = () => selectPlot(p.plot_id);
          
          card.innerHTML = `
            <div class="flex justify-between items-center mb-1">
              <span class="text-[11px] font-black text-slate-800">Plot ${{p.plot_id}}</span>
              <span class="text-[9px] font-bold text-white px-1.5 py-0.2 rounded ${{trtBadge[p.treatment]}}">${{p.treatment}}</span>
            </div>
            <div class="text-[11px] space-y-0.5">
              <div class="flex justify-between text-slate-500"><span>Yield:</span> <strong class="text-slate-700">${{p.grain_yield_tha.toFixed(2)}} t</strong></div>
              <div class="flex justify-between text-slate-500"><span>WP:</span> <strong class="text-emerald-700 font-bold">${{p.water_productivity_kg_m3.toFixed(2)}}</strong></div>
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

    // --- RENDER COMPARATIVE ANALYTICS CHARTS ---
    function renderAnalyticsCharts() {{
      // 1. Sawtooth SVG Chart
      const svgSaw = document.getElementById('svg-sawtooth');
      svgSaw.innerHTML = '';

      // Draw Axes
      const w = 500, h = 300, padX = 45, padY = 25;
      const plotW = w - padX - 20;
      const plotH = h - padY - 35;

      // Map day (1..110) to x, z (+8..-24) to y
      const mapX = d => padX + ((d - 1) / 109) * plotW;
      const mapY = z => padY + ((8 - z) / 32) * plotH;

      // Surface line (z=0)
      const surfY = mapY(0);
      svgSaw.innerHTML += `<line x1="${{padX}}" y1="${{surfY}}" x2="${{w-20}}" y2="${{surfY}}" stroke="#94a3b8" stroke-width="1.2"/>`;
      svgSaw.innerHTML += `<text x="5" y="${{surfY + 3}}" font-size="9" fill="#64748b" font-weight="bold">0 cm</text>`;

      // Threshold line (-15)
      const thY = mapY(-15);
      svgSaw.innerHTML += `<line x1="${{padX}}" y1="${{thY}}" x2="${{w-20}}" y2="${{thY}}" stroke="#dc2626" stroke-width="1.2" stroke-dasharray="4,3"/>`;
      svgSaw.innerHTML += `<text x="5" y="${{thY + 3}}" font-size="9" fill="#dc2626" font-weight="bold">-15 cm</text>`;

      // Flowering Shading (Days 58-72)
      const flX1 = mapX(58), flX2 = mapX(72);
      svgSaw.innerHTML += `<rect x="${{flX1}}" y="${{padY}}" width="${{flX2 - flX1}}" height="${{plotH}}" fill="#fef3c7" opacity="0.6"/>`;
      svgSaw.innerHTML += `<text x="${{(flX1+flX2)/2}}" y="${{padY + 12}}" font-size="8" fill="#b45309" text-anchor="middle" font-weight="bold">Flowering</text>`;

      // Plot Trajectories
      const trtKeys = [
        {{ key: 't1_z_cm', color: '#D9534F', width: 1.5 }},
        {{ key: 't2_z_cm', color: '#337AB7', width: 1.5 }},
        {{ key: 't3_z_cm', color: '#5CB85C', width: 2.0 }},
        {{ key: 't4_z_cm', color: '#8E44AD', width: 2.0 }}
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

      // 2. Pareto Sensitivity SVG Chart
      const svgPar = document.getElementById('svg-pareto');
      svgPar.innerHTML = '';
      
      // Sweep data: threshold (0 to -30), WP (0.7 to 1.5), Proline (0 to 12)
      const mapParX = th => padX + (Math.abs(th) / 30) * plotW;
      const mapWP = wp => padY + ((1.5 - wp) / 0.8) * plotH;
      const mapPro = p => padY + ((12.0 - p) / 12.0) * plotH;

      // Draw Safety Zone (-15 cm line)
      const critParX = mapParX(-15);
      svgPar.innerHTML += `<rect x="${{padX}}" y="${{padY}}" width="${{critParX - padX}}" height="${{plotH}}" fill="#dcfce7" opacity="0.45"/>`;
      svgPar.innerHTML += `<rect x="${{critParX}}" y="${{padY}}" width="${{w - 20 - critParX}}" height="${{plotH}}" fill="#fee2e2" opacity="0.45"/>`;
      svgPar.innerHTML += `<line x1="${{critParX}}" y1="${{padY}}" x2="${{critParX}}" y2="${{padY + plotH}}" stroke="#d97706" stroke-width="1.8"/>`;
      svgPar.innerHTML += `<text x="${{critParX}}" y="${{padY + 12}}" font-size="8" fill="#d97706" text-anchor="middle" font-weight="bold">-15 cm Capillary Boundary</text>`;

      // Plot WP Curve
      let wpPath = '';
      SWEEP_DATA.forEach((pt, i) => {{
        const px = mapParX(pt.threshold_cm);
        const py = mapWP(pt.water_productivity_kg_m3);
        wpPath += (i === 0 ? `M ${{px}} ${{py}}` : ` L ${{px}} ${{py}}`);
      }});
      svgPar.innerHTML += `<path d="${{wpPath}}" fill="none" stroke="#16a34a" stroke-width="2.5"/>`;

      // Plot Proline Curve
      let proPath = '';
      SWEEP_DATA.forEach((pt, i) => {{
        const px = mapParX(pt.threshold_cm);
        const py = mapPro(pt.proline_umol_g);
        proPath += (i === 0 ? `M ${{px}} ${{py}}` : ` L ${{px}} ${{py}}`);
      }});
      svgPar.innerHTML += `<path d="${{proPath}}" fill="none" stroke="#dc2626" stroke-width="2.2" stroke-dasharray="4,3"/>`;

      // Validation Plot Star
      const starX = mapParX(-15.0);
      const starY = mapWP(1.364);
      svgPar.innerHTML += `<polygon points="${{starX}},${{starY-7}} ${{starX+2.5}},${{starY-2}} ${{starX+8}},${{starY-2}} ${{starX+3}},${{starY+2}} ${{starX+5}},${{starY+7}} ${{starX}},${{starY+4}} ${{starX-5}},${{starY+7}} ${{starX-3}},${{starY+2}} ${{starX-8}},${{starY-2}} ${{starX-2.5}},${{starY-2}}" fill="#f59e0b" stroke="#78350f" stroke-width="1"/>`;

      // Populate ANOVA Table
      const anovaTbody = document.getElementById('anova-table-body');
      anovaTbody.innerHTML = `
        <tr><td class="py-1.5 px-3 font-semibold text-slate-800">Irrigation Water (mm)</td><td class="py-1.5 px-3">659.9a</td><td class="py-1.5 px-3">609.4b</td><td class="py-1.5 px-3">501.7c</td><td class="py-1.5 px-3">475.4d</td><td class="py-1.5 px-3">0.58</td><td class="py-1.5 px-3">1.80</td><td class="py-1.5 px-3 font-bold text-red-600">** (P<0.001)</td></tr>
        <tr><td class="py-1.5 px-3 font-semibold text-slate-800">Grain Yield (t/ha)</td><td class="py-1.5 px-3">6.59b</td><td class="py-1.5 px-3">6.62a</td><td class="py-1.5 px-3">6.55c</td><td class="py-1.5 px-3">6.60b</td><td class="py-1.5 px-3">0.01</td><td class="py-1.5 px-3">0.02</td><td class="py-1.5 px-3 font-bold text-red-600">** (Parity)</td></tr>
        <tr><td class="py-1.5 px-3 font-semibold text-slate-800">Water Productivity (kg/m³)</td><td class="py-1.5 px-3">1.00d</td><td class="py-1.5 px-3">1.09c</td><td class="py-1.5 px-3">1.31b</td><td class="py-1.5 px-3">1.39a</td><td class="py-1.5 px-3">0.001</td><td class="py-1.5 px-3">0.004</td><td class="py-1.5 px-3 font-bold text-red-600">** (P<0.001)</td></tr>
        <tr><td class="py-1.5 px-3 font-semibold text-slate-800">Relative Water Content (RWC %)</td><td class="py-1.5 px-3">84.43a</td><td class="py-1.5 px-3">84.44a</td><td class="py-1.5 px-3">84.33a</td><td class="py-1.5 px-3">84.44a</td><td class="py-1.5 px-3">0.08</td><td class="py-1.5 px-3">NS</td><td class="py-1.5 px-3 font-bold text-emerald-600">NS (P=0.58)</td></tr>
        <tr><td class="py-1.5 px-3 font-semibold text-slate-800">Leaf Chlorophyll (SPAD)</td><td class="py-1.5 px-3">40.25a</td><td class="py-1.5 px-3">40.28a</td><td class="py-1.5 px-3">40.17a</td><td class="py-1.5 px-3">40.28a</td><td class="py-1.5 px-3">0.08</td><td class="py-1.5 px-3">NS</td><td class="py-1.5 px-3 font-bold text-emerald-600">NS (P=0.20)</td></tr>
        <tr><td class="py-1.5 px-3 font-semibold text-slate-800">Free Proline (µmol/g FW)</td><td class="py-1.5 px-3">1.92a</td><td class="py-1.5 px-3">1.92a</td><td class="py-1.5 px-3">1.92a</td><td class="py-1.5 px-3">1.95a</td><td class="py-1.5 px-3">0.01</td><td class="py-1.5 px-3">NS</td><td class="py-1.5 px-3 font-bold text-emerald-600">NS (P=0.84)</td></tr>
      `;
    }}

    // --- FARMER EXTENSION CALCULATOR ---
    function calculateSavings() {{
      const areaVal = parseFloat(document.getElementById('input-area').value) || 0;
      const unit = document.getElementById('select-unit').value;
      const pumpType = document.querySelector('input[name="pumpType"]:checked').value;
      const method = document.getElementById('select-method').value;

      // Convert input area to hectares
      let ha = areaVal;
      if (unit === 'bigha') ha = areaVal / 7.475;
      else if (unit === 'katha') ha = areaVal / (7.475 * 20.0);
      else if (unit === 'acre') ha = areaVal / 2.47105;

      // Savings per hectare
      // T3: 1584 m3/ha, T4: 1848 m3/ha
      const m3PerHa = (method === 'T4') ? 1848.0 : 1584.0;
      const totalM3 = m3PerHa * ha;
      const totalLitres = totalM3 * 1000.0;

      document.getElementById('out-water-litres').innerText = Math.round(totalLitres).toLocaleString();
      document.getElementById('out-water-m3').innerText = `(~${{totalM3.toFixed(1)}} m³ of aquifer water preserved)`;

      if (pumpType === 'electric') {{
        const kwhSaved = totalM3 * 0.35;
        const inrSaved = kwhSaved * 3.50; // WBSEDCL agricultural tariff
        document.getElementById('out-cost-inr').innerText = '₹' + Math.round(inrSaved).toLocaleString();
        document.getElementById('out-energy-saved').innerText = `${{kwhSaved.toFixed(1)}} kWh electricity saved (WBSEDCL Rs. 3.50/kWh)`;
      }} else {{
        const dieselSaved = totalM3 * 0.28;
        const inrSaved = dieselSaved * 92.50; // Diesel price Rs. 92.50/L
        document.getElementById('out-cost-inr').innerText = '₹' + Math.round(inrSaved).toLocaleString();
        document.getElementById('out-energy-saved').innerText = `${{dieselSaved.toFixed(1)}} Litres diesel saved (Rs. 92.50/L)`;
      }}
    }}

    // Bilingual Toggle
    const TRANSLATIONS = {{
      'en': {{
        badge: 'Farmer Extension Advisory',
        title: 'Egra Sub-Division Rice AWD Water & Cost Savings Calculator',
        desc: 'Calculate exact groundwater, pumping energy, and money saved on your farm in Purba Medinipur.',
        farmDetails: 'Farm Land & Pumping Setup',
        area: 'Total Cultivated Area',
        unitNote: 'Standard Bengal Bigha: 1 Bigha = 20 Katha = 1,338 m²',
        pump: 'Irrigation Pump Type',
        elecPump: 'Electric Submersible (STW)',
        dieselPump: 'Diesel Engine Pump',
        method: 'AWD Irrigation Technology',
        pipeAdvice: '<strong>Pani Pipe Fabrication:</strong> 1.25 m long 4-inch PVC pipe with bottom 15 cm perforated. Cost: ~₹120 per pipe. Payback achieved in less than 10 days of pumping!',
        outWater: 'Groundwater Saved',
        outCost: 'Net Money Saved (Season)',
        guideTitle: 'Key Field Recommendations for Purba Medinipur Farmers',
        guideList: `
          <li><strong>Pani Pipe Placement:</strong> Install one Pani Pipe per bigha in an average field spot (avoid depressions and bund edges).</li>
          <li><strong>Reflood Schedule:</strong> Do not irrigate until water drops to the -15 cm bottom mark. Reflood to 5 cm.</li>
          <li><strong class="text-red-600">CRITICAL FLOWERING WARNING:</strong> During panicle emergence & flowering (Days 58 to 72), maintain shallow standing water (2–3 cm) constantly to avoid grain sterility!</li>
          <li><strong>Terminal Ripening Drainage:</strong> Stop all irrigation 10 days before harvest to hasten uniform grain ripening.</li>
        `
      }},
      'bn': {{
        badge: 'কৃষক সম্প্রসারণ নির্দেশিকা',
        title: 'এগরা মহকুমা ধান চাষে অল্টারনেট ওয়েটিং-ড্রাইং (AWD) জল ও খরচ সাশ্রয় ক্যালকুলেটর',
        desc: 'পূর্ব মেদিনীপুরে আপনার জমিতে ভূগর্ভস্থ জল, পাম্পের বিদ্যুৎ/ডিজেল এবং মোট কত টাকা সাশ্রয় হবে হিসাব করুন।',
        farmDetails: 'জমির পরিমাণ ও পাম্প নির্বাচন',
        area: 'মোট চাষের জমির পরিমাণ',
        unitNote: 'বাংলার মাপ: ১ বিঘা = ২০ কাঠা = ১,৩৩৮ বর্গমিটার',
        pump: 'সেচ পাম্পের ধরন',
        elecPump: 'বৈদ্যুতিক সাবমার্সিবল পাম্প',
        dieselPump: 'ডিজেল ইঞ্জিন পাম্প',
        method: 'AWD সেচ প্রযুক্তি',
        pipeAdvice: '<strong>পানি পাইপ তৈরি:</strong> ১.২৫ মিটার লম্বা ৪ ইঞ্চি পিভিসি পাইপের নিচের ১৫ সেমিতে ছিদ্র করুন। খরচ: পাইপ প্রতি মাত্র ₹১২০ টাকা। কয়েকদিন পাম্প চালালেই সম্পূর্ণ খরচ উঠে আসে!',
        outWater: 'ভূগর্ভস্থ জল সাশ্রয়',
        outCost: 'মরসুমে মোট টাকা সাশ্রয়',
        guideTitle: 'পূর্ব মেদিনীপুরের কৃষকদের জন্য জরুরি মাঠ নির্দেশিকা',
        guideList: `
          <li><strong>পানি পাইপ বসানো:</strong> প্রতি বিঘায় একটি করে পানি পাইপ জমির মাঝামাঝি সাধারণ উচ্চতায় বসান (আইল বা গর্তের পাশে নয়)।</li>
          <li><strong>সেচ দেওয়ার সময়:</strong> পাইপের ভেতর জল মাটির নিচে -১৫ সেমি দাগে না নামা পর্যন্ত সেচ দেবেন না। জল নামলে ৫ সেমি সেচ দিন।</li>
          <li><strong class="text-red-600">ফুল আসার সতর্কবার্তা:</strong> থোড় ও ফুল আসার সময় (৫৮ থেকে ৭২ দিন) জমিতে সর্বদা ২-৩ সেমি পাতলা জল ধরে রাখুন, অন্যথায় ধান চিটা হতে পারে!</li>
          <li><strong>পাকার সময় শুকানো:</strong> ধান কাটার ১০ দিন আগে সমস্ত সেচ বন্ধ করে জমি শুকিয়ে নিন।</li>
        `
      }}
    }};

    function setLanguage(lang) {{
      currentLang = lang;
      const t = TRANSLATIONS[lang];
      document.getElementById('calc-badge').innerText = t.badge;
      document.getElementById('calc-title').innerText = t.title;
      document.getElementById('calc-desc').innerText = t.desc;
      document.getElementById('lbl-farm-details').innerText = t.farmDetails;
      document.getElementById('lbl-area').innerText = t.area;
      document.getElementById('lbl-unit-note').innerText = t.unitNote;
      document.getElementById('lbl-pump').innerText = t.pump;
      document.getElementById('lbl-elec-pump').innerText = t.elecPump;
      document.getElementById('lbl-diesel-pump').innerText = t.dieselPump;
      document.getElementById('lbl-method').innerText = t.method;
      document.getElementById('lbl-pipe-advice').innerHTML = t.pipeAdvice;
      document.getElementById('out-lbl-water').innerText = t.outWater;
      document.getElementById('out-lbl-cost').innerText = t.outCost;
      document.getElementById('lbl-guide-title').innerText = t.guideTitle;
      document.getElementById('lbl-guide-list').innerHTML = t.guideList;

      if (lang === 'bn') {{
        document.getElementById('btn-lang-bn').className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition bg-white text-emerald-900 shadow';
        document.getElementById('btn-lang-en').className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition text-white hover:text-emerald-100';
      }} else {{
        document.getElementById('btn-lang-en').className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition bg-white text-emerald-900 shadow';
        document.getElementById('btn-lang-bn').className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition text-white hover:text-emerald-100';
      }}
      calculateSavings();
    }}

    // Initialize on Page Load
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

with open(os.path.join(DOCS_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated standalone interactive HTML5 Digital Twin in: {os.path.join(DOCS_DIR, 'index.html')}")
