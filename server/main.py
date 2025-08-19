from fastapi import FastAPI
from server.api.routes import router

app = FastAPI()
app.include_router(router, prefix="/api")