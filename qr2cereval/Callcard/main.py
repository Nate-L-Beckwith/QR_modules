import os
import logging
from vcard import create_VCard  # Updated function name
from qr_code import generate_qr_code, get_dominant_color  # Updated module name
from defaults import DEFAULT_FILL_COLOR, DEFAULT_BACK_COLOR

# Create a directory for logs if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(filename='logs/qr_code.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Log the start of the process
logging.info('Starting the QR code generation process...')

# Get user input
logging.info('Prompting user for contact information...')
name = input('Enter the name for the contact: ')
phone = input('Enter the phone number for the contact: ')
email = input('Enter the email address for the contact: ')
phone2 = input('Enter the second phone number for the contact (optional): ')
email2 = input('Enter the second email address for the contact (optional): ')
company = input('Enter the company name for the contact (optional): ')

# Log the provided contact information
logging.info(f'User provided contact information: Name: {name}, Phone: {phone}, Email: {email}')

# Hardcoded path to the image for color extraction
image_path = 'path_to_image.jpg'

try:
    logging.info('Generating vCard...')
    vcard = create_VCard(name, phone, email, phone2, email2, company)  # Updated function name

    # Check if the logo file exists
    if os.path.exists(image_path):
        logging.info(f'Logo found at {image_path}. Extracting color...')
        color = get_dominant_color(image_path)
    else:
        logging.warning(f'No logo found at {image_path}. Asking user for action...')
        print('No logo found. Okay to continue with defaults? (yes/no)')
        user_input = input().strip().lower()
        if user_input == 'yes':
            logging.info('User chose to continue with default colors.')
            color = DEFAULT_FILL_COLOR
        else:
            logging.error('User chose not to proceed without logo.')
            raise FileNotFoundError('Logo file not found, and user chose not to proceed with defaults.')

    logging.info(f'Generating QR code with fill color: {color}, back color: {DEFAULT_BACK_COLOR}')
    qr_image = generate_qr_code(vcard, color, DEFAULT_BACK_COLOR)

    # Save the QR code
    save_path = "contact_qr.png"
    qr_image.save(save_path)
    logging.info(f'QR code generated and saved successfully at {save_path}.')
    print(f'QR code generated and saved as "{save_path}"')
except Exception as e:
    error_message = f'An error occurred: {str(e)}'
    logging.error(error_message)
    print(error_message)
    
print(vcard)
