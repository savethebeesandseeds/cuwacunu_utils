# Create or run the Docker enviroment
docker run -it --name=cuwacunu_concepts -v .:/src debian:11
docker exec -it cuwacunu_concepts /bin/bash

# Install dependencies
apt update
apt upgrade
apt install --no-install-recommends curl
apt install --no-install-recommends unzip
apt install --no-install-recommends python3
apt install --no-install-recommends python3-pip

# install python dependencies
pip install numpy
pip install matplotlib
pip install pandas
pip install colorama

