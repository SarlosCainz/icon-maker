import io
import shutil
import sys
from configparser import ConfigParser
from pathlib import Path

import pytest
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
TEST_FONT = FIXTURES / "fonts" / "Roboto-Regular.ttf"

# img.font_styles と同じ順。conftest で参照するため値をここにも持つ
WEIGHTS = ["Thin", "Light", "Regular", "Medium", "Bold", "Black"]


@pytest.fixture
def app_dir(tmp_path, monkeypatch):
    """app.py / img.py がカレントディレクトリに期待するものを tmp_path に組み立てる

    docs/test.md の「前提の作り方」を参照。
    """
    # config.ini は misc/config.ini の [fonts] だけテスト用フォントに差し替えて書く (docs/test.md T5)
    conf = ConfigParser()
    conf.read(REPO / "misc" / "config.ini", "UTF-8")
    assert conf.has_section("fonts"), "misc/config.ini に [fonts] が無い"
    for key in conf["fonts"]:
        conf.set("fonts", key, "Roboto-{}.ttf")
    with (tmp_path / "config.ini").open("w", encoding="UTF-8") as f:
        conf.write(f)

    # fonts/ はテスト用フォント 1 本を 6 ウェイト分の名前にコピーして作る (docs/test.md T4)
    fonts = tmp_path / "fonts"
    fonts.mkdir()
    for weight in WEIGHTS:
        shutil.copy(TEST_FONT, fonts / "Roboto-{}.ttf".format(weight))

    # for_web の zip に入る同梱ファイル。img.py がカレントディレクトリ相対で読む
    for name in ("manifest.webmanifest", "sample.html"):
        shutil.copy(REPO / "misc" / name, tmp_path / name)

    monkeypatch.chdir(tmp_path)

    return tmp_path


@pytest.fixture
def config(app_dir):
    conf = ConfigParser()
    conf.read(app_dir / "config.ini", "UTF-8")

    return conf


@pytest.fixture
def logger():
    import logging

    return logging.getLogger("test")


@pytest.fixture
def app_module(app_dir):
    """chdir したあとに app を import する

    app.py は import 時にカレントディレクトリの config.ini を読むため、順序が重要
    (docs/test.md の「前提の作り方」)。モジュール変数に設定を持つのでテストごとに読み直す。
    """
    for name in ("app", "img", "util"):
        sys.modules.pop(name, None)
    import app as module

    return module


@pytest.fixture
def client(app_module):
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as c:
        yield c


def png_bytes(size, mode="RGB", color=(255, 0, 0)):
    """テストで貼り付ける画像を作る (docs/test.md T8)"""
    if mode == "RGBA" and len(color) == 3:
        color = color + (128,)
    image = Image.new(mode, size, color)
    buf = io.BytesIO()
    image.save(buf, "png")
    buf.seek(0)

    return buf
