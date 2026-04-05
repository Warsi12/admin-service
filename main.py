from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from math import radians, sin, cos, sqrt, atan2
from urllib.parse import unquote
import threading
import time
import requests
from sqlalchemy.orm import Session
import models, schemas, security
from database import engine, get_db

# Tables will be created on startup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # or ["https://typebot.io"] for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from typing import List

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
            "/nearest/{lat_lon}": "GET - Find nearest mechanics by lat,lng (path variable format)",
            "/emergency-request": "POST - Create an emergency request",
            "/emergency-request/history/{phone_number}": "GET - List history of emergency requests",
            "/list_requests": "GET - List requests by query parameter (phone_number)"
        }
    }

# Nearest mechanic endpoint with path variable
@app.get("/nearest/{lat_lon}")
async def get_nearest(lat_lon: str, db: Session = Depends(get_db)):
    # Try to split the lat_lon string into lat and lon
    try:
        decoded = unquote(lat_lon)
        lat_str, lon_str = decoded.split(",")
        lat = float(lat_str)
        lon = float(lon_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid lat_lon format. It should be 'lat,lon' (e.g., '28.6110,77.3355')")

    # Fetch mechanics from DB (only ONLINE ones)
    db_mechanics = db.query(models.MechanicProfile).filter(models.MechanicProfile.status == "ONLINE").all()
    print(db_mechanics)
    distances = []
    for m in db_mechanics:
        if not m.current_location:
            continue
        try:
            m_lat_str, m_lon_str = m.current_location.split(",")
            m_lat = float(m_lat_str)
            m_lng = float(m_lon_str)
            
            d = distance(lat, lon, m_lat, m_lng)
            # Find associated user name from join or if we just want to return what we have
            # For now, let's assume we want to return the mechanic's details we have
            distances.append({
                "id": str(m.id),
                "name": m.name,
                "lat": m_lat,
                "lng": m_lng,
                "distance_km": round(d, 2),
                "rating": float(m.rating) if m.rating else 0.0,
                "status": m.status
            })
        except (ValueError, AttributeError):
            continue

    # Sort by distance & return nearest 3
    distances.sort(key=lambda x: x["distance_km"])
    return distances[:3]

@app.post("/emergency-request", response_model=schemas.EmergencyRequestResponse)
def create_emergency_request(request: schemas.EmergencyRequestCreate, db: Session = Depends(get_db)):
    new_request = models.EmergencyRequest(
        customer_phone_number=request.customer_phone_number,
        location=request.location,
        service_type=request.service_type,
        vehicle_type=request.vehicle_type,
        description=request.description,
        status="PENDING"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@app.get("/emergency-request/history/{phone_number}", response_model=List[schemas.EmergencyRequestResponse])
def get_emergency_history(phone_number: str, db: Session = Depends(get_db)):
    history = db.query(models.EmergencyRequest).filter(
        models.EmergencyRequest.customer_phone_number == phone_number
    ).order_by(models.EmergencyRequest.created_at.desc()).all()
    return history

@app.get("/list_requests", response_model=List[schemas.EmergencyRequestResponse])
def list_requests(phone_number: str, db: Session = Depends(get_db)):
    history = db.query(models.EmergencyRequest).filter(
        models.EmergencyRequest.customer_phone_number == phone_number
    ).order_by(models.EmergencyRequest.created_at.desc()).all()
    return history



# -------------------- AUTH ENDPOINTS --------------------

@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.phone_number == user.phone_number).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    hashed_password = security.get_password_hash(user.password)
    new_user = models.User(
        phone_number=user.phone_number, 
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.phone_number == user.phone_number).first()
    if not db_user or not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password",
        )
    return {
        "message": "Login successful", 
        "user": {
            "id": db_user.id, 
            "phone_number": db_user.phone_number,
            "full_name": db_user.full_name
        }
    }

# -------------------- SELF-PING JOB --------------------
PING_URL = "https://admin-service-ve96.onrender.com/"
def ping_self():
    while True:
        try:
            requests.get(PING_URL, timeout=10)
            print("Self ping sent")
        except Exception as e:
            print("Ping failed:", e)
        time.sleep(180)  # every 5 minutes

@app.on_event("startup")
def startup_event():
    print("--- STARTUP: Initializing database ---")
    try:
        models.Base.metadata.create_all(bind=engine)
        print("--- STARTUP: Database initialization complete ---")
    except Exception as e:
        print(f"--- STARTUP: Database initialization FAILED: {e} ---")
    
    # Start the self-ping job
    thread = threading.Thread(target=ping_self, daemon=True)
    thread.start()
# ------------------------------------------------------
