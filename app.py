#cd 2017\Digital_Programming
#c:\Python34\python.exe hello.py

from flask import Flask, render_template
app = Flask(__name__, template_folder="templates")

@app.route("/")
def hello():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()