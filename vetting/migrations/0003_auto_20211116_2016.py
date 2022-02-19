# Generated by Django 3.2.9 on 2021-11-16 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vetting', '0002_vetterdetails_vettingdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='vettingdetails',
            name='company',
            field=models.CharField(default='Rydal inc', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vettingdetails',
            name='location',
            field=models.CharField(default='London', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vettingdetails',
            name='name',
            field=models.CharField(default='Rob', max_length=80),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vettingdetails',
            name='avatar_url',
            field=models.URLField(max_length=240),
        ),
        migrations.AlterField(
            model_name='vettingdetails',
            name='email',
            field=models.EmailField(max_length=240),
        ),
        migrations.AlterField(
            model_name='vettingdetails',
            name='website',
            field=models.URLField(max_length=240),
        ),
        migrations.DeleteModel(
            name='VetterDetails',
        ),
    ]