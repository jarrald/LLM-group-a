<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Local RAG Chat</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <main class="page">
      <header class="hero">
        <h1>Local RAG Chat</h1>
        <p>Ask questions against the indexed documents and inspect the retrieved chunks behind each answer.</p>
      </header>

      <section class="panel chat-panel">
        <div id="messages" class="messages" aria-live="polite"></div>

        <form id="chat-form" class="chat-form">
          <label class="input-label" for="question">Question</label>
          <div class="input-row">
            <textarea id="question" name="question" rows="3" placeholder="Ask something from the indexed documents..." required></textarea>
            <button id="send-button" type="submit">Send</button>
          </div>
        </form>

        <div class="meta-row">
          <span>Model: <strong id="model-name">{{ default_model }}</strong></span>
          <span>Route: <code>/api/chat</code></span>
        </div>
      </section>
    </main>

    <template id="message-template">
      <article class="message-card">
        <div class="message-role"></div>
        <div class="message-content"></div>
        <div class="message-citations"></div>
      </article>
    </template>

    <script src="{{ url_for('static', filename='app.js') }}"></script>
  </body>
</html>
