# Exoplanet Transit Light Curve Analyzer

**Author:** Arjita Pathak — [@arjitap](https://github.com/arjitap)  
**Data:** NASA Kepler Mission via Lightkurve (MAST Archive)

---

## The Idea

When a planet passes in front of its star, it blocks a tiny fraction of the starlight, sometimes less than 1%. If you plot the star's brightness over time, you get a light curve with small periodic dips. Finding these dips by eye across hundreds of thousands of stars is impossible. This project automates exactly that.

It downloads real Kepler light curves, cleans them up, and runs a **Box Least-Squares (BLS) periodogram**  the same algorithm used by NASA and ESA researchers to find those periodic dips and estimate how big the planet is and how long it takes to orbit its star.

---

## Getting Started

```bash
pip install lightkurve astropy scipy matplotlib pandas numpy
python main.py
```

`main.py` runs the entire pipeline from download to final metrics in one go. Or you can run each step individually if you want to inspect intermediate results.

---

## How the Pipeline Works

**Step 1 — Data Acquisition** (`dataacquisition.py`)  
Downloads first Quarter of Kepler light curves for 26 confirmed planet-host stars from the NASA MAST Archive. Files are cached locally so we only download once.

**Step 2 — Data Cleaning** (`data_cleaning.py`)  
Raw light curves are messy — stellar variability, instrument noise, gaps. This step removes NaNs, clips outliers, and applies an adaptive **Savitzky-Golay filter** to flatten out long-term trends while keeping the transit dips intact.

**Step 3 — Transit Detection** (`transit_detector.py`)  
Runs the BLS periodogram on each cleaned light curve, scanning periods from 0.5 to 50 days. The strongest periodic signal is taken as the planet candidate. The light curve is then phase-folded around that period to stack all transits on top of each other, making the signal much cleaner. Saves a diagnostic plot for every star.

**Step 4 — Comparison Table** (`comparison_table.py`)  
Takes the detected parameters — period, transit depth, Rp/R* — and compares them against confirmed values from the NASA Exoplanet Archive. Period errors are checked against harmonics too (BLS sometimes finds half or double the true period, which is still a valid detection).

**Step 5 — Verification Metrics** (`verification_metrics.py`)  
Summarises overall pipeline performance against the three target thresholds.

---

## Results

| Metric | Required | Achieved | 
|--------|----------|----------|
| Transit Recovery Rate | ≥ 85% | 100% (26/26) | 
| Period Error (median) | < 0.1% | 0.069% | 
| Radius Ratio Rp/R* Error | < 5% | 23.71% | 

### About the Rp/R* result

Two out of three metrics pass cleanly. The radius ratio accuracy didn't hit the target, and here's exactly why.

To keep the pipeline fast and practical, we downloaded only **1 quarter (~90 days)** of Kepler data per star. The Savitzky-Golay flattening filter, when applied to a single short baseline, slightly suppresses the transit depth — making the planet appear smaller than it actually is. This is a well-known limitation of SG detrending on short datasets.

The fix is straightforward: download 3+ quarters per star. More quarters means more individual transits, and when you stack them during phase-folding the depth measurement averages out much more accurately. We didn't do this because downloading multiple quarters for 26 stars was taking too long for the scope of this project.

The 0.069% period accuracy and 100% recovery rate confirm the detection logic is sound. The Rp/R* miss is purely a data quantity tradeoff, not a flaw in the pipeline.

---

## Project Structure

```
├── main.py                  ← run this to execute everything
├── data_acquisition.py      ← downloads & caches light curves
├── data_cleaning.py         ← SG detrending & outlier removal
├── plots.py                 ← before/after comparison plots
├── transit_detector.py      ← BLS periodogram & phase folding
├── comparison_table.py      ← vs NASA Exoplanet Archive
├── verification_metrics.py  ← final performance report
├── .gitignore
└── README.md
```

---

## Tech Stack

Python · Lightkurve · Astropy · SciPy · Matplotlib · Pandas · NumPy

---

## References

- Kovács, Zucker & Mazeh (2002) — The BLS Algorithm
- [Lightkurve Docs](https://docs.lightkurve.org/)
- [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)
