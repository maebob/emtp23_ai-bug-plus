FROM python:3.10-bullseye

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src/api /code/api
COPY src/engine /code/engine

ENV PYTHONPATH "${PYTHONPATH}:/code"
EXPOSE 80

CMD ["uvicorn", "api.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]