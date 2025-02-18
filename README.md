# Camera and Lighting Positioning

Tool to calculate and visualize camera and lighting distances for flat art and copywork setups.

1). Given a camera, lens, and object (usually flat works like flat art on paper, paintings, prints, etc.), determine the camera position for a chosen output resolution. The distance between camera and object is returned.

2). Given an object, determine the position of lights (a minimum of two, one on each side of the object).

## Using the Distance and Resolution tool

### Launch

Launch the streamlit app in your web browser from you cli.

```commandline
streamlit run app.py
```

### Enter Parameters:
* camera: Choose a camera or digital back from the dictionary of cameras
* lens_focal_len_mm: Select the focal length of the lens in millimeters
* real_object_units: Select the unit of measurement used to measure the width and height of the artwork
* real_object_width: Width of the artwork in units selected in real_object_units
* real_object_height: Height of the artwork in units selected in real_object_units
* set_ppi: Set to desired resolution in pixels per inch
* radius_multiply: Set to desired radius multiplier to control light coverage. A value of 1 will set light coverage to fit object at 100%. Increase multiplier to expand light coverage and reduce vignetting in image area.

### Output:
* Sensor usage in percent for width and height
* MAX PPI: The maximum ppi value possible with selected camera and focal length when fitting the whole artwork within
* 5% Fit PPI: The maximum ppi value possible reduced by 5%
* Dimensions: The output image dimensions in pixels (widthxheight)
* PPI: The ppi value set in set_ppi
* Camera: The camera or digital back being used
* Sensor size: The camera's sensor size in millimeters(mm) and pixels(px)
* Focal length: The focal length of the lens in millimeters(mm)
* Camera distance: Distance from the camera to the center of the artwork in millimeters(mm), centimeters(cm), inches(in), and feet(ft) and inches(in)
* Lights distance x: Distance from the light to the center of the artwork on the x-axis (artwork plane) in millimeters(mm), centimeters(cm), inches(in), and feet(ft) and inches(in)
* Lights distance y: Distance from the light to the center of the artwork on the y-axis (lens plane) in millimeters(mm), centimeters(cm), inches(in), and feet(ft) and inches(in)
