
# Docker workshop

First command to try:

    docker build .

Fix issues, and repeat.

To make it simple to run, tag the build

    docker build . -t copilot
    docker run -it copilot

That should also have failed, as not all dependencies are met. By
specifying a shell as command we can debug:

    docker run -it copilot /bin/bash

After debugging, the following lines will run the "default" R script
and the Python alternative, respectively:

    docker run -v /c/Users/$USER/repos/dockshop/tests:/results \
        -ti copilot
    docker run -v /c/Users/$USER/repos/dockshop/tests:/results \
        -ti copilot python3 /app/hello.py

