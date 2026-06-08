import lightkurve as lk

def test_data_fetch(target_name):
    print(f"--- Searching NASA MAST Archive for {target_name} ---")
    
    # Search for Kepler light curves for the target
    search_result = lk.search_lightcurve(target_name, mission='Kepler')
    print(f"Found {len(search_result)} data files for {target_name}.")
    
    # Downloading just the first available quarter to test our connection
    if len(search_result) > 0:
        print(f"Downloading Quarter 1 data...")
        lc = search_result[0].download()
        print(f"Success! Data points fetched: {len(lc.time)}")
        return lc
    else:
        print("No data found.")
        return None

if __name__ == "__main__":
    # Using Kepler-22 because its a well known star and its the first star found by Kepler in the habitable zone.
    test_data_fetch("Kepler-22")
    

