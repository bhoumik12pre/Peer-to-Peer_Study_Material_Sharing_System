from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from models import db, StudyMaterial

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db.init_app(app)

# Home Route
@app.route('/')
def index():
    materials = StudyMaterial.query.all()
    return render_template('index.html', materials=materials)

# Upload Route
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        subject = request.form['subject']
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_material = StudyMaterial(title=title, subject=subject, filename=filename)
            db.session.add(new_material)
            db.session.commit()

            flash('File uploaded successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('upload.html')

# Download Route
@app.route('/download/<filename>')
def download(filename):
    return redirect(url_for('static', filename=f'uploads/{filename}'))

# Admin Route (for managing content)
@app.route('/admin')
def admin():
    materials = StudyMaterial.query.all()
    return render_template('admin.html', materials=materials)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
