FROM python:3.10.6-slim

# Install app
COPY . /usr/app
WORKDIR /usr/app

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Create a new user to run the application required for centml endpoints
ARG USERNAME="centml"

RUN useradd -u 1024 -m -d /home/${USERNAME} -s /bin/bash ${USERNAME} && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}
USER 1024

EXPOSE 8000

# Run Battlesnake
CMD [ "python", "main.py" ]
#CMD [ "python", "main-2.py" ]
#ENTRYPOINT ["python", "main.py"]