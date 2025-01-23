# VidCraft

## Description
This backend application is built using FastAPI and is designed to generate videos based on user-defined topics and backgrounds. It integrates multiple AI services for text generation, audio synthesis, image creation, and subtitle generation. The application handles various tasks, including cleaning text, formatting subtitles, and generating video files using FFmpeg.

## Project Overview
This project is aimed at generating videos using AI technologies. It leverages advanced algorithms to create high-quality video content based on user inputs.

## Frontend Description
The frontend of this project is built using modern web technologies including React.js for a dynamic user experience. The interface is designed to be intuitive, allowing users to easily input their preferences and view the generated videos. Key features include:
- **Responsive Design**: The application is fully responsive, ensuring a seamless experience on both desktop and mobile devices.
- **Real-time Preview**: Users can see a real-time preview of their video as they adjust settings.
- **User-Friendly Interface**: The layout is clean and organized, making navigation simple.

## Installation Instructions
### Backend Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/LohiyaH/VidCraft
   cd shorty
   ```
2. Install the required dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Set up environment variables in a `.env` file:
   ```
   GEMINI_API_KEY=<your-gemini-api-key>
   ELEVENLABS_API_KEY=<your-elevenlabs-api-key>
   HUGGINGFACE_API_KEY=<your-huggingface-api-key>
   ```

### Frontend Installation
To set up the frontend, follow these steps:
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the application: `npm start`

## Usage
### Backend Usage
1. Run the FastAPI application:
   ```bash
   uvicorn backend.main:app --reload
   ```
2. Access the API documentation at `http://localhost:8000/docs`.

### Frontend Usage
Once the application is running, users can input their video preferences in the provided fields and click on the 'Generate Video' button to create their AI-generated video. The results will be displayed in the preview section.

## API Endpoints
- **POST** `/api/generate-video`
  - **Request Body**:
    ```json
    {
      "topic": "string",
      "background": "string"
    }
    ```
  - **Response**:
    ```json
    {
      "videoUrl": "string"
    }
    ```

- **GET** `/api/test`
  - Returns a simple test message.

[Watch the video](https://drive.google.com/file/d/1WjUGrYiH2_ghVuXiveTgCI0QvJksH7Dc/view?usp=sharing)

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
