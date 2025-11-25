### .env file
to be update

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
|-- crawl_data2db               <- init web data here
|   |-- main.py
|   `-- master_data.json
|-- django-code                 <- django codes here
|   |-- e_commerce
|   |-- manage.py
|   |-- media
|   |-- mysite
|   |-- requirements.txt
|   `-- static
`-- training_model              <- code for training model
    |-- dataset
    |-- output
    |-- requirements.txt
    `-- train_model.py
```