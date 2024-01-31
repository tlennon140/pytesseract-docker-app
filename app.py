import os
import io
from pdf2image import convert_from_bytes
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
    processed_bucket_name = "processed-hact-reports"

    total_pdfs = sum(1 for obj in client.list_objects(bucket_name, recursive=True) if obj.object_name.endswith(".pdf"))
    processed_pdfs_count = 0  # Assuming starting from 0

    # Main processing loop
    total_pdfs = sum(1 for obj in client.list_objects(bucket_name, recursive=True) if obj.object_name.endswith(".pdf"))

    objects = client.list_objects(bucket_name, recursive=True)
    for obj in objects:
        print(obj.object_name)
        cumulative_text=""
        response = client.get_object(bucket_name, obj.object_name)
        pdf_stream = io.BytesIO(response.read())
        pages = convert_from_bytes(pdf_stream.read())
        
        for page_number, image in enumerate(pages):
            text = pytesseract.image_to_string(image)
            cumulative_text+=" "+text

        text_filename = obj.object_name.split('.')[0] + ".txt"  # Change the extension to .txt
        text_file_stream = io.BytesIO(cumulative_text.encode())  # Convert string to bytes

        client.put_object(
            bucket_name=processed_bucket_name,
            object_name=text_filename,
            data=text_file_stream,
            length=text_file_stream.getbuffer().nbytes,
            content_type='text/plain'
        )
        

    return pytesseract.image_to_string(Image.open('test.png'))
