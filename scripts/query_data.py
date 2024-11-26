import psycopg2
import json

# Replace credentials if necessary
DB_CREDENTIALS = {
    "user": "postgres",
    "password": "****",
    "host": "localhost",
    "port": "4321",
    "dbname": "osm_data"
}

def query_museum_data(city):
    query = """
    SELECT 
        *, 
        ST_AsGeoJSON(way) AS geometry, 
        CONCAT(tags->'addr:street', ' ', tags->'addr:housenumber') AS address
    FROM 
        planet_osm_polygon
    WHERE 
        tags->'addr:city' = 'Münster' 
        AND tourism = 'museum';"""

    try:
        conn = psycopg2.connect(**DB_CREDENTIALS)
        cursor = conn.cursor()
        cursor.execute(query, (city,))
        rows = cursor.fetchall()

        if not rows:
            print(f"No data found for museums in the city: {city}")
            return False

        geojson_features = []
        for row in rows:
            properties = dict(zip([desc[0] for desc in cursor.description], row))
            geojson_features.append({
                "type": "Feature",
                "geometry": None,  # No geometry since it's removed
                "properties": properties
            })

        geojson_data = {"type": "FeatureCollection", "features": geojson_features}

        # Save GeoJSON to file
        with open("data/museums.geojson", "w") as f:
            json.dump(geojson_data, f, indent=2)
        print("Query results saved to 'data/museums.geojson'")

        cursor.close()
        conn.close()
        return True

    except psycopg2.Error as e:
        print(f"Database query error: {e}")
        return False

if __name__ == "__main__":
    city_name = "Münster"
    query_museum_data(city_name)