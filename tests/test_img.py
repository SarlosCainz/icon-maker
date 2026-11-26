import io
import zipfile

import pytest
from PIL import Image

import img
import util
from conftest import png_bytes

# wand の import には ImageMagick の共有ライブラリが必要 (docs/test.md T6)
wand_image = pytest.importorskip("wand.image", reason="ImageMagick が無いため skip する")


def make(config, logger, params=None, files=None):
    return img.make(params or {}, files or {}, config, logger)


def open_icon(file):
    return Image.open(file)


def test_default_is_256_rgb_png(config, logger):
    """I1"""
    icon = open_icon(make(config, logger))
    assert icon.format == "PNG"
    assert icon.size == (256, 256)
    assert icon.mode == "RGB"


@pytest.mark.imagemagick
def test_for_web_returns_zip_with_six_entries(config, logger):
    """I2"""
    with zipfile.ZipFile(make(config, logger, {"for_web": 1})) as z:
        assert sorted(z.namelist()) == sorted([
            "favicon.ico",
            "apple-touch-icon.png",
            "icon-192.png",
            "icon-512.png",
            "manifest.webmanifest",
            "sample.html",
        ])


def test_for_ios_returns_zip_with_thirteen_entries(config, logger):
    """I3"""
    sizes = [20, 29, 40, 58, 60, 76, 80, 87, 120, 152, 167, 180]
    with zipfile.ZipFile(make(config, logger, {"for_ios": 1})) as z:
        assert sorted(z.namelist()) == sorted(
            ["icon_1024.png"] + ["icon_{}.png".format(s) for s in sizes])
        for size in sizes:
            with z.open("icon_{}.png".format(size)) as f:
                assert Image.open(io.BytesIO(f.read())).size == (size, size)
        with z.open("icon_1024.png") as f:
            assert Image.open(io.BytesIO(f.read())).size == (1024, 1024)


def test_bg_color_is_used(config, logger):
    """I4"""
    icon = open_icon(make(config, logger, {"bg_color": "#123456"}))
    assert icon.getpixel((0, 0)) == (0x12, 0x34, 0x56)


def test_text_is_drawn(config, logger):
    """I5 位置は検証せず、背景色以外のピクセルが生まれたことだけを見る (docs/test.md B5)"""
    params = {"text": "M", "bg_color": "#000000", "text_color": "#ffffff"}
    icon = open_icon(make(config, logger, params))
    assert icon.getcolors(maxcolors=65536) is None or len(icon.getcolors(maxcolors=65536)) > 1


def test_text_with_japanese_font(config, logger):
    """I6"""
    icon = open_icon(make(config, logger, {"text": "あ", "lang": "ja"}))
    assert icon.size == (256, 256)


def test_unknown_lang_is_rejected(config, logger):
    """I7"""
    with pytest.raises(util.InvalidParam) as e:
        make(config, logger, {"text": "M", "lang": "xx"})
    assert e.value.param == "lang"


@pytest.mark.parametrize("font_style", [6, -1])
def test_font_style_out_of_range_is_rejected(config, logger, font_style):
    """I8"""
    with pytest.raises(util.InvalidParam) as e:
        make(config, logger, {"text": "M", "font_style": font_style})
    assert e.value.param == "font_style"


def test_style_round_makes_corners_transparent(config, logger):
    """I9"""
    icon = open_icon(make(config, logger, {"style": 1, "round": 30}))
    assert icon.mode == "RGBA"
    assert icon.getpixel((0, 0))[3] == 0
    assert icon.getpixel((128, 128))[3] == 255


def test_style_circle_makes_corners_transparent(config, logger):
    """I10"""
    icon = open_icon(make(config, logger, {"style": 2}))
    assert icon.mode == "RGBA"
    for xy in [(0, 0), (255, 0), (0, 255), (255, 255)]:
        assert icon.getpixel(xy)[3] == 0
    assert icon.getpixel((128, 128))[3] == 255


def test_style_none_has_no_alpha(config, logger):
    """I11"""
    assert open_icon(make(config, logger, {"style": 0})).mode == "RGB"


def test_rgb_image_is_pasted(config, logger):
    """I12"""
    files = {"image": png_bytes((100, 100), "RGB")}
    assert open_icon(make(config, logger, {}, files)).size == (256, 256)


def test_rgba_image_is_pasted_with_mask(config, logger):
    """I13"""
    files = {"image": png_bytes((100, 100), "RGBA")}
    assert open_icon(make(config, logger, {}, files)).size == (256, 256)


def test_image_size_does_not_change_icon_size(config, logger):
    """I14"""
    files = {"image": png_bytes((100, 100), "RGB")}
    assert open_icon(make(config, logger, {"image_size": 50}, files)).size == (256, 256)


