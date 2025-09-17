FROM python:3.11-slim

# Create a non-root user and models directory
RUN groupadd --system piper && \
    useradd  --system --gid piper --home-dir /home/piper piper && \
    mkdir -p /models && \
    chown -R piper:piper /models

# Switch to piper, set up paths
USER piper
ENV HOME=/home/piper
ENV PATH="${HOME}/.local/bin:${PATH}"
WORKDIR /home/piper

# Upgrade pip inside the container's user environment
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Piper-TTS & Flask into ~/.local
RUN pip install --no-cache-dir piper-tts flask

# Download your model into /models
ARG MODEL=en_GB-cori-medium
RUN python3 -m piper.download_voices ${MODEL} --download-dir /models

EXPOSE 5000

CMD ["python3", "-m", "piper.http_server", \
     "--host", "0.0.0.0", \
     "--port", "5000", \
     "--data-dir", "/models", \
     "--model", "en_GB-cori-medium", \
     "--speaker", "0", \
     "--length_scale", "1", \
     "--noise_scale", "0.667", \
     "--noise_w", "0.8"]
