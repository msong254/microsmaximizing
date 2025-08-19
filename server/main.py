from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.api.routes import router  # ✅ THIS imports your routes

app = FastAPI()

# ✅ Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include the real routes under the /api path
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Hello from Render — backend is connected!"}