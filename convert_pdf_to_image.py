from pdf2image import convert_from_bytes
import io

def convert_pdf_to_images(pdf_content):
    # Convert PDF binary to a list of PIL Image objects
    # dpi=300 ensures high quality
    images = convert_from_bytes(pdf_content, dpi=300)
    
    output_images = []
    
    for img in images:
        img_byte_arr = io.BytesIO()
        # You can save as JPEG, PNG, or WEBP
        img.save(img_byte_arr, format='JPEG', quality=95)
        output_images.append(img_byte_arr.getvalue())
        
    return output_images