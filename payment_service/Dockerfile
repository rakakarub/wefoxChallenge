FROM python:3.6
WORKDIR /app
COPY dependencies.txt ./
RUN pip install -r dependencies.txt
COPY src /app
#CMD ["python", "runner.py"]