from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

@app.route('/')
def front_page():
    print("USER JOINED")
    return render_template("front-page.html")

app.debug = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443)