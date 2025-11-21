

---

# **Maximum Covering Location Problem (MCLP) Optimization Framework**

📄 *Markdown Conversion of Your PDF*

---

## 📋 **Project Overview**

This project implements a modular Python framework to solve the **Maximum Covering Location Problem (MCLP)**.
The goal is to select a fixed number of facilities (**k**) to maximize the total covered demand within a radius **R**.

The framework benchmarks **constructive heuristics** against **metaheuristics**, showing trade-offs between runtime and solution quality.
It is based on formulations from **Cordeau, Furini & Ljubić (2019)**.

---

## 🎯 **Key Deliverables**

### **1. Constructive Heuristics**

Fast baseline algorithms such as:

* **Greedy** selection
* **Closest-Neighbor** (distance-based)

### **2. Metaheuristics**

Advanced optimization engines:

* **Multi-Start Local Search**
  Supports *1-flip* and *swap* moves.
* **Tabu Search**
  Includes short-term memory and aspiration criteria.

### **3. Experimental Suite**

Automated pipeline running **300+ experiments** to validate:

* performance
* stability
* statistical significance

---

## 📂 **Repository Structure**

```
.
├── config.yaml                  # Master configuration
├── requirements.txt             # Python dependencies
├── data/                        # Benchmark instances
│   ├── S1.json, S2.json         # Small (50 facilities)
│   ├── M1.json, M2.json         # Medium (100 facilities)
│   └── L1.json, L2.json         # Large (200 facilities)
├── src/                         # Algorithm implementations
│   ├── greedy.py
│   ├── closest_neighbor.py
│   ├── local_search.py
│   ├── tabu_search.py
│   └── run_mclp.py              # CLI driver
├── scripts/
│   ├── run_full_experiments.ps1 # Run 1–5 reproducibility protocol
│   ├── analyze_results.py
│   └── generate_client_assets.py
├── results/                     # All experimental output (CSV)
└── report/                      # Final report + visualizations
```

---

## 🚀 **Installation & Setup**

### **Prerequisites**

* Python **3.8+**
* Standard libraries:
  `numpy`, `pandas`, `matplotlib`, `seaborn`

### **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## 💻 **Usage Guide**

### **1. Reproduce the “Long Run” (Recommended)**

This replicates the full academic experiment suite (Run 1–5 protocol).
It executes:

* all algorithms
* all benchmark instances
* 10 random seeds each

```powershell
# Run from project root
.\scripts\run_full_experiments.ps1
```

**Duration:** ~3–4 hours depending on hardware
**Output:**

* timestamped CSV in `/results/`
* auto-generated analysis reports

---

### **2. Run a Single Algorithm**

#### **Run Tabu Search on Large Instance L1**

```bash
python src/run_mclp.py --instance data/L1.json --algorithm ts --seed 42
```

#### **Run Greedy Baseline**

```bash
python src/run_mclp.py --instance data/M1.json --algorithm greedy
```

---

If you want, I can also turn this into a README.md file with styling, emojis removed, or converted into a more academic tone.
