import math
import random
import colorsys
from PIL import Image
from typing import Tuple

def generate_bitmap_permutations(X: int, Y: int, output_path: str) -> None:
    """
    Generates an image containing all 2^(X*Y) permutations of a bitmap with dimensions X×Y
    """

    total_permutations: int = 2 ** (X * Y)

    grid_cols: int = math.ceil(math.sqrt(total_permutations))
    grid_rows: int = math.ceil(math.sqrt(total_permutations))

    spacing: int = 1
    background_color: str = "#1f1f1f"

    final_width: int = grid_cols * X + (grid_cols + 1) * spacing
    final_height: int = grid_rows * Y + (grid_rows + 1) * spacing

    if final_width > 4096 or final_height > 4096:
        print("Error: final image dimensions are too big, if you want to proceed remove this threshold in code.")
        return

    print(f"Generating image with dimensions {final_width} x {final_height} pixels...")
    final_image: Image.Image = Image.new("RGB", (final_width, final_height), background_color)

    for perm in range(total_permutations):
        # Determine block position in the grid
        col: int = perm % grid_cols
        row: int = perm // grid_cols
        x_offset: int = spacing + col * (X + spacing)
        y_offset: int = spacing + row * (Y + spacing)

        # Generate a random light color based on HSL:
        random_hue: float = random.uniform(0, 360)
        saturation: float = 0.83
        lightness: float = 0.70
        # colorsys uses HLS order with hue in [0,1]
        r_float, g_float, b_float = colorsys.hls_to_rgb(random_hue / 360.0, lightness, saturation)
        rgb_color: Tuple[int, int, int] = (int(r_float * 255), int(g_float * 255), int(b_float * 255))

        # Create a binary string representation of the permutation, padded with zeros
        bin_str: str = format(perm, f'0{X * Y}b')

        # Draw the bitmap for this permutation.
        for y in range(Y):
            for x in range(X):
                bit_index: int = y * X + x
                if bin_str[bit_index] == '1':
                    final_image.putpixel((x_offset + x, y_offset + y), rgb_color)
                else:
                    # Black pixel remains black.
                    final_image.putpixel((x_offset + x, y_offset + y), (0, 0, 0))

    final_image.save(f"{output_path}permutations.png", "PNG")
    print(f"Image saved as '{output_path}permutations.png'")

if __name__ == "__main__":
    X: int = 2 # Width of one cell
    Y: int = 4 # Height of one cell

    output_path: str = f"./assets/fonts/{X}x{Y}/"

    if X * Y > 16:
        print("Warning: the number of permutations is huge and this may take a very long time to run.")

    generate_bitmap_permutations(X, Y, output_path)
