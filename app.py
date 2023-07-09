from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("firstpage.html")

@app.route("/plans")
def plans1():
    return render_template("secondpage.html")

@app.route("/library")
def library1():
    return render_template("thirdpage.html")

if __name__ == "__main__":
    app.run()
