# Generated by Django 4.0 on 2021-12-18 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0010_auto_20211204_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='url_slug',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='url_slug',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='url_slug',
            field=models.TextField(blank=True, null=True),
        ),
    ]
