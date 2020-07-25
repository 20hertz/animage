from flask import request, abort, Blueprint, current_app
from functools import wraps
from http import HTTPStatus
from werkzeug.utils import secure_filename
import base64
import cv2
import os

MIME_TYPES = {"image/jpeg"}

transform_blueprint = Blueprint("transform", __name__)

# @cross_origin(
#     origin="https://d289aztbzuse4k.cloudfront.net",
#     headers=["Content- Type", "Authorization"],
# )


def ingest(effect):
    @wraps(effect)
    def wrapper():
        attachment = request.files.get("image")

        if not attachment:
            abort(HTTPStatus.BAD_REQUEST, "no file was attached")

        validate_attachment(attachment)

        image = save_file(attachment)

        return effect(image)

    return wrapper


def validate_attachment(attachment):
    is_mime_type_allowed = attachment.content_type == "image/jpeg"
    if not is_mime_type_allowed:
        abort(HTTPStatus.BAD_REQUEST, "allowed MIME type is image/jpeg")


def save_file(attachment):
    UPLOAD_FOLDER = current_app.config["UPLOAD_FOLDER"]
    filename = secure_filename(attachment.filename)  # save file
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    attachment.save(filepath)
    image = cv2.imread(filepath)
    return image


@transform_blueprint.route("/grayscale", methods=["POST"])
@ingest
def grayscale(image):

    UPLOAD_FOLDER = current_app.config["UPLOAD_FOLDER"]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Write grayscale image to UPLOAD_FOLDER
    cv2.imwrite(os.path.join(current_app.config["UPLOAD_FOLDER"], "gray.jpg"), gray)

    with open(f"{UPLOAD_FOLDER}/gray.jpg", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        encoded_img = str.decode("utf-8")

    return {"body": encoded_img}


@transform_blueprint.route("/edges", methods=["POST"])
@ingest
def canny(image):

    UPLOAD_FOLDER = current_app.config["UPLOAD_FOLDER"]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=30, threshold2=100)
    # Write detected edges image to UPLOAD_FOLDER
    cv2.imwrite(os.path.join(UPLOAD_FOLDER, "edges.jpg"), edges)

    with open(f"{UPLOAD_FOLDER}/edges.jpg", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        encoded_img = str.decode("utf-8")

    return {"body": encoded_img}


@transform_blueprint.route("/contour", methods=["POST"])
@ingest
def contour(image):

    UPLOAD_FOLDER = current_app.config["UPLOAD_FOLDER"]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 255, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    image_with_added_contour = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

    # Write new image to UPLOAD_FOLDER
    cv2.imwrite(
        os.path.join(UPLOAD_FOLDER, "contour.jpg"), image_with_added_contour,
    )

    with open(f"{UPLOAD_FOLDER}/contour.jpg", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        encoded_img = str.decode("utf-8")

    return {"body": encoded_img}
