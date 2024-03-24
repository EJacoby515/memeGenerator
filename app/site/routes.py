from flask import Blueprint, render_template, redirect, flash, request, send_file, url_for
from flask_login import current_user
from app.models import db, Image as DBImage
from .. import site
from io import BytesIO
from PIL import Image as PILImage
from werkzeug.utils import secure_filename

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/about')
def about():
    return render_template('about.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')

@site.route('/mememe')
def mememe():
    return render_template('meme-me.html')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@site.route('/upload_route', methods=['GET','POST'])
def upload_route():
    if 'file' not in request.files:
        return render_template('upload.html', error ='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('upload.html',  error = 'No selected file')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print('Received file:', filename)

        pil_image = PILImage.open(file)
        pil_image = pil_image.convert('RGB')

        resized_image = pil_image.resize((450, 250), PILImage.BICUBIC)

        image_data_io = BytesIO()
        resized_image.save(image_data_io, format='JPEG') 

        image_bytes = image_data_io.getvalue()

        new_image = DBImage(filename=filename, data=image_bytes, user_id=current_user.id)

        db.session.add(new_image)
        db.session.commit()

        print('Changes made to the database.')

        return render_template('meme-me.html', uploaded_image=new_image)

    return render_template('upload.html', error='Invalid file type')

@site.route('/display_meme/<int:image_id>')
def display_meme(image_id):
    image = DBImage.query.get_or_404(image_id)
    return send_file(BytesIO(image.data), mimetype="image/jpeg")

# @site.route('/update_meme/<int:image_id>', methods=['GET', 'POST'])
# def update_meme(image_id):
#     meme = DBImage.query.get_or_404(image_id)

#     if request.method == 'POST':
#         # Update the meme as needed
#         # For example: meme.filename = request.form['new_filename']
#         db.session.commit()

#         flash(f'Meme {meme.filename} updated successfully!', 'success')
#         return redirect(url_for('site.display_meme', image_id=image_id))

#     return render_template('update_meme.html', meme=meme)

# @site.route('/delete_meme/<int:image_id>')
# def delete_meme(image_id):
#     try:
#         meme = DBImage.query.get(image_id)

#         if meme:
#             db.session.delete(meme)
#             db.session.commit()

#             flash(f'Successfully deleted meme with ID {image_id}', 'delete-success')
#         else:
#             flash('Meme not found', 'delete-error')

#     except Exception as e:
#         flash(f'Error deleting meme: {str(e)}', 'delete-error')

#     return redirect(url_for('site.home'))
