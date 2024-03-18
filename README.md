
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


