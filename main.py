from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from convert_pdf_to_image import convert_pdf_to_images
import os
import shutil

# Importing your separate files
from convert_image import convert_image_to_pdf
from convert_text import convert_text_to_pdf
from convert_office import convert_office_to_pdf

app = FastAPI(title="DoctorPDF API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convert/image")
async def api_image_to_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        pdf_bytes = convert_image_to_pdf(content)
        output_name = f"converted_{file.filename}.pdf"
        with open(output_name, "wb") as f:
            f.write(pdf_bytes)
        return FileResponse(output_name, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/convert/text")
async def api_text_to_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode("utf-8")
        output_name = "text_output.pdf"
        convert_text_to_pdf(text, output_name)
        return FileResponse(output_name, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/convert/office")
async def api_office_to_pdf(file: UploadFile = File(...)):
    # Works for both .docx and .pptx
    temp_input = f"temp_{file.filename}"
    with open(temp_input, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    if convert_office_to_pdf(temp_input, "."):
        output_pdf = temp_input.rsplit('.', 1)[0] + ".pdf"
        return FileResponse(output_pdf, media_type="application/pdf")
    raise HTTPException(status_code=500, detail="Office conversion failed")

@app.post("/convert/pdf-to-image")
async def api_pdf_to_image(file: UploadFile = File(...)):
    try:
        # Read the PDF file content
        content = await file.read()
        
        # Convert PDF to a list of image bytes (one for each page)
        image_list = convert_pdf_to_images(content)
        
        if not image_list:
            raise HTTPException(status_code=400, detail="Could not extract images from PDF")

        # For now, let's return the first page of the PDF as a JPEG
        output_name = f"page_1_{file.filename.rsplit('.', 1)[0]}.jpg"
        with open(output_name, "wb") as f:
            f.write(image_list[0])
            
        return FileResponse(output_name, media_type="image/jpeg", filename="converted_page.jpg")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF to Image Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)