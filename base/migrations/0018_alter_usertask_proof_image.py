# Generated by Django 5.1.7 on 2025-04-08 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_withdrawal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertask',
            name='proof_image',
            field=models.ImageField(default='images/hero-illustration.svg', upload_to='task_proofs/'),
        ),
    ]
