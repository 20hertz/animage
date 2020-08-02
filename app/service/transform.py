from flask import request, abort, Blueprint, current_app, jsonify
from functools import wraps
from http import HTTPStatus
from werkzeug.utils import secure_filename
import base64
import cv2
import os
import numpy as np

MIME_TYPES = {"image/jpeg"}

transform_blueprint = Blueprint("transform", __name__)

# @cross_origin(
#     origin="https://d289aztbzuse4k.cloudfront.net",
#     headers=["Content- Type", "Authorization"],
# )


def safe_run(func, image):
    UPLOAD_FOLDER = current_app.config["UPLOAD_FOLDER"]
    try:
        with_detected_shapes = func(image)
        encoded_img = save_transformation(with_detected_shapes, UPLOAD_FOLDER)
        return jsonify(body=encoded_img)
    except TypeError:
        current_app.logger.debug("HoughLinesP failed")
        encoded_img = save_transformation(image, UPLOAD_FOLDER)
        return (
            jsonify(
                message="Sorry, no lines were detected.  No edits were made to the image.",  # noqa
            ),
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )
    else:
        current_app.logger.debug("Unknown error")
        return (
            jsonify(
                message="Sorry, something went wrong processing this image.  It's not you it's us.",  # noqa
            ),
            HTTPStatus.NOT_IMPLEMENTED,
        )


def ingest(effect):
    @wraps(effect)
    def wrapper():
        attachment = request.files.get("image")
        if not attachment:
            abort(HTTPStatus.BAD_REQUEST, "no file was attached")

        validate_attachment(attachment)

        image = save_file(attachment)

        return safe_run(effect(), image)

    return wrapper


def validate_attachment(attachment):
    is_mime_type_allowed = attachment.content_type == "image/jpeg"
    if not is_mime_type_allowed:
        abort(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "allowed MIME type is image/jpeg")


def save_file(attachment):
    UPLOAD_FOLDER = current_app.config["UPLOAD_FOLDER"]
    filename = secure_filename(attachment.filename)  # save file
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    attachment.save(filepath)
    image = cv2.imread(filepath)
    return image


def applyGrayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def applyEdgeDetection(image):
    return cv2.Canny(image, threshold1=30, threshold2=100)


def save_transformation(image, upload_dir):
    # Write image image to UPLOAD_FOLDER
    cv2.imwrite(os.path.join(upload_dir, "transformed.jpg"), image)

    with open(f"{upload_dir}/transformed.jpg", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        encoded_img = str.decode("utf-8")

    return encoded_img


def apply_grayscale(image):
    gray = applyGrayscale(image)
    return gray


def apply_canny(image):
    gray = applyGrayscale(image)
    edges = applyEdgeDetection(gray)
    return edges


def apply_contour(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = applyGrayscale(rgb)
    _, binary = cv2.threshold(gray, 255, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    image_with_added_contour = cv2.drawContours(rgb, contours, -1, (0, 255, 0), 2)
    return image_with_added_contour


def detect_lines(image):
    gray = applyGrayscale(image)
    edges = applyEdgeDetection(gray)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 60, np.array([]), 50, 5)
    if lines is None:
        raise TypeError("HoughLinesP failed")
        # return None
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), (20, 220, 20), 3)
            return image


@transform_blueprint.route("/grayscale", methods=["POST"])
@ingest
def grayscale():
    return apply_grayscale


@transform_blueprint.route("/edges", methods=["POST"])
@ingest
def edges():
    return apply_canny


@transform_blueprint.route("/contour", methods=["POST"])
@ingest
def contour():
    return apply_contour


@transform_blueprint.route("/shapes", methods=["POST"])
@ingest
def shapes():
    return detect_lines
