__author__ = 'chill'

# https://en.wikipedia.org/wiki/ANSI_escape_code

# The escape character is \x1b
# Then everything between [ and m are the parameters

# We use 0 to reset the formatting. Usually after each time we print something.
reset = '\x1b[0m'

# 4 is used to underline text
print(f'\x1b[4mTEXT COLORS{reset}')

# 30-37 are different standard text color options
for color_value in range(30, 38):
    ansi_format = f'\x1b[{color_value}m'
    print(ansi_format + f'Here is the color value: {color_value}{reset}')
print()

print(f'\x1b[4mBACKGROUNDS{reset}')

# 40-47 are different standard background color options
for color_value in range(40, 48):
    ansi_format = f'\x1b[{color_value}m'
    print(ansi_format + f'Here is the color value: {color_value}{reset}')
print()

print(f'\x1b[4mTEXT AND BACKGROUND COMBINATIONS{reset}')

# We can combine the text and color backgrounds by putting a simi-colon between the arguments
for text_value in range(30, 38):
    for bg_value in range(40, 48):
        ansi_format = f'\x1b[{text_value};{bg_value}m'
        print(f'{ansi_format} {text_value};{bg_value} {reset}', end='')
    print()
print()

# We can also do RGB values for both text and background using the arguments 38 and 48.
# Both arguments are followed by 2;r;g;b

print(f'\x1b[4mTEAL IN RGB{reset}')

# Let's make the color teal using the following RGB values
r = 50
g = 200
b = 200

ansi_format = f'\x1b[38;2;{r};{g};{b}m'
print(f'{ansi_format}This is the color teal.{reset}')
print()

print(f'\x1b[4mRGB TEXT AND BACKGROUND COLORS{reset}')

# Now let's put it on a background RGB color

bg_r = 150
bg_g = 50
bg_b = 100

ansi_format = f'\x1b[38;2;{r};{g};{b};48;2;{bg_r};{bg_g};{bg_b}m'
print(f'{ansi_format}This is the color teal.{reset}')
print()

print(f'\x1b[4mRGB COLOR TRANSITION{reset}')

# Now we'll do something fun!!!!! The red and blue values will remain constant as the green value increases.
bg_r = 150
bg_g = 50
bg_b = 100

for bg_g in range(0, 256, 2):
    ansi_format = f'\x1b[48;2;{bg_r};{bg_g};{bg_b}m'
    print(f'{ansi_format} {reset}', end='')