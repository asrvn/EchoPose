from flask import Flask, render_template, url_for, redirect, request

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
    print("DOING STUFF")

    # print(request.files['reference_video'])
    # print(request.files['user_video'])

    referenceFile = request.files['reference_video']
    userFile = request.files['user_video']

    referenceFile.save('/')
    userFile.save('/static/videos/')

    return "yay"
    
app.debug = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443)