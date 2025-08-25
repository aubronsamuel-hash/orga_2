from fastapi import FastAPI

from .db import engine
from .models import Base
from .routers import auth, availability, missions, technicians

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(technicians.router)
app.include_router(missions.router)
app.include_router(availability.router)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return {}
