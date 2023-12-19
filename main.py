import uuid
import os

from typing import Union
from fastapi import FastAPI, File, UploadFile, templating, Request

from libs import Google

app = FastAPI()

template = templating.Jinja2Templates(directory='templates')

@app.get("/")
def read_root(request: Request):
    return template.TemplateResponse('index.html', { 'request': request })

@app.post('/upload')
async def upload(gambar: UploadFile = File(...)):
    name = str(uuid.uuid4()) + '.' + gambar.filename.split('.')[-1]
    with open(f'img/{name}', 'wb') as f:
        f.write(gambar.file.read())

    data = Google().start(f'{os.getcwd()}/img/{name}')

    os.remove(f'{os.getcwd()}/img/{name}')

    return data
