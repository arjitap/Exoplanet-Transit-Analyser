import lightkurve as lk
import matplotlib.pyplot as plt
import os
import pandas as pd

def run_planet_search():
    # Create a folder to save our final planet discovery plots
    if not os.path.exists("plots"):
        os.makedirs("plots")
        print("Created plots directory.")

    # Get the list of all our cleaned data files
    clean_files = [f for f in os.listdir("cleaned_data") if f.endswith(".fits")]
    
    # A list to store the parameters we find so we can make a table tomorrow
    extracted_parameters = []

    for file_name in clean_files:
        target_name = file_name.replace("_clean.fits", "")
        print(f"\nSearching for transits in: {target_name}")
        
        try:
            
            lc = lk.read(f"cleaned_data/{file_name}")
            
            #Run BLS to scan for periods between 0.5 and 15 days
            periodogram = lc.to_periodogram(method='bls', minimum_period=0.7, maximum_period=15.0)
            
            
            best_period = periodogram.period_at_max_power.value
            best_t0 = periodogram.transit_time_at_max_power.value
            best_duration = periodogram.duration_at_max_power.value
            best_depth = periodogram.depth_at_max_power.value
            
            print(f"-> Found Period: {best_period:.4f} days")
            print(f"-> Found Depth: {best_depth:.2e}")

            #Phase-fold the light curve around the discovered period
            folded_lc = lc.fold(period=best_period, epoch_time=best_t0)
            
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            
            # Left Plot: The BLS search spectrum (The highest peak shows the planet's period)
            periodogram.plot(ax=ax1, color='navy')
            ax1.set_title(f"{target_name} - BLS Period Search Spectrum")
            
            # Right Plot: The Phase-Folded Profile
            folded_lc.scatter(ax=ax2, color='darkred', s=2)
            ax2.set_xlim(-0.2, 0.2)  # Zoom in closely around the center of the transit
            ax2.set_title(f"{target_name} - Phase-Folded Transit Profile")
            
            
            plt.tight_layout()
            plot_path = f"plots/{target_name}_detection.png"
            plt.savefig(plot_path, dpi=150)
            plt.close()
            print(f"Saved diagnostic plots to {plot_path}")
            
            # Saving these numbers so we can build our final Pandas table 
            extracted_parameters.append({
                "Target": target_name,
                "Period_days": best_period,
                "Transit_Depth": best_depth,
                "Duration_days": best_duration
            })
            
        except Exception as e:
            print(f"Error analyzing {target_name}: {e}")

    # Save this data to a temporary CSV file
    df = pd.DataFrame(extracted_parameters)
    df.to_csv("detected_parameters.csv", index=False)
    print("\n=== BLS Search Complete! Parameters saved to detected_parameters.csv ===")

if __name__ == "__main__":
    run_planet_search()