FROM node:20-bookworm-slim AS airtable
WORKDIR /airtable
COPY airtable/package*.json ./
RUN npm ci --omit=dev --ignore-scripts

FROM python:3.12-slim-bookworm

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends libpq-dev gcc curl libstdc++6 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=airtable /usr/local/bin/node /usr/local/bin/node
COPY --from=airtable /airtable/node_modules /app/airtable/node_modules

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
