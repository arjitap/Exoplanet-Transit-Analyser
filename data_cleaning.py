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
            
            #chanding the window length to 31 for short period transits
            flattened_lc = lc.flatten(window_length=101)
            
            #Remove extreme outliers
            clean_lc = flattened_lc.remove_outliers(sigma=5)
            
            #Save the clean data tonew folder
            file_path = f"cleaned_data/{target_name}_clean.fits"
            clean_lc.to_fits(file_path, overwrite=True)
            print(f"Successfully cleaned and saved to {file_path}")
            
        except Exception as e:
            print(f"Error processing {target_name}: {e}")

if __name__ == "__main__":
    clean_and_detrend_data()