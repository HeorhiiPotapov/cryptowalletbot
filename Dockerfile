FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    chromium-driver \
    libnss3 \
    libgconf-2-4 \
    xvfb \
    libatk-bridge2.0-0 libgbm1 \
    wget \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver

ENV DISPLAY=:99

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PATH="/usr/local/bin/:$PATH"

CMD ["python", "main.py"]
