# English to Irish translator
Welcome.

I decided to create an English to Irish translation app with a flashcard component. I've been trying to learn the language for years and thought it would be a good way to integrate something I like into code. I decided to use both Django and React for this app as one of the projects I'm on at work is a Django app, and leadership is looking at the idea of integrating React into instead of all the .handlebar templates.

I'm using a couple APIs for this. One of them gets a translation, and the other gets the pronunciation of the translation. When these API calls happen, they are created as shared_tasks within my Celery and RabbitMQ containers. They then get the data, the data is combined and then saved into an SQL database. Since Django has a serverless SQLite database ready to go, I opted to use that to reduce complexity.

I dont have much in the way of env variables, but I am setting a DEBUG env variable. For local development it's set to True and in Heroku it is set to False.

Grafana and Prometheus have been integrated for monitoring. Unit tests and integration tests have also been written and are passing.

The flashcard functionality is primitive but allows users to flip the card or to venture a guess in English. Without digging into UI/UX this is as refined as this app will get. Future enhancements could involve two-way translations, Irish text to speech, 404 handling, etc.


