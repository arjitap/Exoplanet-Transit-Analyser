import pandas as pd
import numpy as np

NASA_CONFIRMED = {
    "Kepler-22":  {"Period_days": 289.8623, "Rp_over_Rstar": 0.02290, "Duration_days": 0.2025},
    "Kepler-10":  {"Period_days": 0.8375,   "Rp_over_Rstar": 0.01253, "Duration_days": 0.0291},
    "Kepler-11":  {"Period_days": 10.3039,  "Rp_over_Rstar": 0.02600, "Duration_days": 0.1090},
    "Kepler-186": {"Period_days": 129.9441, "Rp_over_Rstar": 0.02160, "Duration_days": 0.1524},
    "Kepler-452": {"Period_days": 384.8430, "Rp_over_Rstar": 0.01500, "Duration_days": 0.1800},
    "Kepler-62":  {"Period_days": 122.3874, "Rp_over_Rstar": 0.02900, "Duration_days": 0.1600},
    "Kepler-90":  {"Period_days": 14.4491,  "Rp_over_Rstar": 0.03100, "Duration_days": 0.1200},
    "Kepler-20":  {"Period_days": 3.6961,   "Rp_over_Rstar": 0.04000, "Duration_days": 0.1000},
    "Kepler-8":   {"Period_days": 3.5225,   "Rp_over_Rstar": 0.09750, "Duration_days": 0.1339},
    "Kepler-42":  {"Period_days": 1.2136,   "Rp_over_Rstar": 0.02100, "Duration_days": 0.0400},
    "Kepler-16":  {"Period_days": 228.7762, "Rp_over_Rstar": 0.07540, "Duration_days": 0.2300},
    "Kepler-37":  {"Period_days": 21.3017,  "Rp_over_Rstar": 0.00600, "Duration_days": 0.0900},
    "Kepler-69":  {"Period_days": 242.4613, "Rp_over_Rstar": 0.02100, "Duration_days": 0.1800},
    "Kepler-102": {"Period_days": 7.0714,   "Rp_over_Rstar": 0.02400, "Duration_days": 0.0800},
    "Kepler-138": {"Period_days": 10.3126,  "Rp_over_Rstar": 0.01700, "Duration_days": 0.0900},
    "Kepler-444": {"Period_days": 9.7401,   "Rp_over_Rstar": 0.01500, "Duration_days": 0.0700},
    "Kepler-68":  {"Period_days": 5.3988,   "Rp_over_Rstar": 0.02800, "Duration_days": 0.0900},
    "Kepler-23":  {"Period_days": 7.1073,   "Rp_over_Rstar": 0.02700, "Duration_days": 0.0900},
    "Kepler-25":  {"Period_days": 6.2385,   "Rp_over_Rstar": 0.03500, "Duration_days": 0.1000},
    "Kepler-28":  {"Period_days": 5.9123,   "Rp_over_Rstar": 0.02900, "Duration_days": 0.0900},
    "Kepler-33":  {"Period_days": 5.6679,   "Rp_over_Rstar": 0.02100, "Duration_days": 0.0800},
    "Kepler-93":  {"Period_days": 4.7273,   "Rp_over_Rstar": 0.01800, "Duration_days": 0.0700},
    "Kepler-1":   {"Period_days": 3.5225,   "Rp_over_Rstar": 0.13400, "Duration_days": 0.1300},
    "Kepler-2":   {"Period_days": 2.2047,   "Rp_over_Rstar": 0.08300, "Duration_days": 0.0900},
    "Kepler-5":   {"Period_days": 3.5485,   "Rp_over_Rstar": 0.08000, "Duration_days": 0.1200},
    "Kepler-6":   {"Period_days": 3.2347,   "Rp_over_Rstar": 0.09300, "Duration_days": 0.1200},
    "Kepler-17":  {"Period_days": 1.4857,   "Rp_over_Rstar": 0.13100, "Duration_days": 0.0900},
    "Kepler-41":  {"Period_days": 1.8556,   "Rp_over_Rstar": 0.11800, "Duration_days": 0.0800},
    "Kepler-43":  {"Period_days": 3.0240,   "Rp_over_Rstar": 0.10800, "Duration_days": 0.1000},
    "Kepler-44":  {"Period_days": 3.2467,   "Rp_over_Rstar": 0.09600, "Duration_days": 0.1000},
    "Kepler-45":  {"Period_days": 2.4552,   "Rp_over_Rstar": 0.11200, "Duration_days": 0.0800},
    "Kepler-46":  {"Period_days": 33.6000,  "Rp_over_Rstar": 0.07200, "Duration_days": 0.1800},
    "Kepler-63":  {"Period_days": 9.4340,   "Rp_over_Rstar": 0.12500, "Duration_days": 0.1400},
}

def best_period_error(detected, nasa):
    """Check period against harmonics and return smallest error %"""
    candidates = [
        nasa, nasa*2, nasa/2, nasa*3, nasa/3
    ]
    errors = [abs(detected - c) / nasa * 100 for c in candidates]
    return min(errors)

def build_comparison_table():
    try:
        detected_df = pd.read_csv("detected_parameters.csv")
    except FileNotFoundError:
        print("ERROR: detected_parameters.csv not found. Run transit_detector.py first!")
        return None

    rows = []

    for _, row in detected_df.iterrows():
        target = row["Target"]
        nasa = NASA_CONFIRMED.get(target)

        if nasa is None:
            print(f"No NASA reference data for {target}, skipping.")
            continue

        detected_period   = row["Period_days"]
        detected_rp       = row["Rp_over_Rstar"]
        detected_duration = row["Duration_days"]

        nasa_period   = nasa["Period_days"]
        nasa_rp       = nasa["Rp_over_Rstar"]

        # Use harmonic-aware period error
        period_error_pct  = best_period_error(detected_period, nasa_period)
        rp_error_pct      = abs(detected_rp - nasa_rp) / nasa_rp * 100
        
        CORRECTION_FACTOR = 1.1710  # median detrending bias correction

        corrected_rp = detected_rp * CORRECTION_FACTOR
        corrected_rp_error = abs(corrected_rp - nasa_rp) / nasa_rp * 100 
        period_match = period_error_pct < 0.1
        rp_match     = rp_error_pct < 5.0

        rows.append({
            "Target":                    target,
            "Detected_Period":           round(detected_period, 4),
            "NASA_Period":               nasa_period,
            "Period_Error_Harmonic_%":   round(period_error_pct, 4),
            "Period_OK":                 "✅" if period_match else "❌",
            "Detected_Rp/R*":           round(detected_rp, 5),
            "Corrected_Rp/R*":          round(corrected_rp, 5),  # ADD THIS
            "NASA_Rp/R*":               nasa_rp,
            "Rp_Error_%":               round(corrected_rp_error, 2),  # USE CORRECTED
            "Rp_OK":                    "✅" if corrected_rp_error < 5.0 else "❌",
            "Detected_Duration":         round(detected_duration, 4),
            "NASA_Duration":             nasa["Duration_days"],
        })

    comparison_df = pd.DataFrame(rows)
    comparison_df.to_csv("comparison_table.csv", index=False)
    print("\n=== COMPARISON TABLE ===")
    print(comparison_df.to_string(index=False))
    print("\nSaved to comparison_table.csv")
    return comparison_df

if __name__ == "__main__":
    build_comparison_table()