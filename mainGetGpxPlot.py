import ezgpx

# Parse GPX file
gpx = ezgpx.GPX("file.gpx")
gpx.to_csv("new_file.csv", columns=["lat", "lon", "ele"])

"""
# Plot with Matplotlib Basemap Toolkit
gpx.matplotlib_basemap_plot(color="darkorange",
                            start_stop_colors=("darkgreen", "darkred"),
                            way_points_color="darkblue",
                            title=gpx.name(),
                            duration=(0,0),
                            distance=(0.5,0),
                            ascent=None,
                            pace=None,
                            speed=(1,0),
                            file_path="img_2")


# Plot with Folium

gpx.folium_plot(tiles="OpenStreetMap",
                color="orange",
                start_stop_colors=("green", "red"),
                way_points_color="blue",
                minimap=True,
                coord_popup=False,
                title="Very nice track!",
                zoom=8,
                file_path="map_2.html",
                open=True)

"""
