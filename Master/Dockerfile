# Use the slim version of the official Python 3.12 image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install Dask with distributed support
RUN apt-get update && apt-get install -y --no-install-recommends \
    && pip install dask[distributed] \
    && apt-get remove --purge -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy your script into the container
COPY /socket_master.py /app/socket_master.py

# Expose the necessary port for the Dask scheduler
EXPOSE 8786

# Command to run the Dask scheduler and your script
CMD ["sh", "-c", "dask-scheduler --port 8786 & python socket_master.py"]