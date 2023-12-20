import uvicorn
from fastapi import FastAPI

from libs.controllers import googleController
from libs.controllers import bingController

app: FastAPI = FastAPI(title='Image-Searcher', version='v1.0.0', description='image searcher using google and bing')

app.include_router(googleController.router, prefix="/google", tags=["Google Search image"])
app.include_router(bingController.router, prefix="/bing", tags=["Bing Search image"])

if(__name__ == "__main__"):
    uvicorn.run(app, port=4444)