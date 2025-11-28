# Stage 1: Build Stage
FROM python:3.10-slim-bookworm AS builder

# install first
RUN apt-get update && \
    apt-get install -y \    
        curl python3-dev default-libmysqlclient-dev \
        build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY ./crawl_data2db ./crawl_data2db
WORKDIR /app

COPY ./django-code/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy later
COPY ./django-code/mysite ./mysite
COPY ./django-code/e_commerce ./e_commerce
COPY ./django-code/manage.py .
COPY ./django-code/.env ./.env
COPY ./django-code/.celery.env ./.celery.env
COPY ./django-code/entrypoint.sh /usr/local/bin/


# Stage 2: Final/Runtime Stage
FROM python:3.10-slim-bookworm AS final

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /crawl_data2db /crawl_data2db
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /app /app
COPY --from=builder /usr/local/bin/ /usr/local/bin/

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]