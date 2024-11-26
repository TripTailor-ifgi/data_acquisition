import os
import requests

def download_osm_data(url, output_path):
    if os.path.exists(output_path):
        print(f"File already exists at {output_path}. Skipping download.")
        return
    print(f"Starting download from {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Download complete. File saved to {output_path}")
    else:
        print(f"Failed to download data. HTTP Status Code: {response.status_code}")

if __name__ == "__main__":
    osm_url = "https://download.geofabrik.de/europe/germany/nordrhein-westfalen/muenster-regbez-latest.osm.pbf"
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    output_file = os.path.join(data_dir, "muenster-regbez-latest.osm.pbf")
    download_osm_data(osm_url, output_file)