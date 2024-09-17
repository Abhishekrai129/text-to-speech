import streamlit as st
from TTS.api import TTS
import soundfile as sf

# Initialize the TTS model
@st.cache_resource
def load_tts_model():
    # Instantiate the TTS class
    tts = TTS('tts_models/en/ljspeech/fast_pitch')

    # List available TTS models
    try:
        available_models = tts.list_models()  # Ensure this method is correct
        st.write("Available models:", available_models)  # Debugging line to check available models
        st.write("Type of available_models:", type(available_models))  # Debugging line to check the type
    except Exception as e:
        st.error(f"Error listing models: {e}")
        st.stop()

    # Select a FastSpeech2 model
    model_name = 'tts_models/en/ljspeech/fast_pitch'

    # Check if the model_name is in available_models
    if isinstance(available_models, list) and model_name not in available_models:
        st.error(f"Model {model_name} is not available.")
        st.stop()
    
    # If available_models is not a list, check its attributes or methods
    if not isinstance(available_models, list):
        st.write("Available models are not in a list format. Trying alternative methods.")
        # If available_models has a method or attribute to get model names, use it
        # For example: available_models.get_model_names() or available_models.models

    return tts

tts = load_tts_model()

st.title('Text to Speech using FastSpeech')
st.write('Enter text and generate speech output.')

# Text input
user_input = st.text_area("Enter the text to convert to speech", "")

if st.button("Generate Speech"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Generating speech..."):
            # Generate speech waveform
            wav = tts.tts(user_input)
            
            # Debugging: Inspect the generated audio
            st.write("Type of generated audio:", type(wav))
            if hasattr(wav, 'shape'):
                st.write("Shape of generated audio:", wav.shape)
            
            # Determine the sample rate (if applicable)
            # You might need to get the sample rate from somewhere else or set it manually
            sample_rate = 22050  # Use default or appropriate sample rate

            # Save the audio to a file
            try:
                sf.write('output.wav', wav, sample_rate)
                st.success("Speech generated successfully!")
            except Exception as e:
                st.error(f"Error saving audio: {e}")

            # Display audio player
            st.audio('output.wav', format='audio/wav')
