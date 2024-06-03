FROM python:3.8.0

ENV TZ UTC
ARG UNAME=lidar-driver-hokuyo

COPY . lidar-driver-hokuyo
RUN pip3 install -r /lidar-driver-hokuyo/requirements.txt

ENTRYPOINT ["python3", "/lidar-driver-hokuyo/driver.py"]
