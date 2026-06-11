import lightkurve as lk
import os
import numpy as np

def clean_and_detrend_data():
    
    if not os.path.exists("cleaned_data"):
        os.makedirs("cleaned_data")
        print("Created cleaned_data directory.")

    # list of all raw files we downloaded
    raw_files = [f for f in os.listdir("raw_data") if f.endswith(".fits")]
    
    for file_name in raw_files:
        target_name = file_name.replace("_raw.fits", "")
        print(f"\nCleaning data for: {target_name}")
        
        try:
            
            lc = lk.read(f"raw_data/{file_name}")
            
            #Drop NaN (missing) values from time or flux columns
            lc = lc.remove_nans()
            
            cadence_days = float(np.median(np.diff(lc.time.value)))
            window_length = int(7.0 / cadence_days)  # 7-day window
            if window_length % 2 == 0:
                window_length += 1  # must be odd
            window_length = max(window_length, 301)  # minimum 101
            print(f"  Using window_length={window_length}")
            flattened_lc = lc.flatten(window_length=window_length)
            
            #Remove extreme outliers
            clean_lc = flattened_lc.remove_outliers(sigma_upper=5, sigma_lower=10)
            
            #Save the clean data tonew folder
            file_path = f"cleaned_data/{target_name}_clean.fits"
            clean_lc.to_fits(file_path, overwrite=True)
            print(f"Successfully cleaned and saved to {file_path}")
            
        except Exception as e:
            print(f"Error processing {target_name}: {e}")

if __name__ == "__main__":
    clean_and_detrend_data()