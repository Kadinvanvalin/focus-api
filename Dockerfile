FROM python:3.11-slim
# Install git and system deps
RUN apt-get update && \
	    apt-get install -y git openssh-client && \
	    apt-get clean && \
	    rm -rf /var/lib/apt/lists/*

#RUN mkdir -p /root/.ssh && \
#					ssh-keyscan github.com >> /root/.ssh/known_hosts

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
