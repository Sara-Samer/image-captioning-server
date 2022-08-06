from flask import Flask, render_template, request
# if you encounter dependency issues using 'pip install flask-uploads'
# try 'pip install Flask-Reuploaded'
from flask_uploads import UploadSet, configure_uploads, IMAGES
from inference import infer_caption
# from keras.preprocessing.image import load_img
# the pretrained model
# from model import process_image, predict_class

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

# path for saving uploaded images
app.config['UPLOADED_PHOTOS_DEST'] = './static/img'
configure_uploads(app, photos)

# professionals have standards :p
@app.route('/home', methods=['GET', 'POST'])
def home():
    welcome = "Hello, World !"
    return welcome

# the main route for upload and prediction
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        # save the image
        filename = photos.save(request.files['photo'])
        # load the image
        img_path = './static/img/' + filename
        caption = infer_caption(img_path)
        # image = load_img('./static/img/'+filename, target_size=(224, 224))
        # process the image
        # image = process_image(image)
        # make prediction
        # prediction, percentage = predict_class(image)
        # the answer which will be rendered back to the user
        answer = "<br>The Caption is is : {}".format(caption)
        return answer
    # web page to show before the POST request containing the image
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)