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

@app.route("/charter/")
def charter():
    return render_template("charter.html")

@app.route("/bookings/")
def bookings():
    return render_template("bookings.html")

@app.route("/about_us/")
def about_us():
    return render_template("about_us.html")

@app.route("/faqs/")
def faqs():
    return render_template("faqs.html")

@app.route("/not_available")
def na():
    return render_template("not_available.html")

if __name__ == "__main__":
    app.run()