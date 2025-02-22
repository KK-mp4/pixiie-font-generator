import os
from collections import Counter


def frequency_analysis(input_path, output_path, start_unicode_dec, end_unicode_dec):
    if not os.path.exists(input_path):
        print(f"Error: The file {input_path} does not exist.")
        return

    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Count ASCII character frequencies
        ascii_counts = Counter(char.upper() for char in text if start_unicode_dec <= ord(char.upper()) <= end_unicode_dec)

        # Sort characters by frequency (descending), then by ASCII value
        sorted_counts = sorted(ascii_counts.items(), key=lambda x: (-x[1], x[0]))

        # Write sorted frequencies to the output file
        with open(output_path, 'a', encoding='utf-8') as file:
            for char, _ in sorted_counts:
                if char.isprintable():
                    file.write(f"{char}\n")

            for char, _ in sorted_counts:
                if char.isprintable():
                    file.write(f"{char.lower()}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    eng_input_file = "./assets/t8.shakespeare.txt"
    rus_input_file = "./assets/война_и_мир.txt"
    output_file = "./assets/character_frequencies.txt"

    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(" \n") # Space
        for num in range(0, 10):
            file.write(f"{num}\n")

    frequency_analysis(eng_input_file, output_file, 65, 90)

    extra_chars = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~∎"
    with open(output_file, 'a', encoding='utf-8') as file:
        for char in extra_chars:
            file.write(f"{char}\n")

    frequency_analysis(rus_input_file, output_file, 1040, 1071)

    print(f"Character frequencies successfully written to {output_file}")