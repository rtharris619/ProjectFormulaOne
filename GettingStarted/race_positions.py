import matplotlib.pyplot as plt
import fastf1.plotting


def plot_race_position_changes():
  fastf1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')

  # Bahrain Grand Prix
  session = fastf1.get_session(2023, 1, 'R')
  session.load(telemetry=False, weather=False)

  _, ax = plt.subplots(figsize=(8.0, 4.9))
  
  for driver in session.drivers:
    laps = session.laps.pick_drivers(driver)
    abbreviation = laps['Driver'].iloc[0]

    style = fastf1.plotting.get_driver_style(identifier=abbreviation, style=['color', 'linestyle'], session=session)
    ax.plot(laps['LapNumber'], laps['Position'], label=abbreviation, **style)

  ax.set_ylim([20.5, 0.5])
  ax.set_yticks([1, 5, 10, 15, 20])
  ax.set_xlabel('Lap')
  ax.set_ylabel('Position')

  ax.legend(bbox_to_anchor=(1.0, 1.02))

  plt.suptitle(f"{session.event.year} {session.event['EventName']} position changes during a Race")

  plt.tight_layout()
  plt.show()