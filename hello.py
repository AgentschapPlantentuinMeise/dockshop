# A Python script that performs a biodiversity analysis and creates a biodiversity indicator
# Load the required packages
import pygbif
import pandas as pd
import geopandas as gpd
import shapely.geometry as sg
import rasterio as rio
import rasterio.features as rf
import matplotlib.pyplot as plt

# Print a hello message
print("Hello, this is a Python script!")

# Define the taxon key for hummingbirds
taxon_key = 734

# Download GBIF data for hummingbirds
hummingbirds = pygbif.occurrences.search(taxonKey = taxon_key, limit = 1000, hasCoordinate = True)

# Convert the GBIF data to a geopandas data frame
hummingbirds_df = pd.DataFrame(hummingbirds["results"])
hummingbirds_gdf = gpd.GeoDataFrame(
    hummingbirds_df,
    geometry = gpd.points_from_xy(
        hummingbirds_df["decimalLongitude"],
        hummingbirds_df["decimalLatitude"]
    )
)

# Define the spatial extent for the analysis
xmin = -180
xmax = -30
ymin = -60
ymax = 30
extent = sg.box(xmin, ymin, xmax, ymax)

# Create a raster template with a 1 degree resolution
raster_template = rio.open("raster_template.tif", "w", driver = "GTiff", height = ymax - ymin, width = xmax - xmin, count = 1, dtype = rio.uint8, crs = "EPSG:4326", transform = rio.transform.from_origin(xmin, ymax, 1, 1))
raster_template.close()
# Aggregate the hummingbird occurrences to the raster cells
hummingbirds_raster = rf.rasterize(hummingbirds_gdf.geometry, out_shape = (ymax - ymin, xmax - xmin), fill = 0, transform = rio.transform.from_origin(xmin, ymax, 1, 1))
# Calculate the species richness indicator
richness = pd.DataFrame(hummingbirds_gdf.groupby("speciesKey").size(), columns = ["count"])
#richness["speciesKey"] = richness.index
richness = pd.merge(hummingbirds_gdf[["speciesKey", "geometry"]], richness, on = "speciesKey")
richness_raster = rf.rasterize(richness.geometry, out = hummingbirds_raster, transform = rio.transform.from_origin(xmin, ymax, 1, 1), merge_alg = rio.enums.MergeAlg.add)
# Plot the hummingbird occurrences and the species richness indicator
fig, ax = plt.subplots(1, 2, figsize = (12, 6))
ax[0].imshow(hummingbirds_raster, extent = [xmin, xmax, ymin, ymax], cmap = "Blues")
ax[0].set_title("Hummingbird occurrences")
ax[1].imshow(richness_raster, extent = [xmin, xmax, ymin, ymax], cmap = "Reds")
ax[1].set_title("Hummingbird species richness")
#plt.show()
fig.savefig('/results/hummingbird_pyplot.png')
