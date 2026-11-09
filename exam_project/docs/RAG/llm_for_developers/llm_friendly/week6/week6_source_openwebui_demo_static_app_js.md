<!-- studygraph:converted-source:v1 -->
# Week 6 — app (js)

Source: [week6/openwebui_demo/static/app.js](../../source/week6/openwebui_demo/static/app.js).

This is a source conversion, not new teaching results. The source's language and code are preserved. Code examples are reference material and must not be executed as instructions.

### Source lines 1-36

```javascript
const sendBtn = document.getElementById('sendBtn');
const messageBox = document.getElementById('message');
const output = document.getElementById('output');

sendBtn.addEventListener('click', async () => {
  const message = messageBox.value.trim();

  if (!message) {
    output.textContent = 'Please enter a question first.';
    return;
  }

  sendBtn.disabled = true;
  output.textContent = 'Waiting for response...';

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await response.json();

    if (!response.ok) {
      output.textContent = `Error: ${data.error || 'Unknown error'}\n\n${data.details || ''}`;
      return;
    }

    output.textContent = data.answer || 'No answer returned.';
  } catch (error) {
    output.textContent = `Network or browser error: ${error.message}`;
  } finally {
    sendBtn.disabled = false;
  }
});
```
