# Use the slim version of the official Python 3.12 image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install Dask with distributed support
RUN apt-get update && apt-get install -y --no-install-recommends \
    && pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib\
    && apt-get remove --purge -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy your script into the container
COPY /emailingservice.py /app/emailingservice.py
COPY /credentials.json /app/credentials.json
COPY /token.json /app/token.json
# Expose the necessary port for the Dask scheduler
EXPOSE 61000

# Command to run the Dask scheduler and your script
CMD ["python3", "-u", "emailingservice.py"]