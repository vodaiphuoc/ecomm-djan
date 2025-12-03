### .env file
[example](django-code/.example.env)

### Dockerfile/DockerCompose files
to be update

### erd image
to be update to match models

### highlight depenedencies
- mysqlclient
- celery
- fasttext

### project structure overview
```
.
|-- Readme.md
|-- crawl_data2db           <--- crawl data for product list and reviews
|   |-- main.py
|   `-- master_data.json
|-- django-code             <--- django project (contains .env, .celery.env)
|   |-- Dockerfile
|   |-- accounts            <--- accounts app
|   |   |-- __init__.py
|   |   |-- admin.py
|   |   |-- apps.py
|   |   |-- forms.py
|   |   |-- migrations
|   |   |-- models.py
|   |   |-- templates
|   |   |-- tests.py
|   |   |-- urls.py
|   |   |-- utils.py
|   |   `-- views.py
|   |-- carts               <--- carts app
|   |   |-- __init__.py
|   |   |-- admin.py
|   |   |-- apps.py
|   |   |-- cart.py
|   |   |-- context_processors.py
|   |   |-- migrations
|   |   |-- templates
|   |   |-- tests.py
|   |   |-- urls.py
|   |   `-- views.py
|   |-- e_commerce_old      <--- this is deprecated app (already ignored in urls)
|   |   |-- __init__.py
|   |   |-- admin.py
|   |   |-- apps.py
|   |   |-- cart.py
|   |   |-- context_processors.py
|   |   |-- forms.py
|   |   |-- migrations
|   |   |-- ml_service
|   |   |-- models.py
|   |   |-- signals.py
|   |   |-- static
|   |   |-- tasks.py
|   |   |-- templates
|   |   |-- tests.py
|   |   |-- urls.py
|   |   |-- utils.py
|   |   `-- views
|   |-- entrypoint.sh       <--- entrypoint for running in docker compose
|   |-- manage.py
|   |-- mysite              <--- endpoints and core settings
|   |   |-- __init__.py
|   |   |-- asgi.py         <--- ednpoints to run in docker compose
|   |   |-- celery.py       <--- endpoint for celery app
|   |   |-- settings.py
|   |   |-- urls.py         <--- urls for all apps and its prefix
|   |   `-- wsgi.py
|   |-- orders              <--- orders app
|   |   |-- __init__.py
|   |   |-- admin.py
|   |   |-- apps.py
|   |   |-- forms.py
|   |   |-- migrations
|   |   |-- models.py
|   |   |-- templates
|   |   |-- tests.py
|   |   |-- urls.py
|   |   |-- utils.py
|   |   `-- views.py
|   |-- products            <--- products app
|   |   |-- __init__.py
|   |   |-- admin.py
|   |   |-- apps.py
|   |   |-- migrations
|   |   |-- models.py
|   |   |-- static
|   |   |-- templates
|   |   |-- tests.py
|   |   |-- urls.py
|   |   `-- views.py
|   |-- requirements.txt    <--- dependencies
|   |-- reviews             <--- reviews app
|   |   |-- __init__.py
|   |   |-- admin.py
|   |   |-- apps.py
|   |   |-- forms.py
|   |   |-- migrations
|   |   |-- ml_service      <--- ML inference
|   |   |-- models.py
|   |   |-- signals.py      <--- logic to trigger ML inference
|   |   |-- tasks.py        <--- tasks for celery run ML and update in DB
|   |   |-- templates
|   |   |-- tests.py
|   |   `-- views.py
|   |-- static              <--- global static
|   |   |-- css
|   |   |-- image
|   |   `-- js
|   `-- templates           <--- global template
|       |-- base.html
|       |-- footer.html
|       `-- header.html
|-- docker-compose.yaml     <--- docker compose
|-- nginx                   <--- for `gateway` service, use nginx to serve static and routing to `django_app` service
|   |-- Dockerfile
|   `-- nginx.conf
`-- training_model          <--- code and dataset for training model
    |-- Readme.md
    |-- dataset
    |   |-- test.csv
    |   `-- train.csv
    |-- output
    |   |-- test.txt
    |   `-- train.txt
    |-- requirements.txt
    `-- train_model.py
```


### docker compose explaination
```
name: ecomm-django

services:
  mysql_ecomm:
    image: mysql:latest
    container_name: ecomm-django-db
    ports:
      - "3306:3306"
    env_file:
      - ./django-code/.env
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - ecomm-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 10s
      retries: 5

  django_app:
    container_name: ecomm-django-container
    image: ecomm-django-image
    build:
      context: .
      dockerfile: ./django-code/Dockerfile
    depends_on:
      mysql_ecomm:
        condition: service_healthy
    networks:
      - ecomm-network
    volumes:
      - static_data:/vol/web/static
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://0.0.0.0:8000/health || exit 1 "]   <--- health check api by `django-health-check` library
      interval: 15s
      timeout: 10s
      retries: 7
  
  # redis service for celery
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - ecomm-network
    healthcheck:
      test: ["CMD-SHELL", "redis-cli ping | grep PONG"]
      interval: 10s
      timeout: 5s
      retries: 3
  
  # celery worker
  celery_worker:
    container_name: ecomm-django-celery-container
    image: ecomm-django-image           <---- same image as `django_app` service
    working_dir: /app
    entrypoint: celery -A mysite worker -l info  <--- use different entrypoint to start celery
    depends_on:
      redis:
        condition: service_healthy
      django_app:
        condition: service_healthy
    networks:
      - ecomm-network

  # let all run behind nginx and serving static files
  gateway:
    container_name: ecomm-django-gateway
    image: ecomm-django-gateway-image
    build:
      context: .
      dockerfile: ./nginx/Dockerfile
    ports:
      - "8080:80"                  <--- open at port 8080 at host
    depends_on:
      django_app:
        condition: service_healthy
    networks:
      - ecomm-network
    volumes:
      - static_data:/vol/web/static

networks:
  ecomm-network:
    driver: bridge

volumes:
  static_data:      <--- this is a shared volume between `django_app` service and `gateway` service, in entrypoint.sh of `django_app`, static files are generated and copied to /vol/web/static of this volume, so `gateway` service doesnt need to run python manage.py collectstatic

    driver: local
  mysql_data:
    driver: local
  redis_data:
    driver: local
```