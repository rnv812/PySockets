from flask import Flask, render_template, redirect


app = Flask(__name__)


@app.route("/")
def home():
    return redirect('/auth')


@app.route("/auth")
def authorize():
    return render_template('authorize.html')


@app.route("/acc")
def account():
    return render_template('account.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000)
