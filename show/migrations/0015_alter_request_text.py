# Generated by Django 3.2.8 on 2021-11-27 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0014_auto_20211111_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
