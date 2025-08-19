from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI()

# ✅ Add this block for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://msong254.github.io"],  # Only your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")