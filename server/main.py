 
from fastapi import FastAPI
from server.api.routes import router

app = FastAPI()
app.include_router(router, prefix="/api")
Root health check route
@app.get("/")
def root():
    return {"message": "Backend is running"}

# Include API routes
app.include_router(router, prefix="/api")
