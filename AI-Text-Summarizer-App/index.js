const express = require('express');
const app = express();
const port = 3000;
const summarizeText = require('./summarize.js')



// Parses JSON bodies (as sent by API clients)
app.use(express.json());

// Serves static files from the 'public' directory
app.use(express.static('public'));

// API ROUTE: /summarize
// Handles the summaryizing end point
app.post('/summarize', (req, res) => {
    const text = req.body.text_to_summarize
      // Call the summarizeText function
    summarizeText(text)
    .then(response => {
      res.send(response);
    })
    .catch(error => {
      console.log(error.message)
    })
})
// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
