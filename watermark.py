#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageEnhance, ImageFont, ImageDraw
from optparse import OptionParser
import glob, os

parser = OptionParser();
parser.add_option("-p", "--path", dest="path", help="Path for the image files. e.g. /path/to/img/dir/")
parser.add_option("-f", "--format", dest="format", help="Image format. e.g. jpg")

(options, args) = parser.parse_args()

def reduce_opacity(im, opacity):
    # Returns an image with reduced opacity.
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark_img(file_name):
    # CHANGE TO YOUR CONTENT
    font_name = 'fonts/HelveticaNeue.ttf'
    watermark_text = u"\u00a9 Js Lim"
    font_size = 2
    opacity = 0.5
    # total width of image
    watermark_scale = 0.03

    # font file & font size
    font = ImageFont.truetype(font_name, font_size)

    img = Image.open(file_name).convert('RGBA')

    watermark_position = ((int)(img.size[0] * watermark_scale), (int)(img.size[0] * watermark_scale))

    # create watermark
    watermark_max_width = (int)(img.size[0] * 0.2)
    watermark = Image.new('RGBA', img.size, (0,0,0,0))
    draw = ImageDraw.Draw(watermark, 'RGBA')
    font = ImageFont.truetype(font_name, font_size)
    n_width, n_height = font.getsize(watermark_text)

    while (n_width < watermark_max_width):
        font_size += 2
        font = ImageFont.truetype(font_name, font_size)
        n_width, n_height = font.getsize(watermark_text)

    draw.text(((img.size[0] - n_width - watermark_position[0]), (img.size[1] - n_height - watermark_position[1])), watermark_text, font=font)

    watermark = reduce_opacity(watermark, opacity)

    Image.composite(watermark, img, watermark).save(file_name)

if __name__ == '__main__':

    img_files = [os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(options.path)
        for f in files if f.endswith('.' + options.format)]

    for img in img_files:
        watermark_img(img)
