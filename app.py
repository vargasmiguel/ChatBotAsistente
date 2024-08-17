import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from time import sleep

st.set_page_config(initial_sidebar_state='collapsed', 
                    page_title="Miguel ChatBot",
                    page_icon="🤖")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.html(hide_st_style)


GOOGLE_API_KEY=st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

if "history" not in st.session_state:
    st.session_state.history = []


# Create the model
generation_config = {
  "temperature": 0,
#  "top_p": 0.95,
#  "top_k": 64,
  "max_output_tokens": 512, #8192,
#  "response_mime_type": "text/plain",
}

safety_set={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  safety_settings = safety_set,
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction=f"Eres Miguel Vargas (versión Bot de IA), vas a hablar con primos y familiares. Eres de Cali Colombia, te gusta comer aborrajado, sancocho, chuleta, lechona y cholado, te gusta tomar champus y wisky del bueno. Eres doctor en Matemáticas aplicada, del Centro de investigación en Matemáticas de México, te gusta debatir sobre política y tecnología. Actualmente vives en Pereira Risaralda. pero en terminos laborales estás emprendiendo con una startup de desarrollo de software de inteligencia artifical y automatizaciones en New York, en remoto. Eres católico. Eres pragmático. Te gusta la programación en Python. Tienes una esposa llamada Angela Rodas, quién es psicoorientadora. No tienes hijos, pero tienes un perrito llamado Pascal al que quieres como a un hijo. Tu papá se llama Jesús y tu mamá se llama Susana, quieres están jubilados, tranquilos y saludables en casa en Cali. Tu hermana se llama Laura y recientemente tuvo una bebe llamada Luciana, ellas viven en Espiritu Santo Brasil. La mayoría de tus primos y familiares son de la Costa Atlantica colombian, debes preguntarle el nombre para comenzar hablar y pregunta desde que parte te escriben."
)


chat = model.start_chat(history = st.session_state.history)

def stream_generator(response):
    for chunk in response:
         sleep(0.1)
         yield chunk.text
    

st.title("🤖 Miguel ChatBot")


for message in chat.history:
    role ="assistant" if message.role == 'model' else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("Cuentame en qué te puedo ayudar?"):
    with st.chat_message("user"):
            st.markdown(prompt)
    with st.chat_message("assistant"):  
            try:
                stream=stream_generator(chat.send_message(prompt, stream=True))
                response = st.write_stream(stream)
            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)
            st.session_state.history = chat.history