# Filename: color_helper.py

from colorthief import ColorThief

def get_dominant_and_secondary_colors(image_path):
    """Get dominant and secondary colors from an image."""
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count=2)
    secondary_color = palette[1] if len(palette) > 1 else dominant_color
    return dominant_color, secondary_color
