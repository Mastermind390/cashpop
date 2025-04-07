# Generated by Django 5.1.7 on 2025-04-04 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_userlogin'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='link',
            field=models.CharField(default='enter a link', max_length=200),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('social_media', 'Social Media'), ('videos', 'Videos'), ('survey', 'Survey'), ('others', 'Others')], default='others', max_length=100),
        ),
    ]
