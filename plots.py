import lightkurve as lk
import matplotlib.pyplot as plt
import os

def plot_before_after(target_name):
    raw_path = f"raw_data/{target_name}_raw.fits"
    clean_path = f"cleaned_data/{target_name}_clean.fits"
    
    if not os.path.exists(raw_path) or not os.path.exists(clean_path):
        print(f"Data files missing for {target_name}")
        return

    # Load both files
    lc_raw = lk.read(raw_path)
    lc_clean = lk.read(clean_path)

    # Setup side-by-side plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Plot 1: Raw data with all the stellar waves
    lc_raw.scatter(ax=ax1, color='firebrick', s=2)
    ax1.set_title(f"{target_name} - Raw Data (Stellar Variability)")

    # Plot 2: Cleaned data where the transit dips become crystal clear
    lc_clean.scatter(ax=ax2, color='darkred', s=2)
    ax2.set_title(f"{target_name} - Flattened Data (Ready for BLS)")

    
    plt.tight_layout()
    output_image = f"{target_name}_comparison.png"
    plt.savefig(output_image, dpi=150)
    print(f"Saved comparison plot to {output_image}")
    plt.close()

if __name__ == "__main__":
    # testing it on a known target like Kepler-10 or Kepler-22
    plot_before_after("Kepler-10")