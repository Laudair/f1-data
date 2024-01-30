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

def get_qualifying_results(year, race):
    fastf1.Cache.enable_cache('../cache')  # Adjust the path as needed
    qualifying = fastf1.get_session(year, race, 'Q')
    qualifying.load()
    return qualifying.results

def get_race_results(year, race):
    fastf1.Cache.enable_cache('../cache')  # Adjust the path as needed
    race_session = fastf1.get_session(year, race, 'R')
    race_session.load()
    return race_session.results

def upload_json_to_firebase(data, file_path):
    json_data = json.dumps(data, indent=4)
    cache_dir = Path('../cache')
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file_path = cache_dir / file_path
    with open(cache_file_path, 'w') as file:
        file.write(json_data)
    ref = db.reference(f'f1data/{Path(file_path).stem}')
    ref.set(data)

if __name__ == "__main__":
    year = int(sys.argv[1])
    race = sys.argv[2]

    qualifying_results = get_qualifying_results(year, race)
    race_results = get_race_results(year, race)
    race_winner = race_results.iloc[0]['Driver']

    combined_data = {
        'QualifyingResults': qualifying_results.to_dict(),
        'RaceResults': race_results.to_dict(),
        'RaceWinner': race_winner.to_dict()
    }

    upload_json_to_firebase(combined_data, f'{year}_{race}_results.json')
