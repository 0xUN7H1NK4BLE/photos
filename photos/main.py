from flask import Flask, request, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '.'

# Ensure base upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML template
HTML = '''
<!doctype html>
<title>Upload Files</title>
<h2>Upload Any Files</h2>
<form method=post enctype=multipart/form-data>
  Name: <input type="text" name="name" required><br><br>
  Select files: <input type="file" name="files" multiple required><br><br>
  <input type="submit" value="Upload">
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form['name'].strip()
        files = request.files.getlist('files')

        if not name:
            return "Name is required", 400

        user_folder = os.path.join(UPLOAD_FOLDER, secure_filename(name))
        os.makedirs(user_folder, exist_ok=True)

        saved_files = []
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(user_folder, filename)
                file.save(filepath)
                saved_files.append(filename)

        return f"Uploaded {len(saved_files)} file(s) to folder: {user_folder}"
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
