from fastapi import FastAPI
from app.mail_api.routes import router as alert_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alert_router, prefix="/api")

# Vercel expects a 'handler' variable for ASGI apps
handler = app