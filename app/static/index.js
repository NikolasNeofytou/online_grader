(function() {
  const { useState, useEffect } = React;

  function App() {
    const [code, setCode] = useState('');
    const [output, setOutput] = useState(null);

    useEffect(() => {
      const editor = ace.edit('editor');
      editor.session.setMode('ace/mode/c_cpp');
      editor.setTheme('ace/theme/monokai');
      editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true
      });
      editor.session.on('change', function() {
        setCode(editor.getValue());
      });
    }, []);

    async function compile() {
      const res = await fetch('/api/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      const data = await res.json();
      setOutput(data.output);
      requestAnimationFrame(() => { if (window.hljs) { hljs.highlightAll(); } });
    }

    return React.createElement('div', { className: 'app-container' }, [
      React.createElement('h1', { key: 'title' }, 'Online C++ Grader'),
      React.createElement('div', { id: 'editor', key: 'editor', style: { height: '300px', width: '100%', border: '1px solid #ccc' } }),
      React.createElement('button', { key: 'btn', onClick: compile }, 'Compile'),
      output ? React.createElement('pre', { key: 'out', className: 'output' }, output) : null
    ]);
  }

  ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
})();
