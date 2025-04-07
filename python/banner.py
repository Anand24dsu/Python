from PIL import Image, ImageDraw, ImageFont

def create_named_banner(name, banner_size, text_color, banner_color):
    banner = Image.new('RGB', banner_size, banner_color)
    draw = ImageDraw.Draw(banner)
    try:
        font = ImageFont.truetype("ariali.ttf", 1)  
    except IOError:
        font = ImageFont.load_default() 
    max_font_size = banner_size[1] // 2  
    for font_size in range(max_font_size, 0, -1):
        try:
            font = ImageFont.truetype("ariali.ttf", font_size)  
        except IOError:
            font = ImageFont.load_default() 
        text_bbox = draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        if text_width <= banner_size[0] and text_height <= banner_size[1]:
            break
    position = ((banner_size[0] - text_width) // 2, (banner_size[1] - text_height) // 2)

    shadow_offset = 10
    draw.text((position[0] + shadow_offset, position[1] + shadow_offset), name, fill='black', font=font)
    draw.text(position, name, fill=text_color, font=font)
    banner.show()
    banner.save('anand.png')
create_named_banner(
    name='Anand',
    banner_size=(1920, 1080),
    text_color='white',
    banner_color='black'
)
