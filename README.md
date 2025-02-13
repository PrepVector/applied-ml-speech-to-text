# Automatic Speech Recognition Using OpenAI Whisper

## Overview

This project aims to implement Automatic Speech Recognition (ASR) using the Whisper ASR system. The repository is structured with several key components for developing, training, and deploying ASR models.

## Repository Structure

1. **app**: Contains a Streamlit app for interacting with the ASR system.
    - **pages**: Subdirectory for multiple pages of the Streamlit app.

2. **config**: Centralized location for configuration files.

3. **data**: Stores different versions of data in distinct folders.
    - **raw**: Original, unprocessed data.
    - **interim**: Intermediate data during processing.
    - **processed**: Processed and cleaned data.
    - **uploaded**: Location for uploaded data.

4. **models**: Directory for saving and loading ASR models.

5. **notebooks**: Google Colab notebooks for ASR and Whisper fine-tuning.

6. **references**: Contains a document with references used in the project.

7. **src**: Main source code directory with the following subfolders:
    - **data_processing**: Functions for processing audio files.
    - **feature_engineering**: Extracts or engineers new features from audio.
    - **evaluation**: Evaluation scripts for assessing model performance.
    - **model**: Contains code to load ASR models.
    - **utils**: Helper and utility functions.

8. **main.py**: Placeholder file for model fine-tuning and other functionalities.

9. **Dockerfile**: Configuration for setting up the project in a Docker container.

## Setting Up the Project

### Prerequisites

- Docker installed on your machine.

### Instructions - Docker

1. Clone the repository:

    ```bash
    git clone  https://github.com/PrepVector/Applied-ML.git
    ```

2. Build the Docker image:

    ```bash
    docker build -t asr-project .
    ```

3. Run the Docker container:

    ```bash
    docker run -p 8501:8501 asr-project
    ```

4. Access the Streamlit app in your web browser at [http://localhost:8501](http://localhost:8501).

### Instructions - Docker Compose

1. Clone the repository:

    ```bash
    git clone  https://github.com/PrepVector/Applied-ML.git
    ```

2. Start application using docker compose:

    ```bash
    docker compose --profile app up
    ```

3. Access the Streamlit app in your web browser at [http://localhost:8501](http://localhost:8501).

4. To stop the application

    ```bash
    docker compose down
    ```

### Additional Commands

- To enter the Docker container shell:

    ```bash
    docker run -it asr-project /bin/bash
    ```

- To stop the running container:

    ```bash
    docker stop $(docker ps -q --filter ancestor=asr-project)
    ```

Adjust the instructions based on your specific project needs.
