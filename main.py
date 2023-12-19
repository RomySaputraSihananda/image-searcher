from fastapi import FastAPI

from libs.controllers import Google

app = FastAPI()

app.include_router(Google.router, prefix="/google", tags=["Google Search image"])