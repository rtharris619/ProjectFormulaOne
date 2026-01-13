import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta

import fastf1
import fastf1.plotting
from fastf1.core import Laps


def plot_results():
  fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None)

  session = fastf1.get_session(2021, 'Spanish Grand Prix', 'Q')
  session.load()

  drivers = pd.unique(session.laps['Driver'])

  fastest_laps = list()
  for driver in drivers:
    driver_fastest_lap = session.laps.pick_drivers(driver).pick_fastest()
    fastest_laps.append(driver_fastest_lap)
  
  laps = Laps(fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
  
  pole = laps.pick_fastest()
  laps['LapTimeDelta'] = laps['LapTime'] - pole['LapTime']

  print(laps[['Driver', 'LapTime', 'LapTimeDelta']])

  team_colors = list()
  for _, lap in laps.iterlaps():
    color = fastf1.plotting.get_team_color(lap['Team'], session=session)
    team_colors.append(color)

  _, ax = plt.subplots()
  ax.barh(laps.index, laps['LapTimeDelta'], color=team_colors, edgecolor='grey')
  ax.set_yticks(laps.index)
  ax.set_yticklabels(laps['Driver'])

  # show fastest at the top
  ax.invert_yaxis()

  ax.set_axisbelow(True)
  ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

  lap_time = strftimedelta(pole['LapTime'], '%m:%s.%ms')
  plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
               f"Fastest Lap: {lap_time} ({pole['Driver']})")
  plt.show()
