import io
import os.path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import util

font_styles = ["Thin", "Light", "Regular", "Medium", "Bold", "Black"]


def make(params, files, config, logger):
    icon_size = (256, 256)
    bg_color = util.get_param(params, "bg_color", "#000000")

    icon = Image.new("RGB", icon_size, bg_color)
    draw = ImageDraw.Draw(icon)

    image_file = util.get_param(files, "image", None)
    if image_file is not None:
        image_size = util.get_int_param(params, "image_size", 100) / 100
        image = Image.open(image_file)

        # 貼り付ける画像をアスペクト比を保ったままアイコンサイズにリサイズ
        width = int(icon_size[0] * image_size)
        height = int(width * image.size[1] / image.size[0])
        image = image.resize((width, height))

        image_rotate = util.get_int_param(params, "image_rotate", 0)
        image = image.rotate(image_rotate)

        offset_x = util.get_int_param(params, "image_offset_x", 0)
        offset_y = util.get_int_param(params, "image_offset_y", 0)

        x = int((icon_size[0] - image.size[0]) / 2) + offset_x
        y = int((icon_size[1] - image.size[1]) / 2) + offset_y
        ch = image.split()
        if len(ch) == 4:
            icon.paste(image, (x, y), image)
        else:
            icon.paste(image, (x, y))

    text = util.get_param(params, "text", "")
    if text:
        text_color = util.get_param(params, "text_color", "#ffffff")
        font_idx = util.get_param(params, "font", 0)
        font_size = util.get_int_param(params, "font_size", 100)
        font_style = util.get_int_param(params, "font_style", 2)

        font = config.get("fonts", font_idx)
        font_style_name = font_styles[font_style]
        font_name = "static/{}-{}.ttf".format(font, font_style_name)
        font = ImageFont.truetype(font_name, font_size)

        offset_x = util.get_int_param(params, "text_offset_x", 0)
        offset_y = util.get_int_param(params, "text_offset_y", 0)

        font_img = Image.new("RGBA", icon_size, (0, 0, 0, 0))
        font_draw = ImageDraw.Draw(font_img)

        lines = text.splitlines()
        coefficient = config.getfloat("coefficient", font_idx)
        y = icon.size[1] / 2 - len(lines) * (font_size * coefficient) + offset_y
        for line in lines:
            length = draw.textlength(line, font=font)
            x = icon.size[0] / 2 - length / 2 + offset_x
            font_draw.multiline_text((x, y), line, font=font, fill=text_color)
            y += font_size

        font_rotate = util.get_int_param(params, "font_rotate", 0)
        font_img = font_img.rotate(font_rotate)

        icon.paste(font_img, mask=font_img)

    style = util.get_int_param(params, "style", 0)
    if style > 0:
        style_img = Image.new("L", icon_size, 0)
        style_draw = ImageDraw.Draw(style_img)

        if style == 1:
            r = util.get_int_param(params, "round", 0)
            style_draw.rectangle((0, r, icon_size[0] - 1, icon_size[1] - 1 - r), fill=255)
            style_draw.rectangle((r, 0, icon_size[0] - 1 - r, icon_size[1] - 1), fill=255)
            style_draw.pieslice((0, 0) + (r * 2, r * 2), 180, 270, fill=255)
            style_draw.pieslice((0, icon_size[1] - 1 - r * 2) + (r * 2, icon_size[1] - 1), 90, 180, fill=255)
            style_draw.pieslice((icon_size[0] - 1 - r * 2, icon_size[1] - 1 - r * 2) +
                      (icon_size[0] - 1, icon_size[1] - 1), 0, 180, fill=255)
            style_draw.pieslice((icon_size[0] - 1 - r * 2, 0) +
                      (icon_size[0] - 1, r * 2), 270, 360, fill=255)
        elif style == 2:
            style_draw.ellipse((0, 0, icon_size[0] - 1, icon_size[1] - 1), fill=255)
        icon.putalpha(style_img)

    file = io.BytesIO()
    icon.save(file, "png")
    file.seek(0)

    return file
