from PIL import Image, ImageFont, ImageDraw
from typing import Tuple
import textwrap

FONT_COLOUR = (255, 255, 255)
OUTLINE_WIDTH = 5
OUTLINE_COLOUR = (0, 0, 0)
FONT_PATH = "assets/impact.ttf"

Position = Tuple[int, int]


font_cache = {i: ImageFont.truetype(FONT_PATH, i) for i in range(20, 200)}


def get_font_object(font_size: int):
    if font_size < 20:
        return font_cache[20]

    if font_size not in font_cache:
        font_cache[font_size] = ImageFont.truetype(FONT_PATH, font_size)

    return font_cache[font_size]


def calculate_font_size(image_dimensions: Position, text: str, size_fraction: float, maximum_size: int = None) -> int:
    """Binary search algorithm to calculate required font size.

    Returns the required font size.

    Adapted from https://stackoverflow.com/a/61891053
    """
    breakpoint = size_fraction * image_dimensions[0]
    jump_size = 75
    font_size = 20
    while True:
        font = get_font_object(font_size)
        text_width, _ = font.getsize(text)

        if text_width < breakpoint:
            font_size += jump_size
        else:
            jump_size = jump_size // 2
            font_size -= jump_size

        if jump_size <= 1:
            return min(font_size, maximum_size)


def write_centred_text(image, image_dimensions: Position, text: str, size_fraction: int, on_bottom: bool) -> None:
    """Writes the text on top or bottom, changing font size accordingly."""

    font_size = calculate_font_size(image_dimensions, text, size_fraction, 70)
    font = get_font_object(font_size)

    anchor_x = image_dimensions[0] // 2
    anchor_y = image_dimensions[1] if on_bottom else 0

    # note: requires at least pillow 8.0.0!!!! anchor isn't implemented if before then
    anchor = "md" if on_bottom else "ma"

    image.multiline_text(
        (anchor_x, anchor_y),
        text, 
        font=font,
        fill=FONT_COLOUR,
        stroke_width=OUTLINE_WIDTH,
        stroke_fill=OUTLINE_COLOUR,
        align="center",
        spacing=0,
        anchor=anchor
    )


def generate_captioned_image(input_path: str, output_path: str, top_text: str, bottom_text: str, uppercase: bool = True):
    if uppercase:
        top_text = top_text.upper()
        bottom_text = bottom_text.upper()
    
    top_text = "\n".join(textwrap.wrap(top_text, 30))
    bottom_text = "\n".join(textwrap.wrap(bottom_text, 30))

    original_image = Image.open(input_path)
    image_dimensions = original_image.size
    image = ImageDraw.Draw(original_image)

    write_centred_text(image, image_dimensions, top_text, 0.8, False)
    write_centred_text(image, image_dimensions, bottom_text, 0.8, True)

    original_image.save(output_path)


if __name__ == "__main__":
    generate_captioned_image("testsrc.png", "captioned.png", "you and me", "but unironically", False)
    # generate_captioned_image("testsrc.png", "captioned.png", "when cereal", "no haves milk")
    
