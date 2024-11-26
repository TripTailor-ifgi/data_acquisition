import json
import os
from pyproj import Transformer


def reproject_coordinates(coordinates, transformer):
    return [list(transformer.transform(x, y)) for x, y in coordinates]


def reproject_geometry(geometry, transformer):
    if geometry["type"] == "Polygon":
        # Reproject each ring of the polygon
        geometry["coordinates"] = [
            reproject_coordinates(ring, transformer) for ring in geometry["coordinates"]
        ]
    elif geometry["type"] == "MultiPolygon":
        # Reproject each polygon in the multipolygon
        geometry["coordinates"] = [
            [reproject_coordinates(ring, transformer) for ring in polygon]
            for polygon in geometry["coordinates"]
        ]
    return geometry


def generate_leaflet_map(geojson_file):
    # Resolve the path of the GeoJSON file relative to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Project root
    geojson_path = os.path.join(base_dir, geojson_file)

    if not os.path.exists(geojson_path):
        print(f"Error: GeoJSON file '{geojson_path}' not found.")
        return

    # Load the GeoJSON data
    with open(geojson_path, "r") as f:
        geojson_data = json.load(f)

    # Transformer for EPSG:3857 to EPSG:4326
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

    # Parse geometry from `properties` and reproject
    for feature in geojson_data["features"]:
        if not feature["geometry"] and feature["properties"].get("geometry"):
            geometry = feature["properties"]["geometry"]
            try:
                # Parse the geometry JSON stored as a string
                geometry = json.loads(geometry)
                # Reproject geometry
                feature["geometry"] = reproject_geometry(geometry, transformer)
            except (json.JSONDecodeError, TypeError):
                print(f"Invalid geometry for feature: {feature['properties'].get('name', 'Unknown')}")
                feature["geometry"] = None

    # Filter out features with invalid geometries
    geojson_data["features"] = [
        feature for feature in geojson_data["features"] if feature["geometry"]
    ]

    # HTML template for the map
    html_content = f'''
    <!DOCTYPE HTML>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
        <style>
          html, body {{
            height: 100%;
            padding: 0;
            margin: 0;
          }}
          #map {{
            width: 100%;
            height: 100%;
          }}
        </style>
      </head>
      <body>
        <div id="map"></div>
        <script>
          // Initialize Leaflet map
          var map = L.map('map').setView([51.95, 7.62], 12);  // Center on Münster

          // Add the OpenStreetMap tiles
          L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19,
            attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
          }}).addTo(map);

          // GeoJSON data for museums
          var geojsonData = {json.dumps(geojson_data)};

          // Add GeoJSON layer to the map
          L.geoJSON(geojsonData, {{
            onEachFeature: function (feature, layer) {{
                if (feature.properties) {{
                    const popupContent = `
                        <strong>${{feature.properties.name || "No Name"}}</strong><br>
                        Address: ${{feature.properties.address || "N/A"}}<br>
                    `;
                    layer.bindPopup(popupContent);
                }}
            }}
          }}).addTo(map);

        </script>
      </body>
    </html>
    '''
    # Save the map as an HTML file
    output_path = os.path.join(base_dir, "data/map.html")
    with open(output_path, "w") as f:
        f.write(html_content)
    print(f"Map saved to '{output_path}'")


if __name__ == "__main__":
    generate_leaflet_map("data/museums.geojson")