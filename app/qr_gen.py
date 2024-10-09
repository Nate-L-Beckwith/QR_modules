# Filename: qr_code_generator.py

import os
import qrcode
from PIL import Image, ImageDraw
import logging

# Constants for QR Code generation
VERSION = 1
ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_H
BOX_SIZE = 10
BORDER = 1

def round_corners(img, radius):
    """Apply rounded corners to an image."""
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

def resize_logo(logo, qr_size, logo_size_ratio=0.2):
    """Resize logo based on QR size and ratio."""
    logo_size = int(qr_size * logo_size_ratio)
    return logo.resize((logo_size, logo_size))

def generate_qr_code(data, logo_path=None, save_path="qr_code.png"):
    """
    Generate a general QR code.
    :param data: Data to encode in the QR code (URL, text, etc.)
    :param logo_path: Optional logo image path
    :param save_path: Path to save the QR code image
    """
    qr = qrcode.QRCode(
        version=VERSION,
        error_correction=ERROR_CORRECTION,
        box_size=BOX_SIZE,
        border=BORDER,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    qr_img = round_corners(qr_img, 10)

    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo = resize_logo(logo, qr_img.size[0])
        pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
        qr_img.paste(logo, pos, logo)

    qr_img.save(save_path)
    logging.info(f"QR code saved at: {save_path}")

def generate_wifi_qr_code(ssid, password, security, logo_path=None, save_path="wifi_qr_code.png"):
    """
    Generate a QR code to connect to a WiFi network.
    :param ssid: SSID of the WiFi network
    :param password: WiFi password
    :param security: Security type (WPA, WEP, or leave empty for open networks)
    :param logo_path: Optional logo image path
    :param save_path: Path to save the QR code image
    """
    wifi_template = f"WIFI:S:{ssid};T:{security};P:{password};;"
    generate_qr_code(wifi_template, logo_path, save_path)
