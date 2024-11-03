# Use the official MySQL image from the Docker Hub
FROM mysql:8.0

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=cloud
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=root

# Add a custom SQL script to initialize the database (optional)
COPY ./init.sql /docker-entrypoint-initdb.d/

# Expose the default MySQL port
EXPOSE 3306

