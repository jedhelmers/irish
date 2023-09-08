from django.db import models
from django.contrib.auth.models import User


class Tags(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag

class UserQueries(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_text = models.TextField()
    output_text = models.TextField()
    pronunciation = models.TextField()
    correct_answers = models.PositiveIntegerField(default=0)
    incorrect_answers = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tags, related_name='queries')

    def __str__(self):
        return f'Query by {self.user.username} at {self.creation}'


def populate_tags():
    predefined_tags = ['travel', 'food', 'photography', 'technology', 'music', 'fitness']

    for tag_name in predefined_tags:
        tag, created = Tags.objects.get_or_create(tag=tag_name)
        if created:
            print(f"Added new tag: {tag_name}")
        else:
            print(f"Tag {tag_name} already exists")
