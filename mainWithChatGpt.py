from xml.dom import minidom
import gpxpy
from geopy.distance import great_circle
from datetime import timedelta

def getNome(gpx_file):
    data=open(gpx_file)
    xmldoc = minidom.parse(data)
    dom_elements = xmldoc.getElementsByTagName("name")
    nome=dom_elements[0].firstChild.nodeValue
    return(nome)

def calculate_total_distance(gpx_file):
    gpx = gpxpy.parse(open(gpx_file))
    total_distance = 0
    
    for track in gpx.tracks:
        for segment in track.segments:
            for i in range(1, len(segment.points)):
                total_distance += segment.points[i-1].distance_2d(segment.points[i])
                
    return total_distance / 1000  # Conversione da metri a chilometri

def calculate_total_duration(gpx_file):
    gpx = gpxpy.parse(open(gpx_file))
    total_duration_seconds = 0
    
    for track in gpx.tracks:
        for segment in track.segments:
            total_duration_seconds += (segment.points[-1].time - segment.points[0].time).total_seconds()
            
    return timedelta(seconds=total_duration_seconds)

def calculate_average_speed(gpx_file):
    total_distance = calculate_total_distance(gpx_file)
    total_duration = calculate_total_duration(gpx_file)
    total_duration_hours = total_duration.total_seconds() / 3600
    if total_duration_hours == 0:
        return 0
    else:
        return total_distance / total_duration_hours

def calculate_max_speed(gpx_file):
    gpx = gpxpy.parse(open(gpx_file))
    max_speed = 0
    
    for track in gpx.tracks:
        for segment in track.segments:
            for i in range(1, len(segment.points)):
                speed = segment.points[i-1].speed_between(segment.points[i])
                if speed is not None and speed > max_speed:
                    max_speed = speed * 3.6  # Conversione da metri al secondo a chilometri all'ora (km/h)
    
    return max_speed

# File GPX di esempio
gpx_file = 'lonetti_scuola.gpx'

# Calcolo delle statistiche
total_distance = calculate_total_distance(gpx_file)
total_duration = calculate_total_duration(gpx_file)
total_hours = total_duration.seconds // 3600
total_minutes = (total_duration.seconds % 3600) // 60
total_seconds = total_duration.seconds % 60
average_speed = calculate_average_speed(gpx_file)
max_speed = calculate_max_speed(gpx_file)

# Output delle statistiche
print("Distanza totale percorsa: {:.2f} km".format(total_distance))
print("Tempo totale impiegato: {} ore, {} minuti e {} secondi".format(total_hours, total_minutes, total_seconds))
print("Velocità media: {:.2f} km/h".format(average_speed))
print("Velocità massima registrata: {:.2f} km/h".format(max_speed))

nome=getNome(gpx_file)
print("nome: " ,nome)