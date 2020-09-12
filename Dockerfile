FROM python:latest

WORKDIR /temperature_sensor

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "temperature_sensor.py"]