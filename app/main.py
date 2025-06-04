from flask import Flask, render_template, request
import subprocess
import tempfile
import os
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    code = ''
    if request.method == 'POST':
        code = request.form.get('code', '')
        output = compile_code(code)
        code = output.get('code', code)
    return render_template('index.html', output=output, code=code)

def format_code(code: str) -> str:
    """Format C++ code using clang-format if available."""
    try:
        proc = subprocess.run(['clang-format'], input=code, capture_output=True, text=True)
        if proc.stdout:
            return proc.stdout
    except FileNotFoundError:
        pass
    return code


def compile_code(code: str) -> dict:
    formatted = format_code(code)
    with tempfile.TemporaryDirectory() as tmpdir:
        source_path = os.path.join(tmpdir, 'main.cpp')
        with open(source_path, 'w') as f:
            f.write(formatted)
        exe_path = os.path.join(tmpdir, 'prog')
        result = subprocess.run(
            ['g++', source_path, '-std=c++17', '-fdiagnostics-color=never', '-o', exe_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            run = subprocess.run([exe_path], capture_output=True, text=True)
            return {
                'message': 'Compilation succeeded.\nProgram output:\n' + run.stdout,
                'line': None,
                'code': formatted,
            }
        else:
            suggestion = ''
            err = result.stderr
            if 'cout' in err and 'declared' in err:
                suggestion += "\nHint: Did you forget to prefix 'cout' with 'std::'?"
            if 'cin' in err and 'declared' in err:
                suggestion += "\nHint: Did you forget to prefix 'cin' with 'std::'?"
            m = re.search(r'main\.cpp:(\d+):', err)
            line = int(m.group(1)) if m else None
            return {
                'message': 'Compilation failed:\n' + err + suggestion,
                'line': line,
                'code': formatted,
            }

if __name__ == '__main__':
    app.run(debug=True)
