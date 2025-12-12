from fastapi import FastAPI, Request
from math import radians, sin, cos, sqrt, atan2
from urllib.parse import unquote
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
import threading
import time
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # or ["https://typebot.io"] for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy mechanic data stored in Python (You can replace with DB later)
mechanics = [
    {"id": 1, "name": "Mechanic Faraz", "lat": 28.6110459, "lng": 77.3355300, "phone": "9999999991"},
    {"id": 2, "name": "Mechanic Shoaib", "lat": 28.6119292, "lng": 77.3353148, "phone": "9999999992"},
    {"id": 3, "name": "Mechanic Irfan", "lat": 28.6114247, "lng": 77.3355300, "phone": "9999999993"},
    {"id": 4, "name": "Mechanic D", "lat": 28.6300, "lng": 77.2150, "phone": "9999999994"},
]

# Haversine formula to calculate distance
def distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

@app.get("/")
def root():
    return {
        "message": "MechieBro Admin Service API",
        "endpoints": {
            "/nearest/{lat_lon}": "GET - Find nearest mechanics by lat,lng (path variable format)"
        }
    }

# Nearest mechanic endpoint with path variable
@app.get("/nearest/{lat_lon}")
async def get_nearest(lat_lon: str):
    # Try to split the lat_lon string into lat and lon
    try:
        decoded = unquote(lat_lon)
        print("DECODED "+decoded)
        lat_str, lon_str = decoded.split(",")
        lat = float(lat_str)
        lon = float(lon_str)
    except ValueError:
        return {"error": "Invalid lat_lon format. It should be 'lat,lon' (e.g., '28.6110,77.3355')"}

    distances = []
    for m in mechanics:
        d = distance(lat, lon, m["lat"], m["lng"])
        distances.append({
            "name": m["name"],
            "lat": m["lat"],
            "lng": m["lng"],
            "phone": m["phone"],
            "distance_km": round(d, 2)
        })

    # Sort by distance & return nearest 3
    distances.sort(key=lambda x: x["distance_km"])
    return [
        {
            "name": m["name"],
            "lat": m["lat"],
            "lng": m["lng"],
            "phone": m["phone"],
            "distance_km": m["distance_km"]
        }
        for m in distances[:3]
    ]



# -------------------- SELF-PING JOB --------------------
PING_URL = "https://admin-service-ve96.onrender.com/"
def ping_self():
    while True:
        try:
            requests.get(PING_URL, timeout=10)
            print("Self ping sent")
        except Exception as e:
            print("Ping failed:", e)
        time.sleep(300)  # every 5 minutes

@app.on_event("startup")
def start_pinger():
    thread = threading.Thread(target=ping_self, daemon=True)
    thread.start()
# ------------------------------------------------------
