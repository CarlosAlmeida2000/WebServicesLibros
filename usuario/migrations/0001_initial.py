# Generated by Django 3.2.6 on 2021-08-28 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('rol', models.CharField(max_length=2)),
                ('usuario', models.CharField(max_length=15)),
                ('clave', models.CharField(max_length=15)),
            ],
        ),
    ]
