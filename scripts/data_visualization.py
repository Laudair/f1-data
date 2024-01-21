import sys
import json
import fastf1
from fastf1 import utils
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin
cred = credentials.Certificate('../api/f1-data-admin-sdk.json')  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://f1-data-6fee2-default-rtdb.asia-southeast1.firebasedatabase.app'  # Update this URL
})

def get_f1_data(year, race, driver):
    fastf1.Cache.enable_cache('../cache')  # Adjust the path as needed
    session = fastf1.get_session(year, race, 'R')
    session.load()
    laps = session.laps.pick_driver(driver)
    fastest_lap = laps.pick_fastest()
    telemetry = fastest_lap.get_telemetry()
    telemetry_data = {
        'Distance': list(telemetry['Distance']),
        'Speed': list(telemetry['Speed']),
        'Gear': list(telemetry['nGear'])
    }
    return telemetry_data

def upload_json_to_firebase(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    ref = db.reference(f'f1data/{Path(file_path).stem}')
    ref.set(data)

if __name__ == "__main__":
    year = int(sys.argv[1])
    race = sys.argv[2]
    driver = sys.argv[3]
    data = get_f1_data(year, race, driver)
    
    # Serialize data to JSON
    json_data = json.dumps(data, indent=4)

    # Ensure the cache directory exists
    cache_dir = Path('../cache')
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Write JSON data to a file in the cache directory
    cache_file_path = cache_dir / f'{year}_{race}_{driver}.json'
    with open(cache_file_path, 'w') as file:
        file.write(json_data)

    # Upload JSON data to Firebase
    upload_json_to_firebase(cache_file_path)
