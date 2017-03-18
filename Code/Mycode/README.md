# Background
Building architectural plans are available as .dxf file , generally genrated in
AutoCad. To do any computation , first the data needs to extracted from the file,
made sense of . The first challenge is to extract information about walls.
<br>
# Aim
This program extracts data from .dxf file, find walls and represent the wall using
a single line namely the centerline. The centerline can be used to store all
information about the wall . The advantage of storing a wall as a single line
is that it can be used to run graph algorithms on it.
<br>
# Libraries Used
* <b> Ezdxf </b> : to read data from .dxf file .
        <br>
        `Installation : sudo pip install ezdxf`
* <b> Osgeo </b> : to genrate the output inform of a shape file .
        <br>
        `Installation : sudo apt-get install libgdal-dev &&
                        sudo apt install gdal-bin python-gdal python3-gdal`
        <br>
* A small python based 2d geometry that i wrote.
  <br> Link  : https://github.com/FundamentalEq/2D-Geometry-Python-Library

# Usage
#### python ExtractLine.py  <i> filename.dxf </i>
<b> Note </b> : For Adjusting the Minimum wall width and Maximum wall width edit values in GlobalValues.py

# Output
Output is produced in form of a shape file .
