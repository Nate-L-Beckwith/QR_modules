# qr_gen.py

import os
import qrcode
import qr_gen
from PIL import Image, ImageDraw
import logging
from color_helper import get_dominant_and_secondary_colors
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import argparse

ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_H
BOX_SIZE = 10
BORDER = 1

def round_corners(img, radius):
    try:
        circle = Image.new("L", (radius * 2, radius * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
        alpha = Image.new("L", img.size, "white")
        w, h = img.size
        alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
        alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
        alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
        alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
        img.putalpha(alpha)
    except Exception as e:
        logging.error(f"Error applying rounded corners: {str(e)}")
    return img

def resize_logo(logo, qr_size, logo_size_ratio=0.2):
    try:
        logo_size = int(qr_size * logo_size_ratio)
        return logo.resize((logo_size, logo_size))
    except Exception as e:
        logging.error(f"Error resizing logo: {str(e)}")
        return logo

def generate_qr_code(data, logo_path=None, save_path="qr_code.png", fill_color="black", back_color="white", use_styles=False):
    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECTION, box_size=BOX_SIZE, border=BORDER)
    qr.add_data(data)
    qr.make(fit=True)

    if use_styles:
        qr_img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(), color_mask=RadialGradiantColorMask())
    else:
        qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")
        qr_img = round_corners(qr_img, 10)

    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo = resize_logo(logo, qr_img.size[0])
            pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
            qr_img.paste(logo, pos, logo)
        except IOError:
            logging.error(f"Error opening logo file: {logo_path}")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    qr_img.save(save_path)
    logging.info(f"QR code saved at: {save_path}")

def generate_wifi_qr_code(ssid, password, security, logo_path=None, save_path="/Users/nate/Documents/proj/QR/wifi_qr_code.png", fill_color="black", back_color="white", use_styles=False):
    wifi_template = f"WIFI:S:{ssid};T:{security};P:{password};;"
    generate_qr_code(wifi_template, logo_path, save_path, fill_color, back_color, use_styles)

def main():
    parser = argparse.ArgumentParser(description="Generate custom QR codes.")
    parser.add_argument("--data", type=str, help="Data to encode in the QR code")
    parser.add_argument("--logo", type=str, help="Path to logo image")
    parser.add_argument("--save_path", type=str, default="/Users/nate/Documents/proj/QR/qr_code.png", help="Path to save QR code")
    parser.add_argument("--wifi", action="store_true", help="Flag if the data is a WiFi QR code")
    parser.add_argument("--ssid", type=str, help="WiFi SSID if generating a WiFi QR code")
    parser.add_argument("--password", type=str, help="WiFi Password if generating a WiFi QR code")
    parser.add_argument("--security", type=str, help="WiFi Security type (WPA, WEP, or open)")
    parser.add_argument("--use_styles", action="store_true", help="Flag to use advanced styling for the QR code")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        if args.wifi:
            if not args.ssid:
                logging.error("SSID is required for WiFi QR code generation.")
                return
            generate_wifi_qr_code(args.ssid, args.password, args.security, args.logo, args.save_path, use_styles=args.use_styles)
        else:
            if not args.data:
                logging.error("Data is required to generate a QR code.")
                return
            generate_qr_code(args.data, args.logo, args.save_path, use_styles=args.use_styles)
    except Exception as e:
        logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
