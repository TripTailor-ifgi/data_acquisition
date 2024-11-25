import os
import subprocess
import psycopg2

# Replace credentials if necessary
DB_CREDENTIALS = {
    "user": "postgres",
    "password": "****",
    "host": "localhost",
    "port": "5432",
    "dbname": "osm_data"
}

def create_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_CREDENTIALS["user"],
        password=DB_CREDENTIALS["password"],
        host=DB_CREDENTIALS["host"],
        port=DB_CREDENTIALS["port"]
    )
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {DB_CREDENTIALS['dbname']};")
        print(f"Database '{DB_CREDENTIALS['dbname']}' created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database '{DB_CREDENTIALS['dbname']}' already exists.")
    finally:
        cursor.close()
        conn.close()

def enable_extensions():
    conn = psycopg2.connect(
        dbname=DB_CREDENTIALS["dbname"],
        user=DB_CREDENTIALS["user"],
        password=DB_CREDENTIALS["password"],
        host=DB_CREDENTIALS["host"],
        port=DB_CREDENTIALS["port"]
    )
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
        print("PostGIS extension enabled successfully.")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS hstore;")
        print("Hstore extension enabled successfully.")
    except psycopg2.Error as e:
        print(f"Error enabling extensions: {e}")
    finally:
        cursor.close()
        conn.close()

def load_osm_data(osm_file, lua_script=None):
    # Set the PGPASSWORD environment variable to avoid password prompts
    os.environ["PGPASSWORD"] = DB_CREDENTIALS["password"]

    # Construct the osm2pgsql command
    command = [
        "osm2pgsql",
        "--create",             # Mode (create or append)
        "--output=pgsql",       # Use pgsql output mode for default schema
        "-d", DB_CREDENTIALS["dbname"],  # PostgreSQL database name
        "-U", DB_CREDENTIALS["user"],    # PostgreSQL username
        "-H", DB_CREDENTIALS["host"],    # Host
        "-P", DB_CREDENTIALS["port"],    # PostgreSQL port
        "--slim",               # Use slim tables to reduce memory usage
        "--hstore",             # Include tags in an hstore column
        osm_file                # Input OSM file
    ]

    # Run osm2pgsql to import data
    try:
        subprocess.run(command, check=True, text=True)
        print("OSM data imported successfully using osm2pgsql.")
    except subprocess.CalledProcessError as e:
        print(f"Error running osm2pgsql: {e}")
        raise

def verify_import():
    try:
        conn = psycopg2.connect(
            dbname=DB_CREDENTIALS["dbname"],
            user=DB_CREDENTIALS["user"],
            password=DB_CREDENTIALS["password"],
            host=DB_CREDENTIALS["host"],
            port=DB_CREDENTIALS["port"]
        )
        cursor = conn.cursor()

        # Example query to count imported rows in planet_osm_polygon
        cursor.execute("SELECT COUNT(*) FROM planet_osm_polygon;")
        count = cursor.fetchone()[0]
        print(f"Total polygons imported: {count}")

        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")

if __name__ == "__main__":
    create_database()            # Step 1: Create the database
    enable_extensions()          # Step 2: Enable PostGIS and hstore extensions
    load_osm_data(               # Step 3: Import OSM data
        "../data/muenster-regbez-latest.osm.pbf"
    )
    verify_import()              # Step 4: Verify the data import