import json

with open("config.json", "r") as f:
    config = json.load(f)

ENG_INPUT_FILE_NAME: str = config.get("eng_input_file_name", "t8.shakespeare.txt")
RU_INPUT_FILE_NAME: str = config.get("ru_input_file_name", "war_and_peace.txt")
CHAR_MAP_IMG_NAME: str = config.get("char_map_img_name", "char_map.png")
GLYPH_WIDTH: int = config.get("glyph_width", 2)
GLYPH_HEIGHT: int = config.get("glyph_height", 4)
BG_COLUMNS: int = config.get("bg_columns", 9)
BG_COLOR: str = config.get("bg_color", "#1f1f1f")
FONT_DESC: str = config.get("font_desc", "")