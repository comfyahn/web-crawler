FROM python:3.6
MAINTAINER comfyahn "comfyahn@gmail.com"
COPY requirements.txt /
RUN pip3 install --no-cache-dir -r /requirements.txt
COPY . /app
WORKDIR /app
RUN pip install flask
EXPOSE 8080
CMD ["python", "app.py"]