# TripTailor: Dynamic Travel Route Optimization

## Overview

TripTailor is a travel route optimization tool that integrates open-source geographic data to provide dynamic and accurate travel routes. By leveraging public datasets, we ensure that our platform remains up-to-date and highly reliable for travelers.

---

## Features

- Integrates OSM data to dynamically update routes.
- Visualizes museum data on an interactive map.

---

## Prerequisites

1. Install Python dependencies:
   `pip install -r requirements.txt`

2. Ensure PostgreSQL is installed with PostGIS enabled.

---

## Usage

1. Clone the repository:  
   `git clone https://github.com/username/TripTailor.git`  
   `cd TripTailor`

2. Update database credentials in `db_setup.py` under `DB_CREDENTIALS`.

3. Run the pipeline:  
   `python main.py`

4. Open the map:  
   View the generated `data/map.html` in any browser to explore museums in Münster.

---

## Future Enhancements

1. Add route optimization for multi-stop journeys.
2. Allow users to specify custom points of interest.
3. Enable real-time updates from OpenStreetMap.

## Project Structure
TripTailor/
│
├── data/
│   ├── muenster-regbez-latest.osm.pbf   # Raw OSM data for Münster
│   ├── museums.geojson                  # Extracted museum data in GeoJSON format
│   ├── map.html                         # Generated interactive map
│
├── scripts/
│   ├── getOSM.py                        # Script to download OSM data
│   ├── db_setup.py                      # Script to set up PostgreSQL database
│   ├── query_data.py                    # Script to query museum data
│   ├── visualize_map.py                 # Script to generate the interactive map
│
├── main.py                              # Orchestrates the entire pipeline
├── requirements.txt                     # Python dependencies
└── README.md                            # Project documentation
