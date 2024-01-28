import gpxpy
import gpxpy.gpx
import os 
import pandas as pd
dir='./DATI'
lista=[['Name','Total distance','Total time','Max speed','Data']]
dir_list = os.listdir(dir)
print(dir_list)
for filename in os.listdir(dir): 
    if filename.endswith(".gpx"):
        os.chdir(r'./DATI')
        with open (filename,'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            dati_da_inserire=[] 
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        print(f'Point at ({point.latitude},{point.longitude}) -> {point.elevation}')
                           
