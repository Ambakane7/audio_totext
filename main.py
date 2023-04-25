# Importation des différentes librairies que l'on va utiliser 
import streamlit as st 
from pydub import AudioSegment, silence
import speech_recognition as sr
recognizer = sr.Recognizer()
final_result = ""
# Pour pouvoir donner l'accès à l'appli de sauvegarder dans n'importe quel dossier il faut il donner accès au système
import os 
# On crée une liste de langues que l'on veut convertir 
languages = {'English': 'en-US', 'French': 'fr-FR'}

# Pour afficher notre Titre
st.markdown("<h1 style ='text-align:center;'> Audio to Text Converter</h1>", unsafe_allow_html=True)
st.markdown("<h3 style ='text-align:center;'> By Mr_G</h3>", unsafe_allow_html=True)

# Choix de la langue
language = st.selectbox('Choisir une langue', list(languages.keys()))
lang_code = languages[language]

# Pour tracer une ligne de séparation 
st.markdown("---", unsafe_allow_html=True)

# On définit les formats que l'on veut accepter : le wav, mp3, mp4
audio = st.file_uploader('Veuillez charger votre fichier audio', type=['mp3', 'wav', 'mp4'])

if audio:
    st.audio(audio)
    audio_segment = AudioSegment.from_file(audio)
    chunks = silence.split_on_silence(audio_segment, min_silence_len=500, silence_thresh=audio_segment.dBFS - 20, keep_silence=100)
    for index, chunk in enumerate(chunks):
        chunk.export(str(index) + ".wav", format="wav")
        with sr.AudioFile(str(index) + ".wav") as source:
            recorded = recognizer.record(source)
            try: 
                text = recognizer.recognize_google(recorded, language=lang_code) 
                final_result = final_result + " " + text
            except:
                print('Vous avez dit ?')
                final_result = final_result + " fichier inaudible"
    
    with st.form("Result"):
        # Sauvegarder le texte généré dans une variable result qui pourra ensuite être téléchargée
        result = st.text_area("TEXT", value=final_result)
        # Création d'un bouton de téléchargement du texte généré
        d_btn = st.form_submit_button("Download")
        if d_btn:
            # Définir la variable d'environnement 
            env_var = os.environ
            usr_loc = env_var.get('USERPROFILE')
            loc = usr_loc + "\Downloads\\transcript.txt"
            # Étape très importante pour transformer le texte en fichier txt
            with open(loc, 'w') as file:
                file.write(result)
    
    st.markdown("<div style ='text-align:center; color:red'>Une fois le téléchargement fini, votre fichier sera dans votre dossier de téléchargement sous le nom 'transcript.txt'</div>", unsafe_allow_html=True)

# Pour cacher le menu hamburger et le footer de Streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
