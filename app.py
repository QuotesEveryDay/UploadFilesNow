from flask import Flask, request, render_template
import os
import requests

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def send_to_discord_webhook(file_path):
    webhook_url = 'https://discord.com/api/webhooks/1139686248496246825/blHegQ65BCmPE93qBe8tlMyE3IP6RqQStAetrBOp4Mi7kZRgV1xVNDI2d7TmDwjU5Aln'
    with open(file_path, 'rb') as file:
        response = requests.post(webhook_url, files={'file': file})
    return response.status_code == 204

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            if send_to_discord_webhook(file_path):
                return 'File uploaded successfully and sent to Discord.'
            else:
                return 'Error sending file to Discord'

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>File Upload</title>
    </head>
    <body>
        <h1>Upload Your File</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
