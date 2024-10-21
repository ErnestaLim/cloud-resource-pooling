# Use the slim version of the official Python 3.12 image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install Dask with distributed support and supervisor
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    && pip install dask[distributed] \
    && apt-get remove --purge -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy your scripts into the container
COPY socket_master.py /app/socket_master.py
COPY eval_llm.py /app/eval_llm.py
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the necessary port for the Dask scheduler
EXPOSE 8786

# Command to run the supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
