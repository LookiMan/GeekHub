# Generated by Django 3.2.12 on 2022-02-01 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('by', models.CharField(max_length=128)),
                ('descendants', models.IntegerField()),
                ('ask_id', models.IntegerField()),
                ('score', models.IntegerField()),
                ('text', models.TextField()),
                ('time', models.TimeField()),
                ('title', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('by', models.CharField(max_length=128)),
                ('job_id', models.IntegerField()),
                ('score', models.IntegerField()),
                ('text', models.TextField()),
                ('time', models.TimeField()),
                ('title', models.TextField()),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('by', models.CharField(max_length=128)),
                ('descendants', models.IntegerField()),
                ('story_id', models.IntegerField()),
                ('score', models.IntegerField()),
                ('text', models.TextField()),
                ('time', models.TimeField()),
                ('title', models.TextField()),
                ('url', models.URLField()),
            ],
        ),
    ]
