FROM superlinear/python-gpu:3.12-cuda11.8

# Update system
RUN apt-get update && apt-get install -y build-essential cmake git unzip

# Install CUDA then tinyBenchmarks
RUN pip install torch torchvision torchaudio
RUN pip install git+https://github.com/felipemaiapolo/tinyBenchmarks

# Clone the lm-evaluation-harness repository
RUN git clone https://github.com/EleutherAI/lm-evaluation-harness.git /lm-evaluation-harness

# Install lm-evaluation-harness
WORKDIR /lm-evaluation-harness
RUN pip install -e .

# Set the default working directory
WORKDIR /