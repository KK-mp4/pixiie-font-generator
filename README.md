# Tiny bitmap font generator [work in progress]
## Small tool to help generating small bitmap fonts using [Wave Function Collapse (WFC)](https://en.wikipedia.org/wiki/Wave_function_collapse) algorithm

## Prelude
I wanted to automate the process of making tiny fonts as much as possible. Sadly experiments with upscaling bitmaps with Signed Distance Fields (SDF) and trying to find the closest matches with "normal" fonts didn't produce good results. I guess a valid approach would be trying to teach some small diffusion model to generate you really small glyphs, but that for a future project.
As of today I developed a pipeline that combines really good pattern recognition of humans with some automation.

## Step 1. Character frequencies
It is preferable that each glyph in a font is unique. Meaning that if character "S" took perfect bitmap for number "5", we would have to sacrifice with readability of one of those. I thought that perfect order would be popularity of each symbol, meaning whatever is more popular would get the better bitmap.
I downloaded Shakespeare for Latin letters and War and Peace by Leo Tolstoy for Cyrillic letters and calculated frequencies of each character. With some manual adjustments you can see the final list on the Wiki page. You can input your own datasets to produce better results:

```bash
# Calculate character frequencies
python a_character_frequencies.py
```

## Step 2. Generating template
On the second step I generated template for drawing future font. Glyphs will be ordered one by one vertically and on the horizontal direction I will draw various ways to draw each glyph. The best looking one on the left to the ugliest abstract one on the right. This will be important for WFC algorithm to find the solve.
This step also generated a [YAL](https://yal.cc/tools/pixel-font/) settings file. It's a website that lets you preview and generate TTF fonts.

```bash
# Generate background and YAL settings file
python b_generate_bg.py
```

## Step 3. Generating all possible permutations
To find inspiration for each symbol it is helpful to see all possible permutations of a set bitmap size.

```bash
# Generate all permutations of binary pixels
python c_generate_permutations.py
```

<p align="center">
  <img src="https://github.com/user-attachments/assets/ed1fed2e-1bd3-4490-976f-e83351a04b91" alt="All permutations for 2x4 bitmap">
</p>

## Step 4. WFC
Now final step. Draw your glyphs in order by character_frequencies.txt file. Each line should contain different ways to draw each symbol from best looking and worst. An example of how it would look like on numbers 0-9 can be seen bellow:

<p align="center">
  <img src="https://github.com/user-attachments/assets/39f64d49-d0e5-489b-b33c-52678f793058" alt="Filled template">
</p>

After all characters are drawn start the solver. If it takes too much time it's probably because there is no valid solve.

```bash
# Generate the font bitmap
python d_wfc.py
```

## Tips
1. If your glyph is wider than it is tall, you may consider rotating it.  
`“Ю, ю”`

<p align="center">
  <img src="https://github.com/user-attachments/assets/f0058dbd-06a6-480a-b1fb-b319125ba180" alt="Ю, ю">
</p>

3. Google alternative spelling styles.  
`"3”`

<p align="center">
  <img src="https://github.com/user-attachments/assets/c081462c-359f-4450-b4dd-a3132488b54f" alt="3">
</p>

4. If whole symbol doesn't fit you may consider leaving only recognisable half.  
`"N, n"`  
`"K, k"`  

<p align="center">
  <img src="https://github.com/user-attachments/assets/85543f1a-174b-414c-9b38-1c4d809dfb03" alt="N, n, K, k">
</p>

5. Remember that smaller glyphs can be shifted around and don't need to be glued to one side.  
`"i, i"`  
`"c, c"`

<p align="center">
  <img src="https://github.com/user-attachments/assets/57c4d94b-428e-44ce-8624-ee7f03c51a96" alt="i, i, c, c">
</p>


4. Use [pangrams](https://en.wikipedia.org/wiki/Pangram) (short sentences that contain every letter of the alphabet at least once) to preview font.

## Results
Current progress on the Pixiie 2x4 Monospace:
```json
{
  " !\"#$%&'()*+,-./",
  "0123456789:;<=>?",
  "@ABCDEFGHIJKLMNO",
  "PQRSTUVWXYZ[\\]^_",
  "`abcdefghijklmno",
  "pqrstuvwxyz{|}~∎"
}
```
<p align="center">
  <img src="https://github.com/user-attachments/assets/31300ccb-812c-4389-ada5-3a1ecd3cef1e" alt="PixIIe 2x4 Monospace">
</p>

## License
This program is licensed under the MIT License. Please read the License file to know about the usage terms and conditions.
