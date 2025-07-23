from fastapi import FastAPI
from mail_api.routes import router as alert_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TerraGuard - Flood Prediction Mailer API",
    description="An API for predicting flood likelihood based on rainfall, elevation, and soil moisture.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alert_router, prefix="")

# Vercel expects a 'handler' variable for ASGI apps
handler = app