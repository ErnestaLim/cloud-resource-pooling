FROM superlinear/python-gpu:3.12-cuda11.8

# Update system and install all tools
RUN apt-get update && \
    apt-get install -y build-essential cmake git unzip && \
    pip install torch torchvision torchaudio && \
    pip install git+https://github.com/felipemaiapolo/tinyBenchmarks && \
    apt-get remove --purge -y && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Clone the lm-evaluation-harness repository
RUN git clone https://github.com/EleutherAI/lm-evaluation-harness.git /lm-evaluation-harness

# Install lm-evaluation-harness
WORKDIR /lm-evaluation-harness
RUN pip install -e .

# Our own socket code
WORKDIR /app
COPY helper.py /app/helper.py
COPY socket_storage.py /app/socket_storage.py
COPY socket_slave.py /app/socket_slave.py

EXPOSE 51592

# Command to run the socket_slave.py
ENTRYPOINT ["python3", "-u", "socket_slave.py"]