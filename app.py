# Camera and Lighting Positioning Calculator
#
# Author: Peter Jakubowski
# Date: 2/14/2025
# Description:
#

import streamlit as st
import pandas as pd
import json
from io import BytesIO
from pydantic import BaseModel
from tools import convert_units, print_measurements, plot_lighting_diagram, calculate_max_ppi


# ==============================
# ======== Sensor Info =========
# ==============================


class Sensor(BaseModel):
    sensor_w_mm: float
    sensor_h_mm: float
    sensor_w_px: int
    sensor_h_px: int


sensors: dict[str, Sensor] = {}

# load the dictionary of digital camera bodies and backs with sensor size and pixel dimensions
with open("data/sensors.json", "r") as file:
    sensor_dict = json.loads(file.read())
    for name, attr in sensor_dict.items():
        sensors[name] = Sensor(**attr)

# ==============================
# ========= Streamlit ==========
# ==============================

st.header('Camera and Lighting Positioning')

st.write('Calculate camera and lighting distances for flat art and copywork setups.')

st.divider()

# ==============================
# ======== Form fields =========
# ==============================

with (st.sidebar):
    # select the camera or digital back name
    st.selectbox(label="Camera body / digital back",
                 key="camera",
                 options=sensors.keys()
                 )

    # select the lens focal length
    st.selectbox(label="Lens focal length",
                 key="lens_focal_len_mm",
                 options=[24, 45, 50, 55, 85, 90, 100, 105, 110, 120, 135, 150, 200, 240],
                 index=7
                 )

    # set the object width, physical measurement
    st.number_input(label="Object width",
                    key="real_object_width",
                    min_value=0.0,
                    max_value=100000.0,
                    step=0.01,
                    value=10.00
                    )

    # set the object height, physical measurement
    st.number_input(label="Object height",
                    key="real_object_height",
                    min_value=0.0,
                    max_value=100000.0,
                    step=0.01,
                    value=8.00
                    )

    # select the unit of measurement used to measure the width and height of the artwork
    st.selectbox(label="Unit of measurement",
                 key="real_object_units",
                 options=["mm", "cm", "inches"],
                 index=2,
                 )

    # set the desired resolution in pixels per inch (ppi)
    st.number_input(label="Resolution (ppi)",
                    key="set_ppi",
                    min_value=72,
                    max_value=2000,
                    step=1,
                    value=300
                    )

    # Set to desired radius multiplier to control light coverage.
    st.slider(label="Light coverage",
              key="radius_multiply",
              min_value=1.0,
              max_value=5.0,
              step=0.05,
              value=3.0
              )

    # ==============================
    # ========= Calculate ==========
    # ==============================

    sensor = sensors[st.session_state.camera]
    sensor_ratio = sensor.sensor_w_px / sensor.sensor_h_px

    # convert real object width and height to inches if provided in cm or mm
    if st.session_state.real_object_units == 'cm':
        real_object_width = st.session_state.real_object_width * 0.393701
        real_object_height = st.session_state.real_object_height * 0.393701

    elif st.session_state.real_object_units == 'mm':
        real_object_width = st.session_state.real_object_width * 0.0393701
        real_object_height = st.session_state.real_object_height * 0.0393701

    else:
        real_object_width = st.session_state.real_object_width
        real_object_height = st.session_state.real_object_height

    # check max ppi
    if st.session_state.set_ppi > (max_ppi := calculate_max_ppi(sensor, real_object_width, real_object_height)):
        st.warning((f"Warning! The object does not fit in frame at {st.session_state.set_ppi}ppi. "
                    f"The maximum possible ppi is {max_ppi}"))

    # calculate object width and height in pixels by multiplying ppi by object measurements in inches
    object_w_px = int(st.session_state.set_ppi * real_object_width)
    object_h_px = int(st.session_state.set_ppi * real_object_height)

    # calculate object width and height in mm on sensor by multiplying sensor size in mm by object
    # size in pixels and dividing by the sensor size in pixels
    object_w_on_film_mm = (sensor.sensor_w_mm * object_w_px) / sensor.sensor_w_px
    object_h_on_film_mm = (sensor.sensor_h_mm * object_h_px) / sensor.sensor_h_px

    # calculate object resolution by dividing object in pixels by object in inches (should equal set_ppi value)
    PPI = object_w_px / real_object_width

    # calculate camera distance to object by multiplying object width by lens focal length and dividing
    # by object size on sensor
    distance = (real_object_width * st.session_state.lens_focal_len_mm) / object_w_on_film_mm
    # distance_ft_in = int(distance/12)

    # calculate sensor usage
    sensor_usage_w = round((object_w_on_film_mm / sensor.sensor_w_mm) * 100, 2)
    sensor_usage_h = round((object_h_on_film_mm / sensor.sensor_h_mm) * 100, 2)
    max_w_in = sensor.sensor_w_px / PPI
    max_h_in = sensor.sensor_h_px / PPI

    # check light coverage
    if (real_object_width * st.session_state.radius_multiply) / 2 < max_w_in / 2:
        _radius = st.session_state.radius_multiply + 0.05
        while (real_object_width * _radius) / 2 < max_w_in / 2:
            _radius += 0.05

        st.warning("Warning! The light coverage does not cover the entire viewing area. "
                   f"Increase light coverage to a minimum of {round(_radius, 2)}")

if object_w_on_film_mm > sensor.sensor_w_mm:
    st.warning("Warning! The object width does not fit in frame.")
if object_h_on_film_mm > sensor.sensor_h_mm:
    st.warning("Warning! The object height does not fit in frame.")

lighting_diagram, light_1x, light_1y = plot_lighting_diagram(real_object_width,
                                                             real_object_height,
                                                             st.session_state.radius_multiply,
                                                             distance,
                                                             max_w_in,
                                                             max_h_in)

# ============================
# ====== Plot diagrams =======
# ============================

# Create a buffer for the figure
buf = BytesIO()
# Save the figure in the buffer
lighting_diagram.savefig(buf, format='png')
# Display the figure buffer image
st.image(buf)

# st.pyplot(fig=lighting_diagram)

summary = [("Camera", st.session_state.camera),
           ("Lens focal length", f"{st.session_state.lens_focal_len_mm}mm"),
           ("Sensor size mm", f"{sensor.sensor_w_mm} x {sensor.sensor_h_mm}"),
           ("Sensor size pixels", f"{sensor.sensor_w_px} x {sensor.sensor_h_px}"),
           ("Sensor usage width", f"{sensor_usage_w}%"),
           ("Sensor usage height", f"{sensor_usage_h}%"),
           ("Camera to object distance", f"{print_measurements(convert_units(distance, "inches"))}"),
           ("Lights distance x", f"{print_measurements(convert_units(light_1x, "inches"))}"),
           ("Lights distance y", f"{print_measurements(convert_units(light_1y, "inches"))}"),
           ("Object width", f"{print_measurements(convert_units(real_object_width, "inches"))}"),
           ("Object height", f"{print_measurements(convert_units(real_object_height, "inches"))}"),
           ("Object dimensions pixels", f"{object_w_px} x {object_h_px}"),
           ("Object resolution (ppi)", f"{PPI}")
           ]

df = pd.DataFrame(data=summary, columns=[0, 1])

st.table(df)
