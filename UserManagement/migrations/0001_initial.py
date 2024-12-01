# Generated by Django 4.2.16 on 2024-11-30 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('project_id', models.IntegerField(unique=True)),
                ('project_dis', models.TextField()),
            ],
        ),
    ]
