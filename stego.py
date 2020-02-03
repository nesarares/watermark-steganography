from PIL import Image
import math


def save_image(pixels, size, filename):
    image = Image.new('RGB', size)
    image.putdata(pixels)
    image.save(filename)


def map_value_in_range(value, input_start, input_end, output_start, output_end):
    return int(output_start + ((output_end - output_start) / (input_end - input_start)) * (value - input_start))


def map_pixel(pixel):
    new_val = int(0.2126 * pixel[0] + 0.7152 * pixel[1] + 0.0722 * pixel[2])
    return map_value_in_range(new_val, 0, 255, 0, 64)


def embed_watermark(input_pixel, watermark_pixel):
    mask_input = 0b11111100
    mask_r = 0b00000011
    mask_g = 0b00001100
    mask_b = 0b00110000
    r = (input_pixel[0] & mask_input) | (watermark_pixel & mask_r)
    g = (input_pixel[1] & mask_input) | ((watermark_pixel & mask_g) >> 2)
    b = (input_pixel[2] & mask_input) | ((watermark_pixel & mask_b) >> 4)
    return (r, g, b, input_pixel[3])


def inverse_lsb(input_pixel):
    mask_lsb = 0b00000011
    r = (input_pixel[0] & mask_lsb)
    g = (input_pixel[1] & mask_lsb) << 2
    b = (input_pixel[2] & mask_lsb) << 4
    return r + g + b


def encrypt(options):
    input_img = Image.open(options['input_path'], 'r')
    input_pixels = list(input_img.getdata())
    input_size = input_img.size

    watermark_img = Image.open(options['watermark_path'], 'r')
    watermark_size = watermark_img.size

    if watermark_size[0] > watermark_size[1]:
        watermark_size = options['max_watermark_size'], int(watermark_size[1] * options['max_watermark_size'] / watermark_size[0])
    else:
        watermark_size = int(watermark_size[0] * options['max_watermark_size'] / watermark_size[1]), options['max_watermark_size']

    watermark_img.thumbnail(watermark_size, Image.ANTIALIAS)
    watermark_pixels = list(watermark_img.getdata())

    for index, pixel in enumerate(watermark_pixels):
        watermark_pixels[index] = map_pixel(pixel)

    for row in range(input_size[1]):
        for col in range(input_size[0]):
            watermark_pix = watermark_pixels[(row % watermark_size[1]) * watermark_size[0] + col % watermark_size[0]]
            input_pix = input_pixels[row * input_size[0] + col]
            new_pix = embed_watermark(input_pix, watermark_pix)
            input_pixels[row * input_size[0] + col] = new_pix

    save_image(input_pixels, input_size, options['output_path'])


def decrypt(options):
    new_img = Image.open(options['input_path'], 'r')
    new_img_pixels = list(new_img.getdata())
    new_img_size = new_img.size

    watermark_pixels = []

    for pixel in new_img_pixels:
        mapped = map_value_in_range(inverse_lsb(pixel), 0, 63, 0, 255)
        watermark_pixels.append(mapped)

    watermark_pixels = list(map(lambda x: (x, x, x, 255), watermark_pixels))
    save_image(watermark_pixels, new_img_size, options['output_path'])


def main():
    MAX_WATERMARK_SIZE = 128

    encrypt({
        'input_path':           'images/kfc_fries.png', 
        'watermark_path':       'images/watermark.png', 
        'output_path':          'images/kfc_fries_watermarked.png', 
        'max_watermark_size':   MAX_WATERMARK_SIZE
    })
    
    decrypt({
        'input_path':   'images/mcdonalds_fries.png', 
        'output_path':  'images/mcdonalds_fries_decrypted.png'
    })

# main()
