# Generated by Django 3.2.8 on 2021-10-16 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0004_alter_song_length'),
        ('show', '0008_alter_request_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='used_on_track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='mainsite.song'),
        ),
    ]