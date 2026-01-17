import matplotlib.pyplot as plt
import numpy as np
import fastf1


def rotate(xy, *, angle):
  rotation_matrix = np.array([
    [np.cos(angle), np.sin(angle)],
    [-np.sin(angle), np.cos(angle)]
  ])
  return np.matmul(xy, rotation_matrix)


def plot_track_map():
  session = fastf1.get_session(2023, 'Monza', 'Q')
  session.load()

  lap = session.laps.pick_fastest()
  position = lap.get_pos_data()

  circuit_info = session.get_circuit_info()

  track = position.loc[:, ('X', 'Y')].to_numpy()

  track_angle_radians = circuit_info.rotation / 180 * np.pi

  rotated_track = rotate(track, angle=track_angle_radians)
  plt.plot(rotated_track[:, 0], rotated_track[:, 1])

  # Plotting Corners
  offset_vector = [500, 0]

  for _, corner in circuit_info.corners.iterrows():
    text = f"{corner['Number']}{corner['Letter']}"
    offset_angle_radians = corner['Angle'] / 180 * np.pi
    offset_x, offset_y = rotate(offset_vector, angle=offset_angle_radians)
    text_x = corner['X'] + offset_x
    text_y = corner['Y'] + offset_y
    text_x, text_y = rotate([text_x, text_y], angle=track_angle_radians)
    track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle_radians)

    plt.scatter(text_x, text_y, color='grey', s=140)
    plt.plot([track_x, text_x], [track_y, text_y], color='grey')
    plt.text(text_x, text_y, text, va='center_baseline', ha='center', size='small', color='white')

  plt.title(session.event['Location'])
  plt.xticks([])
  plt.yticks([])
  plt.axis('equal')
  plt.show()
