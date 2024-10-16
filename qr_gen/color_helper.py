from colorthief import ColorThief

def get_dominant_and_secondary_colors(image_path):
    color_thief = ColorThief(image_path)
    # Get the dominant color
    dominant_color = '#%02x%02x%02x' % color_thief.get_color(quality=1)
    # Get the secondary color
    palette = color_thief.get_palette(color_count=2)
    if len(palette) > 1:
        secondary_color = '#%02x%02x%02x' % palette[1]
    else:
        secondary_color = dominant_color
    return dominant_color, secondary_color
