import os
import sys

def run_step(step_name, module_func):
    print(f"\n{'='*60}")
    print(f"  STEP: {step_name}")
    print(f"{'='*60}")
    try:
        module_func()
        print(f"✅ {step_name} completed successfully.")
    except Exception as e:
        print(f"❌ {step_name} FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    from dataacquisition import download_all_curves
    from data_cleaning import clean_and_detrend_data
    from transit_detector import run_planet_search
    from comparison_table import build_comparison_table
    from verification_metrics import calculate_metrics

    run_step("1. Data Acquisition",     download_all_curves)
    run_step("2. Data Cleaning",        clean_and_detrend_data)
    run_step("3. Transit Detection",    run_planet_search)
    run_step("4. Comparison Table",     build_comparison_table)
    run_step("5. Verification Metrics", calculate_metrics)

    print("\n🎉 ALL STEPS COMPLETE! Check your output folders.")