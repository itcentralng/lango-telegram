# Lango Telegram Bot Server

The LanGo server is a backend service for [LanGo Bot](http://t.me/LanGoAI_bot). The server uses Telegram to receive user's input in either audio or text format, if in audio, it pass through Whisper and retrieve the transcript, then sends it to GPT3.5 Turbo for to retrieve a response. The response is then sent to Elevenlas to generate an audio response. Both the audio and the text are sent back to Telegram to the user as response.

## TO RUN:

To run the LanGo server, follow the steps below:

1. Add a `.env` file to the root of the project with the following details:
    ```
    TELEGRAM_TOKEN=a-telegram-bot-token
    OPENAI_API_KEY=open-your-ai-api-key
    ELEVENLABS_API_KEY=your-elevenlabs-api-key
    ```
   Note that you'll need to obtain the necessary API keys to fill out the values.

2. Install Python on your computer.

3. Install dependencies by running `pip install -r requirements.txt`.

4. Start the server by running `python app.py`.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome any contributions or suggestions that can improve the application's functionality.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements

This project makes use of the following libraries and APIs:

- pytelegramBotAPI
- Whisper
- GPT3.5 Turbo
- Elevenlabs
