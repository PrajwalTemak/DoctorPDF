from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import subprocess
from typing import List

# Existing imports
from convert_image import convert_image_to_pdf
from convert_text import convert_text_to_pdf
from convert_office import convert_office_to_pdf
from convert_pdf_to_image import convert_pdf_to_images


app = FastAPI(title="DoctorPDF API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- NEW UTILITY FUNCTIONS ---

def run_pdftk(command: List[str]):
    try:
        subprocess.run(['pdftk'] + command, check=True)
        return True
    except Exception as e:
        print(f"PDFtk Error: {e}")
        return False


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

# --- NEW MERGE & SPLIT ENDPOINTS ---

@app.post("/pdf/merge")
async def api_merge_pdfs(files: List[UploadFile] = File(...)):
    """Merges multiple PDF files into one in the order they are uploaded."""
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="At least two files are required for merging.")
    
    temp_files = []
    try:
        # Save all uploaded files to temp paths
        for file in files:
            temp_path = f"merge_tmp_{file.filename}"
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            temp_files.append(temp_path)
        
        output_pdf = "merged_output.pdf"
        # pdftk file1.pdf file2.pdf cat output merged.pdf
        if run_pdftk(temp_files + ["cat", "output", output_pdf]):
            return FileResponse(output_pdf, media_type="application/pdf", filename="merged.pdf")
        
        raise HTTPException(status_code=500, detail="PDF Merge failed")
    
    finally:
        # Cleanup temp files
        for path in temp_files:
            if os.path.exists(path): os.remove(path)

@app.post("/pdf/split")
async def api_split_pdf(
    file: UploadFile = File(...), 
    page_range: str = Form(..., description="Example: '1-3' or '1-end'")
):
    """Extracts a specific page range from a PDF."""
    temp_input = f"split_tmp_{file.filename}"
    output_pdf = f"split_{page_range}_{file.filename}"
    
    try:
        with open(temp_input, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # pdftk input.pdf cat 1-3 output output.pdf
        if run_pdftk([temp_input, "cat", page_range, "output", output_pdf]):
            return FileResponse(output_pdf, media_type="application/pdf", filename=output_pdf)
        
        raise HTTPException(status_code=500, detail="PDF Split failed. Check your page range format.")
    
    finally:
        if os.path.exists(temp_input): os.remove(temp_input)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)