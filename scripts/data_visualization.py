import sys
import json
import fastf1
from fastf1 import utils
from pathlib import Path

def get_f1_data(year, race, driver):
    # Setup FastF1
    fastf1.Cache.enable_cache('../cache')  # Adjust the path as needed

    # Load the session data
    session = fastf1.get_session(year, race, 'R')
    session.load()

    # Pick a driver
    laps = session.laps.pick_driver(driver)

    # Get the telemetry data for the fastest lap
    fastest_lap = laps.pick_fastest()
    telemetry = fastest_lap.get_telemetry()

    # Convert telemetry data to a dictionary for JSON serialization
    telemetry_data = {
        'Distance': list(telemetry['Distance']),
        'Speed': list(telemetry['Speed']),
        'Gear': list(telemetry['nGear'])
    }

    return telemetry_data

if __name__ == "__main__":
    # Parse command line arguments
    year = int(sys.argv[1])
    race = sys.argv[2]
    driver = sys.argv[3]

    # Get F1 data
    data = get_f1_data(year, race, driver)

    # Serialize data to JSON
    json_data = json.dumps(data, indent=4)

    # Ensure the cache directory exists
    Path('../cache').mkdir(parents=True, exist_ok=True)

    # Write JSON data to a file in the cache directory
    cache_file_path = f'../cache/{year}_{race}_{driver}.json'
    with open(cache_file_path, 'w') as file:
        file.write(json_data)
