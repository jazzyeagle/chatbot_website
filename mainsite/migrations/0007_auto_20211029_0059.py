# Generated by Django 3.2.8 on 2021-10-29 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0006_alter_venue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='date',
            field=models.DateField(unique_for_date=True),
        ),
        migrations.AlterField(
            model_name='venueart',
            name='year',
            field=models.CharField(max_length=30),
        ),
    ]
