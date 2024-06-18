#
FROM python:3.9

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app

# Web-service settings can be overridden via environment variables like:
# ENV STORAGE_CONNECT sqlite://connection_string
#
CMD ["fastapi", "run", "app/api/v1/nmap_api.py", "--port", "5000"]
