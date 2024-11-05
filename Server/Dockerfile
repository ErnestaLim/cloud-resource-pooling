# Use the slim version of the official Python 3.12 image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install Dask with distributed support
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get remove --purge -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy your script into the container
COPY /send_email.py /app/send_email.py
COPY /const.py /app/const.py
COPY /storage_factory.py /app/storage_factory.py
COPY /socket_server.py /app/socket_server.py

# Expose the necessary port for the Dask scheduler
EXPOSE 5000

# Command to run the Dask scheduler and your script
CMD ["python3", "-u", "socket_server.py"]