# Generated by Django 3.2.6 on 2021-10-16 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_alter_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='saymyname',
            field=models.TextField(blank=True, null=True),
        ),
    ]
