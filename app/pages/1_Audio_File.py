import streamlit as st
import time
import streamlit_extras.add_vertical_space as avs
import os
import sys
from pydub import AudioSegment

# Adding the path to the project_root to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.model.transcripts import TranscriptProcessor
from src.model.load_model import WhisperModelManager
from src.utils.load_audio import AudioProcessor


st.set_page_config(page_title="Audio", page_icon=":headphones:", layout="wide")


# creating an object for whisper model
whisper_model = WhisperModelManager().load_model("base")
transcript_processor = TranscriptProcessor(whisper_model)

# text alignment
title_style = """
            <style>
            .title {
                text-align: center;
                color:#faa356;
            }
            </style>
        """
st.markdown(title_style, unsafe_allow_html=True)


# hiding hamburger menu
hide_menu_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    .stApp [data-testid="stToolbar"]{display:none;}
                    footer {visibility:hidden}
                    </style>
                    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# header
st.markdown(
    "<h1 class='title'>Audio File Transcription <span style='color:#b3cee5'>&#x1F3B5;</span>&#x1F4D3;</h1>",
    unsafe_allow_html=True,
)

# objective markdown text
objective = """
    <h3 style="color:#a2d2fb">Objective</h3>

    > The objective of this page is to empower users to effortlessly transcribe pre-recorded audio files. By
    providing a seamless and user-friendly interface, this page allows users to upload audio files in various formats
    and generate accurate text transcriptions with a simple click. The page
    aims to offer a comprehensive solution for batch audio transcription, ensuring efficiency, accuracy,
    and user satisfaction throughout the process. """
st.markdown(objective, unsafe_allow_html=True)

# usage markdown text
using = """
    <h3 style="color:#a2d2fb">How to Use ?</h3>

    <span style="color:#7ce38b">1. Upload Audio File:</span>
    Click on the designated area or button to upload your audio file. Supported formats include MP3, WAV, and more.

    <span style="color:#7ce38b">2. Generate Transcription:</span> After uploading the audio file, find the "Generate"
    button and click on it. This initiates the transcription process. Wait for the system to process the audio and
    generate the text transcription.

    <span style="color:#7ce38b">3. Play Audio:</span> Use the "Play" button to
    listen to the audio and review the corresponding text transcription. The play button allows you to hear the audio
    content alongside the displayed text, facilitating a comprehensive review.

    <span style="color:#7ce38b">4. Review Transcription:</span> Once the transcription is complete, the text result
    will be displayed on the page. Review the transcription for accuracy. You can copy the text for
    further use. """

st.markdown(using, unsafe_allow_html=True)


# main function to display text
def main():

    # file upload header
    file_upload = """
        <h3 style="color:#a2d2fb">Audio Transcriber</h3>
    """
    st.markdown(file_upload, unsafe_allow_html=True)

    # creating columns
    upload_btn, play_btn, generate_btn = st.columns([3, 1, 1])
    text_area, transcription_time = st.columns([3, 1])

    with upload_btn:
        uploaded_file = st.file_uploader(
            "Choose a file", help="Please upload a audio file", type=["wav", "mp3"]
        )

        BASE_PATH = "./data/uploaded"
        file_path = ""

        # removing all the files if directory already exits
        for file in os.listdir(BASE_PATH):
            file_path = os.path.join(BASE_PATH, file)
            # print(file_path)
            os.remove(file_path)

        if uploaded_file:
            # checking the file type & saving on server
            file_name = uploaded_file.name
            audio_file_path = f"{BASE_PATH}/{file_name}"
            # print(file_name)
            try:
                if file_name.endswith(".mp3"):
                    audio = AudioSegment.from_mp3(uploaded_file)
                    audio.export(audio_file_path, format="wav")
                else:
                    wav_file = AudioSegment.from_wav(uploaded_file)
                    wav_file.export(audio_file_path, format="wav")
                st.session_state["correct_upload"] = True
            except Exception as e:
                st.error("Error in converting file! Please verify the format.")
                st.session_state["correct_upload"] = False

    # creating "play audio" button
    with play_btn:
        avs.add_vertical_space(2)
        if uploaded_file and st.session_state["correct_upload"]:
            audio_file = open(audio_file_path, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/ogg")
            # st.audio(file_path,)
        avs.add_vertical_space(3)

    # creating "transcribe audio" button
    with generate_btn:
        avs.add_vertical_space(3)
        transcribe_btn = st.button("Transcribe Audio", type="primary")
        with st.spinner("Transcribing Audio..!!"):
            if transcribe_btn:
                # throwing an error if file was not uploaded
                if not uploaded_file:
                    error = st.error("Upload an audio file.")
                    time.sleep(1)
                    error.empty()
                else:
                    with text_area:
                        t_duration = None
                        # calling get_transcripts() to get the transcripts
                        if file_path:
                            results = transcript_processor.get_transcripts(file_path)
                            if results:
                                transcripts, t_duration = results
                                st.markdown(
                                    '<h3 style="color:#a2d2fb">Transcripts</h3>',
                                    unsafe_allow_html=True,
                                )
                                st.text_area(label=" ", value=transcripts["text"])
                            else:
                                st.error(f"The transcription results is {results}")
                                st.write(results)

                            # markdown text for showing time taken to transcribe the audio file
                            if t_duration:
                                with transcription_time:
                                    avs.add_vertical_space(5)
                                    st.metric(
                                        label="Time took to transcribe (In Sec)",
                                        value=t_duration,
                                    )


if __name__ == "__main__":
    main()
