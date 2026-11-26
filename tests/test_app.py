import io
from configparser import ConfigParser

import pytest

from conftest import REPO, png_bytes

PNG_MAGIC = b"\x89PNG"
ZIP_MAGIC = b"PK"


def config_langs():
    conf = ConfigParser()
    conf.read(REPO / "misc" / "config.ini", "UTF-8")

    return [{"idx": key, "lang": conf.get("lang", key)} for key in conf["lang"]]


def test_index_returns_empty(client):
    """A1"""
    res = client.get("/")
    assert res.status_code == 200
    assert res.data == b""


def test_lang_without_header(client):
    """A2"""
    res = client.get("/api/lang")
    assert res.status_code == 200
    body = res.get_json()
    assert body["default"] == "en"
    assert body["list"] == config_langs()


@pytest.mark.parametrize("header,expected", [
    ("ja", "ja"),              # A3
    ("ja;q=0.9", "ja"),        # A4
    ("JA", "ja"),              # A5
    ("fr", "en"),              # A6
    ("fr,ja", "ja"),           # A7 ブラウザが送る空白なしの形式は 2 番目以降も一致する
    ("ja,en-US;q=0.9,en;q=0.8", "ja"),  # A7 実際のブラウザの形式
    ("fr, ja", "en"),          # A7 空白付きは一致しない (現在の挙動。docs/test.md B1)
    ("zh-hans", "zh-hans"),    # A8
])
def test_lang_from_accept_language(client, header, expected):
    """A3〜A8"""
    res = client.get("/api/lang", headers={"Accept-Language": header})
    assert res.get_json()["default"] == expected


def test_img_returns_png(client):
    """A9"""
    res = client.post("/api/img", data={})
    assert res.status_code == 200
    assert res.data.startswith(PNG_MAGIC)


def test_img_response_headers(client):
    """A10 Content-Type は download_name="icon" に拡張子が無いため推定されない (docs/test.md B6)"""
    res = client.post("/api/img", data={})
    disposition = res.headers["Content-Disposition"]
    assert "attachment" in disposition
    assert "filename=icon" in disposition
    assert res.headers["Content-Type"] == "application/octet-stream"


@pytest.mark.imagemagick
def test_img_for_web_returns_zip(client):
    """A11"""
    res = client.post("/api/img", data={"for_web": 1})
    assert res.status_code == 200
    assert res.data.startswith(ZIP_MAGIC)


def test_img_with_uploaded_image(client):
    """A12"""
    data = {"image": (png_bytes((100, 100), "RGB"), "src.png")}
    res = client.post("/api/img", data=data, content_type="multipart/form-data")
    assert res.status_code == 200
    assert res.data.startswith(PNG_MAGIC)


def test_img_rejects_get(client):
    """A13"""
    assert client.get("/api/img").status_code == 405


def test_img_rejects_non_number(client):
    """A14"""
    res = client.post("/api/img", data={"font_size": "abc", "text": "M"})
    assert res.status_code == 400
    assert res.get_json()["param"] == "font_size"


def test_img_rejects_unknown_lang(client):
    """A15"""
    res = client.post("/api/img", data={"text": "M", "lang": "xx"})
    assert res.status_code == 400
    assert res.get_json()["param"] == "lang"


def test_bad_request_body_shape(client):
    """A16"""
    res = client.post("/api/img", data={"style": "9"})
    assert res.status_code == 400
    assert res.headers["Content-Type"].startswith("application/json")
    body = res.get_json()
    assert set(body) == {"error", "param", "reason"}
    assert body["error"] == "invalid parameter"
    assert body["param"] == "style"
    assert body["reason"]


def test_too_large_body_returns_413(app_module):
    """A17 実際に 8MB を送らず、上限を下げて経路を確認する (docs/validation.md V7)"""
    app_module.app.config.update(TESTING=True, MAX_CONTENT_LENGTH=1024)
    with app_module.app.test_client() as client:
        data = {"image": (io.BytesIO(b"x" * 4096), "src.png")}
        res = client.post("/api/img", data=data, content_type="multipart/form-data")
    assert res.status_code == 413
