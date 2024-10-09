# Filename: cli_interface.py

import logging
from qr_gen import generate_wifi_qr_code, generate_qr_code

def get_user_input(prompt):
    """Utility function to get input from the user."""
    return input(prompt)

def qr_type_selection():
    """Prompt the user to select the type of QR code to generate."""
    print("Select the type of QR code you want to generate:")
    print("1: WiFi QR Code")
    print("2: URL QR Code")
    print("3: Text QR Code")
    choice = get_user_input(":")
    return choice

def gather_wifi_info():
    """Prompt the user for WiFi network details."""
    ssid = get_user_input("Enter the WiFi SSID: ")
    password = get_user_input("Enter the WiFi Password: ")
    security = get_user_input("Enter the Security Type (WPA/WEP or leave empty for open networks): ")
    return ssid, password, security

def gather_url_info():
    """Prompt the user for URL details."""
    url = get_user_input("Enter the URL: ")
    return url

def gather_text_info():
    """Prompt the user for the text to encode."""
    text = get_user_input("Enter the text to encode in the QR code: ")
    return text

def qr_code_generation_interface():
    """Main function to handle the CLI input and QR code generation."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    choice = qr_type_selection()

    logo_path = get_user_input("Enter the logo image path (or press Enter to skip): ")
    save_path = get_user_input("Enter the path to save the QR code (default: ./qr_code.png): ")
    save_path = save_path if save_path else "./qr_code.png"

    if choice == '1'  :
        ssid, password, security = gather_wifi_info()
        generate_wifi_qr_code(ssid, password, security, logo_path, save_path)
    elif choice == '2':
        url = gather_url_info()
        generate_qr_code(url, logo_path, save_path)
    elif choice == '3':
        text = gather_text_info()
        generate_qr_code(text, logo_path, save_path)
    else:
        logging.error("Invalid choice! Exiting.")
        return

    logging.info(f"QR code generated and saved at {save_path}")

if __name__ == "__main__":
    qr_code_generation_interface()
