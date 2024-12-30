import streamlit as st
import streamlit_extras.add_vertical_space as avs
import os
import sys

# Adding the path to the project_root to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.utils.extract_youtube_audio import YouTubeAudioExtractor
from src.model.load_model import WhisperModelManager
from src.model.transcripts import TranscriptProcessor


st.set_page_config(page_title="Video", page_icon=":movie_camera:", layout="wide")

yt_extractor = YouTubeAudioExtractor()

whisper_model = WhisperModelManager().load_model("base")
transcript_processor = TranscriptProcessor(whisper_model)


if "uploaded" not in st.session_state:
    st.session_state["uploaded"] = False
    st.session_state["extracted"] = False
    st.session_state["url"] = ""
    st.session_state["file_path"] = ""


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
    "<h1 class='title'>YouTube Audio Transcription <span style='color:#b3cee5'>&#x1F4FD;</span>&#x1F4D3;</h1>",
    unsafe_allow_html=True,
)

# objective markdown text
youtube_objective = """
    <h3 style="color:#a2d2fb">Objective</h3>

    > The objective of this page is to facilitate users in extracting audio and generating accurate text transcriptions from YouTube videos.
    By accepting a YouTube video link as input, this page streamlines the process of extracting audio content and performing automatic transcription.
    The user-friendly interface ensures a seamless experience, allowing users to obtain text transcriptions effortlessly.
    This page aims to provide an efficient solution for transcription from YouTube videos, ensuring accuracy and user satisfaction throughout the process.
    """
st.markdown(youtube_objective, unsafe_allow_html=True)

# usage markdown text
youtube_using = """
    <h3 style="color:#a2d2fb">How to Use ?</h3>

    <span style="color:#7ce38b">1. Enter YouTube Video Link:</span>
    Input the YouTube video link in the designated area or field on the page.

    <span style="color:#7ce38b">2. Extract Audio:</span> After entering the YouTube video link, locate the "Extract Audio"
    button and click on it. This initiates the process of extracting audio from the provided YouTube video.

    <span style="color:#7ce38b">3. Generate Transcription:</span> Once the audio extraction is complete, find the "Generate Transcription"
    button and click on it. This triggers the automatic transcription process. Wait for the system to process the audio and
    generate the text transcription.

    <span style="color:#7ce38b">4. Play Audio:</span> Utilize the "Play" button to listen to the extracted audio and review the corresponding text transcription.
    The play button facilitates an integrated review of the audio content alongside the displayed text.

    <span style="color:#7ce38b">5. Review Transcription:</span> Once the transcription is complete, the text result
    will be displayed on the page. Review the transcription for accuracy and make any necessary adjustments.
    Copy the text for further use or analysis.
    """
st.markdown(youtube_using, unsafe_allow_html=True)


# main function to display text
# @st.cache_data(experimental_allow_widgets=True)
def main():

    # file upload header
    youtube_transcriber = """
         <h3 style="color:#a2d2fb">YouTube Audio Transcriber</h3>
        """
    st.markdown(youtube_transcriber, unsafe_allow_html=True)

    # creating columns
    url_input, audio_extract_btn = st.columns([3, 1])
    audio_btn, transcripts = st.columns([3, 1])
    transcripts_text, duration = st.columns([3, 1])

    with url_input:
        url = st.text_input(
            label="Enter Any YouTube Video URL ", help="Please Upload a Short Video"
        )
        if url:
            st.session_state["uploaded"] = True
            st.session_state["url"] = url

    with audio_extract_btn:
        avs.add_vertical_space(2)

        extract_btn = st.button("Extract Audio", type="primary")

        if extract_btn and st.session_state["uploaded"] == True:
            st.session_state["file_path"] = "./data/uploaded/youtube_audio.m4a"
            yt_extractor.extract_audio(url)
            st.session_state["extracted"] = True

    avs.add_vertical_space(2)
    with audio_btn:
        if st.session_state["file_path"]:
            st.audio(st.session_state["file_path"])

    with transcripts:
        transcripts_btn = st.button("Get Transcripts", type="primary")

        if transcripts_btn and st.session_state["file_path"]:
            with st.spinner("Transcribing Audio !!!"):
                result = transcript_processor.get_transcripts(
                    st.session_state["file_path"]
                )
                if result:
                    transcripts, t_duration = result

                avs.add_vertical_space(2)
                with transcripts_text:
                    st.text_area(
                        label="Transcripts for YouTube Video", value=transcripts["text"]
                    )

                with duration:
                    st.metric(
                        label="Time took to transcribe ( In Sec )", value=t_duration
                    )


if __name__ == "__main__":
    main()
