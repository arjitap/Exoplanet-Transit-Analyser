import lightkurve as lk
import os

# 26 Kepler mission stars 
TARGETS = [
    "Kepler-22", "Kepler-10", "Kepler-11", "Kepler-186", "Kepler-452",
    "Kepler-62", "Kepler-90", "Kepler-20", "Kepler-8", "Kepler-42",
    "Kepler-16", "Kepler-37", "Kepler-69", "Kepler-102", "Kepler-138",
    "Kepler-444", "Kepler-68", "Kepler-23", "Kepler-25", "Kepler-28",
    "Kepler-33", "Kepler-93", "Kepler-1", "Kepler-2", "Kepler-5", "Kepler-6"
]

def download_all_curves():
    if not os.path.exists("raw_data"):
        os.makedirs("raw_data")
        print("Created raw_data directory.")

    successful_downloads = 0

    for target in TARGETS:
        print(f"\nFetching data for: {target}")
        try:
            # Search specifically for Kepler mission data
            search = lk.search_lightcurve(target, mission="Kepler")
            if len(search) == 0:
                print(f"Skipping {target}: No data found in archive.")
                continue
                
            # Download the first available quarter
            lc = search[0].download()
            
            # Save locally as a fits file
            file_path = f"raw_data/{target}_raw.fits"
            lc.to_fits(file_path, overwrite=True)
            print(f"Saved {target} data to {file_path}")
            successful_downloads += 1
            
        except Exception as e:
            print(f"Error downloading {target}: {e}")
            
    print(f"\n=== DOWNLOAD COMPLETED ===")
    print(f"Successfully downloaded {successful_downloads} stars out of {len(TARGETS)}.")
    if successful_downloads >= 20:
        print("Verification Safe: We have met the target count requirement of >=20!")
    else:
        print("Warning: Still below 20 targets.")

if __name__ == "__main__":
    download_all_curves()