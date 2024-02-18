import gpxpy
import numpy as np
import os 
import pandas as pd
from geopy import distance
from math import sqrt, floor
import datetime
dir='DATI'
lista=[['Name','Total distance','Total time','Max speed','Data']]
dati_da_inserire=[] 
for filename in os.listdir(dir): 
    if filename.endswith(".gpx"):
        file_path = os.path.join(dir, filename)
        with open("file.gpx",'r', encoding='utf-8') as gpx_file:
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
#print(df.head())
#print(df.describe())
#####################
len_tracks = len(gpx_data.tracks)
len_segments = len(gpx_data.tracks[0].segments)
len_points = len(gpx_data.tracks[0].segments[0].points)          

delta_elev = [0]    # change in elevation between records
delta_time = [0]    # time interval between records

delta_sph2d = [0]   # segment distance from spherical geometry only
delta_sph3d = [0]   # segment distance from spherical geometry, adjusted for elevation
dist_sph2d = [0]   # cumulative distance from spherical geometry only
dist_sph3d = [0]   # cumulative distance from spherical geometry, adjusted for elevation

delta_geo2d = [0]   # segment distance from geodesic method only
delta_geo3d = [0]   # segment distance from geodesic method, adjusted for elevation
dist_geo2d = [0]   # cumulative distance from geodesic method only
dist_geo3d = [0]   # cumulative distance from geodesic method, adjusted for elevation

gpx_points = gpx_data.tracks[0].segments[0].points
for idx in range(1, len(gpx_points)): # index will count from 1 to lenght of dataframe, beginning with the second row
    start = gpx_points[idx-1]
    end = gpx_points[idx]

    # elevation
    temp_delta_elev = end.elevation - start.elevation
    delta_elev.append(temp_delta_elev)

    # time
    temp_delta_time = (end.time - start.time).total_seconds()
    delta_time.append(temp_delta_time)

    # distance from spherical model
    temp_delta_sph2d = distance.great_circle((start.latitude, start.longitude), (end.latitude, end.longitude)).m

    delta_sph2d.append(temp_delta_sph2d)

    dist_sph2d.append(dist_sph2d[-1] + temp_delta_sph2d)

    temp_delta_sph3d = sqrt(temp_delta_sph2d**2 + temp_delta_elev**2)

    delta_sph3d.append(temp_delta_sph3d)

    dist_sph3d.append(dist_sph3d[-1] + temp_delta_sph3d)

    # distance from geodesic model
    temp_delta_geo2d = distance.distance((start.latitude, start.longitude), (end.latitude, end.longitude)).m

    delta_geo2d.append(temp_delta_geo2d)

    dist_geo2d.append(dist_geo2d[-1] + temp_delta_geo2d)

    temp_delta_geo3d = sqrt(temp_delta_geo2d**2 + temp_delta_elev**2)

    delta_geo3d.append(temp_delta_geo3d)

    dist_geo3d.append(dist_geo3d[-1] + temp_delta_geo3d)

# dump the lists into the dataframe
df['delta_elev'] = delta_elev
df['delta_time'] = delta_time
df['delta_sph2d'] = delta_sph2d
df['delta_sph3d'] = delta_sph3d
df['dist_sph2d'] = dist_sph2d
df['dist_sph3d'] = dist_sph3d
df['delta_geo2d'] = delta_geo2d
df['delta_geo3d'] = delta_geo3d
df['dist_geo2d'] = dist_geo2d
df['dist_geo3d'] = dist_geo3d
df['inst_mps'] = df['delta_geo3d'] / df['delta_time']
# check bulk results
#print(f"Spherical Distance 2D: {dist_sph2d[-1]/1000}km \nSpherical Distance 3D: {dist_sph3d[-1]/1000}km \nElevation Correction: {(dist_sph3d[-1]) - (dist_sph2d[-1])} meters \nGeodesic Distance 2D: {dist_geo2d[-1]/1000}km \nGeodesic Distance 3D: {dist_geo3d[-1]/1000}km \nElevation Correction: {(dist_geo3d[-1]) - (dist_geo2d[-1])} meters \nModel Difference: {(dist_geo3d[-1]) - (dist_sph3d[-1])} meters \nTotal Time: {str(datetime.timedelta(seconds=sum(delta_time)))}")

for threshold in np.arange(0.1, 2.1, 0.1): # delta-distance thresholds from 0 to 2 meters by 0.1 meters
    stop_time = sum(df[df['inst_mps'] < threshold]['delta_time'])
    #print(f"Distance Threshold: {round(threshold,2)}m ==> {str(datetime.timedelta(seconds=stop_time))}")


df.fillna(0, inplace=True) # fill in the NaN's in the first row of distances and deltas with 0. They were breaking the overall average speed calculation

df_moving = df[df['inst_mps'] >= 0.9] # make a new dataframe filtered to only records where instantaneous speed was greater than 0.9m/s

avg_mps = (sum((df['inst_mps'] * df['delta_time'])) / sum(df['delta_time']))

avg_mov_mps = (sum((df_moving['inst_mps'] * df_moving['delta_time'])) / sum(df_moving['delta_time']))

print(f"Maximum Speed: {round((2.23694 * df['inst_mps'].max(axis=0)), 2)} mph")
print(f"Average Speed: {round((2.23694 * avg_mps), 2)} mph")
print(f"Average Moving Speed: {round((2.23694 * avg_mov_mps), 2)} mph")
print(f"Moving Time: {str(datetime.timedelta(seconds=sum(df_moving['delta_time'])))}")

