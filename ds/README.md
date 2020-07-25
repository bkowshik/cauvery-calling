# README


## Setup

```bash
# Clone the repository.
git clone https://github.com/bkowshik/cauvery-calling.git

# Get inside the data science directory.
cd 'cauvery-calling/ds'

# Create a new virtual environment in the ".env" folder.
python3 -m venv .env

# Activate the new environment.
source .env/bin/activate

# Install the package locally.
pip install -r requirements.txt
```


## Datasets

```bash
# The data folder contains all the datasets.
cd 'data/'

# Download the latest pbf of India from Geofabrik.
curl -O 'https://download.geofabrik.de/asia/india-latest.osm.pbf'
```


## Snippets


### Generate `GeoJSON` of the Cauvery river

```bash
# Create a GeoJSON file.
$ python geojson_of_cauvery.py
```
