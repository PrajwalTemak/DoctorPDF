import subprocess

def merge_pdfs(input_paths, output_path):
    """
    Merges multiple PDFs into one using PDFtk.
    input_paths: List of strings (paths to PDFs)
    output_path: String (path for the resulting merged PDF)
    """
    try:
        # pdftk file1.pdf file2.pdf cat output merged.pdf
        command = ['pdftk'] + input_paths + ['cat', 'output', output_path]
        
        subprocess.run(command, check=True)
        return True
    except Exception as e:
        print(f"PDF Merge Error: {e}")
        return False