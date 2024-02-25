from flask import Flask, render_template, url_for, redirect, request
import os

app = Flask(__name__)

@app.route('/')
def main_page():
    print("USER JOINED")
    return render_template("main.html")

@app.route('/foo')
def pleaseWork():
    return render_template('file_upload.html')

@app.route('/test')
def test():
    return render_template('loading.html')



@app.route('/output')
def output():
    return render_template('ytTest.html')

@app.route('/file_upload/<upload1>/<upload2>/<times>')
def uploadFiles(upload1, upload2, times):
#process
    print(upload1)
    print(upload2)
    print(times)
    return render_template('loading.html')
    # return redirect(url_for('main_page'))

@app.route('/upload', methods=['POST'])
def upload_files():
    # Assuming 'static/videos/' is the directory where you want to save the files
    target_directory = os.path.join(app.root_path, 'static', 'videos')
    os.makedirs(target_directory, exist_ok=True)  # Ensure the directory exists

    # referenceFile = request.files['reference_video']
    # userFile = request.files['user_video']
    # referenceFile = request.files['reference_video']
    # if referenceFile:
    if 'reference_video' in request.files:
        referenceFile = request.files['reference_video']
        referenceFilePath = os.path.join(target_directory, referenceFile.filename)
        referenceFile.save(referenceFilePath)

    if 'user_video' in request.files:
        userFile = request.files['user_videos']
        userFilePath = os.path.join(target_directory, userFile.filename)
        userFile.save(userFilePath)
    



    blob = request.files['blob']
    blobPath = os.path.join(target_directory, blob.filename)
    blob.save(blobPath)

    print("SAVED")
    # referenceFilePath = os.path.join(target_directory, referenceFile.filename)
    # userFilePath = os.path.join(target_directory, userFile.filename)

    # referenceFile.save(referenceFilePath)
    # userFile.save(userFilePath)

    return "YAY"    
app.debug = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443)