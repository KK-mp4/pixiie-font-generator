from os import makedirs, path
from sys import exit
from json import load, dump
from PIL import Image, ImageDraw


def generate_pattern(X: int, Y: int, N: int, M: int) -> None:
    background_color = "#1f1f1f"
    rectangle_color = "#000000"

    width = N * X + (N - 1) + 2
    height = M * Y + (M - 1) + 2

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    for row in range(M):
        for col in range(N):
            top_left_x = col * (X + 1) + 1
            top_left_y = row * (Y + 1) + 1
            bottom_right_x = top_left_x + X
            bottom_right_y = top_left_y + Y
            draw.rectangle(
                [top_left_x, top_left_y, bottom_right_x - 1, bottom_right_y - 1],
                fill=rectangle_color,
            )

    folder_path = f"./output/{X}x{Y}/"
    makedirs(folder_path, exist_ok=True)
    image.save(f"{folder_path}background.png")


def yal_settings(X: int, Y: int) -> None:
    font_name = f"Pixiie {X}x{Y} Monospace"

    with open("./assets/yal_settings.json", "r", encoding="utf-8") as f:
        data = load(f)

    data["font-name"] = font_name
    data["font-desc"] = "Smallest possible font for ASCII characters"

    with open(
        f"./output/{X}x{Y}/{font_name} settings.json", "w", encoding="utf-8"
    ) as f:
        dump(data, f, indent=4, ensure_ascii=False)


def count_lines(file_path: str) -> int | None:
    if not path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)


if __name__ == "__main__":
    X = 2  # Width of one cell
    Y = 4  # Height of one cell
    N = 9  # Number of cells in the horizontal direction
    M = count_lines("./assets/characters/character_frequencies.txt")

    if M is None:
        print(f"Error: the file 'character_frequencies.txt' does not exist.")
        exit(1)

    generate_pattern(X, Y, N, M)

    yal_settings(X, Y)
