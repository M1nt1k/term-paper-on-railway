# Generated by Django 4.1.4 on 2022-12-17 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_places_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='third_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='third_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
