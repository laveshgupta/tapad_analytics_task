FROM python:3.9-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY config.py config.py
COPY constants.py constants.py
COPY logger.py logger.py
COPY redis_connection_pool.py redis_connection_pool.py
COPY tapad_analytics_helper.py tapad_analytics_helper.py
COPY tapad_analytics_server.py tapad_analytics_server.py
COPY tapad_analytics_task.json tapad_analytics_task.json
CMD ["python", "tapad_analytics_server.py"]
