from flask import Flask
from PIL import Image
import pytesseract
from minio import Minio

app = Flask(__name__)

@app.route('/')
def ocr():
    # test.png from the pytesseract project: https://github.com/madmaze/pytesseract/tree/master/tests/data
    
    client = Minio("minio-server-lrgd.onrender.com",
        access_key="vG+Csz1r01GQJPlHR6rybVB/1UpJ6iN/UEI75X48Kgw=",
        secret_key="bdklcAgSv2W9OLic7eelfdWcu/tQjuONKoWtp47P35s=",
    )

    bucket_name = "hact-reports"
    #bucket_name = "prodocs"

    objects = client.list_objects(bucket_name)
    for obj in objects:
        print(obj)

    return pytesseract.image_to_string(Image.open('test.png'))
