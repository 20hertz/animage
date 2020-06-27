from flask import request, abort, Blueprint, current_app
from http import HTTPStatus
from werkzeug.utils import secure_filename
import base64
import cv2
import os

transform_blueprint = Blueprint("transform", __name__)

MIME_TYPES = {"image/jpeg"}


@transform_blueprint.route("/", methods=["POST"])
def upload():

    files = request.files
    attachment = files.get("image")

    if not attachment:
        abort(HTTPStatus.BAD_REQUEST, "no file was attached")

    validate_attachment(attachment)

    filename = secure_filename(attachment.filename)  # save file
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    attachment.save(filepath)
    image = cv2.imread(filepath)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Write grayscale image to /tmp
    cv2.imwrite(os.path.join(current_app.config["UPLOAD_FOLDER"], "gray.jpg"), gray)

    with open("/tmp/gray.jpg", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        encoded_img = str.decode("utf-8")

    return {"body": encoded_img}, 200


def validate_attachment(attachment):
    is_mime_type_allowed = attachment.content_type == "image/jpeg"
    if not is_mime_type_allowed:
        abort(HTTPStatus.BAD_REQUEST, "allowed MIME type is image/jpeg")
