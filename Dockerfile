# Use ubuntu as the base image
FROM ubuntu:latest

# Install Python, pip, R, and rgbif
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    r-base
#    r-cran-rgbif
RUN apt-get install -y build-essential libcurl4-gnutls-dev libxml2-dev libssl-dev

RUN R -e "install.packages('rgbif', clean=TRUE)"
RUN R -e "install.packages('sp', clean=TRUE)"
RUN apt-get install -y  gdal-bin libgdal-dev
RUN R -e "install.packages('raster', clean=TRUE)"
#RUN R -e "install.packages('terra', clean=TRUE)" # maptools legacy

# Copy the Python and R scripts to the working directory
COPY hello.py /app/hello.py
COPY hummingbirds.R /app/hummingbirds.R

# Run the Python and R scripts
CMD ["python3", "/app/hello.py"]
CMD ["Rscript", "/app/hummingbirds.R"]
