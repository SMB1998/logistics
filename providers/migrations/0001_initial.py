# Generated by Django 5.0.3 on 2024-08-27 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Providers',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('direccion', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
            ],
        ),
    ]
