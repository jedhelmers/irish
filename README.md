# English to Irish translator
Welcome.

I decided to create an English to Irish translation app with a flashcard component. I've been trying to learn the language for years and thought it would be a good way to integrate something I like into code. I decided to use both Django and React for this app as one of the projects I'm on at work is a Django app, and leadership is looking at the idea of integrating React into instead of all the .handlebar templates.

I'm using a couple APIs for this. One of them gets a translation, and the other gets the pronunciation of the translation. When these API calls happen, they are created as shared_tasks within my Celery and RabbitMQ containers. They then get the data, the data is combined and then saved into an SQL database. Since Django has a serverless SQLite database ready to go, I opted to use that to reduce complexity.

I dont have much in the way of env variables, but I am setting a DEBUG env variable. For local development it's set to True and in Heroku it is set to False.

Grafana and Prometheus have been integrated for monitoring. Unit tests and integration tests have also been written and are passing.

The flashcard functionality is primitive but allows users to flip the card or to venture a guess in English. Without digging into UI/UX this is as refined as this app will get. Future enhancements could involve two-way translations, Irish text to speech, 404 handling, etc.

## React
I haven't integrated **npm run buil** into my docker-compose.yml yet, so you may have to build the frontend manually. Simply:
**cd** into **frontend** ```cd frontend && npm run build```.

## Monitoring
For this project, I opted for Grafana and Prometheus for monitoring and data visualisation. Prometheus actively monitors the app in both the local env and production env (https://jedsirish-702019bcf03c.herokuapp.com/monitoring/metrics). Grafana, however, only works in the local env. After learning Heroku does not play well with docker-compose.yml files, I realized I would need to switch to GCP (or another provider) to get it working properly.

```http://localhost:3001/``` should get you to the local Grafan instance.
```localhost:8000/monitoring/metrics``` should get you to the raw Prometheus data.

## Production
I have set env variables for both local and production. To run locally, a .env is required at the project root. Create a **.env** and add the following code:
```
REACT_APP_API_URL=http://localhost:8000
DEBUG=True
RABBITMQ_DEFAULT_USER=myuser
RABBITMQ_DEFAULT_PASS=mypassword
```

If launching in production, you will need to set these variables.

## Build/Deploy
A simple ```docker-compose build``` and ```docker-compose up -d``` should get the project going. If for some reason migrations are required then run ```python manage.py migrate```. If updating a model then ```python manage.py makemigrations``` followed by ```python manage.py migrate```.

If pushing to GitHub, there is a workflow that will build the container in github's CI/CD. **.github/workflows/docker-image.yml** should take care of everything.

If using Heroku, create a new project and point it to the github branch. Once github's workflow has complete, the container should deploy to the public facing site.