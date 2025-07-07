**ChefFlow – AI Cooking Voice Assistant**  
ChefFlow is a voice-controlled AI assistant designed to help you cook hands-free. Whether you're trying out a new recipe or just need help remembering the next step, ChefFlow makes the experience smoother by allowing you to interact naturally through voice commands. It extracts instructions from YouTube videos or recipe websites and guides you through the process step by step.

---

**Features**

- Voice interaction for hands-free cooking  
- AI-powered responses to questions like "What do I do next?" or "How much salt should I add?"  
- Extracts step-by-step instructions from YouTube or recipe websites  
- Real-time contextual understanding of where you are in the recipe  
- Easy-to-use interface with built-in voice recognition  
- Built with extensibility in mind for future features like language support, timers, and substitutions  

---

**How It Works**

1. Paste a YouTube video link or recipe website URL into the app.  
2. The assistant scrapes the content and extracts the instructions.  
3. Press the "Record Voice" button and speak your command or question.  
4. The assistant uses AI to respond based on where you are in the recipe.  
5. Continue cooking while asking questions like "What’s the next step?" or "How long do I sauté this?"  

---

**Tech Stack**

- Python (Backend)  
- Streamlit (Frontend)  
- SpeechRecognition + Google Web Speech API (Voice input)  
- BeautifulSoup (Web scraping)  
- OpenAI / Deepseek API via OpenRouter (AI responses)  
- Custom prompt engineering and logic for step tracking  

---

**Installation**

```bash
# Clone the repository
git clone https://github.com/your-username/chefflow.git
cd chefflow

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

---

**Sample Commands**

You can speak naturally to the assistant during your cooking process. Examples include:

- "I’ve added the onions. What’s next?"  
- "How much salt should I add?"  
- "Can I substitute olive oil with butter?"  
- "I’m done sautéing. What do I do now?"  
- "What’s the temperature for baking this?"  

---

**Future Improvements**

- Support for multiple languages  
- Timers and reminders for cooking durations  
- Save and manage your favorite recipes  
- Automatic ingredient substitution suggestions  
- Nutrition information and portion scaling  
- Shopping list generation based on selected recipes  

---

**Deployment**

ChefFlow can be deployed locally or hosted on platforms like Streamlit Cloud, Vercel, or any Python-compatible server.

---

**Contributing**

Contributions are welcome. To contribute:

1. Fork the repository  
2. Create a new branch (`git checkout -b feature/your-feature-name`)  
3. Make your changes  
4. Commit and push (`git commit -m "Add feature"` then `git push`)  
5. Open a pull request  

---

**License**

This project is licensed under the MIT License. You are free to use, modify, and distribute the software.

---

**About the Author**

ChefFlow is a collaborative project by Harshini Male and Sanjana Chitthoor, student developers passionate about building practical AI tools that improve everyday life. This project was created as part of a larger initiative to explore real-time AI interaction in hands-on environments.
