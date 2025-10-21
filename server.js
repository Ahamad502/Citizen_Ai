const express = require('express');
const path = require('path');
const app = express();
const port = 8000;

// Serve static files from the templates directory
app.use(express.static(path.join(__dirname, 'templates')));

// Serve index.html at the root
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});