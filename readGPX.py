import gpxpy
import gpxpy.gpx
import pandas as pd

with open("file.gpx",'r', encoding='utf-8') as gpx_file:
    gpx_data=gpxpy.parse(gpx_file)
