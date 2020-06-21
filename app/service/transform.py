from flask import request, flash, Blueprint, current_app
from werkzeug.utils import secure_filename
import base64
import cv2
import os
from flask_cors import CORS

# @app.before_request
# def log_request_info(app):
#     app.logger.debug("Headers: %s", request.headers)
#     app.logger.debug("Body: %s", request.get_data())

transform_blueprint = Blueprint("transform", __name__)

CORS(
    transform_blueprint,
    resources={
        r"/": {
            "origins": [
                "http://localhost:1234",
                "https://d289aztbzuse4k.cloudfront.net",
            ]
        }
    },
)


@transform_blueprint.route("/", methods=["POST"])
def upload():

    if "image" not in request.files:
        flash("No file part")
        return "Please include an image."

    file = request.files["image"]

    filename = secure_filename(file.filename)  # save file
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)
    image = cv2.imread(filepath)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Write grayscale image to /tmp
    cv2.imwrite(os.path.join(current_app.config["UPLOAD_FOLDER"], "gray.jpg"), gray)

    with open("/tmp/gray.jpg", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        encoded_img = str.decode("utf-8")

    return {"body": encoded_img}
