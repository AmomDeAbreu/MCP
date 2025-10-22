import os
import json
import subprocess
import sys
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')

PATH_FILE = 'preco.json'


def run_update_test():
    cmd = [sys.executable, '-m', 'pytest', '-q', '-s', 'main.py::test_search_and_get']
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def data():
    candidates = [os.path.abspath(PATH_FILE), os.path.abspath(os.path.join('/workspaces', os.getenv('GITHUB_WORKSPACE', ''), PATH_FILE)), os.path.abspath(os.path.join('/workspaces', PATH_FILE))]
    existing_path = None
    for p in candidates:
        if p and os.path.exists(p):
            existing_path = p
            break
    if not existing_path:
        return jsonify({'data': []})
    with open(existing_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
    return jsonify({'data': data})


@app.route('/update', methods=['POST'])
def update():
    code, out, err = run_update_test()
    return jsonify({'returncode': code, 'stdout': out, 'stderr': err})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
