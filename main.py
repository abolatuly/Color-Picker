import os
from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from colorthief import ColorThief

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = "static/images"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):                         # check if an extension is valid
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/color-palette', methods=["POST"])
def success():
    if request.method == 'POST':
        if 'file' not in request.files:             # check if the post request has the file part
            flash('No file part')
            return redirect(url_for('home'))

        img = request.files["file"]

        if img.filename == '':                    # if the user does not select a file
            flash('No selected file')
            return redirect(url_for('home'))

        if img and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img.save(full_filename)
        else:
            flash('The chosen file is not an image')

        color_thief = ColorThief(full_filename)
        palette = color_thief.get_palette(color_count=11)
        print(palette)

        return render_template('color_picker.html', image=full_filename, colors=palette)


if __name__ == "__main__":
    app.run(debug=True)