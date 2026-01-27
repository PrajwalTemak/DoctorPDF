import img2pdf
from PIL import Image
import io

def convert_image_to_pdf(content):
    with Image.open(io.BytesIO(content)) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        return img2pdf.convert(img_byte_arr.getvalue())