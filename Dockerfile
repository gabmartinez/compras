FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y curl gnupg2 unixodbc-dev gcc && \
    export DEBVER=$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2 | cut -d '.' -f 1) && \
    curl -sSL -O https://packages.microsoft.com/config/debian/$DEBVER/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "compras.wsgi"]
