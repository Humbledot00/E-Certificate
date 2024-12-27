import PyPDF2
from PyPDF2 import PdfReader, PdfWriter

def get_pdf_dimensions(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        page = pdf_reader.pages[0]
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        return width, height

def scale_page_content(page, scale_factor):
    page.scale_by(scale_factor)

def resize_pdf(input_pdf, output_pdf, target_width, target_height):
    with open(input_pdf, 'rb') as f:
        pdf_reader = PdfReader(f)
        pdf_writer = PdfWriter()
        
        for page in pdf_reader.pages:
            # Get original page dimensions
            orig_width = float(page.mediabox.width)
            orig_height = float(page.mediabox.height)
            
            # Calculate scale factor (preserving aspect ratio)
            scale_factor = min(target_width / orig_width, target_height / orig_height)
            
            # Scale the page content
            scale_page_content(page, scale_factor)
            
            # Add the resized page to the writer
            pdf_writer.add_page(page)
        
        # Write the final resized PDF to output
        with open(output_pdf, 'wb') as out_f:
            pdf_writer.write(out_f)

# Paths to original and updated PDFs
original_pdf_path = 'Certificate.pdf'
updated_pdf_path = 's.pdf'
output_pdf_path = 'final_certificate.pdf'

# Get dimensions of the original PDF
orig_width, orig_height = get_pdf_dimensions(original_pdf_path)

# Resize the updated PDF to match the original PDF's dimensions
resize_pdf(updated_pdf_path, output_pdf_path, orig_width, orig_height)

print(f"The updated PDF has been resized to match the original dimensions: {orig_width} x {orig_height}")
