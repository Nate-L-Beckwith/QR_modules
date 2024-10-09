# color_helper.py
import logging
from colorthief import ColorThief


def get_dominant_and_secondary_colors(image_path):
    """Get dominant and secondary colors from an image.
    :param image_path: Path to the image file
    :return: Tuple containing dominant and secondary colors
    """
    try:
        color_thief = ColorThief(
            image_path
        )  # Create a ColorThief instance to extract colors
        dominant_color = color_thief.get_color(
            quality=1
        )  # Get the most dominant color from the image
        palette = color_thief.get_palette(
            color_count=5
        )  # Get a palette of the top 5 colors

        if len(palette) > 2:
            secondary_color = palette[
                2
            ]  # Use the third color if more than 2 major colors are present
        else:
            secondary_color = (
                palette[1] if len(palette) > 1 else dominant_color
            )  # Default to second color or dominant color
    except Exception as e:
        logging.error(f"Error extracting colors: {str(e)}")
        dominant_color = (0, 0, 0)
        secondary_color = (255, 255, 255)
    return dominant_color, secondary_color
