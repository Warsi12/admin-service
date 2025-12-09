from fastapi import FastAPI, Query
from math import radians, sin, cos, sqrt, atan2

app = FastAPI()

# ---- Dummy mechanic data stored in Python (You can replace with DB later) ----
mechanics = [
    {"id": 1, "name": "Mechanic A", "lat": 28.6139, "lng": 77.2090, "phone": "9999999991"},
    {"id": 2, "name": "Mechanic B", "lat": 28.6120, "lng": 77.2050, "phone": "9999999992"},
    {"id": 3, "name": "Mechanic C", "lat": 28.6200, "lng": 77.2000, "phone": "9999999993"},
    {"id": 4, "name": "Mechanic D", "lat": 28.6300, "lng": 77.2150, "phone": "9999999994"},
]

# ---- Haversine formula to calculate distance ----
def distance(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

@app.get("/nearest")
def get_nearest(lat: float = Query(...), lng: float = Query(...)):
    distances = []

    for m in mechanics:
        d = distance(lat, lng, m["lat"], m["lng"])
        distances.append({**m, "distance_km": round(d, 2)})

    # sort by distance & return nearest 3
    distances.sort(key=lambda x: x["distance_km"])
    return distances[:3]
