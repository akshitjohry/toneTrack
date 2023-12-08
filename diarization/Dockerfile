FROM python:3.8-slim

RUN apt update && apt install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    git \
    python3 \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade redis jsonpickle requests flask minio

# RUN git clone -b main --single-branch https://github.com/facebookresearch/demucs /lib/demucs
# WORKDIR /lib/demucs
RUN python3 -m pip install google-cloud google-api-python-client google-cloud-vision google-cloud-speech scipy

# # Install dependencies
# RUN python3 -m pip install -e . --no-cache-dir
# # Run once to ensure demucs works and trigger the default model download
# RUN python3 -m demucs -d cpu test.mp3 
# # Cleanup output - we just used this to download the model
# RUN rm -r separated

# VOLUME /data/input
# VOLUME /data/output
# VOLUME /data/models
COPY ./speech_diarization.py /
COPY ./commercial1.wav /
COPY ./commercial2.wav /
COPY ./service-credentials.json /

COPY ./worker_diarization.py /

WORKDIR /
CMD  python3 /worker_diarization.py