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
RUN git clone https://github.com/Jiaxin-Ye/TIM-Net_SER.git /lib/TIM-Net_SER
WORKDIR /lib/TIM-Net_SER/Code

# RUN ls >> check_ls.txt
RUN python3 -m pip install cvxopt==1.3.0 h5py==3.1.0 keras==2.7.0 librosa==0.9.2 matplotlib==3.6.1 numba==0.56.3 numpy==1.19.5 openpyxl==3.0.10 pandas==1.3.0 prettytable==3.4.1 scikit-learn==1.1.2 scipy==1.9.2 spafe==0.2.0 speechpy==2.4 tensorflow==2.7.0 tqdm==4.63.1
# RUN python3 -m pip install -r requirement.txt
RUN python3 -m pip install protobuf==3.20

# # Install dependencies
# RUN python3 -m pip install -e . --no-cache-dir
# # Run once to ensure demucs works and trigger the default model download
# RUN python3 -m demucs -d cpu test.mp3 
# # Cleanup output - we just used this to download the model
# RUN rm -r separated

# VOLUME /data/input
# VOLUME /data/output
# VOLUME /data/models
COPY ./10-fold_weights_best_1.hdf5 /lib/TIM-Net_SER/Code/
COPY ./Model.py /lib/TIM-Net_SER/Code/
COPY ./inference.py /lib/TIM-Net_SER/Code/

COPY ./worker.py /

WORKDIR /
CMD  python3 /worker.py