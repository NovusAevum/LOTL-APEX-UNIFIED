from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
CONFIG_PATH = 'config.json'

def read_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {}

def write_config(data):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    config = read_config()
    if request.method == 'POST':
        for key in config:
            if key in request.form:
                config[key] = request.form[key]
        write_config(config)
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', config=config)

if __name__ == '__main__':
    app.run(debug=True)
