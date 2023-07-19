import os
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('main.html', files=files)

def remove_illegal_chars(text):
    import re
    pattern = r"[^\w\s]"  # Matches any character that is not a word character (\w) or whitespace (\s)
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return 'File uploaded successfully'
    elif 'text' in request.form:
        text = request.form['text']
        if text.strip() != '':
            file_name = remove_illegal_chars(text.split()[0])
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            with open(file_path+".txt", 'w', encoding='utf-8') as f:
                f.write(text)
            return 'Text uploaded successfully'
    
    return 'No file or text selected'

@app.route('/view/<filename>')
def view(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5000)
    
