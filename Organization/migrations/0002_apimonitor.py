# Generated by Django 4.2.16 on 2024-12-09 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIMonitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_name', models.CharField(max_length=1000)),
                ('employee', models.CharField(max_length=100)),
                ('hit_time', models.CharField(max_length=100)),
            ],
        ),
    ]
