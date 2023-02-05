from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Image, PageBreak
import os

# Define the number of columns and rows per page
cols, rows = 5, 4

# Define the gap size
gap = 2 * mm

# Create a list of images to include in the contact sheet
image_files = [f for f in os.listdir("images") if f.endswith(".jpg")]
images = [Image(f"images/{f}") for f in image_files]

# Create the PDF document
pdf_file = "contact_sheet.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=landscape(letter))

# Add images to the PDF in a grid format
y = 0
for i in range(0, len(images), cols*rows):
    for j in range(rows):
        row = []
        for k in range(cols):
            try:
                im = images[i+j*cols+k]
                im.drawHeight = (doc.height - (rows - 1) * gap) / rows
                im.drawWidth = (doc.width - (cols - 1) * gap) / cols
                im.y = y
                row.append(im)
                y = y + im.drawHeight + gap
            except IndexError:
                pass
        doc.build(row)
        if i+j*cols+k < len(images) - 1:
            doc.build([PageBreak()])
        y = 0

# Save the PDF document
doc.save()
