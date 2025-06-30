import os
# from dotenv import load_dotenv
# load_dotenv()
import streamlit as st
import sys
sys.path.append(os.path.dirname(__file__))




from scraping.scraper import scrape_website
from assistant.chat_logic import CookingAssistant

st.set_page_config(page_title="ChefFlow", page_icon="🍳", layout="centered")
st.title("🍳 ChefFlow - Your Cooking Assistant")

#MODE TOGGLE:
st.sidebar.header("Select Chat Mode")
mode = st.sidebar.radio("Choose how to interact:", ["Text Chat", "Voice Chat"], index=0)

#---------------------------TEXT MODE----------------------------------
if mode == "Text Chat":
    # --- Session state setup
    if "assistant" not in st.session_state:
        st.session_state.assistant = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_user_input" not in st.session_state:
        st.session_state.pending_user_input = None

    # --- Sidebar
    st.sidebar.header("Paste Recipe Link")
    url_input = st.sidebar.text_input("Enter a recipe URL:")

    if st.sidebar.button("Fetch Recipe"):
        if url_input:
            recipe_data = scrape_website(url_input)
            if recipe_data and recipe_data["steps"]:
                st.session_state.assistant = CookingAssistant(recipe_data)
                st.session_state.messages = []
                st.session_state.pending_user_input = None
                st.success(f"Loaded recipe: {recipe_data['title']}")
            else:
                st.error("Could not extract steps. Try a different link!")

    # --- Chat area
    st.subheader("👩‍🍳 Chat with ChefFlow")

    if st.session_state.assistant:

        # Render *previous* chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Process pending user input immediately
        if st.session_state.pending_user_input:
            user_text = st.session_state.pending_user_input
            with st.chat_message("user"):
                st.write(user_text)
            st.session_state.messages.append({"role": "user", "content": user_text})

            with st.spinner("ChefFlow is thinking..."):
                assistant_reply = st.session_state.assistant.respond(user_text)

            with st.chat_message("assistant"):
                st.write(assistant_reply)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

            st.session_state.pending_user_input = None
            # assistant_reply = st.session_state.assistant.respond(user_text)
            # with st.chat_message("assistant"):
            #     st.write(assistant_reply)
            # st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

            # st.session_state.pending_user_input = None

        # Input box always visible at bottom
        new_input = st.chat_input("Say something to ChefFlow...")
        if new_input:
            st.session_state.pending_user_input = new_input
            st.rerun()

    else:
        st.info("Paste a recipe link in the sidebar to begin!")


#-------------------------------------VOICE MODE------------------------
elif mode == "Voice Chat":
    st.subheader("🎤 Voice Chat Assistant")

    # --- Session state setup
    if "assistant" not in st.session_state:
        st.session_state.assistant = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_voice_input" not in st.session_state:
        st.session_state.last_voice_input = None

    st.sidebar.header("Paste Recipe Link")
    url_input = st.sidebar.text_input("Enter a recipe URL:")

    if st.sidebar.button("Fetch Recipe"):
        if url_input:
            recipe_data = scrape_website(url_input)
            if recipe_data and recipe_data["steps"]:
                st.session_state.assistant = CookingAssistant(recipe_data)
                st.session_state.messages = []
                st.session_state.last_voice_input = None
                st.success(f"Loaded recipe: {recipe_data['title']}")
            else:
                st.error("Could not extract steps. Try a different link!")

    if st.session_state.assistant:

        # --- Render previous conversation
        st.subheader("Chat History")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # --- RECORD VOICE BUTTON
        if st.button("🎤 Record Your Voice"):
            # RECORD AUDIO FROM MIC AND TRANSCRIBE
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.Microphone() as source:
                with st.spinner("Listening..."):
                    audio = r.listen(source, phrase_time_limit=5)
                try:
                    user_text = r.recognize_google(audio)
                    st.success(f"You said: {user_text}")
                    st.session_state.last_voice_input = user_text
                except sr.UnknownValueError:
                    st.warning("Sorry, I couldn't understand.")
                except sr.RequestError as e:
                    st.error(f"Error with recognition service: {e}")

        # --- Process new voice input
        if st.session_state.last_voice_input:
            user_text = st.session_state.last_voice_input
            st.session_state.messages.append({"role": "user", "content": user_text})

            with st.spinner("ChefFlow is thinking..."):
                assistant_reply = st.session_state.assistant.respond(user_text)

            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

            # --- SPEAK ASSISTANT REPLY ALOUD
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(assistant_reply)
            engine.runAndWait()

            st.session_state.last_voice_input = None

    else:
        st.info("Paste a recipe link in the sidebar to begin!")