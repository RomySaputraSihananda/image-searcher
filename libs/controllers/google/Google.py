import uuid
import os

from fastapi import  File, UploadFile, APIRouter

from libs import Google

router = APIRouter()

@router.post('/search')
async def upload(gambar: UploadFile = File(...)):
    name = str(uuid.uuid4()) + '.' + gambar.filename.split('.')[-1]
    with open(f'img/{name}', 'wb') as f:
        f.write(gambar.file.read())

    data = Google().start(f'{os.getcwd()}/img/{name}')

    os.remove(f'{os.getcwd()}/img/{name}')

    return data
