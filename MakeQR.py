# QR Generator For Wilson
# Jefferson Kline, 5/8/25

# Requires rigid formatting in list 

import segno
from PIL import Image, ImageDraw, ImageFont
from itertools import cycle


def start(QR_msg, filename_suffix="default"):
    
    qrcode = segno.make_qr(QR_msg)

    filename = f"QR_{filename_suffix}.png"
    qrcode.save(filename, scale=12, border=2)

    print(f"QR code saved to {filename}")




