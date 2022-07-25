FROM python:alpine3.15

COPY . .

RUN pip install -r requirements.txt

# RUN crontab crontab

# CMD ["crond", "-f"]

# Replace with storage connection string in prod
ENV VOL_OUTPUT_DIR=/ns1_records.json
ENV AZURE_STORAGE_CONNECTION_STRING="..."

CMD ["python", "task.py"]