# **TripTailor: Dynamic Travel Route Optimization**

## **Overview**

**TripTailor** is a powerful travel route optimization tool that uses open-source geographic data to create dynamic, accurate travel routes. By leveraging public datasets, TripTailor ensures an up-to-date and highly reliable platform for travelers.

---

## **Key Features**

- **Dynamic Route Updates**: Seamlessly integrates with OpenStreetMap (OSM) data for real-time updates.
- **Interactive Mapping**: Visualizes museum data on an interactive, user-friendly map.

---

## **Data**

The project tries to combine different data sources for the route algorithm and visualization.
This project skeleton uses [OSM data](https://opendata.stadt-muenster.de/dataset/openstreetmaps-rohdaten-f%C3%BCr-m%C3%BCnster) for the beginning. 

---

## **Getting Started**

Follow these steps to set up and use TripTailor:

### **1. Clone the Repository**
```bash
git clone https://github.com/TipTailor/data_acquisition
cd data_acquisition
```

### **2. Set Up a Virtual Environment**
```bash
python3 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
```

### **3. Configure Database Credentials**
Update the following files with your database credentials:
`db_setup.py` and `query_data.py` under `DB_CREDENTIALS`

### **4. Install and Configure PostgreSQL**
Ensure PostgreSQL is installed and has **PostGIS** enabled.

### **5. Run the Data Pipeline**
```bash
python main.py
```

### **6. View the Interactive Map**
Open the generated file `data/map.html` in any web browser to explore museums in Münster.

---

## **Planned Enhancements**

1. 🌍 **Multi-Stop Route Optimization**: Add functionality to optimize journeys with multiple stops.
2. 📌 **Custom Points of Interest**: Enable users to specify personalized locations of interest.
3. 🔄 **Real-Time Updates**: Incorporate live updates directly from OpenStreetMap.
