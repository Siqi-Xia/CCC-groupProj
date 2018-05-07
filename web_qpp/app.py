from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("test.html")


@app.route('/S1')
def S1():
    return render_template("s1_temp.html")


@app.route('/S2')
def S2():
    return render_template("s2_temp.html")


@app.route('/S3')
def S3():
    return render_template("s3_temp.html")

@app.route('/Graphic')
def graphic():
	return render_template("graph.html")


if __name__ == "__main__":
    app.run(debug=True)
