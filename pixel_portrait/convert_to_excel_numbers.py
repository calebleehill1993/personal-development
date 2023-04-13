__author__ = 'chill'

import os
import sys
from PIL import Image
import random

def unique_colors(image):
    width, height = image.size
    colors = []
    for i in range(width):
        for j in range(height):
            r, g, b = image.getpixel((i, j))
            if (r, g, b) not in colors:
                colors.append((r, g, b))
    return colors

def grey_value(r, g, b):
    return int(r * 0.3 + g * 0.59 + b * 0.11)

def grey_color(r, g, b):
    grey = grey_value(r, g, b)
    return (grey, grey, grey)

def even_split(numbers, min, max):
    splits = numbers - 2
    diff = max - min
    split_size = diff / (numbers - 1)
    l = [int(min + split_size * i) for i in range(numbers)]
    l[0] = int(l[0] + (split_size / 2))
    l[-1] = int(l[-1] - (split_size / 2))
    return l

def color_count(image):
    width, height = image.size
    counter = {}
    for i in range(width):
        for j in range(height):
            r, g, b = image.getpixel((i, j))
            if r in counter.keys():
                counter[r] += 1
            else:
                counter[r] = 1

    keys = list(counter.keys())
    keys.sort()
    sorted_counter = {i: counter[i] for i in keys[::-1]}

    return sorted_counter

def even_distribution(number, image):
    width, height = image.size
    total = width * height
    number_per_split = total // number

    counter = color_count(image)

    splits = [list(counter.keys())[0]]
    count = 0
    for key in counter.keys():
        count += counter[key]
        if count > number_per_split:
            count = counter[key]
            splits.append(key)

    return splits[:-1]


def closest_number(num, num_list):
    closest = num_list[0]
    for n in num_list:
        if abs(num - n) < abs(num - closest):
            closest = n
    if closest not in num_list:
        print(closest)
    return closest

def highest_number(num, num_list):
    highest = num_list[0]
    for n in num_list:
        if num <= n:
            highest = n

    return highest


input_image = Image.open("jake.jpeg")
pixels_across = 35

og_width, og_height = input_image.size

block_size = og_width // pixels_across
pixels_down = og_height // block_size

new_width = block_size * pixels_across
new_height = pixels_down * block_size

width_diff = og_width - new_width
height_diff = og_height - new_height

width_buffer = width_diff // 2
height_buffer = height_diff // 2

print(f'{pixels_across} x {pixels_down}. Total of {pixels_across * pixels_down} pixels.')

output_image = Image.new(mode='RGB', size=(pixels_across, pixels_down))
output_map = output_image.load()

pixels_per_block = block_size ** 2

for x in range(pixels_across):
    for y in range(pixels_down):

        r_total = 0
        g_total = 0
        b_total = 0

        starting_x = block_size * x + width_buffer
        starting_y = block_size * y + height_buffer

        for i in range(block_size):
            for j in range(block_size):
                r, g, b = input_image.getpixel((starting_x + i, starting_y + j))
                r_total += r
                g_total += g
                b_total += b

        r_avg = r_total // pixels_per_block
        g_avg = g_total // pixels_per_block
        b_avg = b_total // pixels_per_block

        output_map[x, y] = (r_avg, g_avg, b_avg)

output_image.save('pixelated.png')


# GREY THE IMAGE
input_image = Image.open('pixelated.png')
width, height = input_image.size
output_image = Image.new(mode='RGB', size=(width, height))
output_map = output_image.load()

for i in range(width):
    for j in range(height):
        r, g, b = input_image.getpixel((i, j))

        output_map[i, j] = grey_color(r, g, b)

output_image.save('pixelated_grey.png')




# ONLY SELECTED NUMBER OF COLORS
input_image = Image.open('pixelated_grey.png')
width, height = input_image.size
output_image = Image.new(mode='RGB', size=(width, height))
output_map = output_image.load()

colors = 7

min = 255
max = 0
for i in range(width):
    for j in range(height):
        r, g, b = input_image.getpixel((i, j))

        if r > max:
            max = r
        if r < min:
            min = r

# grey_colors = even_split(colors, min, max)[::-1]

grey_colors = even_distribution(colors, input_image)

spread_sheet_list = []

for i in range(height):
    spread_sheet_list.append([])
    for j in range(width):
        r, g, b = input_image.getpixel((j, i))

        # value = closest_number(r, grey_colors)
        value = highest_number(r, grey_colors)

        spread_sheet_list[i].append(grey_colors.index(value) + 1)
        output_map[j, i] = (value, value, value)

output_image.save('color_map.png')

import pandas as pd
df = pd.DataFrame(spread_sheet_list)
df.to_csv('numbers.csv', index=False, header=False)


# COLORING IMAGE
random_colors = []
color_values = []
color_pairs = {}
for i in range(colors):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    value = grey_value(r, g, b)
    color_values.append(value)
    color_pairs[value] = (r, g, b)

ordered_colors = [color_pairs[n] for n in sorted(color_values)[::-1]]

input_image = Image.open('color_map.png')
width, height = input_image.size
output_image = Image.new(mode='RGB', size=(width, height))
output_map = output_image.load()

for i in range(height):
    for j in range(width):
        output_map[j, i] = ordered_colors[spread_sheet_list[i][j] - 1]

output_image.save('pixelated_color.png')