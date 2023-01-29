# About

```pyROUTE``` is a user-centric route optimization and iterneraty schedualling solution developed by AmplifiQation.

Adaptable and enginmeered for scalability, ```pyROUTE``` delivers quantum enhanced:

- Evening and
- Vaccation and buisness trip schedualling.

```pyROUTE``` is available under the MIT license [here](/LICENSE).

# About

```pyTEM``` is a *high-level* scripting interface enabling the *user-friendly* control of, and automated data 
 acquisition on, Thermo Fisher Scientific and FEI microscopes from a pure Python environment. Bolted directly on top 
 of a COM interface, ```pyTEM``` is a Python wrapper for, and extension of, the prerequisite Thermo Fisher Scientific 
 / FEI scripting and advanced scripting interfaces.

While it may depend on your microscope installation, ```pyTEM``` will likely need to be run on a microscope control 
 computer with the prerequisite Thermo Fisher Scientific / FEI scripting and advanced scripting interfaces installed 
 and properly configured. For detailed information regarding your microscope's scripting capabilities, please refer to 
 the documentation accompanying your microscope or contact to your microscope supplier.

In addition to the main scripting interface, pyTEM ships with various [scripts](#scripts). Besides being useful 
 in-and-of-themselves, these scripts demonstrate how to interface with and control the microscopes using ```pyTEM```. 
 A list of available scripts can be found [below](#scripts). These scripts are included as part of pyTEM for the sake 
 of consolidating the TEM Laboratory's scripting efforts.
 
Supported Python versions: [3.8](https://www.python.org/downloads/release/python-380/).

# Contribution & Contact Info

```pyTEM``` is developed and maintained by the TEM Microscopy Laboratory at BASF SE in Ludwigshafen, Germany. If you 
 have any questions about the ```pyTEM``` project or would like to contribute or collaborate, please contact Philipp 
 Müller at [philipp.mueller@basf.com](mailto:philipp.mueller@basf.com).

Issues should be reported to the issues board [here](https://github.com/basf/pyTEM/issues).

# Interface

```pyTEM``` is a microscope scripting interface. This means that you can issue commands to, and receive microscope data 
 from, compatible microscopes by calling ```pyTEM``` functions. This is not a complete interface in that it does not 
 provide access to all the microscope's functionality. However, it provides access to all fundamental microscope 
 functions as well as some more advanced functions which were required for the development of one or more 
 [```pyTEM``` scripts](#scripts).

```pyTEM``` aims to be more *user-friendly* than the underlying Fisher Scientific / FEI scripting and advanced 
 scripting interfaces. To this end: 
- ```pyTEM``` functions return only built-in data types or instances of useful, simple classes (no pointers).
- ```pyTEM``` accepts input and returns results in *user-friendly* units. For example, stage position is set in 
 microns/degrees, and tilt speed in degrees-per-second.
- ```pyTEM``` provides many additional functions not directly available through the underlying interface. For example, 
 tilt-while-acquiring, metadata evaluation, and save-to-file functionality.
- ```pyTEM``` is open source and licensed such that users can make any changes or modifications required to
  suit their own installation.

Finally, ```pyTEM``` is a good starting place for those interested in learning how to control their microscope from a 
 pure Python environment.

```pyTEM``` [controls](#controls) are divided across Python 
 [mixins](https://www.pythontutorial.net/python-oop/python-mixin/). This simplified 
 [class-diagram](/docs/pyTEM%20Class%20Diagram%20-%20Simple.jpg) 
 was built to help articulate ```pyTEM```'s architecture. Notice that some mixins include other mixins, and a pyTEM 
 ```Interface``` includes all mixins along with some [interface-level controls](#interface-level-controls).
 
### Controls

#### Acquisition Controls

Microscope acquisition controls including ```acquisition()``` and ```acquisition_series()``` functions. By means of 
 multitasking, both functions offer beam-blanker optimization and acquire-while-tilting functionality.

These functions return ```pyTEM``` ```Acquistion``` and ```AcquisitionSeries``` objects, respectively. Both the 
 ```Acquistion``` and ```AcquisitionSeries``` classes provide helpful methods for further image and metadata 
 manipulation as well as save-to-file functionality. 

#### Acquisition Controls Example

```
from pyTEM.Interface import Interface
from pathlib import Path


my_microscope = Interface()

# Get a list of available cameras.
available_cameras = my_microscope.get_available_cameras()

if len(available_cameras) > 0:
    # Let's see what each camera can do...
    for camera in available_cameras:
        my_microscope.print_camera_capabilities(camera_name=camera)

    # Perform a single blanker-optimized acquisition using the first available camera.
    acq = my_microscope.acquisition(camera_name=available_cameras[0], exposure_time=1, 
                                    sampling='4k', blanker_optimization=True)

    # Downsample the acquisition (bilinear decimation by a factor of 2).
    acq.downsample()
    
    # Display a pop-up with the results of our acquisition.
    acq.show_image()

    # Save the acquisition to file.
    downloads_path = str(Path.home() / "Downloads")
    acq.save_to_file(out_file=downloads_path + "/test_acq.tif")

else:
    print("No available cameras!")
```

#### Magnification Controls

When in *imaging* mode, get and set both TEM and STEM magnification. When in *diffraction* mode, get and set 
 camera-length.

#### Magnification Controls Example

```
from pyTEM.Interface import Interface
my_microscope = Interface()

# Make sure we are in TEM imaging mode.
my_microscope.set_mode(new_mode="TEM")
my_microscope.set_projection_mode(new_projection_mode="imaging")

# Print out the current magnification.
current_magnification = my_microscope.get_magnification()
print("Current magnification: " + str(current_magnification) + "x Zoom")

# Print a list of available magnifications.
my_microscope.print_available_magnifications()

# TEM magnification is set by index, let's increase the magnification by three notches.
current_magnification_index = my_microscope.get_magnification_index()
my_microscope.set_tem_magnification(new_magnification_index=current_magnification_index + 3)

# And decrease it back down by one notch.
my_microscope.shift_tem_magnification(magnification_shift=-1)
```

#### Image and Beam Shift Controls

Get and set both image and beam shift.

#### Image and Beam Shift Controls Example

```
from pyTEM.Interface import Interface
my_microscope = Interface()

# Print out the current image shift.
u = my_microscope.get_image_shift()
print("Current image shift in the x-direction: " + str(u[0]))
print("Current image shift in the y-direction: " + str(u[1]))

# Print out the current beam shift.
v = my_microscope.get_beam_shift()
print("\nCurrent beam shift in the x-direction: " + str(v[0]))
print("Current beam shift in the y-direction: " + str(v[1]))

# Shift the image 2 microns to the right, and 3 microns up.
my_microscope.set_image_shift(x=u[0] + 2, y=u[1] + 3)

# Move the beam shift to (-10 um, 5 um).
my_microscope.set_beam_shift(x=-10, y=5)

# Print out the new image shift.
u = my_microscope.get_image_shift()
print("\nNew image shift in the x-direction: " + str(u[0]))
print("New image shift in the y-direction: " + str(u[1]))

# Print out the new beam shift.
v = my_microscope.get_beam_shift()
print("\nNew beam shift in the x-direction: " + str(v[0]))
print("New beam shift in the y-direction: " + str(v[1]))

# Zero both image and beam shift.
my_microscope.zero_shifts()
```

#### Mode Controls

Microscope mode controls, including getters and setters for instrument, illumination, and projection mode.

#### Mode Controls Example
