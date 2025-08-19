from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.api.routes import router  # <- this imports your real API routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")  # <- mount all your API endpoints under /api

@app.get("/")
def root():
    return {"message": "Hello from Render — API connected!"}