# Generated by Django 3.2.9 on 2021-11-16 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contributor', '0005_auto_20211114_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='repomodel',
            name='discussion_url',
            field=models.URLField(default='url', max_length=240),
            preserve_default=False,
        ),
    ]