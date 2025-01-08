import json
import os

def generate_leaflet_map(geojson_file):
    if not os.path.exists(geojson_file):
        print(f"Error: GeoJSON file '{geojson_file}' not found.")
        return

    with open(geojson_file, "r") as f:
        geojson_data = json.load(f)

    # Extract geometry directly from `properties["geometry"]`
    for feature in geojson_data["features"]:
        try:
            feature["geometry"] = json.loads(feature["properties"]["geometry"])
        except (json.JSONDecodeError, KeyError, TypeError):
            print(f"Invalid geometry for feature: {feature['properties'].get('name', 'Unknown')}")
            feature["geometry"] = None

    # Filter out features with invalid or missing geometries
    geojson_data["features"] = [
        feature for feature in geojson_data["features"] if feature["geometry"]
    ]

    # Leaflet map HTML content
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
          var map = L.map('map').setView([51.95, 7.62], 12);

          L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19,
            attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
          }}).addTo(map);

          var geojsonData = {json.dumps(geojson_data)};

          L.geoJSON(geojsonData, {{
              style: function (feature) {{
                  return {{
                      color: "#3388ff",
                      weight: 2,
                      fillOpacity: 0.5
                  }};
              }},
              onEachFeature: function (feature, layer) {{
                  if (feature.properties) {{
                      const popupContent = `
                          <strong>${{feature.properties.name || "No Name"}}</strong><br>
                          Address: ${{feature.properties.address || "N/A"}}
                      `;
                      layer.bindPopup(popupContent);
                  }}
              }}
          }}).addTo(map);
        </script>
      </body>
    </html>
    '''

    output_path = os.path.join(os.path.dirname(geojson_file), "map.html")
    with open(output_path, "w") as f:
        f.write(html_content)
    print(f"Map saved to '{output_path}'")


if __name__ == "__main__":
    generate_leaflet_map("data/museums.geojson")