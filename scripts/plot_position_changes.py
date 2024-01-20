import fastf1
from fastf1 import plotting
import matplotlib.pyplot as plt

# Setup FastF1
fastf1.Cache.enable_cache('../cache')  # Set path to cache folder
plotting.setup_mpl()  # Set up matplotlib for FastF1

# Load the session data
year = 2021
grand_prix = 'Monaco'
session = 'R'
race = fastf1.get_session(year, grand_prix, session)
race.load()

# Prepare data for plottingso 
laps = race.laps
laps = laps.pick_accurate()  # Only consider laps with accurate timing data
driver_stints = laps[['Driver', 'Stint', 'LapNumber', 'Position']]

# Create the plot
fig, ax = plt.subplots()
for driver in driver_stints['Driver'].unique():
    driver_stints_driver = driver_stints[driver_stints['Driver'] == driver]
    for stint in driver_stints_driver['Stint'].unique():
        stint_laps = driver_stints_driver[driver_stints_driver['Stint'] == stint]
        ax.plot(stint_laps['LapNumber'], stint_laps['Position'], label=f'{driver} Stint {stint}')

# Customizing the plot
ax.set_title(f'Position Changes During {year} {grand_prix} GP')
ax.set_xlabel('Lap Number')
ax.set_ylabel('Position')
ax.invert_yaxis()  # Invert y-axis so that position 1 is at the top
ax.legend()

# Show the plot
plt.show()
