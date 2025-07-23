from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.schemas import AlertRequest
from app.services.email_sender import send_email
from sqlalchemy import text

router = APIRouter()
@router.get("/")
def home():
    return {"message": "Welcome to TerraGuard Mailer API"}

@router.post("/send-alert")
def send_alert(data: AlertRequest, db: Session = Depends(get_db)):
    try:
        alert_date = datetime.strptime(data.date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    today = datetime.today().date()
    if not (today <= alert_date <= today + timedelta(days=7)):
        return {"message": "Email not sent, date above 7 days."}

    if data.percentage < 60:
        return {"message": "Percentage too low. No alert sent."}

    query = text("SELECT email FROM users WHERE location = :loc")
    users = db.execute(query, {"loc": data.location}).fetchall()

    if not users:
        return {"message": "No users found at this location."}

    for user in users:
        send_email(
            to_email=user[0], 
            subject=f"Disaster Alert for {data.location}",
            body=f"There is a {data.percentage}% chance of a disaster on {data.date}. Stay alert!"
        )

    return {"message": f"Sent alert to {len(users)} users"}
