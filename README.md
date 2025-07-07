ChefFlow – AI Cooking Voice Assistant
ChefFlow is your personal AI-powered kitchen companion that helps you cook with confidence. Whether you're a beginner or an experienced home chef, ChefFlow guides you step-by-step through recipes using natural voice interactions. Just talk, cook, and enjoy the process — hands-free

 Features
🎤 Voice Interaction: Talk to your assistant while cooking. Ask questions like “What do I do after adding onions?” or “How much salt should I add?”

🧠 AI-Powered Guidance: Uses natural language understanding to give smart, context-aware responses.

📺 YouTube & Website Integration: Extracts instructions from recipe videos or cooking websites and breaks them into easy steps.

🗣️ Multi-language Support (Coming Soon): Interact in your preferred language — from English and Hindi to Japanese, Russian, and beyond.

🔥 Real-Time Cooking Assistant: Stay in the flow without switching tabs or touching your device.


How It Works
Paste a YouTube link or recipe website URL.

ChefFlow scrapes the content and extracts the steps.

Click “Record Voice” to start interacting with the assistant.

Ask your questions — like “What’s the next step?” or “Can I substitute butter with oil?”

Enjoy a smoother, more intuitive cooking experience.

Tech Stack
Frontend: Streamlit

Backend: Python (FastAPI-style architecture)

Voice Recognition: SpeechRecognition + Google Web Speech API

AI Model: OpenAI / Deepseek / OpenRouter API

Web Scraping: BeautifulSoup, custom parsers for YouTube & recipe sites

Natural Language Processing: Prompt engineering + contextual step handling

Installation

# Clone the repo
git clone https://github.com/your-username/chefflow.git
cd chefflow

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

Deployment
You can deploy ChefFlow on:

🔗 Streamlit Cloud

☁️ Vercel / Netlify (with FastAPI + frontend deployment)

💻 Locally on your machine

Contributing
Want to make ChefFlow better? Contributions are welcome!

Fork the project

Create your branch (git checkout -b feature/awesome-feature)

Commit your changes

Push and open a pull request

 About the Creator
This was a collabortive project by Harshini Male and Sanjana Chitthoor. Student developers passionate about building AI-powered tools

