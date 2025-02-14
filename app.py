# Camera Distance and Resolution
#
# Author: Peter Jakubowski
# Date: 2/14/2025
# Description:
#

import streamlit as st
import json
from pydantic import BaseModel
from tools import convert_units, print_measurements, plot_sensor_fit, plot_lighting_diagram


# ==============================
# ======== Form fields =========
# ==============================


class Sensor(BaseModel):
    sensor_w_mm: float
    sensor_h_mm: float
    sensor_w_px: int
    sensor_h_px: int


sensors: dict[str, Sensor] = {}

# load the dictionary of digital camera bodies and backs with sensor size and pixel dimensions
with open("data/cameras.json", "r") as file:
    sensor_dict = json.loads(file.read())
    for name, attr in sensor_dict.items():
        sensors[name] = Sensor(**attr)

# ==============================
# ========= Streamlit ==========
# ==============================

st.header('Distance and Resolution')

st.write('Calculate resolution, sensor usage, and camera and lighting distances for flat art / copywork setups.')

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

    # select the unit of measurement used to measure the width and height of the artwork
    st.selectbox(label="Unit of measurement",
                 key="real_object_units",
                 options=["mm", "cm", "inches"],
                 index=2,
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

    # set the desired resolution in pixels per inch (ppi)
    st.number_input(label="Resolution (ppi)",
                    key="set_ppi",
                    min_value=72,
                    max_value=3200,
                    step=1,
                    value=300
                    )

    # Set to desired radius multiplier to control light coverage.
    st.slider(label="Light coverage",
              key="radius_multiply",
              min_value=1.0,
              max_value=2.0,
              step=0.01,
              value=1.2
              )

    # Click the button when ready to calculate results
    calculate = st.button(label="Calculate",
                          key="calculate")

# ==============================
# ========= Calculate ==========
# ==============================

if calculate:

    sensor = sensors[st.session_state.camera]
    sensor_ratio = sensor.sensor_w_px / sensor.sensor_h_px

    # convert real object width and height to inches if provided in cm or mm
    if st.session_state.real_object_units == 'cm':
        st.session_state.real_object_width = st.session_state.real_object_width * 0.393701
        st.session_state.real_object_height = st.session_state.real_object_height * 0.393701
    elif st.session_state.real_object_units == 'mm':
        st.session_state.real_object_width = st.session_state.real_object_width * 0.0393701
        st.session_state.real_object_height = st.session_state.real_object_height * 0.0393701

    # calculate object width and height in pixels by multiplying ppi by object measurements in inches
    object_w_px = int(st.session_state.set_ppi * st.session_state.real_object_width)
    object_h_px = int(st.session_state.set_ppi * st.session_state.real_object_height)

    # calculate object width and height in mm on sensor by multiplying sensor size in mm by object
    # size in pixels and dividing by the sensor size in pixels
    object_w_on_film_mm = (sensor.sensor_w_mm * object_w_px) / sensor.sensor_w_px
    object_h_on_film_mm = (sensor.sensor_h_mm * object_h_px) / sensor.sensor_h_px

    # calculate object resolution by dividing object in pixels by object in inches (should equal set_ppi value)
    PPI = object_w_px / st.session_state.real_object_width

    # calculate camera distance to object by multiplying object width by lens focal length and dividing
    # by object size on sensor
    distance = (st.session_state.real_object_width * st.session_state.lens_focal_len_mm) / object_w_on_film_mm
    # distance_ft_in = int(distance/12)

    sensor_usage_w = round((object_w_on_film_mm / sensor.sensor_w_mm) * 100, 2)
    sensor_usage_h = round((object_h_on_film_mm / sensor.sensor_h_mm) * 100, 2)
    max_w_px = sensor.sensor_w_px / st.session_state.real_object_width
    max_h_px = sensor.sensor_h_px / st.session_state.real_object_height
    max_w_in = sensor.sensor_w_px / PPI

    if object_w_on_film_mm > sensor.sensor_w_mm:
        st.warning("Warning! The object width does not fit in frame.")
    if object_h_on_film_mm > sensor.sensor_h_mm:
        st.warning("Warning! The object height does not fit in frame.")

    col1, col2 = st.columns(2)

    with col1:
        st.text('Using ' + str(sensor_usage_w) + "% of sensor's width and "
                + str(sensor_usage_h) + "% of height")

        if st.session_state.real_object_width >= st.session_state.real_object_height * sensor_ratio:
            st.text("MAX PPI: " + str(round(max_w_px, 2)))
            st.text("5% Fit PPI: " + str(round(max_w_px * .95, 2)))
        else:
            st.text("MAX PPI: " + str(round(max_h_px, 2)))
            st.text("5% Fit PPI: " + str(round(max_h_px * .95, 2)))

        st.text("\nDimensions: " + str(object_w_px) + " x " + str(object_h_px) + " pixels")
        st.text("PPI: " + str(round(PPI, 2)))

    with col2:

        # plot figure showing object fit on sensor
        st.pyplot(fig=plot_sensor_fit(sensor, object_w_on_film_mm, object_h_on_film_mm))

    lighting_diagram, light_1x, light_1y = plot_lighting_diagram(st.session_state, distance, max_w_in)

    col1, col2 = st.columns(2)

    with col1:
        # print a summary with camera and distance info
        some_text = (f"Camera: {st.session_state.camera}\n"
                     f"Sensor size: {sensor.sensor_w_mm} x {sensor.sensor_h_mm}mm / {sensor.sensor_w_px} x {sensor.sensor_h_px} pixels\n"
                     f"Focal length: {st.session_state.lens_focal_len_mm}mm\n"
                     f"Camera distance: {print_measurements(convert_units(distance, "inches"))}\n"
                     f"Lights distance x: {print_measurements(convert_units(light_1x, "inches"))}\n"
                     f"Lights distance y: {print_measurements(convert_units(light_1y, "inches"))}\n"
                     )
        st.text(some_text)

    with col2:
        # plot figure showing camera and lighting diagram
        st.pyplot(fig=lighting_diagram)

