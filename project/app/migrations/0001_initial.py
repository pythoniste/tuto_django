# Generated by Django 5.0.6 on 2024-06-16 13:52

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=32, unique=True, verbose_name='name')),
                ('duration', models.DurationField(blank=True, null=True, verbose_name='duration')),
                ('status', models.CharField(choices=[('draft', 'draft'), ('ready', 'ready'), ('ongoing', 'ongoing'), ('done', 'done')], db_index=True, default='draft', max_length=8, verbose_name='status')),
                ('level', models.SmallIntegerField(blank=True, choices=[(1, 'easy'), (2, 'medium'), (3, 'hard'), (4, 'extreme'), (5, 'nightmare')], db_index=True, null=True, verbose_name='level')),
            ],
            options={
                'verbose_name': 'game',
                'verbose_name_plural': 'games',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=32, unique=True, verbose_name='name')),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254, null=True, unique=True, verbose_name='email')),
                ('description', models.TextField(verbose_name='description')),
                ('score', models.PositiveIntegerField(verbose_name='score')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='creation datetime')),
                ('last_modification_datetime', models.DateTimeField(auto_now=True, verbose_name='last modification datetime')),
                ('subscription_date', models.DateField(blank=True, null=True, verbose_name='subscription date')),
                ('profile_activated', models.BooleanField(verbose_name='profile activated')),
                ('signed_engagement', models.FileField(blank=True, max_length=256, null=True, upload_to=app.models.compute_signed_engagement_path, verbose_name='signed engagement')),
                ('avatar', models.ImageField(blank=True, max_length=256, null=True, upload_to=app.models.compute_avatar_path, verbose_name='avatar')),
            ],
            options={
                'verbose_name': 'player',
                'verbose_name_plural': 'players',
                'ordering': ('name',),
            },
        ),
    ]
