const express = require('express');
const cors = require('cors');
const path = require('path');
const axios = require('axios');

require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5001;

app.use(cors());
app.use(express.json());

// Add these headers to handle CORS
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

// Serve static files from the build directory
app.use(express.static(path.join(__dirname, '../client/build')));

// Correctly handle the default route to serve index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
});

async function generateImage(prompt) {
  const API_KEY = process.env.OPENAI_API_KEY;

  // Check if API key is present
  if (!API_KEY) {
    throw new Error('OpenAI API key is missing');
  }

  const url = 'https://api.openai.com/v1/images/generations';

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`,
  };

  const data = {
    prompt: prompt,
  };
  
  

  try {
    const response = await axios.post(url, data, { headers });
    return response.data;
  } catch (error) {
    // Log the error details
    console.error('OpenAI API Error:', error.response ? error.response.data : error.message);
    throw error;
  }
}




app.post('/generate-image', async (req, res, next) => {
  const { prompt } = req.body;

  try {
    // Send preliminary response with the image generation in progress
    res.json({ status: 'generating', message: 'Image generation in progress' });

    const response = await generateImage(prompt);

    // Check if the response has already been sent
    if (!res.headersSent) {
      // Include the image URL in the same response
      res.json({ ...response, status: 'generated' });
    }
  } catch (error) {
    // Handle the AxiosError
    console.error('AxiosError:', error.message);

    if (error.response && error.response.status === 400) {
      // Send a 400 Bad Request response to the client
      if (!res.headersSent) {
        res.status(400).json({ error: 'Bad Request', message: 'Invalid input or bad request to external API' });
      }
    } else {
      // Pass other errors to the next middleware
      next(error);
    }
  }
});




// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ status: 'error', message: 'Something went wrong!' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