def test_image_rotate_does_not_raise(config, logger):
    """I15"""
    files = {"image": png_bytes((100, 100), "RGB")}
    assert open_icon(make(config, logger, {"image_rotate": 90}, files)).size == (256, 256)


def test_get_bytes_resizes(config, logger):
    """I16"""
    icon = Image.new("RGB", (256, 256), "#000000")
    assert Image.open(io.BytesIO(img.get_bytes(icon, size=64))).size == (64, 64)


@pytest.mark.imagemagick
def test_make_favicon_returns_ico(config, logger):
    """I17"""
    icon = Image.new("RGB", (256, 256), "#000000")
    assert Image.open(io.BytesIO(img.make_favicon(icon))).format == "ICO"


def test_for_ios_wins_over_for_web(config, logger):
    """I18"""
    with zipfile.ZipFile(make(config, logger, {"for_ios": 1, "for_web": 1})) as z:
        assert "icon_1024.png" in z.namelist()


def test_style_out_of_range_is_rejected(config, logger):
    """I19"""
    with pytest.raises(util.InvalidParam) as e:
        make(config, logger, {"style": 3})
    assert e.value.param == "style"


@pytest.mark.parametrize("output", [{}, {"for_web": 1}, {"for_ios": 1}])
def test_round_upper_bound_works_for_every_size(config, logger, output):
    """I20 round の上限は、どの書き出しサイズでも Pillow が描ける最大値になっている"""
    params = {"style": 1, "round": img.LIMITS["round"][1]}
    params.update(output)
    if output.get("for_web"):
        pytest.importorskip("wand.image")
    make(config, logger, params)


def test_round_over_upper_bound_is_rejected(config, logger):
    """I20"""
    with pytest.raises(util.InvalidParam) as e:
        make(config, logger, {"style": 1, "round": img.LIMITS["round"][1] + 1})
    assert e.value.param == "round"


@pytest.mark.parametrize("key", ["bg_color", "text_color"])
def test_invalid_color_is_rejected(config, logger, key):
    """I21"""
    params = {"text": "M", key: "zzz"}
    with pytest.raises(util.InvalidParam) as e:
        make(config, logger, params)
    assert e.value.param == key


def test_text_at_length_limit_is_accepted(config, logger):
    """I22"""
    make(config, logger, {"text": "M" * img.TEXT_MAX_LENGTH})


def test_text_over_length_limit_is_rejected(config, logger):
    """I22"""
    with pytest.raises(util.InvalidParam) as e:
        make(config, logger, {"text": "M" * (img.TEXT_MAX_LENGTH + 1)})
    assert e.value.param == "text"


def test_text_at_line_limit_is_accepted(config, logger):
    """I22"""
    make(config, logger, {"text": "\n".join(["M"] * img.TEXT_MAX_LINES)})


def test_text_over_line_limit_is_rejected(config, logger):
    """I22"""
    text = "\n".join(["M"] * (img.TEXT_MAX_LINES + 1))
    with pytest.raises(util.InvalidParam) as e:
        make(config, logger, {"text": text})
    assert e.value.param == "text"


def test_non_image_upload_is_rejected(config, logger):
    """I23"""
    files = {"image": io.BytesIO(b"this is not an image")}
    with pytest.raises(util.InvalidParam) as e:
        make(config, logger, {}, files)
    assert e.value.param == "image"


def test_too_many_pixels_is_rejected(config, logger, monkeypatch):
    """I24 上限そのものを下げて経路を通す (巨大な画像を作らない)"""
    monkeypatch.setattr(img, "IMAGE_MAX_PIXELS", 100)
    files = {"image": png_bytes((20, 20), "RGB")}
    with pytest.raises(util.InvalidParam) as e:
        make(config, logger, {}, files)
    assert e.value.param == "image"


# UI (ui/src/components/Body.jsx) のスライダー・ラジオが取りうる端の値 (docs/validation.md)
UI_EDGE_VALUES = {
    "style": [0, 1, 2],
    "round": [30, 90],
    "font_style": [0, 5],
    "font_size": [20, 400],
    "font_rotate": [-180, 180],
    "text_offset_x": [-100, 100],
    "text_offset_y": [-100, 100],
    "image_size": [30, 200],
    "image_rotate": [-180, 180],
    "image_offset_x": [-100, 100],
    "image_offset_y": [-100, 100],
    "for_ios": [0, 1],
    "for_web": [0, 1],
}


@pytest.mark.parametrize("key,value", [(k, v) for k, vs in UI_EDGE_VALUES.items() for v in vs])
def test_ui_edge_values_are_accepted(config, logger, key, value):
    """I25 画面の操作が 400 にならないことを担保する (docs/validation.md のリスク)"""
    minimum, maximum = img.LIMITS[key]
    assert minimum <= value <= maximum, "UI の範囲が LIMITS の外に出ている"
