# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.7
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev gcc ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download dependencies using cache mount and bind mount
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# RUN apt-get update && apt-get install -y ffmpeg

# Copy the source code into the container.
COPY . .

EXPOSE 8501

# Run the application.
ENTRYPOINT ["streamlit", "run", "app/app.py"]
