import logging
from configparser import ConfigParser
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS

import img

app = Flask(__name__)
CORS(app)
if not app.debug:
    logging.basicConfig(level=logging.INFO)

config = ConfigParser()
config.read("config.ini", 'UTF-8')


@app.route('/api/img', methods=['POST'])
def api_img():
    img_file = img.make(request.form, request.files, config, app.logger)
    response = send_file(img_file, attachment_filename="icon.png", as_attachment=True)

    return response


@app.route('/api/fonts', methods=['GET'])
def api_fonts():
    result = []

    for key in config["fonts"]:
        font = config.get("fonts", key)
        result.append({"idx": key, "font": font})

    return jsonify(result)


if __name__ == '__main__':
    app.run()
