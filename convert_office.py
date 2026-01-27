import subprocess
import os

def convert_office_to_pdf(input_path, output_folder):
    try:
        # LibreOffice command to convert docx/pptx to pdf
        command = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_folder,
            input_path
        ]
        
        # This executes the system command
        subprocess.run(command, check=True)
        return True
    except Exception as e:
        print(f"Office Conversion Error: {e}")
        return False