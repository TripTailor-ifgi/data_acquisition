# TripTailor: Dynamic Travel Route Optimization

## Overview

TripTailor is a travel route optimization tool that integrates open-source geographic data to provide dynamic and accurate travel routes. By leveraging public datasets, we ensure that our platform remains up-to-date and highly reliable for travelers.

---

## Features

- Integrates OSM data to dynamically update routes.
- Visualizes museum data on an interactive map.

---

## Usage

1. Clone the repository:  
   `git clone https://github.com/TipTailor/data_acquisition`  
   `cd data_acquisition`

2. Install Python dependencies (create venv in repo):
   `python3 -m venv venv/`
   `source venv/bin/activate`
   `pip install -r requirements.txt`

3. Update database credentials in `db_setup.py` and `query_data` under `DB_CREDENTIALS`.

4. Ensure PostgreSQL is installed with PostGIS enabled.

5. Run the pipeline:  
   `python main.py`

6. Open the map:  
   View the generated `data/map.html` in any browser to explore museums in Münster.

---

## Future Enhancements

1. Add route optimization for multi-stop journeys.
2. Allow users to specify custom points of interest.
3. Enable real-time updates from OpenStreetMap.