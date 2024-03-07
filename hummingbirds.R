# An R script that performs a biodiversity analysis and creates a biodiversity indicator
# Load the required packages
library(rgbif)
library(sp)
library(raster)
library(maptools)

# Define the taxon key for hummingbirds
taxon_key <- 734
# Download GBIF data for hummingbirds
hummingbirds <- occ_search(taxonKey = taxon_key, limit = 1000, hasCoordinate = TRUE)
# Convert the GBIF data to a spatial points data frame
hummingbirds_sp <- occ2sp(hummingbirds)

# Define the spatial extent for the analysis
xmin <- -180
xmax <- -30
ymin <- -60
ymax <- 30
extent <- c(xmin, xmax, ymin, ymax)

# Create a raster template with a 1 degree resolution
raster_template <- raster(extent = extent, resolution = 1)

# Aggregate the hummingbird occurrences to the raster cells
hummingbirds_raster <- rasterize(hummingbirds_sp, raster_template, fun = "count")

# Calculate the species richness indicator
richness <- occ2richness(hummingbirds, raster_template)

# Plot the hummingbird occurrences and the species richness indicator
par(mfrow = c(1, 2))
plot(hummingbirds_raster, main = "Hummingbird occurrences")
plot(richness, main = "Hummingbird species richness")
