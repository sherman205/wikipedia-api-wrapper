FROM python:3.9-slim
WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 80

CMD ["python", "-u", "app.py"]
