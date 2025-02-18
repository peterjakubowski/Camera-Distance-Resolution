# Camera and Lighting Positioning Calculator
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


def plot_lighting_diagram(real_object_width, real_object_height, radius_multiply, distance, max_w_in, max_h_in):
    """
    Plots the lighting diagram using Matplotlib with emojis.
    """

    # Create a figure and axes
    fig, ax = plt.subplots(1, figsize=(6,5), dpi=300)

    # Camera image area
    camera_view = patches.Rectangle(((-max_w_in / 2), (-max_h_in / 2)),
                                    max_w_in,
                                    max_h_in,
                                    fc='#FF7F00',  # Orange
                                    ec="#FF0000",  # Red
                                    lw=1.0,
                                    alpha=1.0)
    ax.add_patch(camera_view)

    # Artwork rectangle
    artwork = patches.Rectangle(((-real_object_width / 2), (-real_object_height / 2)),
                                real_object_width,
                                real_object_height,
                                fc='#B0E2FF',  # Light Steel Blue
                                ec="#4682B4",  # Steel Blue
                                lw=1.2,
                                alpha=1.0)
    ax.add_patch(artwork)

    # Radius calculation
    radius = (real_object_width * radius_multiply) / 2

    # Add a yellow circle between the lights
    circle = patches.Circle((0, 0), radius=radius, color='#FFD700', alpha=0.2)
    ax.add_patch(circle)

    # Add an "x" at the center of the rectangle
    ax.text(0, 0, "x", fontsize=10, ha='center', va='center', color='black')

    # Camera placement arrow
    ax.arrow(0.0, distance, 0.0, -distance * 0.95,  # Changed start and end points
             lw=1.5, color='#000000',
             alpha=1.0,
             head_width=0.35, head_length=0.6,  # Reduced head size
             overhang=0.0,  # No overhang
             length_includes_head=True)

    # Light 1 arrow
    light_1x = radius * 2.5
    light_1y = radius * 2
    ax.arrow(light_1x, light_1y, -light_1x * 0.95, -light_1y * 0.95,  # Changed start and end points
             lw=1.5, color='#000000',
             head_width=0.35, head_length=0.6,  # Reduced head size
             overhang=0,
             length_includes_head=True)

    light_1a = lines.Line2D((light_1x, light_1x), (0, light_1y), lw=1.5, linestyle=':', color='#778899')
    light_1b = lines.Line2D((light_1x, 0), (0, 0), lw=1.5, linestyle=':',
                            color='#778899')

    # Light 2 arrow
    light_2x = -radius * 2.5
    light_2y = radius * 2
    ax.arrow(light_2x, light_2y, -light_2x * 0.95, -light_2y * 0.95,  # Changed start and end points
             lw=1.5, color='#000000',
             head_width=0.35, head_length=0.6,  # Reduced head size
             overhang=0,
             length_includes_head=True)

    # Add elements to the axes
    ax.add_line(light_1a)
    ax.add_line(light_1b)

    # Add text annotations
    ax.text(0, distance * 1.025, "camera", fontsize=10, ha='center', va='bottom', color="#101010")
    ax.text(light_1x, light_1y * 1.025, "light", fontsize=10, ha='center', va='bottom', color="#101010")
    ax.text(light_2x, light_2y * 1.025, "light", fontsize=10, ha='center', va='bottom', color="#101010")
    ax.text(-max_w_in / 2, -max_h_in / 2, "image area", fontsize=8, ha='left', va='top',
            color="#101010")  # Image area
    ax.text(-real_object_width / 2, -real_object_height / 2, "object", fontsize=8, ha='left', va='bottom',
            color="#101010")  # Object area

    # Add labels for light distances
    ax.text(light_1x / 1.5, -1, f'{light_1x:.2f} in', fontsize=8, ha='center', va='top',
            color='black')  # Label for light_1x distance
    ax.text(light_1x - 1, light_1y / 2.5, f'{light_1y:.2f} in', fontsize=8, ha='right', va='center',
            color='black')  # Label for light_1y distance
    ax.text(-1, distance / 1.5, f'{distance:.2f} in', fontsize=8, ha='right', va='center',
            color='black')  # Label for light_2x distance

    # Set axis limits and styling
    ax.set_ylim(-distance * 0.5, distance * 1.2)  # Adjusted ylim
    ax.set_xlim(-light_1x * 1.2, light_1x * 1.2)  # Adjusted xlim
    ax.axis('equal')
    ax.tick_params(axis='both', labelsize=8)

    # Add grid
    ax.grid(True, linestyle='--', alpha=0.3)

    # Set the title
    # ax.set_title('Lighting Diagram\n', fontsize=14, color="#333333")

    # Set x label
    ax.set_xlabel('inches', fontsize=10)

    # Remove the frame
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return fig, light_1x, light_1y
