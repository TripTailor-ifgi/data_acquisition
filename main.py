import os
from scripts import getOSM, db_setup, query_data, visualize_map


def main():
    print("Starting OSM processing pipeline...")

    # Step 1: Download the OSM data
    getOSM.download_osm_data(
        "https://download.geofabrik.de/europe/germany/nordrhein-westfalen/muenster-regbez-latest.osm.pbf",
        "data/muenster-regbez-latest.osm.pbf"
    )

    # Step 2: Create the database
    db_setup.create_database()

    # Step 3: Enable PostGIS and hstore extensions
    db_setup.enable_extensions()

    # Step 4: Import OSM data
    db_setup.load_osm_data("data/muenster-regbez-latest.osm.pbf")

    # Step 5: Query the database for museums in Münster
    success = query_data.query_museum_data("Münster")
    if not success:
        print("No museums found in Münster. Skipping visualization.")
        return

    # Step 6: Visualize the queried data on a map
    visualize_map.generate_leaflet_map("data/museums.geojson")

    print("Pipeline completed successfully!")


if __name__ == "__main__":
    main()