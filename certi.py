from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
import os
import pandas as pd


def draw_text_on_pdf(name, event_name, output_pdf_path, font_name="Helvetica", font_size=20, name_x=0, name_y=255, event_x=0, event_y=295):
    # Create a canvas to draw text
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    c.setFont(font_name, font_size)
    font_size1 = 10 
    
    # Draw name
    name_text_width = c.stringWidth(name, font_name, font_size)
    name_position_x = (letter[0] - name_text_width) / 2 + name_x
    c.drawString(name_position_x, name_y, name)
    
    # Draw event name
    event_text_width = c.stringWidth(event_name, font_name, font_size1)
    event_position_x = (letter[0] - event_text_width) / 2 + event_x
    c.drawString(event_position_x, event_y, event_name)
    
    c.save()

def generate_certificates(input_pdf_path,usn, names, event_name, output_dir, font_name="Helvetica", font_size=20, name_x=520, name_y=255, event_x=550, event_y=325):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for usn, name in zip(usn, names):
        # Create a temporary PDF with the name and event
        temp_pdf_path = "temp.pdf"
        draw_text_on_pdf(name, event_name, temp_pdf_path, font_name, font_size, name_x, name_y, event_x, event_y)
        
        # Read the original PDF and the temporary PDF
        with open(input_pdf_path, "rb") as input_pdf_file, open(temp_pdf_path, "rb") as temp_pdf_file:
            input_pdf = PdfReader(input_pdf_file)
            temp_pdf = PdfReader(temp_pdf_file)
            
            # Create a PDF writer
            writer = PdfWriter()
            page = input_pdf.pages[0]
            temp_page = temp_pdf.pages[0]
            
            # Merge the text with the original page
            page.merge_page(temp_page)
            
            # Add the modified page to the writer
            writer.add_page(page)
            
            # Write the output PDF
            output_pdf_path = os.path.join(output_dir, f"{usn}.pdf")
            with open(output_pdf_path, "wb") as output_pdf_file:
                writer.write(output_pdf_file)
        
        # Remove the temporary PDF file
        os.remove(temp_pdf_path)
        
        print(f"Certificate created for: {usn}")

# Example usage
input_pdf_path = "final_certificate.pdf"
# names = ["Alice Johnson", "Bob Smith", "Charlie Brown"]
# event_name = "Python Programming "

csv_file_path = 'core.csv'  # Update this path to your CSV file path
df = pd.read_csv(csv_file_path)

# Extract the names and event
names = df['Name'].tolist()
usn = df['USN'].tolist()
event_name = df['Event'].iloc[0]
output_dir = "CoreFest"
generate_certificates(input_pdf_path,usn, names, event_name, output_dir, font_name="Helvetica-Bold", font_size=18, name_x=115, name_y=255, event_x=170, event_y=219)
