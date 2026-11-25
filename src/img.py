import os
import io
import zipfile

from PIL import Image, ImageDraw, ImageFont
from wand.image import Image as WImage

import util

font_styles = ["Thin", "Light", "Regular", "Medium", "Bold", "Black"]


def make(params, files, config, logger):
    for_ios = util.get_int_param(params, "for_ios", 0)
    for_web = util.get_int_param(params, "for_web", 0)

    icon_size = (1024, 1024) if for_ios else (512, 512) if for_web else (256, 256)
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

        offset_x = util.get_int_param(params, "image_offset_x", 0, for_ios, for_web)
        offset_y = util.get_int_param(params, "image_offset_y", 0, for_ios, for_web)

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
        font_style = util.get_int_param(params, "font_style", 2)
        font_size = util.get_int_param(params, "font_size", 100, for_ios, for_web)

        lang = util.get_param(params, "lang", "en")
        font = config.get("fonts", lang)
        font_style_name = font_styles[font_style]
        font_name = font.format(font_style_name)
        font_path = os.path.join("fonts", font_name)
        font = ImageFont.truetype(font_path, font_size)

        offset_x = util.get_int_param(params, "text_offset_x", 0, for_ios, for_web)
        offset_y = util.get_int_param(params, "text_offset_y", 0, for_ios, for_web)

        font_img = Image.new("RGBA", icon_size, (0, 0, 0, 0))
        font_draw = ImageDraw.Draw(font_img)

        lines = text.splitlines()
        coefficient = config.getfloat("coefficient", lang)
        y = icon.size[1] / 2 - len(lines) * (font_size * coefficient) + offset_y
        for line in lines:
            length = draw.textlength(line, font=font)
            x = icon.size[0] / 2 - length / 2 + offset_x
            font_draw.multiline_text((x, y), line, font=font, fill=text_color)
            y += font_size - 6

        font_rotate = util.get_int_param(params, "font_rotate", 0)
        font_img = font_img.rotate(font_rotate)

        icon.paste(font_img, mask=font_img)

    style = util.get_int_param(params, "style", 0)
    if style > 0:
        style_img = Image.new("L", icon_size, 0)
        style_draw = ImageDraw.Draw(style_img)

        if style == 1:
            r = util.get_int_param(params, "round", 0, for_ios, for_web)

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
    if for_ios:
        with zipfile.ZipFile(file, "w", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("icon_1024.png", get_bytes(icon))
            for size in [20, 29, 40, 58, 60, 76, 80, 87, 120, 152, 167, 180]:
                z.writestr("icon_{}.png".format(size), get_bytes(icon, size=size))
    elif for_web:
        with zipfile.ZipFile(file, "w", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("favicon.ico", make_favicon(icon))
            z.writestr("apple-touch-icon.png", get_bytes(icon, 180))
            z.writestr("icon-192.png", get_bytes(icon, 192))
            z.writestr("icon-512.png", get_bytes(icon, 512))
            z.write("manifest.webmanifest")
            z.write("sample.html")
    else:
        icon.save(file, "png")

    file.seek(0)

    return file


def get_bytes(icon, size=None):
    if size is not None:
        icon = icon.resize((size, size))

    with io.BytesIO() as icon_file:
        icon.save(icon_file, "png")
        icon_file.seek(0)
        value = icon_file.getvalue()

    return value


def make_favicon(icon):
    favicon = io.BytesIO()
    with WImage(blob=get_bytes(icon, 32)) as png32:
        ico32 = png32.convert("ico")
        with WImage(blob=get_bytes(icon, 16)) as png16:
            ico16 = png16.convert("ico")
            ico32.sequence.append(ico16)
        ico32.save(file=favicon)
    favicon.seek(0)

    return favicon.getvalue()
