from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image
import os
import time

def draw_label(c, x, y, qr_path, lines):
    LABEL_WIDTH = 2.63 * inch
    LABEL_HEIGHT = 1.0 * inch
    MARGIN = 0.125 * inch
    QR_SIZE = 0.9 * inch
    TEXT_X_OFFSET = x + QR_SIZE + 0.1 * inch
    TEXT_Y_START = y + LABEL_HEIGHT - 0.15 * inch
    LINE_SPACING = 0.15 * inch
    MAX_LINE_LENGTH = 32  # chars before cutoff, tweak if needed

    # Draw QR code
    if os.path.exists(qr_path):
        c.drawImage(qr_path, x + MARGIN, y + MARGIN, width=QR_SIZE, height=QR_SIZE, preserveAspectRatio=True)

    # Draw text
    c.setFont("Times-Roman", 8)
    for i, line in enumerate(lines[:5]):
        line = line[:MAX_LINE_LENGTH]  # cut off long lines
        c.drawString(TEXT_X_OFFSET, TEXT_Y_START - i * LINE_SPACING, line)

def insert_labels_pdf(qr_folder, labels, output_pdf="AveryLabels.pdf"):
    c = canvas.Canvas(output_pdf, pagesize=letter)

    PAGE_WIDTH, PAGE_HEIGHT = letter
    LABEL_WIDTH = 2.63 * inch
    LABEL_HEIGHT = 1.0 * inch

    LEFT_MARGIN = 0.19 * inch
    TOP_MARGIN = 0.6 * inch
    H_GAP = 0.125 * inch
    V_GAP = 0.0 * inch

    for i, (qr_filename, label_lines) in enumerate(labels):
        label_on_page = i % 30
        row = label_on_page // 3
        col = label_on_page % 3

        x = LEFT_MARGIN + col * (LABEL_WIDTH + H_GAP)
        y = PAGE_HEIGHT - TOP_MARGIN - LABEL_HEIGHT - row * (LABEL_HEIGHT + V_GAP)

        if (qr_filename is None) or (qr_filename == ""):
            qr_path = None
        else:
            qr_path = os.path.join(qr_folder, qr_filename)
            
        draw_label(c, x, y, qr_path, label_lines)

        # After every 30 labels, start a new page
        if label_on_page == 29:
            c.showPage()

    c.save()
    print(f"Saved PDF to: {output_pdf}")