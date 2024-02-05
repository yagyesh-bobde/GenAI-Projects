# Azure Text-to-Speech with Avatar

<p align="center">
  <img src="https://github.com/Sgvkamalakar/Azure-Talking-Avatar/assets/103712713/09fc79f9-cc68-4354-bae7-e75e24add235" width="400" height="400"/>
</p>
This Streamlit app allows you to submit and monitor batch synthesis jobs using Azure Text-to-Speech with Avatar. It leverages the Azure AI Services to create talking avatars based on the provided text.

## Usage
- Choose the language and avatar style using the sidebar dropdowns.
- Type the text you want to synthesize in the selected language.
- Click the "Submit Synthesis Job" button to initiate the batch synthesis job.
- Monitor the status in real-time. Once the job is successful, the talking avatar video will be displayed.

## Supported Languages and Avatars
The application supports multiple languages, each associated with a specific talking avatar style.
<div align='center'>
  <table>
  <thead>
    <tr>
      <th>Language</th>
      <th>Voice</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Arabic</td>
      <td>ZariyahNeural</td>
    </tr>
    <tr>
      <td>Bahasa Indonesian</td>
      <td>GadisNeural</td>
    </tr>
    <tr>
      <td>Bengali</td>
      <td>TanishaaNeural</td>
    </tr>
    <tr>
      <td>Chinese Mandarin</td>
      <td>XiaoxiaoNeural</td>
    </tr>
    <tr>
      <td>Dutch</td>
      <td>FennaNeural</td>
    </tr>
    <tr>
      <td>English</td>
      <td>AvaNeural</td>
    </tr>
    <tr>
      <td>French</td>
      <td>DeniseNeural</td>
    </tr>
    <tr>
      <td>German</td>
      <td>KatjaNeural</td>
    </tr>
    <tr>
      <td>Hindi</td>
      <td>SwaraNeural</td>
    </tr>
    <tr>
      <td>Italian</td>
      <td>ElsaNeural</td>
    </tr>
    <tr>
      <td>Japanese</td>
      <td>NanamiNeural</td>
    </tr>
    <tr>
      <td>Korean</td>
      <td>SunHiNeural</td>
    </tr>
    <tr>
      <td>Russian</td>
      <td>SvetlanaNeural</td>
    </tr>
    <tr>
      <td>Spanish</td>
      <td>ElviraNeural</td>
    </tr>
    <tr>
      <td>Telugu</td>
      <td>ShrutiNeural</td>
    </tr>
  </tbody>
</table>
</div>

## Demo
Check out the demo video:

https://github.com/Sgvkamalakar/Azure-Talking-Avatar/assets/103712713/adf5c293-e1cc-4fb5-94e2-b87ca5f5501c


## Setup
To run the application, you need to set up your Azure Text-to-Speech subscription key, service region, and service host. You can set these values in a `.env` file or directly in the script.

```dotenv
SUBSCRIPTION_KEY=<your_subscription_key>
SERVICE_REGION=<your_service_region>
SERVICE_HOST=<your_service_host>
```

## References
Learn more about Text-to-Speech Avatar on Microsoft Azure [here](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech-avatar/what-is-text-to-speech-avatar)
  
