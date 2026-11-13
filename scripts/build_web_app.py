"""
scripts/build_web_app.py
Generates the comprehensive, standalone interactive HTML5 research application
and field advisory tool in docs/index.html.
Engineered with authentic scientific field-station aesthetics, 100% English terminology,
and zero external backend dependencies.
"""

import os
import json
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")


def build_web_app():
    os.makedirs(DOCS_DIR, exist_ok=True)

    # 1. Load CSV datasets
    df_rcbd = pd.read_csv(os.path.join(DATA_DIR, "rcbd_20plots_full_dataset.csv"))
    df_val = pd.read_csv(os.path.join(DATA_DIR, "independent_validation_plot21.csv"))
    df_daily = pd.read_csv(os.path.join(DATA_DIR, "daily_water_table_110days.csv"))
    df_sweep = pd.read_csv(os.path.join(DATA_DIR, "threshold_sensitivity_sweep.csv"))

    plots_all = df_rcbd.to_dict(orient="records") + df_val.to_dict(orient="records")
    daily_data = df_daily.to_dict(orient="records")
    sweep_data = df_sweep.to_dict(orient="records")

    json_plots = json.dumps(plots_all)
    json_daily = json.dumps(daily_data)
    json_sweep = json.dumps(sweep_data)

    # 2. Template with string replacement for data
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Field Investigation of Alternate Wetting and Drying (AWD) in Boro Rice — Egra, West Bengal</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            't1-col': '#b91c1c',
            't2-col': '#1d4ed8',
            't3-col': '#15803d',
            't4-col': '#7e22ce',
            'val-col': '#d97706',
            'pan-col': '#3e2723',
            'soil-col': '#5d4037'
          }
        }
      }
    };
  </script>
  <style>
    body {
      font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
    }
    .nav-tab-active {
      border-bottom: 2px solid #0f172a;
      color: #0f172a;
      font-weight: 700;
    }
    .table-numeric {
      font-variant-numeric: tabular-nums;
    }
    @keyframes pulseGlow {
      0%, 100% { box-shadow: 0 0 10px rgba(245, 158, 11, 0.5); }
      50% { box-shadow: 0 0 25px rgba(245, 158, 11, 0.9); }
    }
    .star-glow {
      animation: pulseGlow 2s infinite ease-in-out;
    }
    .custom-scroll::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scroll::-webkit-scrollbar-thumb {
      background-color: #cbd5e1;
      border-radius: 3px;
    }
  </style>
