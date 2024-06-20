from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import subprocess
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Folder where uploaded files will be stored
UPLOAD_FOLDER = r'./uploads'
# Folder where processed files will be stored
DATA_FOLDER = r'./data'

# Ensure the upload and data folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATA_FOLDER'] = DATA_FOLDER


#option to directly download the output file or provide download option
DISPLAY_DOWNLOAD_OPTION = True

#run cleaner.py
def run_cleaner(input_file):
    output_file = os.path.join(DATA_FOLDER, 'processed_' + os.path.basename(input_file))
    subprocess.run(['python', 'cleaner.py', input_file, output_file])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Run cleaner.py on the uploaded file
            input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            run_cleaner(input_file_path)
            
            # Assuming cleaner.py produces an output file in DATA_FOLDER
            output_file = os.path.join(app.config['DATA_FOLDER'], 'processed_' + filename)
            
            if DISPLAY_DOWNLOAD_OPTION:
                return redirect(url_for('show_file', filename=os.path.basename(output_file)))
            else:
                return redirect(url_for('download_file', filename=os.path.basename(output_file)))
    
    return render_template('upload.html')

@app.route('/show/<filename>')
def show_file(filename):
    # Generate file path
    file_path = os.path.join(app.config['DATA_FOLDER'], filename)
    return render_template('show_file.html', filename=filename, file_path=file_path)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DATA_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
