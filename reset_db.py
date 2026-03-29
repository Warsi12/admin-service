from database import engine, Base
import models

def reset_db():
    print("Dropping all existing tables...")
    # This will drop all tables defined in models.py
    Base.metadata.drop_all(bind=engine)
    print("Recreating tables...")
    # This will recreate all tables defined in models.py
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully!")

if __name__ == "__main__":
    reset_db()
