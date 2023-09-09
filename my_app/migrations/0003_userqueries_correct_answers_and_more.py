# Generated by Django 4.2.5 on 2023-09-08 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_tags_userqueries'),
    ]

    operations = [
        migrations.AddField(
            model_name='userqueries',
            name='correct_answers',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userqueries',
            name='incorrect_answers',
            field=models.PositiveIntegerField(default=0),
        ),
    ]