</head>
<body class="bg-stone-50 text-stone-900 font-sans antialiased min-h-screen flex flex-col">

  <!-- ====================================================================== -->
  <!-- Top Institutional Header -->
  <!-- ====================================================================== -->
  <header class="bg-white border-b border-stone-200 sticky top-0 z-50 shadow-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo / Title -->
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-md bg-stone-900 flex items-center justify-center text-white font-serif font-black text-sm">
            PM
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <h1 class="text-sm sm:text-base font-bold text-stone-900 leading-tight">Field Evaluation of Reduced Irrigation in Boro Rice</h1>
              <span class="hidden sm:inline-block px-2 py-0.5 rounded text-[10px] font-bold bg-stone-100 text-stone-700 border border-stone-300">ICAR-NCSC Research</span>
            </div>
            <p class="text-xs text-stone-500 font-medium">Farmer's Field, Egra Sub-Division, Purba Medinipur, West Bengal (2025–2026)</p>
          </div>
        </div>

        <!-- Quick Jump to Judge's Challenge -->
        <div class="flex items-center space-x-3">
          <button onclick="switchTab('challenge'); scrollToChallenge();" class="inline-flex items-center px-3 py-1.5 rounded-md text-xs font-bold bg-amber-500 hover:bg-amber-600 text-white shadow-xs transition">
            <span class="mr-1.5">🎯</span> Judge's Challenge
          </button>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <nav class="flex space-x-6 overflow-x-auto custom-scroll text-xs font-semibold text-stone-600 border-t border-stone-100">
        <button onclick="switchTab('cross_section')" id="tab-cross_section" class="nav-tab py-3 px-1 border-b-2 border-transparent hover:text-stone-900 transition whitespace-nowrap">1. Subsurface Cross-Section & Physics</button>
        <button onclick="switchTab('assay_lab')" id="tab-assay_lab" class="nav-tab py-3 px-1 border-b-2 border-transparent hover:text-stone-900 transition whitespace-nowrap">2. Virtual Biochemical Assay Lab</button>
        <button onclick="switchTab('fieldmap')" id="tab-fieldmap" class="nav-tab py-3 px-1 border-b-2 border-transparent hover:text-stone-900 transition whitespace-nowrap">3. 21-Plot Field Map & Logbook</button>
        <button onclick="switchTab('phenology')" id="tab-phenology" class="nav-tab py-3 px-1 border-b-2 border-transparent hover:text-stone-900 transition whitespace-nowrap">4. Crop Phenology & Guardrail</button>
        <button onclick="switchTab('extension')" id="tab-extension" class="nav-tab py-3 px-1 border-b-2 border-transparent hover:text-stone-900 transition whitespace-nowrap">5. Sensor Calibration & Extension</button>
        <button onclick="switchTab('challenge')" id="tab-challenge" class="nav-tab py-3 px-1 border-b-2 border-transparent hover:text-stone-900 transition whitespace-nowrap">6. Judge's Challenge & ANOVA</button>
      </nav>
    </div>
  </header>

  <!-- ====================================================================== -->
  <!-- Main Container -->
  <!-- ====================================================================== -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-8">

    <!-- ==================================================================== -->
    <!-- MODULE 1: SUBSURFACE CROSS-SECTION & SOIL PHYSICS -->
    <!-- ==================================================================== -->
    <section id="sec-cross_section" class="space-y-6">
      <div class="bg-white rounded-xl p-5 border border-stone-200">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 border-b border-stone-100 pb-4">
          <div>
            <div class="text-xs font-bold text-stone-500 uppercase tracking-wider mb-1">Agro-Hydrological State-Space Simulation</div>
            <h2 class="text-lg font-bold text-stone-900">Interactive Paddy Cross-Section (+10 cm to -30 cm Depth)</h2>
            <p class="text-xs text-stone-500 mt-0.5">Observe live capillary fringe feeding, deep percolation loss, PVC Pani Pipe, and capacitive moisture probe telemetry in real time.</p>
          </div>
          <div class="flex items-center space-x-2">
            <span id="badge-capillary-status" class="px-2.5 py-1 rounded text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
              Capillary Continuity Intact
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-6">
          <!-- Canvas Visualizer (7 Cols) -->
          <div class="lg:col-span-7 flex flex-col items-center">
            <div class="relative w-full overflow-hidden rounded-xl border border-stone-200 bg-stone-900 shadow-inner">
              <canvas id="cross-section-canvas" width="680" height="500" class="w-full h-auto block"></canvas>
            </div>
            <div class="w-full mt-3 flex justify-between text-[11px] text-stone-500 px-1">
              <span>Soil surface: z = 0 cm</span>
              <span>Root zone: 0 to -18 cm</span>
              <span>Plough pan: -22 cm</span>
              <span>Capillary limit: -15 cm</span>
            </div>
          </div>

          <!-- Controls & Telemetry Readouts (5 Cols) -->
          <div class="lg:col-span-5 space-y-4">
            <!-- Digital Telemetry Grid -->
            <div class="grid grid-cols-2 gap-3">
              <div class="bg-stone-50 p-3 rounded-lg border border-stone-200">
                <span class="text-[10px] font-bold text-stone-500 uppercase tracking-wider">Water Table Depth (z)</span>
                <div class="mt-0.5 flex items-baseline">
                  <span id="kpi-z" class="text-2xl font-black text-stone-900 table-numeric">-15.0</span>
                  <span class="text-xs font-medium text-stone-500 ml-1">cm</span>
                </div>
                <span id="kpi-z-sub" class="text-[11px] text-emerald-700 font-medium">Safe AWD Trigger</span>
              </div>

              <div class="bg-stone-50 p-3 rounded-lg border border-stone-200">
                <span class="text-[10px] font-bold text-stone-500 uppercase tracking-wider">Volumetric Moisture (θv)</span>
                <div class="mt-0.5 flex items-baseline">
                  <span id="kpi-theta" class="text-2xl font-black text-stone-900 table-numeric">39.2</span>
                  <span class="text-xs font-medium text-stone-500 ml-1">%</span>
                </div>
                <span class="text-[11px] text-stone-600">Saturated θs = 48.5%</span>
              </div>

              <div class="bg-stone-50 p-3 rounded-lg border border-stone-200">
                <span class="text-[10px] font-bold text-stone-500 uppercase tracking-wider">Soil Matric Potential (ψm)</span>
                <div class="mt-0.5 flex items-baseline">
                  <span id="kpi-matric" class="text-2xl font-black text-stone-900 table-numeric">-16.8</span>
                  <span class="text-xs font-medium text-stone-500 ml-1">kPa</span>
                </div>
                <span id="kpi-matric-sub" class="text-[11px] text-emerald-700 font-medium">Tension: Readily Available</span>
              </div>

              <div class="bg-stone-50 p-3 rounded-lg border border-stone-200">
                <span class="text-[10px] font-bold text-stone-500 uppercase tracking-wider">Deep Percolation (DP)</span>
                <div class="mt-0.5 flex items-baseline">
                  <span id="kpi-dp" class="text-2xl font-black text-stone-900 table-numeric">0.0</span>
                  <span class="text-xs font-medium text-stone-500 ml-1">mm/d</span>
                </div>
                <span id="kpi-dp-sub" class="text-[11px] text-emerald-700 font-medium">Hydrostatic Head Relieved</span>
              </div>
            </div>

            <!-- Interactive Sliders -->
            <div class="bg-white p-4 rounded-xl border border-stone-200 space-y-4">
              <h3 class="font-bold text-stone-800 text-xs uppercase tracking-wider">Live Water Table Control</h3>

              <!-- Water Depth Slider -->
              <div>
                <div class="flex justify-between items-center text-xs mb-1.5">
                  <span class="font-semibold text-stone-700">Perched Water Depth (z):</span>
                  <span id="lbl-slider-depth" class="font-mono font-bold text-stone-900 text-sm">-15.0 cm</span>
                </div>
                <input type="range" id="slider-depth" min="-30" max="8" step="0.5" value="-15"
                       oninput="onDepthSliderChange(parseFloat(this.value))"
                       class="w-full h-2 bg-stone-200 rounded-lg appearance-none cursor-pointer accent-stone-900">
                <div class="flex justify-between text-[10px] text-stone-400 mt-1">
                  <span>+8 cm (Heavy Flood)</span>
                  <span class="font-bold text-emerald-700">-15 cm (Safe AWD)</span>
                  <span>-30 cm (Drying Cliff)</span>
                </div>
              </div>

              <!-- Presets -->
              <div>
                <label class="block text-xs font-medium text-stone-600 mb-1.5">Field Treatment Presets</label>
                <div class="grid grid-cols-4 gap-2 text-xs">
                  <button onclick="setDepthPreset(1.5)" class="py-1.5 px-2 rounded font-semibold border border-red-200 bg-red-50 text-red-800 hover:bg-red-100 transition">T1 Farmer (+1.5)</button>
                  <button onclick="setDepthPreset(3.0)" class="py-1.5 px-2 rounded font-semibold border border-blue-200 bg-blue-50 text-blue-800 hover:bg-blue-100 transition">T2 Flood (+3.0)</button>
                  <button onclick="setDepthPreset(-15.0)" class="py-1.5 px-2 rounded font-semibold border border-emerald-300 bg-emerald-50 text-emerald-800 hover:bg-emerald-100 transition">T3 AWD (-15.0)</button>
                  <button onclick="setDepthPreset(-25.0)" class="py-1.5 px-2 rounded font-semibold border border-amber-300 bg-amber-50 text-amber-800 hover:bg-amber-100 transition">Stress (-25.0)</button>
                </div>
              </div>

              <!-- Soil Specific Yield (Sy) Slider -->
              <div>
                <div class="flex justify-between items-center text-xs mb-1">
                  <span class="font-medium text-stone-600">Drainable Porosity (Specific Yield Sy):</span>
                  <span id="lbl-slider-sy" class="font-mono font-bold text-stone-800">0.16</span>
                </div>
                <input type="range" id="slider-sy" min="0.10" max="0.22" step="0.01" value="0.16"
                       oninput="onSySliderChange(parseFloat(this.value))"
                       class="w-full h-1.5 bg-stone-200 rounded appearance-none cursor-pointer accent-stone-700">
                <div class="flex justify-between text-[10px] text-stone-400 mt-0.5">
                  <span>0.10 (Heavy Clay)</span>
                  <span>0.16 (Purba Medinipur Puddled)</span>
                  <span>0.22 (Loam)</span>
                </div>
              </div>

              <!-- Soil Physical Advisory Alert -->
              <div id="box-physics-advisory" class="p-3 bg-stone-50 border border-stone-200 rounded-lg text-xs leading-relaxed text-stone-700">
                <strong>Hydraulic Status:</strong> Perched water table at -15.0 cm sits precisely at the capillary fringe boundary. Capillary flux continuously replenishes the 0 to -18 cm root zone. Deep percolation drops to zero.
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================================================================== -->
    <!-- MODULE 2: VIRTUAL BIOCHEMICAL ASSAY LAB -->
    <!-- ==================================================================== -->
    <section id="sec-assay_lab" class="hidden space-y-6">
      <div class="bg-white rounded-xl p-5 border border-stone-200">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 border-b border-stone-100 pb-4">
          <div>
            <div class="text-xs font-bold text-stone-500 uppercase tracking-wider mb-1">Physiological & Biochemical Laboratory Assays</div>
            <h2 class="text-lg font-bold text-stone-900">Spectrophotometric Proline & Leaf Turgor Verification Lab</h2>
            <p class="text-xs text-stone-500 mt-0.5">Direct laboratory proof showing why leaf water status and metabolites remain statistically identical (P &gt; 0.05 NS) under AWD at -15 cm, but collapse beyond it.</p>
          </div>
          <div class="flex items-center space-x-2">
            <span class="px-2.5 py-1 rounded text-xs font-semibold bg-stone-100 text-stone-800 border border-stone-300">
              Bates et al. (1973) Protocol
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-6">
          <!-- Spectrophotometer Instrument Card (6 Cols) -->
          <div class="lg:col-span-6 bg-stone-900 text-white rounded-xl p-5 shadow-lg border border-stone-800 space-y-4">
            <div class="flex justify-between items-center border-b border-stone-800 pb-3">
              <div>
                <span class="text-[10px] font-mono tracking-widest text-stone-400 uppercase">UV-VIS Spectrophotometer</span>
                <h3 class="text-sm font-bold text-stone-100">Acid-Ninhydrin Free Proline Colorimeter (520 nm)</h3>
              </div>
              <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-stone-800 text-emerald-400 border border-stone-700">ONLINE</span>
            </div>

            <!-- Cuvette Chamber & LCD Display -->
            <div class="grid grid-cols-1 sm:grid-cols-12 gap-4 items-center">
              <!-- Visual Cuvette (5 Cols) -->
              <div class="sm:col-span-5 flex flex-col items-center justify-center p-4 bg-stone-950 rounded-lg border border-stone-800">
                <span class="text-[10px] text-stone-400 mb-2">Toluene Extract Cuvette (1 cm)</span>
                <!-- Glass Cuvette -->
                <div class="w-16 h-44 rounded-t-sm border-2 border-slate-400/80 bg-slate-900/60 p-1 flex flex-col justify-end relative shadow-inner">
                  <!-- Organic Toluene Layer with Chromophore -->
                  <div id="cuvette-liquid" class="w-full h-32 rounded-b-xs transition-colors duration-300 flex items-center justify-center text-[10px] font-mono font-bold text-stone-900/80" style="background-color: rgba(254, 205, 211, 0.75);">
                    520 nm
                  </div>
                  <!-- Liquid Meniscus -->
                  <div class="w-full h-1 bg-white/40 mb-0.5"></div>
                  <!-- Light Beam Path -->
                  <div class="absolute inset-y-16 -left-3 -right-3 h-4 bg-emerald-400/20 pointer-events-none flex items-center justify-between">
                    <span class="text-[8px] text-emerald-300">I₀ ▶</span>
                    <span class="text-[8px] text-emerald-300">▶ I</span>
                  </div>
                </div>
                <span id="cuvette-label" class="text-[10px] font-semibold text-stone-300 mt-2">Pale Baseline Pink</span>
              </div>

              <!-- Digital Spectrophotometer LCD Readout (7 Cols) -->
              <div class="sm:col-span-7 space-y-3">
                <div class="bg-black p-3.5 rounded-lg border border-stone-700 font-mono">
                  <div class="text-[10px] text-emerald-500 uppercase">Absorbance (A₅₂₀)</div>
                  <div id="lcd-abs" class="text-3xl font-black text-emerald-400 table-numeric tracking-wider">0.168</div>
                  <div class="text-[10px] text-stone-500 mt-1">Pathlength: 1.0 cm | λ = 520 nm</div>
                </div>

                <div class="bg-stone-800 p-3 rounded-lg border border-stone-700">
                  <div class="text-[10px] text-stone-400 uppercase font-semibold">Calculated Free Proline</div>
                  <div class="flex items-baseline space-x-1">
                    <span id="lcd-proline" class="text-2xl font-black text-white table-numeric">1.94</span>
                    <span class="text-xs text-stone-400 font-mono">µmol/g FW</span>
                  </div>
                  <div id="lcd-proline-status" class="mt-1 text-xs font-semibold text-emerald-400">
                    NS — Baseline (No Osmotic Shock)
                  </div>
                </div>
              </div>
            </div>

            <!-- Bates Equation -->
            <div class="text-[10px] text-stone-400 bg-stone-950 p-2.5 rounded border border-stone-800 leading-relaxed font-mono">
              Proline (µmol/g FW) = [(Abs₅₂₀ × Vol_toluene / 115.5) / (Sample_wt / 5)]
              <br><span class="text-stone-300">ANOVA: Treatment F = 0.28, P = 0.836 (NS across T1, T2, T3, T4 at -15 cm)</span>
            </div>
          </div>

          <!-- Leaf Turgor & SPAD Meter Widget (6 Cols) -->
          <div class="lg:col-span-6 bg-white rounded-xl p-5 border border-stone-200 space-y-4">
            <div class="flex justify-between items-center border-b border-stone-100 pb-3">
              <div>
                <span class="text-[10px] font-bold text-stone-500 uppercase tracking-wider">Physiological Markers</span>
                <h3 class="text-sm font-bold text-stone-900">Leaf Turgor (RWC %) & SPAD Chlorophyll Meter</h3>
              </div>
              <span id="badge-leaf-health" class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                Full Turgidity
              </span>
            </div>

            <!-- Leaf Cross-Section & Cell Diagram -->
            <div class="bg-stone-50 p-4 rounded-xl border border-stone-200 flex flex-col sm:flex-row items-center justify-between gap-4">
              <!-- Mesophyll Cell Diagram -->
              <div class="flex flex-col items-center">
                <span class="text-[11px] font-semibold text-stone-600 mb-1.5">Mesophyll Cellular Turgor</span>
                <svg id="svg-cells" width="130" height="90" viewBox="0 0 130 90" class="overflow-visible">
                  <!-- Hexagonal cells will update dynamically -->
                </svg>
                <span id="lbl-cell-state" class="text-[10px] font-bold text-emerald-700 mt-1">Turgid Plump Cells</span>
              </div>

              <!-- SPAD Swatch & Reading -->
              <div class="space-y-3 w-full sm:w-48">
                <div>
                  <div class="flex justify-between text-xs mb-1">
                    <span class="font-semibold text-stone-700">SPAD Chlorophyll:</span>
                    <span id="val-spad" class="font-mono font-bold text-stone-900">40.2</span>
                  </div>
                  <div class="w-full bg-stone-200 h-2.5 rounded-full overflow-hidden">
                    <div id="bar-spad" class="bg-emerald-600 h-full rounded-full transition-all duration-300" style="width: 80%;"></div>
                  </div>
                  <div class="flex justify-between text-[10px] text-stone-400 mt-0.5">
                    <span>0 (Chlorotic)</span>
                    <span>40.2 (Baseline)</span>
                    <span>50</span>
                  </div>
                </div>

                <div>
                  <div class="flex justify-between text-xs mb-1">
                    <span class="font-semibold text-stone-700">Leaf Relative Water Content:</span>
                    <span id="val-rwc" class="font-mono font-bold text-stone-900">84.4%</span>
                  </div>
                  <div class="w-full bg-stone-200 h-2.5 rounded-full overflow-hidden">
                    <div id="bar-rwc" class="bg-blue-600 h-full rounded-full transition-all duration-300" style="width: 84.4%;"></div>
                  </div>
                  <div class="flex justify-between text-[10px] text-stone-400 mt-0.5">
                    <span>&lt; 70% (Wilting)</span>
                    <span>84.4% (Turgid)</span>
                    <span>100%</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Interactive Water Depth Slider for Lab -->
            <div class="bg-stone-50 p-4 rounded-xl border border-stone-200 space-y-2">
              <div class="flex justify-between items-center text-xs">
                <span class="font-semibold text-stone-700">Simulate Subsurface Drying Depth:</span>
                <span id="lbl-lab-depth" class="font-mono font-bold text-stone-900">-15.0 cm</span>
              </div>
              <input type="range" id="slider-lab-depth" min="-30" max="5" step="0.5" value="-15"
                     oninput="onLabDepthChange(parseFloat(this.value))"
                     class="w-full h-2 bg-stone-200 rounded-lg appearance-none cursor-pointer accent-stone-900">
              <p class="text-[11px] text-stone-500 leading-normal">
                Drag past <strong>-15 cm</strong> to trigger cellular water deficit: watch the toluene extract transform to deep crimson and the leaf cells lose turgidity.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================================================================== -->
    <!-- MODULE 3: 21-PLOT EGRA FIELD MAP & LOGBOOK -->
    <!-- ==================================================================== -->
    <section id="sec-fieldmap" class="hidden space-y-6">
      <div class="bg-white rounded-xl p-5 border border-stone-200">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 border-b border-stone-100 pb-4">
          <div>
            <div class="text-xs font-bold text-stone-500 uppercase tracking-wider mb-1">Randomized Complete Block Design (RCBD)</div>
            <h2 class="text-lg font-bold text-stone-900">Farmer's Field Spatial Map (20 RCBD Plots + Plot 21 Validation)</h2>
            <p class="text-xs text-stone-500 mt-0.5">Select a heatmap metric to color-code plots. Click any plot to inspect its complete 110-day logbook card.</p>
          </div>
          <!-- Spotlight Button -->
          <div class="flex items-center space-x-2">
            <button onclick="togglePlot21Spotlight()" id="btn-spotlight" class="inline-flex items-center px-3 py-1.5 rounded-md text-xs font-bold bg-amber-100 hover:bg-amber-200 text-amber-900 border border-amber-300 transition">
              ⭐ Spotlight Validation Plot #21
            </button>
          </div>
        </div>

        <!-- Heatmap Metric Switcher -->
        <div class="flex flex-wrap items-center justify-between gap-3 mt-4 p-3 bg-stone-50 rounded-lg border border-stone-200">
          <div class="flex items-center space-x-2">
            <span class="text-xs font-bold text-stone-700">Heatmap Layer:</span>
            <div class="inline-flex rounded-md shadow-xs" role="group">
              <button onclick="setHeatmapMetric('irrigation_mm')" id="btn-heat-irr" class="px-2.5 py-1 text-xs font-semibold rounded-l-md border border-stone-300 bg-white hover:bg-stone-100 text-stone-800">Irrigation (mm)</button>
              <button onclick="setHeatmapMetric('water_productivity_kg_m3')" id="btn-heat-wp" class="px-2.5 py-1 text-xs font-semibold border-t border-b border-stone-300 bg-stone-900 text-white">Water Productivity (kg/m³)</button>
              <button onclick="setHeatmapMetric('grain_yield_tha')" id="btn-heat-yield" class="px-2.5 py-1 text-xs font-semibold border-t border-b border-stone-300 bg-white hover:bg-stone-100 text-stone-800">Grain Yield (t/ha)</button>
              <button onclick="setHeatmapMetric('proline_umol_g')" id="btn-heat-proline" class="px-2.5 py-1 text-xs font-semibold rounded-r-md border border-stone-300 bg-white hover:bg-stone-100 text-stone-800">Proline (µmol/g)</button>
            </div>
          </div>
          <!-- Color Legend -->
          <div class="flex items-center space-x-2 text-xs">
            <span id="legend-min-lbl" class="text-stone-500 font-mono">1.00</span>
            <div class="w-28 h-3 rounded bg-gradient-to-r from-stone-200 via-amber-200 to-emerald-600 border border-stone-300"></div>
            <span id="legend-max-lbl" class="text-stone-900 font-bold font-mono">1.39</span>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-6">
          <!-- Plots Grid (7 Cols) -->
          <div class="lg:col-span-7 space-y-4">
            <div id="plots-container" class="space-y-3">
              <!-- Dynamically populated -->
            </div>

            <!-- Validation Plot 21 Standalone Card -->
            <div id="plot21-card-container" class="pt-3 border-t border-stone-200">
              <!-- Dynamically rendered -->
            </div>
          </div>

          <!-- Selected Plot Logbook Card (5 Cols) -->
          <div class="lg:col-span-5">
            <div class="bg-stone-50 rounded-xl p-5 border border-stone-200 sticky top-24 space-y-4">
              <div class="flex justify-between items-start border-b border-stone-200 pb-3">
                <div>
                  <span class="text-[10px] font-bold text-stone-500 uppercase tracking-wider">Field Logbook Card</span>
                  <h3 id="tel-title" class="text-base font-bold text-stone-900">Plot 1 (Block R1)</h3>
                  <p id="tel-badge-trt" class="text-xs text-stone-600 font-medium mt-0.5">T2: Continuous Submergence (+1.0 to +5.0 cm)</p>
                </div>
                <div class="text-right">
                  <span class="text-[10px] text-stone-500">Water Productivity</span>
                  <div id="tel-wp" class="text-xl font-black text-stone-900 table-numeric">1.09 kg/m³</div>
                </div>
              </div>

              <!-- Mini Sawtooth Hydrograph -->
              <div>
                <span class="text-[11px] font-bold text-stone-600">110-Day Water Table Trajectory</span>
                <div class="w-full h-24 bg-white rounded border border-stone-200 mt-1 p-1">
                  <svg id="tel-mini-sawtooth" width="100%" height="100%" viewBox="0 0 300 80" preserveAspectRatio="none">
                    <!-- Path rendered in JS -->
                  </svg>
                </div>
                <div class="flex justify-between text-[10px] text-stone-400 mt-0.5">
                  <span>Day 1 (Transplant)</span>
                  <span class="text-amber-700 font-semibold">Days 58-72 (Flowering)</span>
                  <span>Day 110 (Harvest)</span>
                </div>
              </div>

              <!-- Complete Agronomic & Biochemical Breakdown -->
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div class="bg-white p-2.5 rounded border border-stone-200">
                  <span class="text-stone-500 block text-[10px]">Seasonal Irrigation:</span>
                  <strong id="tel-irr" class="text-stone-900 table-numeric text-sm">609.4 mm</strong>
                  <span id="tel-sav" class="text-[10px] text-stone-500 block">7.7% vs T1</span>
                </div>

                <div class="bg-white p-2.5 rounded border border-stone-200">
                  <span class="text-stone-500 block text-[10px]">Grain Yield:</span>
                  <strong id="tel-yield" class="text-stone-900 table-numeric text-sm">6.62 t/ha</strong>
                  <span class="text-[10px] text-emerald-700 block font-semibold">Agronomic Parity</span>
                </div>

                <div class="bg-white p-2.5 rounded border border-stone-200">
                  <span class="text-stone-500 block text-[10px]">Effective Tillers:</span>
                  <strong id="tel-tillers" class="text-stone-900 table-numeric">13.9 / hill</strong>
                </div>

                <div class="bg-white p-2.5 rounded border border-stone-200">
                  <span class="text-stone-500 block text-[10px]">Panicle Length:</span>
                  <strong id="tel-pan" class="text-stone-900 table-numeric">23.3 cm</strong>
                </div>

                <div class="bg-white p-2.5 rounded border border-stone-200">
                  <span class="text-stone-500 block text-[10px]">1000-Grain Weight:</span>
                  <strong id="tel-gw" class="text-stone-900 table-numeric">24.0 g</strong>
                </div>

                <div class="bg-white p-2.5 rounded border border-stone-200">
                  <span class="text-stone-500 block text-[10px]">Harvest Index:</span>
                  <strong id="tel-hi" class="text-stone-900 table-numeric">46.9%</strong>
                </div>

                <div class="bg-white p-2.5 rounded border border-stone-200">
                  <span class="text-stone-500 block text-[10px]">Leaf RWC:</span>
                  <strong id="tel-rwc" class="text-stone-900 table-numeric">84.4%</strong>
                </div>

                <div class="bg-white p-2.5 rounded border border-stone-200">
                  <span class="text-stone-500 block text-[10px]">Free Proline:</span>
                  <strong id="tel-proline" class="text-stone-900 table-numeric">1.92 µmol/g</strong>
                </div>
              </div>

              <!-- Side-by-Side Plot 21 Comparison Modal / Box -->
              <div id="box-plot21-spotlight-summary" class="hidden p-3 bg-amber-50 border border-amber-200 rounded-lg text-xs space-y-1.5 text-amber-900">
                <div class="font-bold text-amber-950 flex items-center">
                  <span class="mr-1">⭐</span> Independent Validation Plot #21 Synthesis
                </div>
                <p class="leading-relaxed">
                  Managed under the calibrated <strong>-15.0 cm</strong> threshold: achieved <strong>481.8 mm</strong> irrigation (<strong>27.0% savings</strong> vs. T1), <strong>1.364 kg/m³</strong> water productivity, and <strong>6.57 t/ha</strong> grain yield—confirming empirical replication on untracked soil.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================================================================== -->
    <!-- MODULE 4: 110-DAY CROP PHENOLOGY & FLOWERING GUARDRAIL -->
    <!-- ==================================================================== -->
    <section id="sec-phenology" class="hidden space-y-6">
      <div class="bg-white rounded-xl p-5 border border-stone-200">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 border-b border-stone-100 pb-4">
          <div>
            <div class="text-xs font-bold text-stone-500 uppercase tracking-wider mb-1">Stage-Aware Hydrological Rules</div>
            <h2 class="text-lg font-bold text-stone-900">110-Day Crop Phenology & "Flowering Guardrail" Scrubber</h2>
            <p class="text-xs text-stone-500 mt-0.5">Scrub through the Boro rice growth cycle. Notice how drying is automatically suspended during Flowering (Days 58–72) to protect spikelet fertility.</p>
          </div>
          <div id="badge-guardrail" class="px-2.5 py-1 rounded text-xs font-bold bg-stone-100 text-stone-600 border border-stone-300">
            Guardrail: Standby
          </div>
        </div>

        <!-- Phenology Interactive Scrubber -->
        <div class="mt-6 bg-stone-50 p-5 rounded-xl border border-stone-200 space-y-4">
          <div class="flex justify-between items-center text-xs">
            <div>
              <span class="text-stone-500 uppercase font-semibold text-[10px]">Timeline Position:</span>
              <strong id="lbl-scrub-day" class="text-base text-stone-900 ml-1">Day 65 after Transplanting</strong>
            </div>
            <div>
              <span class="text-stone-500 uppercase font-semibold text-[10px]">Crop Stage:</span>
              <strong id="lbl-scrub-stage" class="text-xs text-amber-800 ml-1">Flowering / Anthesis (Kc = 1.25)</strong>
            </div>
          </div>

          <!-- Slider -->
          <input type="range" id="slider-phenology" min="1" max="110" step="1" value="65"
                 oninput="onPhenologyScrub(parseInt(this.value))"
                 class="w-full h-3 bg-stone-200 rounded-lg appearance-none cursor-pointer accent-stone-900">

          <!-- Phenology 5-Stage Visual Bar -->
          <div class="grid grid-cols-5 gap-1 text-center text-[10px] font-semibold pt-1">
            <div class="p-1.5 rounded bg-blue-50 border border-blue-200 text-blue-800">
              1. Transplanting<br><span class="text-[9px] font-normal">Days 0-15 (Kc 1.05)</span>
            </div>
            <div class="p-1.5 rounded bg-emerald-50 border border-emerald-200 text-emerald-800">
              2. Tillering<br><span class="text-[9px] font-normal">Days 16-42 (Kc 1.15)</span>
            </div>
            <div class="p-1.5 rounded bg-teal-50 border border-teal-200 text-teal-800">
              3. Panicle Init.<br><span class="text-[9px] font-normal">Days 43-57 (Kc 1.20)</span>
            </div>
            <div class="p-1.5 rounded bg-amber-100 border border-amber-300 text-amber-900 ring-2 ring-amber-400">
              4. FLOWERING<br><span class="text-[9px] font-bold text-amber-800">Days 58-72 (Kc 1.25)</span>
            </div>
            <div class="p-1.5 rounded bg-stone-100 border border-stone-200 text-stone-800">
              5. Ripening<br><span class="text-[9px] font-normal">Days 73-110 (Kc 0.90)</span>
            </div>
          </div>

          <!-- Guardrail Alert Banner -->
          <div id="banner-flowering-alert" class="p-4 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-900 space-y-1">
            <div class="font-bold flex items-center text-sm text-amber-950">
              <span class="mr-2">🛡️</span> CRITICAL REPRODUCTIVE WINDOW (Flowering Guardrail Active)
            </div>
            <p class="leading-relaxed">
              At <strong>Day 58 to 72</strong> (Heading and Anthesis), the AWD protocol strictly suspends drying and enforces <strong>shallow standing submergence (+2.5 to +3.0 cm)</strong>. Desiccating the perched water table during pollen meiosis triggers severe spikelet sterility (> 35% empty grains). Once anthesis completes on Day 73, safe AWD reflood triggers (-15 cm) immediately resume.
            </p>
          </div>

          <!-- Multi-Treatment Water Table Status on Scrubbed Day -->
          <div class="bg-white p-4 rounded-xl border border-stone-200">
            <h4 class="text-xs font-bold text-stone-700 uppercase tracking-wider mb-3">Field Perched Water Level Comparison on Selected Day</h4>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
              <div class="p-2.5 rounded bg-red-50/50 border border-red-200">
                <span class="text-red-700 font-bold block">T1 Farmer</span>
                <span id="pheno-t1-z" class="text-lg font-black text-stone-900 table-numeric">+3.2 cm</span>
                <span class="text-[10px] text-stone-500 block">Unstructured flooding</span>
              </div>
              <div class="p-2.5 rounded bg-blue-50/50 border border-blue-200">
                <span class="text-blue-700 font-bold block">T2 Continuous</span>
                <span id="pheno-t2-z" class="text-lg font-black text-stone-900 table-numeric">+2.8 cm</span>
                <span class="text-[10px] text-stone-500 block">Continuous ponding</span>
              </div>
              <div class="p-2.5 rounded bg-emerald-50/50 border border-emerald-200">
                <span class="text-emerald-700 font-bold block">T3 Manual AWD</span>
                <span id="pheno-t3-z" class="text-lg font-black text-stone-900 table-numeric">+2.5 cm</span>
                <span id="pheno-t3-note" class="text-[10px] text-emerald-800 block">Guardrail Ponding</span>
              </div>
              <div class="p-2.5 rounded bg-purple-50/50 border border-purple-200">
                <span class="text-purple-700 font-bold block">T4 Sensor AWD</span>
                <span id="pheno-t4-z" class="text-lg font-black text-stone-900 table-numeric">+2.5 cm</span>
                <span id="pheno-t4-note" class="text-[10px] text-purple-800 block">Guardrail Ponding</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================================================================== -->
    <!-- MODULE 5: SENSOR CALIBRATION & FARMER EXTENSION ADVISORY -->
    <!-- ==================================================================== -->
    <section id="sec-extension" class="hidden space-y-6">
      <div class="bg-white rounded-xl p-5 border border-stone-200">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 border-b border-stone-100 pb-4">
          <div>
            <div class="text-xs font-bold text-stone-500 uppercase tracking-wider mb-1">Translational Agronomy & Extension</div>
            <h2 class="text-lg font-bold text-stone-900">Capacitive Sensor Calibration & Farm-Scale Extension Tool</h2>
            <p class="text-xs text-stone-500 mt-0.5">Explore the electronic sensor calibration curve and calculate farm-level economic and greenhouse gas dividends in local land units.</p>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-6">
          <!-- Sensor Calibration Curve & Drying Simulation (6 Cols) -->
          <div class="lg:col-span-6 bg-stone-50 p-5 rounded-xl border border-stone-200 space-y-4">
            <div class="flex justify-between items-center border-b border-stone-200 pb-2">
              <h3 class="text-xs font-bold text-stone-800 uppercase tracking-wider">T4 Capacitive Soil Moisture Sensor Calibration</h3>
              <button onclick="simulateDryingCycle()" id="btn-sim-drying" class="px-2.5 py-1 text-xs font-semibold rounded bg-stone-900 hover:bg-stone-800 text-white transition">
                ▶ Simulate 5-Day Drying Cycle
              </button>
            </div>

            <!-- SVG Calibration Curve -->
            <div class="w-full h-56 bg-white rounded-lg border border-stone-200 p-2">
              <svg id="svg-calibration" width="100%" height="100%" viewBox="0 0 320 200">
                <!-- Rendered dynamically -->
              </svg>
            </div>

            <!-- Live Sensor Readout -->
            <div class="grid grid-cols-3 gap-2 text-center text-xs">
              <div class="bg-white p-2 rounded border border-stone-200">
                <span class="text-stone-500 text-[10px] block">Sensor Output:</span>
                <strong id="cal-v" class="text-stone-900 font-mono text-sm">1.82 V</strong>
              </div>
              <div class="bg-white p-2 rounded border border-stone-200">
                <span class="text-stone-500 text-[10px] block">Calibrated θv:</span>
                <strong id="cal-theta" class="text-stone-900 font-mono text-sm">39.2%</strong>
              </div>
              <div class="bg-white p-2 rounded border border-stone-200">
                <span class="text-stone-500 text-[10px] block">Perched Depth:</span>
                <strong id="cal-z" class="text-stone-900 font-mono text-sm">-15.0 cm</strong>
              </div>
            </div>
            <p class="text-[11px] text-stone-500 leading-relaxed">
              Capacitance probe detects frequency shift in soil dielectric permittivity (ε = 80 for water vs. 4 for mineral soil). Factory calibrated for Egra puddled clay-loam.
            </p>
          </div>

          <!-- Farm Calculator & Mobile SMS Preview (6 Cols) -->
          <div class="lg:col-span-6 space-y-4">
            <!-- Calculator Card -->
            <div class="bg-white p-5 rounded-xl border border-stone-200 space-y-4">
              <h3 class="text-xs font-bold text-stone-800 uppercase tracking-wider">Farmer Savings & Environmental Impact Calculator</h3>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                <div>
                  <label class="block text-stone-600 font-medium mb-1">Land Area</label>
                  <input type="number" id="input-area" value="1.0" min="0.1" step="0.1"
                         oninput="calculateSavings()"
                         class="w-full p-2 border border-stone-300 rounded focus:ring-1 focus:ring-stone-900 font-mono text-stone-900">
                </div>
                <div>
                  <label class="block text-stone-600 font-medium mb-1">Land Unit</label>
                  <select id="select-unit" onchange="calculateSavings()" class="w-full p-2 border border-stone-300 rounded focus:ring-1 focus:ring-stone-900 text-stone-900">
                    <option value="bigha">Bigha (1 Ha = 7.475 Bigha)</option>
                    <option value="katha">Katha (1 Bigha = 20 Katha)</option>
                    <option value="acre">Acre</option>
                    <option value="hectare" selected>Hectare</option>
                  </select>
                </div>
              </div>

              <!-- Pump Type -->
              <div class="text-xs">
                <label class="block text-stone-600 font-medium mb-1">Pumping Energy Source</label>
                <div class="flex space-x-4">
                  <label class="flex items-center space-x-1.5 cursor-pointer">
                    <input type="radio" name="pumpType" value="electric" checked onchange="calculateSavings()" class="accent-stone-900">
                    <span>Electric Submersible STW (WBSEDCL Rs. 3.50/kWh)</span>
                  </label>
                  <label class="flex items-center space-x-1.5 cursor-pointer">
                    <input type="radio" name="pumpType" value="diesel" onchange="calculateSavings()" class="accent-stone-900">
                    <span>Diesel Pump (Rs. 92.50/L)</span>
                  </label>
                </div>
              </div>

              <!-- Output KPI Cards -->
              <div class="grid grid-cols-2 gap-3 pt-2">
                <div class="p-3 bg-stone-50 rounded-lg border border-stone-200">
                  <span class="text-[10px] font-bold text-stone-500 uppercase">Groundwater Preserved</span>
                  <div id="out-water-litres" class="text-xl font-black text-stone-900 table-numeric">1,845,000</div>
                  <span id="out-water-m3" class="text-[11px] text-stone-600">(1,845.0 m³ preserved)</span>
                </div>

                <div class="p-3 bg-stone-50 rounded-lg border border-stone-200">
                  <span class="text-[10px] font-bold text-stone-500 uppercase">Pumping Cost Saved</span>
                  <div id="out-cost-inr" class="text-xl font-black text-emerald-700 table-numeric">₹2,260</div>
                  <span id="out-energy-saved" class="text-[11px] text-stone-600">645.8 kWh electricity saved</span>
                </div>
              </div>

              <!-- Methane & Sub-Division Impact -->
              <div class="p-3 bg-emerald-50/70 border border-emerald-200 rounded-lg text-xs space-y-1 text-emerald-950">
                <div class="font-bold">🌍 Methane (CH₄) & Regional Scale Dividends:</div>
                <div id="out-methane" class="text-[11px] leading-relaxed">
                  Periodic soil aeration cuts anaerobic methanogenesis by <strong>45%</strong> (IPCC guidelines): saving <strong>135.0 kg CH₄/ha</strong> (~3.78 tonnes CO₂e carbon reduction).
                </div>
                <div class="text-[11px] text-emerald-800 pt-1 border-t border-emerald-200/60">
                  If adopted across Egra Sub-Division's 10,000 ha Boro rice: <strong>18.5 Billion Litres</strong> of groundwater preserved annually.
                </div>
              </div>
            </div>

            <!-- Mobile SMS Alert Card (English) -->
            <div class="bg-stone-900 rounded-2xl p-4 text-white shadow-md max-w-sm mx-auto border border-stone-800">
              <div class="flex justify-between items-center text-[10px] text-stone-400 border-b border-stone-800 pb-2 mb-3">
                <span class="font-mono">EGRA AGRI-TELEMETRY</span>
                <span>4G LTE | 94% 🔋</span>
              </div>
              <div class="bg-stone-800 p-3 rounded-lg border border-stone-700 text-xs space-y-1.5 font-mono">
                <div class="text-amber-400 font-bold flex items-center">
                  <span class="mr-1.5">⚠️</span> FIELD ADVISORY (Plot T4)
                </div>
                <p class="text-stone-300 text-[11px] leading-relaxed">
                  Perched water table has dropped to <strong>-15.0 cm</strong> (Capillary safety limit reached).
                </p>
                <p class="text-emerald-400 text-[11px] font-bold">
                  ACTION: Apply 4.2 cm irrigation reflood within 24 hours.
                </p>
                <div class="text-[10px] text-stone-400 pt-1 border-t border-stone-700">
                  Stage: Tillering (Day 34) | Flowering Guardrail: OK
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================================================================== -->
    <!-- MODULE 6: JUDGE'S CHALLENGE & STATISTICAL SYNTHESIS -->
    <!-- ==================================================================== -->
    <section id="sec-challenge" class="hidden space-y-8">
      <!-- Judge's Challenge Card -->
      <div id="judge-challenge-card" class="bg-white rounded-xl p-6 border-2 border-amber-300 shadow-md space-y-6">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 border-b border-stone-100 pb-4">
          <div>
            <div class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-900 mb-1">
              Interactive Examination Tool
            </div>
            <h2 class="text-xl font-black text-stone-900">Judge's Challenge: Test Your Own Irrigation Threshold</h2>
            <p class="text-xs text-stone-500 mt-0.5">Select any AWD reflood depth from 0 cm down to -30 cm to run the complete Boro season simulation. Observe if your choice hits the biophysical Pareto sweet spot.</p>
          </div>
          <button onclick="runJudgeSimulation()" class="px-4 py-2 rounded-md font-bold text-xs bg-amber-500 hover:bg-amber-600 text-white shadow-xs transition">
            ▶ Run Boro Season Simulation
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
          <!-- Threshold Controls (5 Cols) -->
          <div class="lg:col-span-5 space-y-4">
            <div>
              <div class="flex justify-between items-center text-xs mb-1.5">
                <span class="font-bold text-stone-700">Your Chosen Reflood Depth:</span>
                <span id="judge-chosen-lbl" class="text-base font-black font-mono text-stone-900">-15.0 cm</span>
              </div>
              <input type="range" id="judge-slider-depth" min="-30" max="0" step="1" value="-15"
                     oninput="onJudgeSliderInput(parseInt(this.value))"
                     class="w-full h-2.5 bg-stone-200 rounded-lg appearance-none cursor-pointer accent-amber-600">
              <div class="flex justify-between text-[10px] text-stone-400 mt-1">
                <span>0 cm (Continuous)</span>
                <span class="font-bold text-stone-800">-15 cm</span>
                <span>-30 cm (Extreme)</span>
              </div>
            </div>

            <!-- Preset Depth Buttons -->
            <div>
              <span class="text-xs font-semibold text-stone-600 block mb-1.5">Quick Presets:</span>
              <div class="grid grid-cols-5 gap-1.5 text-xs">
                <button onclick="onJudgeSliderInput(0)" class="py-1 px-1 rounded font-semibold border border-stone-200 bg-stone-50 hover:bg-stone-100">0 cm</button>
                <button onclick="onJudgeSliderInput(-5)" class="py-1 px-1 rounded font-semibold border border-stone-200 bg-stone-50 hover:bg-stone-100">-5 cm</button>
                <button onclick="onJudgeSliderInput(-15)" class="py-1 px-1 rounded font-bold border border-amber-300 bg-amber-50 text-amber-900 hover:bg-amber-100">-15 cm ⭐</button>
                <button onclick="onJudgeSliderInput(-20)" class="py-1 px-1 rounded font-semibold border border-stone-200 bg-stone-50 hover:bg-stone-100">-20 cm</button>
                <button onclick="onJudgeSliderInput(-25)" class="py-1 px-1 rounded font-semibold border border-stone-200 bg-stone-50 hover:bg-stone-100">-25 cm</button>
              </div>
            </div>

            <!-- Verdict Card -->
            <div id="judge-verdict-card" class="p-4 bg-emerald-50 border border-emerald-200 rounded-lg text-xs space-y-1 text-emerald-950">
              <div class="font-bold text-sm">BIOPHYSICAL OPTIMUM IDENTIFIED</div>
              <p class="leading-relaxed text-[11px]">
                At <strong>-15.0 cm</strong>, Water Productivity peaks at <strong>1.39 kg/m³</strong> (+39% vs. local farmer practice) while saving <strong>28.0% water</strong> with zero grain yield loss and baseline proline (1.94 µmol/g FW).
              </p>
            </div>
          </div>

          <!-- Dynamic Output Scorecard (7 Cols) -->
          <div class="lg:col-span-7 grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
            <div class="bg-stone-50 p-3 rounded-lg border border-stone-200">
              <span class="text-stone-500 text-[10px] block">Water Saved vs. T1:</span>
              <strong id="judge-score-sav" class="text-xl font-black text-stone-900 table-numeric">28.0%</strong>
              <span id="judge-score-irr" class="text-[10px] text-stone-500 block">475.4 mm seasonal</span>
            </div>

            <div class="bg-stone-50 p-3 rounded-lg border border-stone-200">
              <span class="text-stone-500 text-[10px] block">Grain Yield:</span>
              <strong id="judge-score-yield" class="text-xl font-black text-stone-900 table-numeric">6.60 t/ha</strong>
              <span id="judge-score-loss" class="text-[10px] text-emerald-700 block font-semibold">0.0% loss (Parity)</span>
            </div>

            <div class="bg-stone-50 p-3 rounded-lg border border-stone-200">
              <span class="text-stone-500 text-[10px] block">Water Productivity:</span>
              <strong id="judge-score-wp" class="text-xl font-black text-emerald-700 table-numeric">1.39 kg/m³</strong>
              <span class="text-[10px] text-stone-500 block">Peak biophysical return</span>
            </div>

            <div class="bg-stone-50 p-3 rounded-lg border border-stone-200">
              <span class="text-stone-500 text-[10px] block">Leaf RWC:</span>
              <strong id="judge-score-rwc" class="text-xl font-black text-stone-900 table-numeric">84.4%</strong>
              <span class="text-[10px] text-emerald-700 block">Full cell hydration</span>
            </div>

            <div class="bg-stone-50 p-3 rounded-lg border border-stone-200">
              <span class="text-stone-500 text-[10px] block">Free Proline:</span>
              <strong id="judge-score-pro" class="text-xl font-black text-stone-900 table-numeric">1.94</strong>
              <span class="text-[10px] text-stone-500 block">µmol/g FW (Baseline)</span>
            </div>

            <div class="bg-stone-50 p-3 rounded-lg border border-stone-200">
              <span class="text-stone-500 text-[10px] block">Hydraulic Safety:</span>
              <strong id="judge-score-fringe" class="text-sm font-bold text-emerald-700 block mt-1">Capillary Connected</strong>
              <span class="text-[10px] text-stone-500 block">Root zone hydrated</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Live Pareto Sensitivity Curve -->
      <div class="bg-white rounded-xl p-5 border border-stone-200 space-y-4">
        <div class="flex justify-between items-center border-b border-stone-100 pb-3">
          <div>
            <h3 class="text-base font-bold text-stone-900">Pareto Calibration Curve (Water Productivity vs. Free Proline)</h3>
            <p class="text-xs text-stone-500">Notice your chosen threshold plotted live as a glowing star against the -15 cm capillary boundary.</p>
          </div>
        </div>

        <div class="w-full h-72 bg-white rounded-lg border border-stone-200 p-2">
          <svg id="svg-pareto" width="100%" height="100%" viewBox="0 0 520 280">
            <!-- Rendered in JS -->
          </svg>
        </div>
      </div>

      <!-- Official ICAR/NCSC Two-Way RCBD ANOVA Table -->
      <div class="bg-white rounded-xl p-5 border border-stone-200 space-y-4">
        <div class="flex justify-between items-center border-b border-stone-100 pb-3">
          <div>
            <div class="text-xs font-bold text-stone-500 uppercase tracking-wider mb-1">Biometrical Logbook Engine</div>
            <h3 class="text-base font-bold text-stone-900">Official ICAR / NCSC Two-Way RCBD ANOVA & Critical Difference Table</h3>
          </div>
          <span class="px-2.5 py-1 rounded text-xs font-mono font-medium bg-stone-100 text-stone-700 border border-stone-300">
            N = 20 Plots (df: Trt=3, Blk=4, Err=12)
          </span>
        </div>

        <div class="overflow-x-auto custom-scroll">
          <table class="w-full text-xs text-left border-collapse">
            <thead>
              <tr class="border-b border-stone-200 bg-stone-50 text-stone-600 font-bold uppercase text-[10px] tracking-wider">
                <th class="py-2.5 px-3">Agro-Hydrological / Physiological Marker</th>
                <th class="py-2.5 px-3 text-right">T1 Farmer</th>
                <th class="py-2.5 px-3 text-right">T2 Continuous</th>
                <th class="py-2.5 px-3 text-right">T3 Manual AWD</th>
                <th class="py-2.5 px-3 text-right">T4 Sensor AWD</th>
                <th class="py-2.5 px-3 text-right">SEm±</th>
                <th class="py-2.5 px-3 text-right">CD (0.05)</th>
                <th class="py-2.5 px-3 text-right">F-Ratio</th>
                <th class="py-2.5 px-3 text-left">Significance</th>
              </tr>
            </thead>
            <tbody id="anova-table-body" class="divide-y divide-stone-100 text-stone-800">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>
        <p class="text-[11px] text-stone-500 italic mt-2">
          Means sharing identical superscript letters are not significantly different at P = 0.05 (Tukey's HSD). SEm±: Standard Error of Mean; CD: Critical Difference at 5% level; NS: Non-Significant (P &gt; 0.05); **: Highly Significant (P &lt; 0.001).
        </p>
      </div>
    </section>

  </main>

  <!-- ====================================================================== -->
  <!-- Footer -->
  <!-- ====================================================================== -->
  <footer class="bg-white border-t border-stone-200 mt-auto py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center text-xs text-stone-500 gap-2">
      <div>
        <strong>Integrated Soil-Water-Plant Dynamics in Boro Rice</strong> | Egra Sub-Division, Purba Medinipur, West Bengal
      </div>
      <div>
        NCSC Technical Report & Oral Defense Edition | 100% Client-Side Interactive Architecture
      </div>
    </div>
  </footer>

  <!-- ====================================================================== -->
  <!-- Embedded Scientific Data & Application Logic -->
  <!-- ====================================================================== -->
  <script>
    // Injected Datasets
    const ALL_PLOTS = /* %%PLOTS_DATA%% */;
    const DAILY_DATA = /* %%DAILY_DATA%% */;
    const SWEEP_DATA = /* %%SWEEP_DATA%% */;

    // Application State
    let activeTab = 'cross_section';
    let simZ = -15.0;
    let simSy = 0.16;
    let selectedPlotId = 4;
    let currentHeatmapMetric = 'water_productivity_kg_m3';
    let plot21Spotlight = false;
    let animFrameId = null;
    let animTimestamp = 0;
    let dryingInterval = null;

    // Navigation Switcher
    function switchTab(tabId) {
      activeTab = tabId;
      const tabIds = ['cross_section', 'assay_lab', 'fieldmap', 'phenology', 'extension', 'challenge'];
      tabIds.forEach(id => {
        const sec = document.getElementById('sec-' + id);
        const tabBtn = document.getElementById('tab-' + id);
        if (sec) sec.classList.toggle('hidden', id !== tabId);
        if (tabBtn) tabBtn.classList.toggle('nav-tab-active', id === tabId);
      });

      if (tabId === 'cross_section') renderCanvas();
      else if (tabId === 'assay_lab') updateAssayLab(simZ);
      else if (tabId === 'fieldmap') {
        populatePlotsGrid();
        selectPlot(selectedPlotId);
      } else if (tabId === 'phenology') {
        onPhenologyScrub(parseInt(document.getElementById('slider-phenology').value));
      } else if (tabId === 'extension') {
        renderCalibrationCurve();
        calculateSavings();
      } else if (tabId === 'challenge') {
        renderParetoCurve();
        populateAnovaTable();
      }
    }

    function scrollToChallenge() {
      const card = document.getElementById('judge-challenge-card');
      if (card) card.scrollIntoView({ behavior: 'smooth' });
    }

    // ========================================================================
    // Biophysical Equations
    // ========================================================================
    function vanGenuchten(z) {
      if (z >= 0) return 48.5;
      const theta_s = 48.5, theta_r = 12.0, alpha = 0.05965, n = 2.0;
      const m = 1.0 - (1.0 / n);
      const absZ = Math.abs(z);
      return theta_r + (theta_s - theta_r) / Math.pow(1.0 + Math.pow(alpha * absZ, n), m);
    }

    function calcMatricPotential(z) {
      if (z >= 0) return 0.0;
      // Approximate retention curve for puddled clay loam (kPa)
      const absZ = Math.abs(z);
      if (absZ <= 15.0) return -(absZ * 1.12);
      return -(16.8 + Math.pow((absZ - 15.0) * 1.8, 1.45));
    }

    function calcDeepPercolation(z) {
      const Kpan = 1.25, Lpan = 10.0;
      if (z > 0) return Kpan * (1.0 + z / Lpan) * 1.9; // Includes initial ponded hydrostatic head
      if (z > -8.0) return Kpan * 0.18 * ((z + 8.0) / 8.0);
      return 0.0;
    }

    function calcProline(z) {
      if (z >= -15.0) return 1.94 + 0.04 * Math.sin(Math.abs(z));
      const s = Math.max(0.0, (-15.0 - z) / 15.0);
      return 1.94 + 6.5 * (Math.exp(2.2 * s) - 1.0);
    }

    function calcRWC(z) {
      if (z >= -15.0) return 84.4;
      const s = Math.max(0.0, (-15.0 - z) / 15.0);
      return Math.max(62.0, 84.4 - 14.5 * s);
    }

    function calcSPAD(z) {
      if (z >= -15.0) return 40.2;
      const s = Math.max(0.0, (-15.0 - z) / 15.0);
      return Math.max(28.0, 40.2 - 9.0 * s);
    }

    // ========================================================================
    // MODULE 1: Subsurface Cross-Section Canvas Animation
    // ========================================================================
    function onDepthSliderChange(val) {
      simZ = val;
      document.getElementById('lbl-slider-depth').innerText = (simZ > 0 ? '+' : '') + simZ.toFixed(1) + ' cm';
      updateMetrics();
      renderCanvas();
    }

    function onSySliderChange(val) {
      simSy = val;
      document.getElementById('lbl-slider-sy').innerText = simSy.toFixed(2);
      updateMetrics();
      renderCanvas();
    }

    function setDepthPreset(val) {
      const slider = document.getElementById('slider-depth');
      slider.value = val;
      onDepthSliderChange(val);
    }

    function updateMetrics() {
      const theta = vanGenuchten(simZ);
      const matric = calcMatricPotential(simZ);
      const dp = calcDeepPercolation(simZ);
      const pro = calcProline(simZ);

      document.getElementById('kpi-z').innerText = (simZ > 0 ? '+' : '') + simZ.toFixed(1);
      document.getElementById('kpi-theta').innerText = theta.toFixed(1);
      document.getElementById('kpi-matric').innerText = matric.toFixed(1);
      document.getElementById('kpi-dp').innerText = dp.toFixed(1);

      const badgeCap = document.getElementById('badge-capillary-status');
      const boxAdv = document.getElementById('box-physics-advisory');
      const kpiZSub = document.getElementById('kpi-z-sub');
      const kpiMatricSub = document.getElementById('kpi-matric-sub');
      const kpiDpSub = document.getElementById('kpi-dp-sub');

      if (simZ > 0) {
        badgeCap.className = 'px-2.5 py-1 rounded text-xs font-semibold bg-blue-50 text-blue-800 border border-blue-200';
        badgeCap.innerText = 'Ponded Submergence';
        kpiZSub.innerText = 'Continuous Flood Head';
        kpiMatricSub.innerText = 'Tension: 0 kPa (Saturated)';
        kpiDpSub.innerText = 'Active Hydrostatic Loss';
        boxAdv.className = 'p-3 bg-blue-50/60 border border-blue-200 rounded-lg text-xs leading-relaxed text-blue-900';
        boxAdv.innerHTML = '<strong>Ponded Hydrostatic Head:</strong> Standing water (+ ' + simZ.toFixed(1) + ' cm) exerts downward pressure, driving active percolation loss (' + dp.toFixed(1) + ' mm/day) through the plough pan.';
      } else if (simZ >= -15.0) {
        badgeCap.className = 'px-2.5 py-1 rounded text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200';
        badgeCap.innerText = 'Capillary Continuity Intact';
        kpiZSub.innerText = 'Safe AWD Zone';
        kpiMatricSub.innerText = 'Tension: Readily Available';
        kpiDpSub.innerText = 'Head Relieved (Near Zero)';
        boxAdv.className = 'p-3 bg-emerald-50/60 border border-emerald-200 rounded-lg text-xs leading-relaxed text-emerald-900';
        boxAdv.innerHTML = '<strong>Capillary Fringe Replenishment:</strong> Perched water at ' + simZ.toFixed(1) + ' cm continuously wicks upward into the root zone (θv = ' + theta.toFixed(1) + '%). Deep percolation drops to zero.';
      } else if (simZ >= -18.0) {
        badgeCap.className = 'px-2.5 py-1 rounded text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-200';
        badgeCap.innerText = 'Approaching Capillary Limit';
        kpiZSub.innerText = 'Capillary Tension Warning';
        kpiMatricSub.innerText = 'Tension: Stress Onset';
        kpiDpSub.innerText = 'Zero Percolation';
        boxAdv.className = 'p-3 bg-amber-50/60 border border-amber-200 rounded-lg text-xs leading-relaxed text-amber-900';
        boxAdv.innerHTML = '<strong>Capillary Tension Warning:</strong> Water table dropping past -15 cm. Upward capillary flux is breaking. Soil matric potential dropping below -25 kPa.';
      } else {
        badgeCap.className = 'px-2.5 py-1 rounded text-xs font-semibold bg-red-50 text-red-800 border border-red-200 animate-pulse';
        badgeCap.innerText = 'Capillary Continuity Broken — Stress Initiated';
        kpiZSub.innerText = 'Severe Dehydration Cliff';
        kpiMatricSub.innerText = 'High Suction (> -45 kPa)';
        kpiDpSub.innerText = 'Zero Percolation';
        boxAdv.className = 'p-3 bg-red-50/70 border border-red-200 rounded-lg text-xs leading-relaxed text-red-900';
        boxAdv.innerHTML = '<strong>Capillary Continuity Broken:</strong> Water table fell below capillary reach. Root hairs are desiccating, free proline surged to ' + pro.toFixed(2) + ' µmol/g FW, triggering spikelet sterility (> 12% yield loss).';
      }
    }

    function renderCanvas() {
      const canvas = document.getElementById('cross-section-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const w = canvas.width, h = canvas.height;

      ctx.clearRect(0, 0, w, h);

      // Depth mapping: +10 cm (top, y=30) to -30 cm (bottom, y=470)
      const topDepth = 10.0, bottomDepth = -30.0;
      const totalDepth = topDepth - bottomDepth; // 40 cm
      const plotTopY = 30, plotBottomY = 470;
      const plotH = plotBottomY - plotTopY;

      const depthToY = z => plotTopY + ((topDepth - z) / totalDepth) * plotH;

      const surfaceY = depthToY(0.0);
      const panY = depthToY(-22.0);
      const waterY = depthToY(simZ);
      const critY = depthToY(-15.0);

      // 1. Sky / Atmosphere Background (above surface)
      ctx.fillStyle = '#f8fafc';
      ctx.fillRect(50, 0, w - 50, surfaceY);

      // 2. Soil Profile Background (below surface)
      const isStressed = simZ < -15.0;
      ctx.fillStyle = isStressed ? '#e2d5c4' : '#d7c7b2';
      ctx.fillRect(50, surfaceY, w - 50, panY - surfaceY);

      // 3. Dense Plough Pan (-22 cm to -30 cm)
      ctx.fillStyle = '#4a3b32';
      ctx.fillRect(50, panY, w - 50, plotBottomY - panY);

      // Diagonal Hatching on Plough Pan
      ctx.strokeStyle = '#382b24';
      ctx.lineWidth = 1.0;
      ctx.beginPath();
      for (let x = 50; x < w; x += 14) {
        ctx.moveTo(x, panY);
        ctx.lineTo(x + 16, plotBottomY);
      }
      ctx.stroke();

      // 4. Perched Groundwater Table (or Ponded Water)
      if (simZ > 0) {
        // Ponded Water above soil
        ctx.fillStyle = 'rgba(56, 189, 248, 0.45)';
        ctx.fillRect(50, waterY, w - 50, surfaceY - waterY);
        // Water surface line
        ctx.strokeStyle = '#0284c7';
        ctx.lineWidth = 2.0;
        ctx.beginPath();
        ctx.moveTo(50, waterY);
        ctx.lineTo(w, waterY);
        ctx.stroke();
      } else {
        // Subsurface Perched Water Table
        ctx.fillStyle = 'rgba(2, 132, 199, 0.40)';
        ctx.fillRect(50, waterY, w - 50, panY - waterY);
        // Water table line
        ctx.strokeStyle = '#0369a1';
        ctx.lineWidth = 2.0;
        ctx.setLineDash([6, 3]);
        ctx.beginPath();
        ctx.moveTo(50, waterY);
        ctx.lineTo(w, waterY);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // 5. Capillary Fringe limit line (-15 cm)
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(50, critY);
      ctx.lineTo(w, critY);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#b45309';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('Capillary Fringe Boundary (-15 cm)', w - 195, critY - 4);

      // 6. ANIMATED FLUX ARROWS
      animTimestamp += 0.05;
      if (simZ > 0) {
        // Ponded: Thick downward blue percolation arrows through plough pan
        const numArrows = 5;
        const arrowSpacing = (w - 180) / numArrows;
        ctx.fillStyle = '#0284c7';
        ctx.strokeStyle = '#0284c7';
        ctx.lineWidth = 2.5;

        for (let i = 0; i < numArrows; i++) {
          const ax = 120 + i * arrowSpacing;
          const offset = (animTimestamp * 40 + i * 25) % (plotBottomY - panY);
          const ay = panY + offset;

          ctx.beginPath();
          ctx.moveTo(ax, ay);
          ctx.lineTo(ax, ay + 14);
          ctx.stroke();

          ctx.beginPath();
          ctx.moveTo(ax - 4, ay + 10);
          ctx.lineTo(ax, ay + 16);
          ctx.lineTo(ax + 4, ay + 10);
          ctx.fill();
        }

        ctx.fillStyle = '#0369a1';
        ctx.font = 'bold 10px sans-serif';
        ctx.fillText('Hydrostatic Deep Percolation Loss (DP ~ 3.8 mm/d)', 180, panY + 22);
      } else if (simZ >= -15.0) {
        // Safe AWD: Upward cyan capillary fringe arrows feeding roots
        const numArrows = 6;
        const arrowSpacing = (w - 180) / numArrows;
        ctx.fillStyle = '#06b6d4';
        ctx.strokeStyle = '#06b6d4';
        ctx.lineWidth = 2.2;

        for (let i = 0; i < numArrows; i++) {
          const ax = 110 + i * arrowSpacing;
          const rangeH = Math.max(20, waterY - surfaceY);
          const offset = (animTimestamp * 35 + i * 20) % rangeH;
          const ay = waterY - offset;

          if (ay > surfaceY + 10) {
            ctx.beginPath();
            ctx.moveTo(ax, ay);
            ctx.lineTo(ax, ay - 12);
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(ax - 3.5, ay - 8);
            ctx.lineTo(ax, ay - 14);
            ctx.lineTo(ax + 3.5, ay - 8);
            ctx.fill();
          }
        }

        ctx.fillStyle = '#0e7490';
        ctx.font = 'bold 10px sans-serif';
        ctx.fillText('Upward Capillary Fringe Flux (Hydrating 0 to -18 cm Roots)', 140, Math.min(critY + 18, waterY - 10));
      } else {
        // Deeper than -15 cm: Capillary break!
        ctx.fillStyle = '#b91c1c';
        ctx.font = 'bold 11px sans-serif';
        ctx.fillText('⚡ CAPILLARY CONTINUITY BROKEN: Hydraulic Contact Severed', 120, critY + 16);
      }

      // 7. Rice Plant Hill at x = 160
      const plantX = 160;
      // Roots (fibrous branching down to -18 cm)
      const rootColor = isStressed ? '#b45309' : '#fef3c7';
      ctx.strokeStyle = rootColor;
      ctx.lineWidth = 1.6;
      const rootDepthY = depthToY(-18.0);

      const rootOffsets = [-28, -20, -12, -4, 4, 12, 20, 28];
      rootOffsets.forEach((rx, idx) => {
        ctx.beginPath();
        ctx.moveTo(plantX, surfaceY);
        ctx.quadraticCurveTo(plantX + rx * 0.5, surfaceY + 30, plantX + rx, rootDepthY - (idx % 3) * 12);
        ctx.stroke();
      });

      // Stem & Green Shoots (above ground up to +10 cm)
      ctx.strokeStyle = '#15803d';
      ctx.lineWidth = 2.4;
      const shootTopY = depthToY(9.5);
      const shootOffsets = [-22, -14, -6, 0, 6, 14, 22];
      shootOffsets.forEach(sx => {
        ctx.beginPath();
        ctx.moveTo(plantX, surfaceY);
        ctx.quadraticCurveTo(plantX + sx * 0.6, surfaceY - 30, plantX + sx, shootTopY + Math.abs(sx) * 0.8);
        ctx.stroke();
      });

      ctx.fillStyle = '#14532d';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('Rice Hill (Oryza sativa)', plantX - 40, surfaceY - 45);

      // 8. PVC Pani Pipe (T3) at x = 320
      const pipeX = 320, pipeW = 34;
      const pipeTopY = depthToY(10.0);
      const pipeBottomY = depthToY(-15.0);

      // Pipe outer casing
      ctx.fillStyle = '#f8fafc';
      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 1.8;
      ctx.fillRect(pipeX, pipeTopY, pipeW, pipeBottomY - pipeTopY);
      ctx.strokeRect(pipeX, pipeTopY, pipeW, pipeBottomY - pipeTopY);

      // Subsurface perforations (bottom 15 cm)
      ctx.fillStyle = '#1e293b';
      for (let py = surfaceY + 12; py < pipeBottomY - 8; py += 15) {
        ctx.beginPath();
        ctx.arc(pipeX + 10, py, 2.2, 0, Math.PI * 2);
        ctx.arc(pipeX + 24, py, 2.2, 0, Math.PI * 2);
        ctx.fill();
      }

      // Water inside tube (rises and falls with perched depth)
      const innerWaterY = Math.max(pipeTopY, Math.min(pipeBottomY, waterY));
      ctx.fillStyle = 'rgba(2, 132, 199, 0.65)';
      ctx.fillRect(pipeX + 2, innerWaterY, pipeW - 4, pipeBottomY - innerWaterY);

      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('Pani Pipe (T3)', pipeX - 10, pipeTopY - 6);

      // 9. Capacitive Probe (T4) at x = 420
      const probeX = 420;
      // Sensor Head (at surface)
      ctx.fillStyle = '#334155';
      ctx.fillRect(probeX - 12, surfaceY - 18, 24, 18);
      ctx.fillStyle = '#38bdf8';
      ctx.fillRect(probeX - 8, surfaceY - 14, 16, 10); // LCD glass

      // Dual metal sensing tines to -15 cm
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      ctx.moveTo(probeX - 6, surfaceY);
      ctx.lineTo(probeX - 6, critY);
      ctx.moveTo(probeX + 6, surfaceY);
      ctx.lineTo(probeX + 6, critY);
      ctx.stroke();

      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('Capacitive Probe (T4)', probeX - 35, surfaceY - 24);

      // 10. Depth Ruler on Left (0 to 50 px)
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(0, 0, 50, h);
      ctx.fillStyle = '#f8fafc';
      ctx.font = '9px monospace';
      ctx.strokeStyle = '#64748b';
      ctx.lineWidth = 1.0;

      for (let d = topDepth; d >= bottomDepth; d -= 1.0) {
        const dy = depthToY(d);
        const isMajor = Math.abs(d) % 5 === 0;
        ctx.beginPath();
        ctx.moveTo(isMajor ? 28 : 38, dy);
        ctx.lineTo(48, dy);
        ctx.stroke();

        if (isMajor) {
          const label = (d > 0 ? '+' : '') + d + 'cm';
          ctx.fillText(label, 4, dy + 3);
        }
      }

      // Soil Surface Line (0 cm)
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 2.0;
      ctx.beginPath();
      ctx.moveTo(50, surfaceY);
      ctx.lineTo(w, surfaceY);
      ctx.stroke();

      // Plough Pan Label
      ctx.fillStyle = '#e2e8f0';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('Impervious Compacted Plough Pan (-22 cm to -32 cm)', 60, panY + 18);
    }

    // Animation Loop
    function startAnimation() {
      if (animFrameId) cancelAnimationFrame(animFrameId);
      function loop() {
        if (activeTab === 'cross_section') {
          renderCanvas();
        }
        animFrameId = requestAnimationFrame(loop);
      }
      animFrameId = requestAnimationFrame(loop);
    }

    // ========================================================================
    // MODULE 2: Virtual Biochemical Assay Lab
    // ========================================================================
    function onLabDepthChange(val) {
      document.getElementById('lbl-lab-depth').innerText = (val > 0 ? '+' : '') + val.toFixed(1) + ' cm';
      updateAssayLab(val);
    }

    function updateAssayLab(z) {
      const pro = calcProline(z);
      const rwc = calcRWC(z);
      const spad = calcSPAD(z);

      // Absorbance at 520 nm ~ Proline * 0.0866
      const abs520 = (pro * 0.0866).toFixed(3);
      document.getElementById('lcd-abs').innerText = abs520;
      document.getElementById('lcd-proline').innerText = pro.toFixed(2);

      // Cuvette Color Interpolation
      const cuvette = document.getElementById('cuvette-liquid');
      const cuvetteLbl = document.getElementById('cuvette-label');
      const proStatus = document.getElementById('lcd-proline-status');

      if (pro <= 2.2) {
        cuvette.style.backgroundColor = 'rgba(254, 205, 211, 0.75)'; // pale pink
        cuvetteLbl.innerText = 'Pale Baseline Pink';
        proStatus.className = 'mt-1 text-xs font-semibold text-emerald-400';
        proStatus.innerText = 'NS — Baseline (Zero Osmotic Shock)';
      } else if (pro <= 4.0) {
        cuvette.style.backgroundColor = 'rgba(244, 63, 94, 0.85)'; // rose red
        cuvetteLbl.innerText = 'Vibrant Rose-Red';
        proStatus.className = 'mt-1 text-xs font-semibold text-amber-400';
        proStatus.innerText = 'Moderate Osmolyte Accumulation';
      } else {
        cuvette.style.backgroundColor = 'rgba(159, 18, 57, 0.95)'; // crimson red
        cuvetteLbl.innerText = 'Deep Crimson-Red (High A₅₂₀)';
        proStatus.className = 'mt-1 text-xs font-semibold text-red-400 animate-pulse';
        proStatus.innerText = 'CRITICAL STRESS: Proline Surge > 300%';
      }

      // SPAD & RWC
      document.getElementById('val-spad').innerText = spad.toFixed(1);
      document.getElementById('bar-spad').style.width = ((spad / 50.0) * 100) + '%';

      document.getElementById('val-rwc').innerText = rwc.toFixed(1) + '%';
      document.getElementById('bar-rwc').style.width = rwc.toFixed(1) + '%';

      const leafBadge = document.getElementById('badge-leaf-health');
      const cellLbl = document.getElementById('lbl-cell-state');
      if (rwc >= 82.0) {
        leafBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800';
        leafBadge.innerText = 'Full Turgidity (P > 0.05 NS)';
        cellLbl.className = 'text-[10px] font-bold text-emerald-700 mt-1';
        cellLbl.innerText = 'Turgid Plump Cells';
      } else if (rwc >= 75.0) {
        leafBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800';
        leafBadge.innerText = 'Mild Flaccidity';
        cellLbl.className = 'text-[10px] font-bold text-amber-700 mt-1';
        cellLbl.innerText = 'Partial Cellular Shrinkage';
      } else {
        leafBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-red-100 text-red-800 animate-pulse';
        leafBadge.innerText = 'Severe Wilting & Stomatal Closure';
        cellLbl.className = 'text-[10px] font-bold text-red-700 mt-1';
        cellLbl.innerText = 'Deflated / Collapsed Cells';
      }

      // Render Hexagonal Cells
      renderMesophyllCells(rwc >= 80.0);
    }

    function renderMesophyllCells(isTurgid) {
      const svg = document.getElementById('svg-cells');
      if (!svg) return;
      svg.innerHTML = '';

      const cellColor = isTurgid ? '#15803d' : '#b45309';
      const cellFill = isTurgid ? 'rgba(34, 197, 94, 0.35)' : 'rgba(217, 119, 6, 0.25)';
      const r = isTurgid ? 15 : 10; // Plump vs shrunken

      const centers = [
        [35, 30], [70, 30], [105, 30],
        [52, 60], [87, 60]
      ];

      centers.forEach(([cx, cy]) => {
        let pts = '';
        for (let a = 0; a < 6; a++) {
          const angle = (Math.PI / 3) * a;
          const px = cx + r * Math.cos(angle);
          const py = cy + r * Math.sin(angle);
          pts += (a === 0 ? `${px},${py}` : ` ${px},${py}`);
        }
        svg.innerHTML += `<polygon points="${pts}" fill="${cellFill}" stroke="${cellColor}" stroke-width="1.8"/>`;
        // Central vacuole
        const vacR = isTurgid ? 6 : 2;
        svg.innerHTML += `<circle cx="${cx}" cy="${cy}" r="${vacR}" fill="${cellColor}" opacity="0.6"/>`;
      });
    }

    // ========================================================================
    // MODULE 3: 21-Plot Field Map & Logbook
    // ========================================================================
    function setHeatmapMetric(metric) {
      currentHeatmapMetric = metric;
      const metrics = ['irrigation_mm', 'water_productivity_kg_m3', 'grain_yield_tha', 'proline_umol_g'];
      metrics.forEach(m => {
        const btn = document.getElementById('btn-heat-' + (m === 'irrigation_mm' ? 'irr' : (m === 'water_productivity_kg_m3' ? 'wp' : (m === 'grain_yield_tha' ? 'yield' : 'proline'))));
        if (btn) {
          btn.className = (m === metric) ?
            'px-2.5 py-1 text-xs font-semibold bg-stone-900 text-white rounded' :
            'px-2.5 py-1 text-xs font-semibold bg-white text-stone-800 hover:bg-stone-100 rounded border border-stone-300';
        }
      });

      // Update Legend Labels
      const vals = ALL_PLOTS.map(p => p[metric]);
      const minV = Math.min(...vals), maxV = Math.max(...vals);
      document.getElementById('legend-min-lbl').innerText = minV.toFixed(2);
      document.getElementById('legend-max-lbl').innerText = maxV.toFixed(2);

      populatePlotsGrid();
    }

    function getHeatmapColor(val, minV, maxV) {
      const norm = Math.max(0, Math.min(1, (val - minV) / (maxV - minV || 1)));
      if (currentHeatmapMetric === 'irrigation_mm') {
        // Less is better (green for low, red for high)
        const g = Math.round(220 * (1 - norm) + 40);
        const r = Math.round(220 * norm + 35);
        return `rgba(${r}, ${g}, 80, 0.28)`;
      } else if (currentHeatmapMetric === 'proline_umol_g') {
        // Lower is baseline (green), higher is stress (red)
        return norm > 0.3 ? 'rgba(220, 38, 38, 0.35)' : 'rgba(34, 197, 94, 0.25)';
      } else {
        // Higher is better (WP, Yield)
        const g = Math.round(200 * norm + 45);
        const b = Math.round(180 * (1 - norm) + 60);
        return `rgba(30, ${g}, ${b}, 0.32)`;
      }
    }

    function populatePlotsGrid() {
      const container = document.getElementById('plots-container');
      if (!container) return;
      container.innerHTML = '';

      const vals = ALL_PLOTS.map(p => p[currentHeatmapMetric]);
      const minV = Math.min(...vals), maxV = Math.max(...vals);

      const blocks = ['R1', 'R2', 'R3', 'R4', 'R5'];
      blocks.forEach(blk => {
        const blkRow = document.createElement('div');
        blkRow.className = 'space-y-1.5';

        const blkLabel = document.createElement('div');
        blkLabel.className = 'text-[11px] font-bold text-stone-500 uppercase tracking-wider flex justify-between';
        blkLabel.innerHTML = `<span>Block ${blk} (Replication)</span><span class="text-[10px] text-stone-400 font-normal">Plots randomized</span>`;
        blkRow.appendChild(blkLabel);

        const grid = document.createElement('div');
        grid.className = 'grid grid-cols-4 gap-2';

        const blkPlots = ALL_PLOTS.filter(p => p.block === blk);
        blkPlots.forEach(p => {
          const card = document.createElement('div');
          const isSelected = p.plot_id === selectedPlotId;
          const bgCol = getHeatmapColor(p[currentHeatmapMetric], minV, maxV);

          const trtTag = {
            'T1': 'text-red-700 bg-red-100',
            'T2': 'text-blue-700 bg-blue-100',
            'T3': 'text-emerald-700 bg-emerald-100',
            'T4': 'text-purple-700 bg-purple-100'
          };

          card.className = `cursor-pointer p-2.5 rounded-lg border transition ${isSelected ? 'ring-2 ring-stone-900 border-stone-900 shadow-sm' : 'border-stone-200 hover:border-stone-400'}`;
          card.style.backgroundColor = bgCol;
          card.onclick = () => selectPlot(p.plot_id);

          const metricVal = p[currentHeatmapMetric].toFixed(2);
          card.innerHTML = `
            <div class="flex justify-between items-center mb-1">
              <span class="text-xs font-bold text-stone-900">Plot #${p.plot_id}</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded ${trtTag[p.treatment]}">${p.treatment}</span>
            </div>
            <div class="text-[11px] flex justify-between items-baseline mt-1">
              <span class="text-stone-500 text-[10px]">Val:</span>
              <strong class="text-stone-900 table-numeric font-bold">${metricVal}</strong>
            </div>
          `;
          grid.appendChild(card);
        });

        blkRow.appendChild(grid);
        container.appendChild(blkRow);
      });

      // Render Validation Plot 21
      renderValidationPlot21Card();
    }

    function renderValidationPlot21Card() {
      const p21Container = document.getElementById('plot21-card-container');
      if (!p21Container) return;

      const p21 = ALL_PLOTS.find(p => p.plot_id === 21);
      if (!p21) return;

      const isSelected = selectedPlotId === 21;
      p21Container.innerHTML = `
        <div class="p-3 rounded-xl border-2 ${plot21Spotlight ? 'border-amber-400 star-glow bg-amber-50/70' : 'border-stone-300 bg-stone-100'} cursor-pointer transition ${isSelected ? 'ring-2 ring-amber-600' : ''}"
             onclick="selectPlot(21)">
          <div class="flex justify-between items-center">
            <div class="flex items-center space-x-2">
              <span class="text-xs font-black text-amber-900">⭐ Independent Validation Plot #21</span>
              <span class="px-2 py-0.2 rounded text-[10px] font-bold bg-amber-200 text-amber-900">Calibrated -15 cm AWD</span>
            </div>
            <span class="text-xs font-bold text-stone-800">WP: ${p21.water_productivity_kg_m3.toFixed(2)} kg/m³</span>
          </div>
          <div class="text-[11px] text-stone-600 mt-1 flex justify-between">
            <span>Irrigation: <strong>${p21.irrigation_mm.toFixed(1)} mm (27.0% saved)</strong></span>
            <span>Grain Yield: <strong>${p21.grain_yield_tha.toFixed(2)} t/ha</strong></span>
            <span>Proline: <strong>${p21.proline_umol_g.toFixed(2)} µmol/g</strong></span>
          </div>
        </div>
      `;
    }

    function togglePlot21Spotlight() {
      plot21Spotlight = !plot21Spotlight;
      const btn = document.getElementById('btn-spotlight');
      btn.className = plot21Spotlight ?
        'inline-flex items-center px-3 py-1.5 rounded-md text-xs font-bold bg-amber-500 text-white shadow-sm transition' :
        'inline-flex items-center px-3 py-1.5 rounded-md text-xs font-bold bg-amber-100 hover:bg-amber-200 text-amber-900 border border-amber-300 transition';

      const boxP21 = document.getElementById('box-plot21-spotlight-summary');
      if (boxP21) boxP21.classList.toggle('hidden', !plot21Spotlight);

      selectPlot(21);
      renderValidationPlot21Card();
    }

    function selectPlot(plotId) {
      selectedPlotId = plotId;
      const plot = ALL_PLOTS.find(p => p.plot_id === plotId);
      if (!plot) return;

      document.getElementById('tel-title').innerText = `Plot #${plot.plot_id} (${plot.block})`;
      document.getElementById('tel-badge-trt').innerText = `${plot.treatment}: ${plot.treatment_name}`;
      document.getElementById('tel-wp').innerText = `${plot.water_productivity_kg_m3.toFixed(2)} kg/m³`;
      document.getElementById('tel-irr').innerText = `${plot.irrigation_mm.toFixed(1)} mm`;
      document.getElementById('tel-sav').innerText = `${plot.water_savings_pct.toFixed(1)}% vs T1`;
      document.getElementById('tel-yield').innerText = `${plot.grain_yield_tha.toFixed(2)} t/ha`;
      document.getElementById('tel-tillers').innerText = `${plot.effective_tillers_hill.toFixed(1)} / hill`;
      document.getElementById('tel-pan').innerText = `${plot.panicle_length_cm.toFixed(1)} cm`;
      document.getElementById('tel-gw').innerText = `${plot.test_weight_1000_g.toFixed(2)} g`;
      document.getElementById('tel-hi').innerText = `${plot.harvest_index_pct.toFixed(1)}%`;
      document.getElementById('tel-rwc').innerText = `${plot.rwc_pct.toFixed(1)}%`;
      document.getElementById('tel-proline').innerText = `${plot.proline_umol_g.toFixed(2)} µmol/g`;

      renderMiniSawtooth(plot.treatment);
      populatePlotsGrid();
    }

    function renderMiniSawtooth(trt) {
      const svg = document.getElementById('tel-mini-sawtooth');
      if (!svg) return;
      svg.innerHTML = '';

      const colKey = trt === 'T1' ? 't1_z_cm' : (trt === 'T2' ? 't2_z_cm' : (trt === 'T3' ? 't3_z_cm' : 't4_z_cm'));
      const w = 300, h = 80;
      const mapX = day => (day / 110) * w;
      const mapY = z => 20 + ((6.5 - z) / 24.5) * 55;

      // Surface line (z=0)
      const surfY = mapY(0);
      svg.innerHTML += `<line x1="0" y1="${surfY}" x2="${w}" y2="${surfY}" stroke="#cbd5e1" stroke-width="1"/>`;

      // Flowering Shading (Days 58-72)
      const fX1 = mapX(58), fX2 = mapX(72);
      svg.innerHTML += `<rect x="${fX1}" y="0" width="${fX2 - fX1}" height="${h}" fill="rgba(245, 158, 11, 0.18)"/>`;

      // Path
      let pathD = '';
      DAILY_DATA.forEach((d, idx) => {
        const px = mapX(d.day);
        const py = mapY(d[colKey]);
        pathD += (idx === 0 ? `M ${px} ${py}` : ` L ${px} ${py}`);
      });

      const strokeCol = trt === 'T1' ? '#b91c1c' : (trt === 'T2' ? '#1d4ed8' : (trt === 'T3' ? '#15803d' : '#7e22ce'));
      svg.innerHTML += `<path d="${pathD}" fill="none" stroke="${strokeCol}" stroke-width="1.8"/>`;
    }

    // ========================================================================
    // MODULE 4: 110-Day Crop Phenology & Guardrail
    // ========================================================================
    function onPhenologyScrub(day) {
      document.getElementById('lbl-scrub-day').innerText = `Day ${day} after Transplanting`;
      const stageLbl = document.getElementById('lbl-scrub-stage');
      const badgeGuard = document.getElementById('badge-guardrail');
      const bannerGuard = document.getElementById('banner-flowering-alert');

      if (day <= 15) {
        stageLbl.innerText = 'Seedling Establishment (Kc = 1.05)';
        badgeGuard.className = 'px-2.5 py-1 rounded text-xs font-semibold bg-stone-100 text-stone-700 border border-stone-300';
        badgeGuard.innerText = 'Guardrail: Standby';
        bannerGuard.className = 'hidden';
      } else if (day <= 42) {
        stageLbl.innerText = 'Active Vegetative Tillering (Kc = 1.15) — AWD Active';
        badgeGuard.className = 'px-2.5 py-1 rounded text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-300';
        badgeGuard.innerText = 'AWD Cycles Active (-15 cm)';
        bannerGuard.className = 'hidden';
      } else if (day <= 57) {
        stageLbl.innerText = 'Panicle Initiation & Booting (Kc = 1.20)';
        badgeGuard.className = 'px-2.5 py-1 rounded text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-300';
        badgeGuard.innerText = 'AWD Cycles Active (-15 cm)';
        bannerGuard.className = 'hidden';
      } else if (day <= 72) {
        stageLbl.innerText = 'Critical Flowering & Anthesis (Kc = 1.25) — GUARDRAIL ENGAGED';
        badgeGuard.className = 'px-2.5 py-1 rounded text-xs font-bold bg-amber-500 text-white shadow-xs';
        badgeGuard.innerText = '🛡️ FLOWERING GUARDRAIL ACTIVE';
        bannerGuard.className = 'p-4 bg-amber-50 border border-amber-300 rounded-lg text-xs text-amber-950 space-y-1 block';
      } else if (day <= 100) {
        stageLbl.innerText = 'Grain Filling & Milk/Dough Stage (Kc = 1.00 -> 0.90)';
        badgeGuard.className = 'px-2.5 py-1 rounded text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-300';
        badgeGuard.innerText = 'AWD Cycles Resumed';
        bannerGuard.className = 'hidden';
      } else {
        stageLbl.innerText = 'Terminal Ripening Drainage (Kc = 0.85) — Field Dried';
        badgeGuard.className = 'px-2.5 py-1 rounded text-xs font-semibold bg-stone-200 text-stone-800 border border-stone-400';
        badgeGuard.innerText = 'Terminal Harvest Drainage';
        bannerGuard.className = 'hidden';
      }

      // Display Water Table for scrubbed day
      const dayData = DAILY_DATA.find(d => d.day === day) || DAILY_DATA[0];
      document.getElementById('pheno-t1-z').innerText = (dayData.t1_z_cm > 0 ? '+' : '') + dayData.t1_z_cm.toFixed(1) + ' cm';
      document.getElementById('pheno-t2-z').innerText = (dayData.t2_z_cm > 0 ? '+' : '') + dayData.t2_z_cm.toFixed(1) + ' cm';
      document.getElementById('pheno-t3-z').innerText = (dayData.t3_z_cm > 0 ? '+' : '') + dayData.t3_z_cm.toFixed(1) + ' cm';
      document.getElementById('pheno-t4-z').innerText = (dayData.t4_z_cm > 0 ? '+' : '') + dayData.t4_z_cm.toFixed(1) + ' cm';
    }

    // ========================================================================
    // MODULE 5: Sensor Calibration & Extension
    // ========================================================================
    function renderCalibrationCurve() {
      const svg = document.getElementById('svg-calibration');
      if (!svg) return;
      svg.innerHTML = '';

      const w = 320, h = 200, padX = 40, padY = 20;
      const plotW = w - padX - 20, plotH = h - padY - 30;

      // Axes
      svg.innerHTML += `<line x1="${padX}" y1="${padY + plotH}" x2="${padX + plotW}" y2="${padY + plotH}" stroke="#94a3b8" stroke-width="1.2"/>`;
      svg.innerHTML += `<line x1="${padX}" y1="${padY}" x2="${padX}" y2="${padY + plotH}" stroke="#94a3b8" stroke-width="1.2"/>`;

      // Labels
      svg.innerHTML += `<text x="${padX + plotW / 2}" y="${h - 6}" font-size="9" fill="#475569" text-anchor="middle" font-weight="bold">Sensor Output Voltage (V)</text>`;
      svg.innerHTML += `<text x="12" y="${padY + plotH / 2}" font-size="9" fill="#475569" text-anchor="middle" transform="rotate(-90, 12, ${padY + plotH / 2})" font-weight="bold">θv (%)</text>`;

      // Calibration Curve: Voltage (1.2V at 48.5% to 2.8V at 20%)
      const mapV = v => padX + ((v - 1.0) / 2.0) * plotW;
      const mapTh = th => padY + plotH - ((th - 15.0) / 35.0) * plotH;

      let curveD = '';
      for (let th = 18; th <= 48.5; th += 1) {
        // Inverse calibration relation
        const v = 3.0 - (th / 48.5) * 1.6;
        const px = mapV(v), py = mapTh(th);
        curveD += (th === 18 ? `M ${px} ${py}` : ` L ${px} ${py}`);
      }
      svg.innerHTML += `<path d="${curveD}" fill="none" stroke="#7e22ce" stroke-width="2"/>`;

      // Operating Point Star at -15 cm (θv = 39.2%, V = 1.82V)
      const opX = mapV(1.82), opY = mapTh(39.2);
      svg.innerHTML += `<circle cx="${opX}" cy="${opY}" r="5" fill="#f59e0b" stroke="#78350f" stroke-width="1.5"/>`;
      svg.innerHTML += `<text x="${opX + 8}" y="${opY - 4}" font-size="8" fill="#7e22ce" font-weight="bold">-15 cm Trigger (1.82 V)</text>`;
    }

    function simulateDryingCycle() {
      if (dryingInterval) clearInterval(dryingInterval);
      const btn = document.getElementById('btn-sim-drying');
      btn.innerText = '⏳ Simulating Drying...';

      let step = 0;
      const cycleSteps = [
        { z: 3.0, v: 1.25, th: 48.5 },
        { z: -2.0, v: 1.42, th: 46.2 },
        { z: -7.0, v: 1.58, th: 43.8 },
        { z: -11.0, v: 1.70, th: 41.5 },
        { z: -15.0, v: 1.82, th: 39.2 }
      ];

      dryingInterval = setInterval(() => {
        if (step >= cycleSteps.length) {
          clearInterval(dryingInterval);
          btn.innerText = '▶ Simulate 5-Day Drying Cycle';
          return;
        }
        const s = cycleSteps[step];
        document.getElementById('cal-z').innerText = (s.z > 0 ? '+' : '') + s.z.toFixed(1) + ' cm';
        document.getElementById('cal-v').innerText = s.v.toFixed(2) + ' V';
        document.getElementById('cal-theta').innerText = s.th.toFixed(1) + '%';
        step++;
      }, 700);
    }

    function calculateSavings() {
      const areaVal = parseFloat(document.getElementById('input-area').value) || 0;
      const unit = document.getElementById('select-unit').value;
      const pumpType = document.querySelector('input[name="pumpType"]:checked').value;

      let ha = areaVal;
      if (unit === 'bigha') ha = areaVal / 7.475;
      else if (unit === 'katha') ha = areaVal / (7.475 * 20.0);
      else if (unit === 'acre') ha = areaVal / 2.47105;

      const m3PerHa = 1845.0; // T4 savings vs T1
      const totalM3 = m3PerHa * ha;
      const totalLitres = totalM3 * 1000.0;

      document.getElementById('out-water-litres').innerText = Math.round(totalLitres).toLocaleString();
      document.getElementById('out-water-m3').innerText = `(${totalM3.toFixed(1)} m³ preserved)`;

      if (pumpType === 'electric') {
        const kwhSaved = totalM3 * 0.35;
        const inrSaved = kwhSaved * 3.50;
        document.getElementById('out-cost-inr').innerText = '₹' + Math.round(inrSaved).toLocaleString();
        document.getElementById('out-energy-saved').innerText = `${kwhSaved.toFixed(1)} kWh electricity saved`;
      } else {
        const dieselSaved = totalM3 * 0.28;
        const inrSaved = dieselSaved * 92.50;
        document.getElementById('out-cost-inr').innerText = '₹' + Math.round(inrSaved).toLocaleString();
        document.getElementById('out-energy-saved').innerText = `${dieselSaved.toFixed(1)} Litres diesel saved`;
      }

      // Methane Reduction
      const ch4Kg = (135.0 * ha).toFixed(1);
      const co2e = (3.78 * ha).toFixed(2);
      document.getElementById('out-methane').innerHTML = `
        Periodic soil aeration cuts methanogenesis by <strong>45%</strong>: saving <strong>${ch4Kg} kg CH₄</strong> (~${co2e} tonnes CO₂e carbon reduction on your land).
      `;
    }

    // ========================================================================
    // MODULE 6: Judge's Challenge & Statistical Synthesis
    // ========================================================================
    function onJudgeSliderInput(depth) {
      document.getElementById('judge-slider-depth').value = depth;
      document.getElementById('judge-chosen-lbl').innerText = (depth > 0 ? '+' : '') + depth.toFixed(1) + ' cm';
      runJudgeSimulation();
    }

    function runJudgeSimulation() {
      const depth = parseInt(document.getElementById('judge-slider-depth').value);
      const sweepPt = SWEEP_DATA.find(pt => Math.abs(pt.threshold_cm - depth) < 0.5) || SWEEP_DATA[15];

      document.getElementById('judge-score-sav').innerText = sweepPt.water_saved_pct.toFixed(1) + '%';
      document.getElementById('judge-score-irr').innerText = sweepPt.irrigation_mm.toFixed(1) + ' mm seasonal';
      document.getElementById('judge-score-yield').innerText = sweepPt.grain_yield_tha.toFixed(2) + ' t/ha';
      document.getElementById('judge-score-loss').innerText = sweepPt.yield_loss_pct > 0.5 ?
        `${sweepPt.yield_loss_pct.toFixed(1)}% yield loss` : '0.0% loss (Parity)';
      document.getElementById('judge-score-wp').innerText = sweepPt.water_productivity_kg_m3.toFixed(2) + ' kg/m³';
      document.getElementById('judge-score-rwc').innerText = sweepPt.rwc_pct.toFixed(1) + '%';
      document.getElementById('judge-score-pro').innerText = sweepPt.proline_umol_g.toFixed(2);

      const fringeLbl = document.getElementById('judge-score-fringe');
      const verdict = document.getElementById('judge-verdict-card');

      if (depth >= -10) {
        fringeLbl.className = 'text-sm font-bold text-blue-700 block mt-1';
        fringeLbl.innerText = 'Saturated / Over-Irrigated';
        verdict.className = 'p-4 bg-blue-50 border border-blue-200 rounded-lg text-xs space-y-1 text-blue-950';
        verdict.innerHTML = `
          <div class="font-bold text-sm">SUB-OPTIMAL WATER PRODUCTIVITY</div>
          <p class="leading-relaxed text-[11px]">
            At <strong>${depth} cm</strong>, plant hydration is completely safe, but <strong>12% to 20% more groundwater</strong> is lost through deep percolation head. Water Productivity remains low (~1.00 to 1.15 kg/m³).
          </p>
        `;
      } else if (depth >= -16) {
        fringeLbl.className = 'text-sm font-bold text-emerald-700 block mt-1';
        fringeLbl.innerText = 'BIOPHYSICAL SWEET SPOT';
        verdict.className = 'p-4 bg-emerald-50 border border-emerald-300 rounded-lg text-xs space-y-1 text-emerald-950';
        verdict.innerHTML = `
          <div class="font-bold text-sm">GLOBAL BIOPHYSICAL OPTIMUM (-15 cm)</div>
          <p class="leading-relaxed text-[11px]">
            At <strong>${depth} cm</strong>, Water Productivity peaks at <strong>${sweepPt.water_productivity_kg_m3.toFixed(2)} kg/m³</strong> (+39% vs T1) with <strong>${sweepPt.water_saved_pct.toFixed(1)}% water saved</strong>, zero grain yield loss, and baseline proline (${sweepPt.proline_umol_g.toFixed(2)} µmol/g FW).
          </p>
        `;
      } else {
        fringeLbl.className = 'text-sm font-bold text-red-700 block mt-1 animate-pulse';
        fringeLbl.innerText = 'Capillary Rupture / Stress';
        verdict.className = 'p-4 bg-red-50 border border-red-300 rounded-lg text-xs space-y-1 text-red-950';
        verdict.innerHTML = `
          <div class="font-bold text-sm">SEVERE HYDRAULIC DISCONNECTION CLIFF</div>
          <p class="leading-relaxed text-[11px]">
            At <strong>${depth} cm</strong>, capillary continuity ruptures. Free proline surges to <strong>${sweepPt.proline_umol_g.toFixed(2)} µmol/g FW</strong> (> 300% osmotic shock), and grain yield collapses by <strong>${sweepPt.yield_loss_pct.toFixed(1)}%</strong> due to spikelet sterility.
          </p>
        `;
      }

      renderParetoCurve(depth);
    }

    function renderParetoCurve(judgeDepth = -15) {
      const svg = document.getElementById('svg-pareto');
      if (!svg) return;
      svg.innerHTML = '';

      const w = 520, h = 280, padX = 55, padY = 25;
      const plotW = w - padX - 55, plotH = h - padY - 35;

      const mapX = th => padX + (Math.abs(th) / 30.0) * plotW;
      const mapWP = wp => padY + plotH - ((wp - 0.7) / 0.8) * plotH;
      const mapPro = pro => padY + plotH - ((pro - 1.5) / 10.5) * plotH;

      // Axes & Grid
      svg.innerHTML += `<line x1="${padX}" y1="${padY + plotH}" x2="${padX + plotW}" y2="${padY + plotH}" stroke="#94a3b8" stroke-width="1.2"/>`;
      svg.innerHTML += `<line x1="${padX}" y1="${padY}" x2="${padX}" y2="${padY + plotH}" stroke="#94a3b8" stroke-width="1.2"/>`;
      svg.innerHTML += `<line x1="${padX + plotW}" y1="${padY}" x2="${padX + plotW}" y2="${padY + plotH}" stroke="#94a3b8" stroke-width="1.2"/>`;

      // Labels
      svg.innerHTML += `<text x="${padX + plotW / 2}" y="${h - 6}" font-size="9" fill="#334155" text-anchor="middle" font-weight="bold">AWD Reflood Trigger Depth (-cm below surface)</text>`;
      svg.innerHTML += `<text x="16" y="${padY + plotH / 2}" font-size="9" fill="#15803d" text-anchor="middle" transform="rotate(-90, 16, ${padY + plotH / 2})" font-weight="bold">Water Productivity (kg/m³)</text>`;
      svg.innerHTML += `<text x="${w - 12}" y="${padY + plotH / 2}" font-size="9" fill="#b91c1c" text-anchor="middle" transform="rotate(90, ${w - 12}, ${padY + plotH / 2})" font-weight="bold">Free Proline (µmol/g FW)</text>`;

      // Boundary Line at -15 cm
      const critX = mapX(-15.0);
      svg.innerHTML += `<line x1="${critX}" y1="${padY}" x2="${critX}" y2="${padY + plotH}" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="4,3"/>`;
      svg.innerHTML += `<text x="${critX}" y="${padY + 12}" font-size="8" fill="#b45309" text-anchor="middle" font-weight="bold">-15 cm Capillary Boundary</text>`;

      // Water Productivity Curve
      let wpPath = '';
      SWEEP_DATA.forEach((pt, i) => {
        const px = mapX(pt.threshold_cm);
        const py = mapWP(pt.water_productivity_kg_m3);
        wpPath += (i === 0 ? `M ${px} ${py}` : ` L ${px} ${py}`);
      });
      svg.innerHTML += `<path d="${wpPath}" fill="none" stroke="#15803d" stroke-width="2.4"/>`;

      // Proline Curve
      let proPath = '';
      SWEEP_DATA.forEach((pt, i) => {
        const px = mapX(pt.threshold_cm);
        const py = mapPro(pt.proline_umol_g);
        proPath += (i === 0 ? `M ${px} ${py}` : ` L ${px} ${py}`);
      });
      svg.innerHTML += `<path d="${proPath}" fill="none" stroke="#dc2626" stroke-width="2.0" stroke-dasharray="5,3"/>`;

      // Validation Plot 21 Star
      const p21X = mapX(-15.0), p21Y = mapWP(1.364);
      svg.innerHTML += `<polygon points="${p21X},${p21Y-8} ${p21X+2.5},${p21Y-2} ${p21X+8},${p21Y-2} ${p21X+3},${p21Y+2} ${p21X+5},${p21Y+8} ${p21X},${p21Y+4} ${p21X-5},${p21Y+8} ${p21X-3},${p21Y+2} ${p21X-8},${p21Y-2} ${p21X-2.5},${p21Y-2}" fill="#f59e0b" stroke="#78350f" stroke-width="1.2"/>`;

      // Judge Chosen Star
      const jSweep = SWEEP_DATA.find(pt => Math.abs(pt.threshold_cm - judgeDepth) < 0.5) || SWEEP_DATA[15];
      const jX = mapX(judgeDepth);
      const jY = mapWP(jSweep.water_productivity_kg_m3);

      svg.innerHTML += `
        <circle cx="${jX}" cy="${jY}" r="9" fill="none" stroke="#f59e0b" stroke-width="2" class="star-glow"/>
        <circle cx="${jX}" cy="${jY}" r="5" fill="#f59e0b"/>
        <text x="${jX}" y="${jY - 14}" font-size="8" fill="#78350f" text-anchor="middle" font-weight="bold">Judge: ${judgeDepth} cm</text>
      `;
    }

    function populateAnovaTable() {
      const tbody = document.getElementById('anova-table-body');
      if (!tbody) return;
      tbody.innerHTML = `
        <tr><td class="py-2.5 px-3 font-semibold text-stone-900">Seasonal Irrigation Water (mm)</td><td class="py-2.5 px-3 text-right table-numeric">659.90a</td><td class="py-2.5 px-3 text-right table-numeric">609.40b</td><td class="py-2.5 px-3 text-right table-numeric">501.74c</td><td class="py-2.5 px-3 text-right table-numeric">475.38d</td><td class="py-2.5 px-3 text-right table-numeric">0.584</td><td class="py-2.5 px-3 text-right table-numeric">1.80</td><td class="py-2.5 px-3 text-right table-numeric">30455.6</td><td class="py-2.5 px-3 font-bold text-red-700">** (P &lt; 0.001)</td></tr>
        <tr><td class="py-2.5 px-3 font-semibold text-stone-900">Grain Yield (t/ha)</td><td class="py-2.5 px-3 text-right table-numeric">6.59b</td><td class="py-2.5 px-3 text-right table-numeric">6.62a</td><td class="py-2.5 px-3 text-right table-numeric">6.55c</td><td class="py-2.5 px-3 text-right table-numeric">6.60b</td><td class="py-2.5 px-3 text-right table-numeric">0.006</td><td class="py-2.5 px-3 text-right table-numeric">0.02</td><td class="py-2.5 px-3 text-right table-numeric">24.8</td><td class="py-2.5 px-3 font-bold text-stone-900">** (Parity &lt; 1%)</td></tr>
        <tr><td class="py-2.5 px-3 font-semibold text-stone-900">Irrigation Water Productivity (kg/m³)</td><td class="py-2.5 px-3 text-right table-numeric">1.00d</td><td class="py-2.5 px-3 text-right table-numeric">1.09c</td><td class="py-2.5 px-3 text-right table-numeric">1.31b</td><td class="py-2.5 px-3 text-right table-numeric">1.39a</td><td class="py-2.5 px-3 text-right table-numeric">0.001</td><td class="py-2.5 px-3 text-right table-numeric">0.004</td><td class="py-2.5 px-3 text-right table-numeric">22769.9</td><td class="py-2.5 px-3 font-bold text-red-700">** (P &lt; 0.001)</td></tr>
        <tr><td class="py-2.5 px-3 font-semibold text-stone-900">Leaf Relative Water Content (RWC %)</td><td class="py-2.5 px-3 text-right table-numeric">84.43a</td><td class="py-2.5 px-3 text-right table-numeric">84.44a</td><td class="py-2.5 px-3 text-right table-numeric">84.33a</td><td class="py-2.5 px-3 text-right table-numeric">84.44a</td><td class="py-2.5 px-3 text-right table-numeric">0.085</td><td class="py-2.5 px-3 text-right text-stone-500 font-bold">NS</td><td class="py-2.5 px-3 text-right table-numeric">0.68</td><td class="py-2.5 px-3 font-bold text-emerald-700">NS (P = 0.58)</td></tr>
        <tr><td class="py-2.5 px-3 font-semibold text-stone-900">Leaf Chlorophyll Index (SPAD)</td><td class="py-2.5 px-3 text-right table-numeric">40.25a</td><td class="py-2.5 px-3 text-right table-numeric">40.28a</td><td class="py-2.5 px-3 text-right table-numeric">40.17a</td><td class="py-2.5 px-3 text-right table-numeric">40.28a</td><td class="py-2.5 px-3 text-right table-numeric">0.077</td><td class="py-2.5 px-3 text-right text-stone-500 font-bold">NS</td><td class="py-2.5 px-3 text-right table-numeric">1.80</td><td class="py-2.5 px-3 font-bold text-emerald-700">NS (P = 0.20)</td></tr>
        <tr><td class="py-2.5 px-3 font-semibold text-stone-900">Leaf Free Proline (µmol/g FW)</td><td class="py-2.5 px-3 text-right table-numeric">1.92a</td><td class="py-2.5 px-3 text-right table-numeric">1.92a</td><td class="py-2.5 px-3 text-right table-numeric">1.92a</td><td class="py-2.5 px-3 text-right table-numeric">1.95a</td><td class="py-2.5 px-3 text-right table-numeric">0.014</td><td class="py-2.5 px-3 text-right text-stone-500 font-bold">NS</td><td class="py-2.5 px-3 text-right table-numeric">0.28</td><td class="py-2.5 px-3 font-bold text-emerald-700">NS (P = 0.84)</td></tr>
        <tr><td class="py-2.5 px-3 font-semibold text-stone-900">Effective Tillers per Hill</td><td class="py-2.5 px-3 text-right table-numeric">13.88b</td><td class="py-2.5 px-3 text-right table-numeric">13.92b</td><td class="py-2.5 px-3 text-right table-numeric">14.56a</td><td class="py-2.5 px-3 text-right table-numeric">14.62a</td><td class="py-2.5 px-3 text-right table-numeric">0.080</td><td class="py-2.5 px-3 text-right table-numeric">0.25</td><td class="py-2.5 px-3 text-right table-numeric">28.5</td><td class="py-2.5 px-3 font-bold text-red-700">** (AWD Stimulus)</td></tr>
        <tr><td class="py-2.5 px-3 font-semibold text-stone-900">Plant Height at Harvest (cm)</td><td class="py-2.5 px-3 text-right table-numeric">100.56a</td><td class="py-2.5 px-3 text-right table-numeric">100.62a</td><td class="py-2.5 px-3 text-right table-numeric">100.44a</td><td class="py-2.5 px-3 text-right table-numeric">100.98a</td><td class="py-2.5 px-3 text-right table-numeric">0.255</td><td class="py-2.5 px-3 text-right text-stone-500 font-bold">NS</td><td class="py-2.5 px-3 text-right table-numeric">0.94</td><td class="py-2.5 px-3 font-bold text-stone-600">NS (P = 0.45)</td></tr>
      `;
    }

    // Window Init
    window.onload = function() {
      switchTab('cross_section');
      updateMetrics();
      startAnimation();
      populatePlotsGrid();
      selectPlot(4);
      calculateSavings();
      renderParetoCurve(-15);
      populateAnovaTable();
    };
  </script>
</body>
</html>
"""

    # Inject data into placeholders
    final_html = html_template.replace("/* %%PLOTS_DATA%% */", json_plots)
    final_html = final_html.replace("/* %%DAILY_DATA%% */", json_daily)
    final_html = final_html.replace("/* %%SWEEP_DATA%% */", json_sweep)

    out_path = os.path.join(DOCS_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Generated clean academic web application in: {out_path}")
    return out_path


if __name__ == "__main__":
    build_web_app()
