import os
from flask import Flask
from PIL import Image
import pytesseract
from minio import Minio

app = Flask(__name__)

@app.route('/')
def ocr():
    # test.png from the pytesseract project: https://github.com/madmaze/pytesseract/tree/master/tests/data
    
    client = Minio("minio-server-lrgd.onrender.com",
        access_key=os.environ.get("MINIO_ACCESS_KEY"),
        secret_key=os.environ.get("MINIO_SECRET_KEY"),
    )

    bucket_name = "hact-reports"
    #bucket_name = "prodocs"

    objects = client.list_objects(bucket_name, recursive=True)
    for obj in objects:
        print(obj.object_name)

    return pytesseract.image_to_string(Image.open('test.png'))
