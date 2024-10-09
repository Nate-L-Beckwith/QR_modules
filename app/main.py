# Filename: main.py

import logging
from qr_gen import generate_qr_code
from color_helper import get_dominant_and_secondary_colors

def main():
    """Main function to generate QR code."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    url = "https://wifi.example.com/connect"
    logo_path = "./logo.png"
    qr_save_path = "./wifi_qr_code.png"

    try:
        dominant_color, secondary_color = get_dominant_and_secondary_colors(logo_path)
        logging.info(f"Dominant Color: {dominant_color}, Secondary Color: {secondary_color}")

        generate_qr_code(url, logo_path, qr_save_path)
    except Exception as e:
        logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
