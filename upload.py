from flask import Flask, render_template, jsonify, request
# if you encounter dependency issues using 'pip install flask-uploads'
# try 'pip install Flask-Reuploaded'
from flask_uploads import UploadSet, configure_uploads, IMAGES
from inference import infer_caption
from models import get_cnn_model
import os
from PIL import Image
import base64
import io
# from keras.preprocessing.image import load_img
# the pretrained model
# from model import process_image, predict_class

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

# path for saving uploaded images
app.config['UPLOADED_PHOTOS_DEST'] = './static/img'
configure_uploads(app, photos)

# professionals have standards :p
@app.route('/', methods=['GET', 'POST'])
def home():
    welcome = "Hello, World !"
    return welcome

# the main route for upload and prediction
@app.route('/caption', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        print('inferring')
        # save the image

        filename = photos.save(request.files['photo'])
        # load the image
        img_path = './static/img/' + filename
        caption = infer_caption(img_path)
        im = Image.open(img_path)
        data = io.BytesIO()
        #First save image as in-memory.
        im.save(data, "JPEG")
        #Then encode the saved image file.
        encoded_img_data = base64.b64encode(data.getvalue())

        os.remove(img_path)

        return render_template("caption.html", img_data=encoded_img_data.decode('utf-8'), caption=caption)

    # web page to show before the POST request containing the image
    return render_template('upload.html')

@app.route('/caption-api', methods=['POST'])
def caption():
    # save the image
    filename = photos.save(request.files['photo'])
    # load the image
    img_path = './static/img/' + filename
    caption = infer_caption(img_path)
    os.remove(img_path)
    # the answer which will be rendered back to the user
    return jsonify({'caption': caption})
    # web page to show before the POST request containing the image



if __name__ == '__main__':
    get_cnn_model()

    app.run(host='0.0.0.0', debug=True)
