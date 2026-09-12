from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.routes import auth, analyze, history
from app.db.session import engine, Base

# Create tables for MVP
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, should be restricted in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "An unexpected server error occurred."}},
    )

@app.get(f"{settings.API_V1_STR}/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(analyze.router, prefix=f"{settings.API_V1_STR}/analyze", tags=["analyze"])
app.include_router(history.router, prefix=f"{settings.API_V1_STR}/history", tags=["history"])
