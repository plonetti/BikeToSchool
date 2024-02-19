import gpxpy
import os 
import pandas as pd

dir='DATI'
lista=[['Name','Total distance','Total time','Max speed','Data']]
dati_da_inserire=[] 
for filename in os.listdir(dir): 
    if filename.endswith(".gpx"):
        file_path = os.path.join(dir, filename)
        with open("lonetti_scuola.gpx",'r', encoding='utf-8') as gpx_file:
            gpx_data = gpxpy.parse(gpx_file)
            for track in gpx_data.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        dati_da_inserire.append({
                            'latitude':point.latitude,
                            'longitude':point.longitude,
                            'elevation':point.elevation,
                            'time':point.time
                            })
            df=pd.DataFrame(dati_da_inserire)
print(df.head())
#print(df.describe())
#####################
