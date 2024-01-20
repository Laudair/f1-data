import fastf1
import matplotlib.pyplot as plt
from fastf1 import plotting

# Setup FastF1 and enable the cache
fastf1.Cache.enable_cache('../cache')

# Load the session data
race = fastf1.get_session(2021, 'Monaco', 'R')
race.load()

# Pick a driver (e.g., 'VER' for Max Verstappen)
driver = 'VER'
laps = race.laps.pick_driver(driver)

# Get the telemetry data for the fastest lap
fastest_lap = laps.pick_fastest()
telemetry = fastest_lap.get_telemetry()

# Plotting
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Distance (meters)')
ax1.set_ylabel('Speed (km/h)', color=color)
ax1.plot(telemetry['Distance'], telemetry['Speed'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Instantiate a second y-axis sharing the same x-axis
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Gear', color=color)
ax2.plot(telemetry['Distance'], telemetry['nGear'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Title and show plot
plt.title(f'Fastest Lap Telemetry for {driver} at 2021 Monaco GP')
fig.tight_layout()
plt.savefig('../data/fastest_lap_telemetry.png')
