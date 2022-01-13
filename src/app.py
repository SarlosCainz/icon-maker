import logging
from configparser import ConfigParser
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS

import img
import util

app = Flask(__name__)
CORS(app)
if not app.debug:
    logging.basicConfig(level=logging.INFO)

config = ConfigParser()
config.read("config.ini", 'UTF-8')


@app.route('/api/img', methods=['POST'])
def api_img():
    img_file = img.make(request.form, request.files, config, app.logger)
    response = send_file(img_file, attachment_filename="icon", as_attachment=True)

    return response


@app.route('/api/lang', methods=['GET'])
def api_lang():
    result = {
        "default": "en",
        "list": []
    }
    lang_conf = config["lang"]

    accept_lang = util.get_param(request.headers, "Accept-Language", "en")
    for lang in accept_lang.split(","):
        lang = lang.split(";")[0].lower()
        if lang in lang_conf:
            result["default"] = lang
            app.logger.debug(lang)
            break

    for key in config["lang"]:
        lang = config.get("lang", key)
        result["list"].append({"idx": key, "lang": lang})

    return jsonify(result)


if __name__ == '__main__':
    app.run()
