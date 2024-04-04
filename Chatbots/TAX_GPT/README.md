## Income Tax Chatbot App

This is an Android application developed using Android Studio and Firebase Authentication for a simple Income Tax Chatbot. Users can sign up, sign in, reset passwords, and communicate with the chatbot to get information about income tax-related queries.

### Features:
- User Authentication (Sign Up, Sign In, Reset Password) using Firebase Authentication.
- Chat interface with a chatbot powered by OpenAI's GPT-3.5.
- Messages sent by the user and responses from the chatbot are displayed in a RecyclerView.
- Firebase Firestore is used to store user information.

### How to Use:
1. Clone the repository to your local machine.
2. Open the project in Android Studio.
3. Replace the Firebase configuration file (`google-services.json`) with your own obtained from the Firebase Console.
4. Replace the OpenAI API key in the `MainActivity.java` file (`CallAPI()` method) with your own API key.
5. Build and run the application on an Android device or emulator.

### OpenAI API Key:
You need to obtain an API key from OpenAI to use the chatbot feature. Visit the [OpenAI website](https://openai.com) to sign up and get your API key.

### Firebase Account:
You need to set up a project on Firebase and enable Firebase Authentication and Firestore. Refer to the [Firebase documentation](https://firebase.google.com/docs) for detailed instructions on setting up Firebase services.

### Note:
- This application is provided as a sample and may require further customization according to your requirements.
- Make sure to handle sensitive information such as API keys securely, especially when sharing the code publicly.

### Contributors:
- Priyanshu Gupta

### License:
- MIT License

Feel free to contribute, report issues, or suggest improvements!
