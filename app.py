from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime
import json
import os

app = Flask(__name__, static_url_path='/static')

DATA_FILE = 'storage/data.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        try:
            data = request.form
            username = data.get('username', 'Anonymous')
            message_text = data.get('message', '')

            with open(DATA_FILE, 'r') as f:
                messages = json.load(f)

            messages[str(datetime.now())] = {
                'username': username,
                'message': message_text
            }

            with open(DATA_FILE, 'w') as f:
                json.dump(messages, f, indent=2)

            return redirect(url_for('read'))
        except Exception as e:
            return f"Error: {str(e)}"

    return render_template('message.html')

@app.route('/read')
def read():
    with open(DATA_FILE, 'r') as f:
        messages = json.load(f)
    return render_template('read.html', messages=messages)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
