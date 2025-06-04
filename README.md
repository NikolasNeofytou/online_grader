# online_grader
An attempt to modernise the grader experience of my school 

## Running the grader

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the development server:

```bash
python app/main.py
```

Then open `http://localhost:5000` in your browser to use the grader.

The page uses CodeMirror to provide syntax highlighting for the code editor. When
common mistakes are detected in the compiler output (for example forgetting the
`std::` prefix for `cout`/`cin`), a hint is appended to the error message.

## Running tests

```bash
pytest
```
