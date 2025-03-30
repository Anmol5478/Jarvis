# Jarvis AI

Jarvis AI is a voice-activated assistant that can interact with users, respond to queries, play music, open websites, and generate AI-powered responses using Google Gemini.

## Features
- Speech recognition using `speech_recognition`.
- AI-powered responses using Google Gemini API.
- Open websites and applications via voice commands.
- Play music and tell the current time.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/jarvis.git
cd jarvis
```

### 2. Set Up a Virtual Environment
Create a virtual environment to manage dependencies:
```bash
python -m venv venv
```
Activate the virtual environment:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Google Gemini API Key
Replace `API_KEY` in `main.py` with your Google Gemini API key.

### 5. Run the Application
```bash
python main.py
```

## Dependencies
The project uses the following Python packages:
- `speech_recognition` – for voice recognition
- `google-generativeai` – for AI-based responses
- `webbrowser` – to open websites
- `datetime` – to fetch and tell the current time
- `pywhatkit` – to play YouTube videos
- `os` – to execute system commands
- `random` – for additional random functionalities
- `re` – for regular expressions

## Usage
- Say **"Open YouTube"** to open YouTube.
- Say **"Play Music"** to play a specific music file.
- Say **"What is the time?"** to get the current time.
- Say **"Tell me a fact about space"** to get an AI response.

## Contributing
Feel free to contribute by creating pull requests or reporting issues!

## License
This project is licensed under the MIT License.

