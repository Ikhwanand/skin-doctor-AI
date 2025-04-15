import sys 
from pathlib import Path 

sys.path.append(str(Path(__file__).parent.parent))


from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import router as api_router 
from app.core.config import settings
from app.core.exceptions import app_exception_handler, AppException
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Skin Doctor API Documentation"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)

# API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__=="__main__":
    uvicorn.run("app.main:app", port=8000, reload=True)