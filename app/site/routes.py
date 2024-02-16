from flask import Blueprint, render_template, url_for, redirect, flash, request, send_file
from app.models import  db, Image as DBImage
from .. import site
from io import BytesIO
from PIL import Image as PILImage
from werkzeug.utils import secure_filename

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/meme-me.html')
def mememe():
    return render_template('meme-me.html')
@site.route('/about.html')
def about():
    return render_template('about.html')


@site.route('/profile.html')
def profile():
    return render_template('profile.html')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@site.route('/upload_route', methods=['GET', 'POST'])
def upload_route():
    if 'file' not in request.files:
        return render_template('upload.html')

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print('Received file:', filename)

        pil_image = PILImage.open(BytesIO(file.read()))

        
        pil_image = pil_image.convert('RGB')

        resized_image = pil_image.resize((450, 250), PILImage.BICUBIC)

        image_data_io = BytesIO()
        resized_image.save(image_data_io, format='JPEG') 

        new_image = DBImage(filename=filename, data=image_data_io.getvalue())

        db.session.add(new_image)
        db.session.commit()

        print('Changes made to the database.')

        return render_template('meme-me.html', uploaded_image=new_image)

    return render_template('upload.html', error='Invalid file type')
    

@site.route('/display_image/<int:image_id>')
def display_image(image_id):
    image = DBImage.query.get_or_404(image_id)
    return send_file(BytesIO(image.data), mimetype="image/jpeg")