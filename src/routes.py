from flask import request, flash
from werkzeug.utils import secure_filename
import base64
import cv2
import os


def configure_routes(app):

    @app.route('/', methods=['POST'])
    def upload():

        if 'image' not in request.files:
            flash('No file part')
            return 'Please include an image.'

        file = request.files['image']
        filename = secure_filename(file.filename)  # save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        image = cv2.imread(filepath)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Write grayscale image to /tmp
        cv2.imwrite(os.path.join(
            app.config['UPLOAD_FOLDER'], 'gray.jpg'), gray)

        with open('/tmp/gray.jpg', 'rb') as imageFile:
            str = base64.b64encode(imageFile.read())
            encoded_img = str.decode('utf-8')

        return {
            'body': encoded_img
        }


# f = request.files['the_file']
# content = f.stream.read()
# if isinstance(content, str): print('content is str')
# content = content.decode('utf-8')
# if isinstance(content, unicode): print('content is unicode')
