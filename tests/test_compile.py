import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import subprocess
import textwrap

from app.main import compile_code

def test_compile_success():
    code = textwrap.dedent("""
    #include <iostream>
    int main() { std::cout << "ok"; return 0; }
    """)
    output = compile_code(code)
    assert "Compilation succeeded" in output
    assert "ok" in output

def test_compile_failure():
    code = "int main() {"  # invalid code
    output = compile_code(code)
    assert "Compilation failed" in output

def test_missing_std_prefix_suggestion():
    code = textwrap.dedent("""
    #include <iostream>
    int main() { cout << "hi"; return 0; }
    """)
    output = compile_code(code)
    assert "Compilation failed" in output
    assert "Hint: Did you forget to prefix 'cout'" in output
