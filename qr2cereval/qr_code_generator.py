import os
import qrcode
import logging
from PIL import Image, ImageDraw, ImageOps
from urllib.parse import urlparse

# Constants
VERSION = 1
ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_H
BOX_SIZE = 10
BORDER = 1  # Reduce this from 4 to 1
LOGO_SIZE_RATIO = 0.7  # Increased this from 0.3 to 0.5

# QR code color parameters
FILL_COLOR = "grey"
BACK_COLOR = "white"

def valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def resize_logo(logo, qr_size):
    logo_size = int(qr_size * LOGO_SIZE_RATIO)
    return logo.resize((logo_size, logo_size))

def round_corners(radius, img):
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
    alpha = Image.new('L', img.size, "white")
    w, h = img.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
    img.putalpha(alpha)
    return img

def generate_qr_code(url, logo_path, qr_path):
    # check if the URL is valid
    if not valid_url(url):
        raise ValueError(f"URL is not valid: {url}")

    # check if the logo file exists
    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logo file does not exist: {logo_path}")

    # check if the logo is an image file
    logo_ext = os.path.splitext(logo_path)[1]
    valid_extensions = ['.jpg', '.png', '.bmp', '.gif', '.tiff', '.jpeg']
    if logo_ext.lower() not in valid_extensions:
        raise ValueError(f"Logo file is not a valid image: {logo_path}")

    try:
        qr = qrcode.QRCode(
            version=VERSION,
            error_correction=ERROR_CORRECTION,
            box_size=BOX_SIZE,
            border=BORDER,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color=FILL_COLOR, back_color=BACK_COLOR).convert('RGBA')
        rounded = round_corners(3, img) 

        # Load and resize logo
        logo = Image.open(logo_path).convert('RGBA')
        logo = resize_logo(logo, img.size[0])

        box = (int((img.size[0] - logo.size[0]) / 2), int((img.size[1] - logo.size[1]) / 2),
               int((img.size[0] + logo.size[0]) / 2), int((img.size[1] + logo.size[1]) / 2))

        # Paste the logo
        rounded.paste(logo, box, logo)
        rounded.save(qr_path, "PNG")  # PNG supports transparency
        logging.info(f"QR code generated successfully at {qr_path}")
    except Exception as e:
        logging.error(f"An error occurred while generating the QR code: {str(e)}")
        raise
