import fastf1
import json

# Setup FastF1 and enable the cache
fastf1.Cache.enable_cache('../cache')  # Adjust the path as needed

# Load the session data
race = fastf1.get_session(2021, 'Monaco', 'R')
race.load()

# Pick a driver
driver = 'VER'
laps = race.laps.pick_driver(driver)

# Get the telemetry data for the fastest lap
fastest_lap = laps.pick_fastest()
telemetry = fastest_lap.get_telemetry()

# Process telemetry data for JSON
telemetry_data = telemetry[['Distance', 'Speed', 'nGear']].to_dict(orient='records')

# Serialize to JSON
json_data = json.dumps(telemetry_data, indent=4)

# Save to a file or return this data
with open('../data/fastest_lap_telemetry.json', 'w') as file:
    file.write(json_data)
