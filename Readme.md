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