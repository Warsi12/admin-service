from database import engine, Base
import models

def reset_db():
    print("Dropping existing table 'users_web'...")
    # This will drop the 'users_web' table if it exists
    models.User.__table__.drop(bind=engine, checkfirst=True)
    print("Recreating tables...")
    # This will recreate all tables defined in models.py
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully!")

if __name__ == "__main__":
    reset_db()
