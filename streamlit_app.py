import streamlit as st
from random import choice
import vertexai
from vertexai.preview.generative_models import GenerativeModel, SafetySetting, Part

my_api_key = st.secrets["api_key"]

def multiturn_generate_content(prompt):
    vertexai.init(api_key=my_api_key)
    model = GenerativeModel(
        "gemini-1.5-flash-002",
        system_instruction=[textsi_1]
    )
    chat = model.start_chat()

    for chunk in chat.send_message(prompt, stream=True):
        yield chunk.text

textsi_1 = """You are a friendly fun greeting bot! Someone will say a greeting to you,
           you will give them back a fun but greeting with the same theme!
           If they say anything except a greeting, you will tell them off in a fun way!"""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]



st.write("Hello to CreateHer Fest!")
possible_responses = ['Heeeyyaaa!!', "yo yo yo", "Hello I'm a bot!!"]

if "messages" not in st.session_state:
    st.session_state['messages'] = []

# load our history!!!!!!!!!!!!!!!!!!!!!
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.write(message['content'])


user_input = st.chat_input("What's your favourite greeting?!")


if user_input:
    with st.chat_message("user"):
        st.write(user_input)
        st.session_state['messages'].append({'role':'user', 'content':user_input})

    with st.chat_message("assistant"):
        response = st.write_stream(multiturn_generate_content(user_input))

        st.session_state['messages'].append({'role':'assistant', 'content':response})
