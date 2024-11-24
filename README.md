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
   `git clone https://github.com/TipTailor/data_acquisition`  
   `cd data_acquisition`

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