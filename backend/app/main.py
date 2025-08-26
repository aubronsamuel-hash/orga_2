from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse, PlainTextResponse

from .db import engine
from .models import Base
from .routers import auth, availability, missions, technicians
from .settings import settings

app = FastAPI(title="CCW API", openapi_url=f"{settings.api_prefix}/openapi.json")

# Include routers under prefix

app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(technicians.router, prefix=settings.api_prefix)
app.include_router(missions.router, prefix=settings.api_prefix)
app.include_router(availability.router, prefix=settings.api_prefix)


@app.get("/healthz")
def healthz():
    # ensure DB is reachable (create tables if sqlite dev)
    try:
        Base.metadata.create_all(bind=engine)
        return {"status": "ok"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "error": str(e)})


@app.get("/metrics", response_class=PlainTextResponse)
def metrics_placeholder():
    return "# placeholder metrics\nccw_up 1"


# simple dependency to read X-User-Id if provided (not enforced)

def current_user_id(x_user_id: str | None = Header(default=None, alias="X-User-Id")) -> str | None:
    return x_user_id
