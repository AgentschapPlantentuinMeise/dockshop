# Use ubuntu as the base image
FROM ubuntu:latest

# Install Python, pip, R, and rgbif
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    r-base
#    r-cran-rgbif

# Copy the Python and R scripts to the working directory
COPY hello.py /app/hello.py
COPY hummingbirds.R /app/hummingbirds.R

# Run the Python and R scripts
CMD ["python3", "/app/hello.py"]
CMD ["Rscript", "/app/hummingbirds.R"]
