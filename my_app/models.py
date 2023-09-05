from django.db import models


class Song(models.Model):
    user_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    notes = models.JSONField()

    # def __str__(self):
    #     return self.user_id

# python3 manage.py makemigrations
# python3 manage.py migrate
