FROM python:3.11

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./docker_entrypoint.sh .
RUN chmod +x ./docker_entrypoint.sh
ENTRYPOINT ["/bin/bash", "docker_entrypoint.sh"]

# Install nano and upgrade existing packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y nano

# Copy the rest of the application code
COPY . .

EXPOSE 8000