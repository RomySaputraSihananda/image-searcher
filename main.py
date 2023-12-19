from typing import Union

from fastapi import FastAPI, File, UploadFile, templating, Request

app = FastAPI()

template = templating.Jinja2Templates(directory='templates')

@app.get("/")
def read_root(request: Request):
    return template.TemplateResponse('index.html', { 'request': request })

@app.post('/upload')
async def upload(gambar: UploadFile = File(...)):
    with open(gambar.filename, 'wb') as f:
        f.write(gambar.file.read())

    return { "filename":  gambar.filename}