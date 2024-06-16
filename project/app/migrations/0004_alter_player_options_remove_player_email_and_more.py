# Generated by Django 5.0.6 on 2024-06-16 19:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_question_and_answer_about_order'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ('user__username',), 'verbose_name': 'player', 'verbose_name_plural': 'players'},
        ),
        migrations.RemoveField(
            model_name='player',
            name='email',
        ),
        migrations.RemoveField(
            model_name='player',
            name='name',
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='player', to=settings.AUTH_USER_MODEL, verbose_name='user'),
            preserve_default=False,
        ),
    ]
