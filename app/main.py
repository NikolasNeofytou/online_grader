from flask import Flask, render_template, request, session, redirect, url_for
import subprocess
import tempfile
import os
import difflib

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

# Simple exercises focused on using std::cout
exercises = [
    {
        'title': 'Hello World',
        'description': 'Write a program that prints "Hello, World!" using cout.',
        'solution_code': '\n'.join([
            '#include <iostream>',
            'int main() {',
            '    std::cout << "Hello, World!";',
            '    return 0;',
            '}'
        ]),
        'expected_output': 'Hello, World!'
    },
    {
        'title': 'Print 1 to 5',
        'description': 'Write a program that prints numbers 1 2 3 4 5 separated by spaces using cout.',
        'solution_code': '\n'.join([
            '#include <iostream>',
            'int main() {',
            '    std::cout << "1 2 3 4 5";',
            '    return 0;',
            '}'
        ]),
        'expected_output': '1 2 3 4 5'
    }
]

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


@app.route('/exercises', methods=['GET', 'POST'])
def exercises_view():
    """Interactive exercises focused on using cout."""
    idx = int(request.args.get('id', 0))
    if idx < 0 or idx >= len(exercises):
        return redirect(url_for('exercises_view', id=0))
    exercise = exercises[idx]
    code = ''
    result = None

    session.setdefault('attempts', {})
    attempts = session['attempts'].get(str(idx), 0)

    if request.method == 'POST':
        code = request.form.get('code', '')
        result = compile_code(code)
        attempts += 1
        session['attempts'][str(idx)] = attempts

        # Provide feedback comparing actual program output with expected output
        if 'Compilation succeeded' in result:
            actual_output = ''
            if 'Program output:\n' in result:
                actual_output = result.split('Program output:\n', 1)[1].strip()
            expected = exercise['expected_output']
            if actual_output == expected:
                result += '\nCorrect!'
            else:
                diff = '\n'.join(difflib.ndiff([expected], [actual_output]))
                result += f"\nExpected output:\n{expected}\nDifferences:\n{diff}"
        else:
            result += f"\nExpected output:\n{exercise['expected_output']}"

    show_solution = attempts >= 3
    return render_template(
        'exercises.html',
        exercises=exercises,
        idx=idx,
        exercise=exercise,
        code=code,
        result=result,
        attempts=attempts,
        show_solution=show_solution
    )

if __name__ == '__main__':
    app.run(debug=True)
