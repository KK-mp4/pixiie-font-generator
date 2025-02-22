from typing import List, Dict, Set
from PIL import Image, ImageDraw


def read_symbols(file_path: str) -> List[Dict[str, List[int]]]:
    symbols_with_bitmaps: List[Dict[str, List[int]]] = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            symbols = file.read().split("\n")[:-1]

            for symbol in symbols:
                symbols_with_bitmaps.append(
                    {
                        "symbol": symbol,
                        "bitmaps": [],  # Initialize with an empty list for bitmaps
                    }
                )
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return symbols_with_bitmaps


def extract_bitmaps(
    image_path: str,
    symbols_with_bitmaps: List[Dict[str, List[int]]],
    rect_width: int = 2,
    rect_height: int = 4,
) -> None:
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        img_width, _ = img.size

        offset_x, offset_y = 1, 1  # 1 pixel border
        spacing_x, spacing_y = 1, 1  # 1 pixel spacing

        for row, symbol_entry in enumerate(symbols_with_bitmaps):
            bitmaps = []
            for col in range(img_width // (rect_width + spacing_x)):
                # Calculate the top-left corner of the rectangle
                start_x = offset_x + col * (rect_width + spacing_x)
                start_y = offset_y + row * (rect_height + spacing_y)

                # Extract the bitmap for the rectangle
                bitmap = 0
                for y in range(rect_height):
                    for x in range(rect_width):
                        pixel = pixels[start_x + x, start_y + y]
                        if pixel == (255, 255, 255):
                            bitmap |= 1 << (y * rect_width + x)
                bitmaps.append(bitmap)

            symbol_entry["bitmaps"] = bitmaps

    except FileNotFoundError:
        print(f"Error: The image file {image_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def associate_symbols(symbols_with_bitmaps: List[Dict[str, List[int]]]) -> bool:
    """
    Associates each symbol with a unique bitmap by ensuring no duplicates.
    Backtracks if necessary to ensure all symbols are assigned a unique bitmap.
    """

    assigned_bitmaps: Set[int] = set()

    def backtrack(index: int) -> bool:
        if index == len(symbols_with_bitmaps):
            return True

        symbol_entry = symbols_with_bitmaps[index]
        for bitmap in symbol_entry["bitmaps"]:
            if bitmap not in assigned_bitmaps:
                assigned_bitmaps.add(bitmap)
                symbol_entry["selected_bitmap"] = bitmap
                if backtrack(index + 1):
                    return True
                assigned_bitmaps.remove(bitmap)

        return False

    if not backtrack(0):
        print("Error: it is impossible to associate each symbol with a unique bitmap.")
        return False

    return True


def draw_bitmaps(
    symbols_with_bitmaps: List[Dict[str, List[int]]],
    output_path: str,
    rect_width: int = 2,
    rect_height: int = 4,
) -> None:
    ordered_symbols = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~∎АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    symbols_map = {
        entry["symbol"]: entry.get("selected_bitmap") for entry in symbols_with_bitmaps
    }

    # Determine the grid size
    symbols_per_row = 16
    num_rows = (len(ordered_symbols) + symbols_per_row - 1) // symbols_per_row

    img_width = symbols_per_row * (rect_width + 1) + 1
    img_height = num_rows * (rect_height + 1) + 1

    img = Image.new("RGB", (img_width, img_height), "#1f1f1f")
    draw = ImageDraw.Draw(img)

    for index, symbol in enumerate(ordered_symbols):
        bitmap = symbols_map.get(symbol)
        if bitmap is None:
            continue  # Skip if the symbol is not in the symbols_with_bitmaps

        # Calculate position of the symbol
        row = index // symbols_per_row
        col = index % symbols_per_row
        start_x = col * (rect_width + 1) + 1
        start_y = row * (rect_height + 1) + 1

        # Draw the bitmap
        for y in range(rect_height):
            for x in range(rect_width):
                if bitmap & (1 << (y * rect_width + x)):
                    draw.point((start_x + x, start_y + y), fill="white")
                else:
                    draw.point((start_x + x, start_y + y), fill="black")

    img.save(output_path)


if __name__ == "__main__":
    X: int = 2  # Width of one cell
    Y: int = 4  # Height of one cell

    character_frequencies_path: str = "./assets/characters/character_frequencies.txt"
    char_map_img_path: str = f"./output/{X}x{Y}/char_map.png"
    output_bitmap_path: str = f"./output/{X}x{Y}/Pixiie {X}x{Y} Monospace bitmap.png"

    symbols = read_symbols(character_frequencies_path)

    extract_bitmaps(char_map_img_path, symbols)

    if associate_symbols(symbols):
        print(f"Successfully associated each symbol with a unique bitmap: {symbols}")

        draw_bitmaps(symbols, output_bitmap_path)
        print(f"Bitmap image saved to '{output_bitmap_path}'")

    else:
        print("Failed to associate each symbol with a unique bitmap.")
