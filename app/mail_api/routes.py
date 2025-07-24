from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import AlertRequest, User
from services.email_sender import send_email
from services.logic_helper import format_date_human
from sqlalchemy import text

router = APIRouter()


@router.get(
    "/",
    summary="API Welcome",
    description="Returns a welcome message for the TerraGuard Mailer API.",
    tags=["General"],
    response_model=None,
)
def home():
    return {"message": "Welcome to TerraGuard Mailer API"}


@router.post(
    "/api/send-alert",
    summary="Send disaster alert email to users",
    description=(
        "Send disaster alert emails to users based on their location. "
        "Each alert includes a date and its corresponding disaster probability percentage. "
        "If no users are found in the location or the percentage is below threshold, no alert is sent."
    ),
    tags=["Alerts"],
    response_model=None,
    status_code=status.HTTP_200_OK,
)


def send_alert(data: AlertRequest, db: Session = Depends(get_db)):
    try:
        alert_date = data.date
        percentage = data.percentage

        query = text("SELECT email FROM users WHERE location = :loc")
        users = db.execute(query, {"loc": data.location}).fetchall()

        if not users:
            return {"message": "No users found at this location."}
        if len(alert_date) != len(percentage):
            return {"error": "Date and percentage lists must be of the same length."}

        for user in users:
            try:
                if len(alert_date) == 1:
                    readable_date = format_date_human(alert_date[0])
                    body = f"There is a {percentage[0]}% chance of a flood on the {readable_date} in {data.location}. Stay alert!"
                else:
                    paired_alerts = [
                        f"{p}% on the {format_date_human(d)}" for p, d in zip(percentage, alert_date)
                    ]
                    if len(paired_alerts) == 2:
                        joined = ' and '.join(paired_alerts)
                    else:
                        joined = ', '.join(paired_alerts[:-1]) + f", and {paired_alerts[-1]}"
                    body = f"Flood chances: {joined} in {data.location}. Stay alert!"

                send_email(
                    to_email=user[0],
                    subject=f"Disaster Alert for {data.location}",
                    body=body
                )
            except Exception as e:
                return {"error": f"Failed to send email to {user[0]}: {str(e)}"}

        return {"message": f"Sent alert to {len(users)} users"}
    except Exception as e:
        return {"error": str(e)}


@router.post(
    "/api/hello",
    summary="Send a test email",
    description="Sends a test email with a greeting message to a given user.",
    tags=["Test"],
    response_model=None,
    status_code=status.HTTP_200_OK,
)
def mailer(data: User):
    try:
        send_email(
            to_email=data.email,
            subject="Hello from TerraGuard",
            body=f"Hi {data.name},\nYou’ll get early warnings if there's a predicted flood or Landslide risk near you. Stay alert and stay safe!"
        )
        return {"message": "Email sent successfully"}
    except Exception as e:
        return {"error": str(e)}
 