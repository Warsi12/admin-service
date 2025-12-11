from fastapi import FastAPI, Query
from math import radians, sin, cos, sqrt, atan2
import threading
import time
import requests
app = FastAPI()



PING_URL = "https://admin-service-ve96.onrender.com/"   # your Render URL

def keep_alive():
    while True:
        try:
            requests.get(PING_URL, timeout=10)
            print("Pinged to keep service awake")
        except Exception as e:
            print("Ping failed:", e)
        time.sleep(300)  # 300 sec = 5 minutes


@app.on_event("startup")
def start_keep_alive():
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()


@app.get("/")
def root():
    return {
        "message": "MechieBro Admin Service API",
        "endpoints": {
            "/nearest": "GET - Find nearest mechanics by lat/lng coordinates"
        }
    }


# ---- Dummy mechanic data stored in Python (You can replace with DB later) ----
mechanics = [
    {
        "id": 1,
        "name": "Mechanic Faraz",
        "lat": 28.6110459,
        "lng": 77.3355300,
        "phone": "9999999991"
    },
    {
        "id": 2,
        "name": "Mechanic Shoaib",
        "lat": 28.6119292,
        "lng": 77.3353148,
        "phone": "9999999992"
    },
    {
        "id": 3,
        "name": "Mechanic Irfan",
        "lat": 28.6114247,
        "lng": 77.3355300,
        "phone": "9999999993"
    },
    {
        "id": 4,
        "name": "Mechanic D",
        "lat": 28.6300,
        "lng": 77.2150,
        "phone": "9999999994"
    },
]


# ---- Haversine formula to calculate distance ----
def distance(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat /
            2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


@app.get("/nearest")
def get_nearest(lat: float = Query(...), lng: float = Query(...)):
    distances = []

    for m in mechanics:
        d = distance(lat, lng, m["lat"], m["lng"])
        distances.append({"name": m["name"], "lat": m["lat"], "lng": m["lng"], "phone": m["phone"], "distance_km": round(d, 2)})

    # sort by distance & return nearest 3
    distances.sort(key=lambda x: x["distance_km"])
    return [{"name": m["name"], "lat": m["lat"], "lng": m["lng"], "phone": m["phone"], "distance_km": m["distance_km"]} for m in distances[:3]]
