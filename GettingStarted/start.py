import fastf1


def get_session_data():
  session = fastf1.get_session(2021, 7, 'Q')
  event = session.event
  # print(event)

  name = event['EventName']
  print(name)


def get_event():
  event = fastf1.get_event(2021, 7)
  race = event.get_race()
  print(race)


def get_event_by_name():
  event = fastf1.get_event(2021, 'Spain')
  print(event)


# (2021)
def get_event_schedule(year: int):
  schedule = fastf1.get_event_schedule(year)
  print(schedule)
  print(schedule['EventName'])


def get_event_by_round():
  schedule = fastf1.get_event_schedule(2021)
  round = schedule.get_event_by_round(12)
  print(round)


def get_session_results():
  session = fastf1.get_session(2021, 'French Grand Prix', 'Q')
  session.load()
  results = session.results
  print(results)

  columns = results.columns
  print(columns)


def get_session_top_ten():
  session = fastf1.get_session(2021, 'French Grand Prix', 'Q')
  session.load()
  results = session.results.iloc[0:10].loc[:, ['Abbreviation', 'TeamName', 'Q3']]
  print(results)


def get_session_laps():
  session = fastf1.get_session(2021, 'French Grand Prix', 'Q')
  session.load()
  laps = session.laps
  print(laps)

  print(laps.columns)


def get_fastest_lap():
  session = fastf1.get_session(2021, 'French Grand Prix', 'Q')
  session.load()
  fastest_lap = session.laps.pick_fastest()
  print(fastest_lap['Driver'], ' - ', fastest_lap['LapTime'])