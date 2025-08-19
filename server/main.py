from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router  # correct import near top

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend is live now!"}