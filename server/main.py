from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.api.routes import router  # Import your router

app = FastAPI()

# Enable CORS so frontend can access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the API routes at /api
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Hello from Render!"}