#cd 2017\DTP\Fox_II_Website
#c:\Python34\python.exe app.py

from flask import Flask, render_template
app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rates/")
def rates():
    return render_template("rates.html")

@app.route("/not_available")
def na():
    return render_template("not_available.html")

if __name__ == "__main__":
    app.run()