import config
from PIL import Image, ImageColor
from typing import Set
from c_generate_permutations import generate_bitmap_permutations


def extract_bitmaps(glyph_width: int, glyph_height: int, img_path: str) -> Set[int]:
    try:
        img = Image.open(img_path).convert("RGB")
        pixels = img.load()
        img_width, img_height = img.size

        offset_x, offset_y = 1, 1  # 1 pixel border
        spacing_x, spacing_y = 1, 1  # 1 pixel spacing

        assigned_bitmaps: Set[int] = set()

        for row in range(img_height // (glyph_height + spacing_y)):
            for col in range(img_width // (glyph_width + spacing_x)):
                # Calculate the top-left corner of the rectangle
                start_x = offset_x + col * (glyph_width + spacing_x)
                start_y = offset_y + row * (glyph_height + spacing_y)

                # Extract the bitmap for the rectangle
                bitmap = 0
                for y in range(glyph_height):
                    for x in range(glyph_width):
                        pixel = pixels[start_x + x, start_y + y]
                        if pixel == (255, 255, 255):
                            bitmap |= 1 << (y * glyph_width + x)
                assigned_bitmaps.add(bitmap)

        return assigned_bitmaps

    except FileNotFoundError:
        print(f"Error: the image file {img_path} was not found.")
        return set()
    except Exception as e:
        print(f"An error occurred: {e}")
        return set()


def hide_assigned_glyphs(
    glyph_width: int, glyph_height: int, img_path: str, assigned_bitmaps: Set[int]
) -> None:
    try:
        img = Image.open(img_path).convert("RGB")
        pixels = img.load()
        img_width, img_height = img.size
        bg_color = ImageColor.getrgb(config.BG_COLOR)

        offset_x, offset_y = 1, 1  # 1 pixel border
        spacing_x, spacing_y = 1, 1  # 1 pixel spacing

        for row in range(img_height // (glyph_height + spacing_y)):
            for col in range(img_width // (glyph_width + spacing_x)):
                # Calculate the top-left corner of the rectangle
                start_x = offset_x + col * (glyph_width + spacing_x)
                start_y = offset_y + row * (glyph_height + spacing_y)

                # Extract the bitmap for the rectangle
                bitmap = 0
                for y in range(glyph_height):
                    for x in range(glyph_width):
                        pixel = pixels[start_x + x, start_y + y]
                        if pixel != (0, 0, 0):
                            bitmap |= 1 << (y * glyph_width + x)

                if bitmap in assigned_bitmaps:
                    for y in range(glyph_height):
                        for x in range(glyph_width):
                            pixels[start_x + x, start_y + y] = bg_color

        img.save(img_path)
        print(f"Image saved as '{img_path}'")

    except FileNotFoundError:
        print(f"Error: the image file {img_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    glyph_width: int = config.GLYPH_WIDTH
    glyph_height: int = config.GLYPH_HEIGHT
    font_img_path = f"./output/{glyph_width}x{glyph_height}/Pixiie {glyph_width}x{glyph_height} Monospace bitmap.png"
    permutations_img_path = f"./output/{glyph_width}x{glyph_height}/"

    generate_bitmap_permutations(glyph_width, glyph_height, permutations_img_path)

    assigned_bitmaps = extract_bitmaps(glyph_width, glyph_height, font_img_path)

    hide_assigned_glyphs(
        glyph_width,
        glyph_height,
        permutations_img_path + "permutations.png",
        assigned_bitmaps,
    )
