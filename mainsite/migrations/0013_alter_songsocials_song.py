# Generated by Django 4.0 on 2021-12-19 01:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0012_alter_songsocials_song'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songsocials',
            name='song',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='socials', to='mainsite.song'),
        ),
    ]