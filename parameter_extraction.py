import pandas as pd
import numpy as np
import os

def compile_final_results():
    print("--- Parameter Extraction & Verification ---")
    
    if not os.path.exists("detected_parameters.csv"):
        print("Error: detected_parameters.csv not found. Please run transit_detector.py first.")
        return
    
    df = pd.read_csv("detected_parameters.csv")
    
    
    df["Target"] = df["Target"].astype(str).str.strip()

    # Physical Radius Ratio (Rp/R* = square root of transit depth)
    df["Radius_Ratio_Derived"] = np.sqrt(df["Transit_Depth"])
    df["Transit_Duration_Hours"] = df["Duration_days"] * 24.0

    # Reference catalog of true values from the NASA Archive

    nasa_truths = {
        "Kepler-10":  {"True_Period": 0.8375,  "True_Ratio": 0.0143},
        "Kepler-22":  {"True_Period": 289.862, "True_Ratio": 0.0192},
        "Kepler-8":   {"True_Period": 3.5225,  "True_Ratio": 0.0956},
        "WASP-12":    {"True_Period": 1.0914,  "True_Ratio": 0.1174},
        "HAT-P-7":    {"True_Period": 2.2047,  "True_Ratio": 0.0776},
        "Kepler-11":  {"True_Period": 10.3040, "True_Ratio": 0.0387},
        "Kepler-186": {"True_Period": 129.944, "True_Ratio": 0.0211},
        "Kepler-452": {"True_Period": 384.843, "True_Ratio": 0.0345}
    }
    
    df["NASA_True_Period"] = df["Target"].map(lambda x: nasa_truths.get(x, {}).get("True_Period", np.nan))
    df["NASA_True_Ratio"] = df["Target"].map(lambda x: nasa_truths.get(x, {}).get("True_Ratio", np.nan))
    
    # error percentages against the true values
    df["Period_Error_Pct"] = np.abs((df["Period_days"] - df["NASA_True_Period"]) / df["NASA_True_Period"]) * 100
    df["Radius_Error_Pct"] = np.abs((df["Radius_Ratio_Derived"] - df["NASA_True_Ratio"]) / df["NASA_True_Ratio"]) * 100

    
    final_cols = [
        "Target", "Period_days", "Transit_Duration_Hours", 
        "Radius_Ratio_Derived", "Period_Error_Pct", "Radius_Error_Pct"
    ]
    
    
    df[final_cols].to_csv("final_exoplanet_report.csv", index=False)
    
    print("\n======================= FINAL PARAMETER TABLE =======================")
    
    matched_results = df[df["NASA_True_Period"].notna()]
    
    with pd.option_context('display.float_format', '{:.6f}'.format):
        if len(matched_results) == 0:
            print("Warning: No targets matched your dictionary keys exactly.")
            print("Showing your derived parameters instead:")
            print(df[["Target", "Period_days", "Transit_Duration_Hours", "Radius_Ratio_Derived"]].to_string(index=False))
        else:
            print(matched_results[final_cols].to_string(index=False))
    print("=====================================================================")
    
    valid_periods = df["Period_Error_Pct"].dropna()
    valid_radii = df["Radius_Error_Pct"].dropna()
    
    if len(valid_periods) > 0:
        print(f"\nAverage Period Error: {valid_periods.mean():.4f}% (Target: < 0.1%)")
        print(f"Average Radius Ratio Error: {valid_radii.mean():.4f}% (Target: < 5.0%)")
        # print("Verification Status: ALL BENCHMARKS SUCCESSFULLY MET!")
    else:
        print("\nCould not calculate error averages because no baseline stars matched perfectly.")

if __name__ == "__main__":
    compile_final_results()