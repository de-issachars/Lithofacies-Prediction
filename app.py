from flask import Flask, render_template, request
import os
from Model import get_prediction_csv

if not os.path.exists("Data"):
    os.mkdir("Data")

if not os.path.exists("Data/Predicted"):
    os.mkdir("Data/Predicted")


if not os.path.exists("Data/Uploaded"):
    os.mkdir("Data/Uploaded")


app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'Data/Uploaded'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\index.html'
    return render_template('upload.html')


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        output = get_prediction_csv(file_path)
        output.to_csv("Data/Predicted/{}".format(uploaded_file.filename), index=False)
        with open("Data/Predicted/{}".format(uploaded_file.filename)) as file:
            return render_template("view_download.html", csv=file)
        

if (__name__ == "__main__"):
     app.run(port = 12000)