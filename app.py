from tlparser import calculate_total_log
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

# creating object of Flask
app = Flask(__name__)

# getting logs
@app.route('/logs', methods=['POST'])
def report():
    file = request.files['log']
    if file:
        name = secure_filename(file.filename)
        # storing the file
        file.save(os.path.join(app.root_path, 'upload', name))
        return render_template("logs.html", output = calculate_total_log(name), file_name = name)


# getting main page
@app.route('/', methods=['GET'])
def main():
    return render_template("main.html")


# running the server
if __name__ == '__main__':
    app.secret_key = '74125896321'
    app.run(debug=True)
