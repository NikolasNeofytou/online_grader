(function() {
  const { useEffect } = React;

  function AceEditor() {
    useEffect(() => {
      const editor = ace.edit('editor');
      editor.session.setMode('ace/mode/c_cpp');
      editor.setTheme('ace/theme/monokai');
      editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true
      });
      const textarea = document.querySelector('textarea[name="code"]');
      editor.session.setValue(textarea.value || '');
      document.querySelector('form').addEventListener('submit', function() {
        textarea.value = editor.getValue();
      });
      if (window.hljs) { hljs.highlightAll(); }
    }, []);
    return React.createElement('div', { id: 'editor', style: { width: '100%', height: '300px', border: '1px solid #ccc' } });
  }

  ReactDOM.createRoot(document.getElementById('editor-root')).render(React.createElement(AceEditor));
})();
