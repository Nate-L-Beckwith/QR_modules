import logging
from qr_code_generator import generate_qr_code

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # for the sake of simplicity, we will use a static url
    url = "https://forms.office.com/r/vFXPAK4QBs"

    # path to the logo
    logo_path = "./logo.png"

    # path to save the generated qr code
    qr_path = "./qr_code.png"

    try:
        generate_qr_code(url, logo_path, qr_path)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
