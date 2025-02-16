# Camera Distance and Resolution
#
# Author: Peter Jakubowski
# Date: 2/14/2025
# Description:
#


from typing import Literal
from numpy import floor
from fractions import Fraction
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines


def calculate_max_ppi(sensor, real_object_width, real_object_height):
    """

    :param sensor:
    :param real_object_width:
    :param real_object_height:
    :return:
    """

    sensor_ratio = sensor.sensor_w_px / sensor.sensor_h_px
    max_w_px = int(floor(sensor.sensor_w_px / real_object_width))
    max_h_px = int(floor(sensor.sensor_h_px / real_object_height))

    if real_object_width >= real_object_height * sensor_ratio:
        return max_w_px

    return max_h_px


def convert_units(measurement: float, unit: Literal["mm", "cm", "inches"] = "inches") -> tuple[float, float, float]:
    """
    Convert a measurement to mm, cm, and inches

    :param measurement: the measurement to convert
    :param unit: string unit of measurement, mm, cm, or in
    :return: tuple of measurement in mm, cm, and in
    """

    if unit == 'cm':
        measurement = measurement * 0.393701
    elif unit == 'mm':
        measurement = measurement * 0.0393701

    return measurement / .0393701, measurement / .393701, measurement


def print_measurements(measurements: tuple[float, float, float]) -> str:
    """
    Utility to format a string of measurements for printing

    Example output: "4088.9 mm / 408.89 cm / 160.98 in / 13 ft 4 49/50 in"

    :param measurements: tuple of measurements mm, cm, in
    :return: string
    """

    mm, cm, inches = measurements
    string = ""
    string += str(round(mm, 2)) + " mm / "
    string += str(round(cm, 2)) + " cm / "
    string += str(round(inches, 2)) + " in / "
    if inches // 12 > 0:
        string += str(int(inches // 12)) + " ft"
    if floor(inches % 12) > 0:
        string += " " + str(int(floor(inches % 12)))
    if round(inches - int(inches), 1) > 0:
        string += " " + str(Fraction(str(round(inches - int(inches), 2))))
    string += " in"

    return string


def plot_sensor_fit(sensor, object_w_on_film_mm, object_h_on_film_mm):
    """
    Plots the sensor and object fit using Matplotlib.

    Args:
        sensor: An object with sensor_w_mm and sensor_h_mm attributes
                representing the sensor width and height in millimeters.
        object_w_on_film_mm: The width of the object projected onto the sensor, in millimeters.
        object_h_on_film_mm: The height of the object projected onto the sensor, in millimeters.
    """

    # Create a figure and axes
    fig, ax = plt.subplots(1)  # creates the figure and assigns the axes to 'ax'

    # Calculate object position
    object_x = (sensor.sensor_w_mm / 2) - (object_w_on_film_mm / 2)
    object_y = (sensor.sensor_h_mm / 2) - (object_h_on_film_mm / 2)

    # Create sensor and object shapes
    sensor_shape = patches.Rectangle((0, 0), sensor.sensor_w_mm, sensor.sensor_h_mm, fc='lightblue', ec="red")
    object_shape = patches.Rectangle((object_x, object_y), object_w_on_film_mm, object_h_on_film_mm, fc='white', ec="blue")

    # Add the shapes to the axes
    ax.add_patch(sensor_shape)
    ax.add_patch(object_shape)

    # Set the title and axis scaling
    ax.set_title('Sensor Fit')
    ax.axis('scaled')  # Ensure correct aspect ratio

    # Set axis limits to view the whole sensor
    ax.set_xlim(0, sensor.sensor_w_mm)
    ax.set_ylim(0, sensor.sensor_h_mm)

    # Show the plot (optional if you are integrating with other code)
    # plt.show()

    return fig


def plot_lighting_diagram(real_object_width, real_object_height, radius_multiply, distance, max_w_in):
    """
    Plots the lighting diagram using Matplotlib.

    Args:

    """

    # Create a figure and axes
    fig, ax = plt.subplots(1)

    # Artwork rectangle
    artwork = patches.Rectangle(((-real_object_width / 2), -real_object_height),
                                real_object_width,
                                real_object_height,
                                fc='lightblue',
                                ec="blue")

    # Radius calculation
    radius = (real_object_width * radius_multiply) / 2

    # Camera placement line
    camera_placement = lines.Line2D((0, 0), (0, distance), lw=1.5, color='black')  # added color

    # Camera view lines
    camera_v1 = max_w_in / 2
    camera_v1_line = lines.Line2D((camera_v1, 0), (0, distance), lw=1.5, linestyle='dashed',
                                  color='black')  # added color
    camera_v2 = -max_w_in / 2
    camera_v2_line = lines.Line2D((camera_v2, 0), (0, distance), lw=1.5, linestyle='dashed',
                                  color='black')  # added color

    # Light 1 lines
    light_1x = radius * 2.5
    light_1y = radius * 2
    light_1 = lines.Line2D((0, light_1x), (0, light_1y), lw=1.5, color='black')  # added color
    light_1a = lines.Line2D((radius, light_1x), (0, light_1y), lw=1.5, linestyle='dashed', color='black')  # added color
    light_1b = lines.Line2D((radius, radius - (light_1x - radius)), (0, light_1y), lw=1.5, linestyle='dotted',
                            color='black')  # added color

    # Light 2 lines
    light_2x = -radius * 2.5
    light_2y = radius * 2
    light_2 = lines.Line2D((0, light_2x), (0, light_2y), lw=1.5, color='black')  # added color
    light_2a = lines.Line2D((-radius, light_2x), (0, light_2y), lw=1.5, linestyle='dashed',
                            color='black')  # added color
    light_2b = lines.Line2D((-radius, -radius - (light_2x + radius)), (0, light_2y), lw=1.5, linestyle='dotted',
                            color='black')  # added color

    # Add elements to the axes
    ax.add_patch(artwork)
    ax.add_line(camera_placement)
    ax.add_line(camera_v1_line)
    ax.add_line(camera_v2_line)
    ax.add_line(light_1)
    ax.add_line(light_1a)
    ax.add_line(light_1b)
    ax.add_line(light_2)
    ax.add_line(light_2a)
    ax.add_line(light_2b)

    # Add text annotations
    ax.text(0, distance, "camera", fontsize=10, ha='center', va='bottom')  # camera location
    ax.text(light_1x, light_1y * 1.025, "light", fontsize=10, ha='center', va='bottom')  # light 1 location
    ax.text(light_2x, light_2y * 1.025, "light", fontsize=10, ha='center', va='bottom')  # light 2 location

    # Set axis limits and styling
    ax.set_ylim(-real_object_height, int(distance * 2))
    ax.axhline(0, color='black')
    ax.axis('equal')
    # ax.set_aspect('equal')  # ensures correct aspect ratio instead of using plt.axis('equal')

    # Set the title
    ax.set_title('Lighting Diagram')

    # Show the plot
    # plt.show()

    return fig, light_1x, light_1y
