# Generated by Django 3.2.8 on 2021-10-29 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_userpronoun'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=255),
        ),
    ]
