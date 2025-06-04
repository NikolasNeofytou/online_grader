from flask import Flask, render_template, request
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    code = ''
    if request.method == 'POST':
        code = request.form.get('code', '')
        output = compile_code(code)
    return render_template('index.html', output=output, code=code)

def compile_code(code: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        source_path = os.path.join(tmpdir, 'main.cpp')
        with open(source_path, 'w') as f:
            f.write(code)
        exe_path = os.path.join(tmpdir, 'prog')
        result = subprocess.run(
            ['g++', source_path, '-o', exe_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            run = subprocess.run([exe_path], capture_output=True, text=True)
            return 'Compilation succeeded.\nProgram output:\n' + run.stdout
        else:
            return 'Compilation failed:\n' + result.stderr

if __name__ == '__main__':
    app.run(debug=True)
