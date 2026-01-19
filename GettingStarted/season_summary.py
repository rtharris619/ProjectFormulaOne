import pandas as pd
import plotly.graph_objects as go
from plotly.io import show
from plotly.subplots import make_subplots
import fastf1 as ff1


def plot_season_summary():
  season = 2024
  schedule = ff1.get_event_schedule(season, include_testing=False)

  standings = []
  short_event_names = []

  for _, event in schedule.iterrows():
    event_name, round_number = event["EventName"], event["RoundNumber"]
    short_event_names.append(event_name.replace("Grand Prix", "").strip())

    race = ff1.get_session(season, event_name, "R")
    race.load(laps=False, telemetry=False, weather=False, messages=False)

    sprint = None
    if event["EventFormat"] == "sprint_qualifying":
      sprint = ff1.get_session(season, event_name, "S")
      sprint.load(laps=False, telemetry=False, weather=False, messages=False)

    for _, driver in race.results.iterrows():
      abbreviation, race_points, race_position = (driver["Abbreviation"], driver["Points"], driver["Position"])

      sprint_points = 0
      if sprint is not None:
        driver = sprint.results[sprint.results["Abbreviation"] == abbreviation]
        if not driver.empty:
          sprint_points = driver["Points"].values[0]
      
      standings.append({
        "EventName": event_name,
        "RoundNumber": round_number,
        "Driver": abbreviation,
        "Points": race_points + sprint_points,
        "Position": race_position
      })

  df = pd.DataFrame(standings)

  heatmap_data = df.pivot(index="Driver", columns="RoundNumber", values="Points").fillna(0)

  heatmap_data["total_points"] = heatmap_data.sum(axis=1)
  heatmap_data = heatmap_data.sort_values(by="total_points", ascending=True)
  total_points = heatmap_data["total_points"].values
  heatmap_data = heatmap_data.drop(columns=["total_points"])

  position_data = df.pivot(index="Driver", columns="RoundNumber", values="Position").fillna("N/A")

  hover_info = [
    [
      {
        "position": position_data.at[driver, race]
      }
      for race in schedule["RoundNumber"]
    ]
    for driver in heatmap_data.index
  ]

  fig = make_subplots(rows=1, cols=2, column_widths=[0.85, 0.15], subplot_titles=(f"F1 {season} Season Summary", "Total Points"))
  fig.update_layout(width=900, height=800)

  fig.add_trace(
    go.Heatmap(
      x=short_event_names,
      y=heatmap_data.index,
      z=heatmap_data.values,
      text=heatmap_data.values,
      texttemplate="%{text}",
      textfont={"size": 12},
      customdata=hover_info,
      hovertemplate=(
        "Driver: %{y}<br>"
        "Race: %{x}<br>"
        "Points: %{z}<br>"
        "Position: %{customdata.position}<extra></extra>"
      ),
      colorscale="YlGnBu",
      showscale=False,
      zmin=0,
      zmax=heatmap_data.values.max(),
    ),
    row=1,
    col=1,
  )

  # Heatmap for total points
  fig.add_trace(
    go.Heatmap(
      x=["Total Points"] * len(total_points),
      y=heatmap_data.index,
      z=total_points,
      text=total_points,
      texttemplate="%{text}",
      textfont={"size": 12},
      colorscale="YlGnBu",
      showscale=False,
      zmin=0,
      zmax=total_points.max(),
    ),
    row=1,
    col=2,
  )
  
  show(fig)
