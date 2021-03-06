# Generated by Django 3.2.5 on 2021-10-08 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainsite', '0001_initial'),
        ('sounds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='sounds',
            field=models.ManyToManyField(related_name='songs', to='sounds.Sound'),
        ),
        migrations.AddField(
            model_name='song',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.venue'),
        ),
    ]
