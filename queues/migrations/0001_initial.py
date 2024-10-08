# Generated by Django 5.0.3 on 2024-08-27 00:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Queues',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('referencia', models.CharField(blank=True, max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('autoacept', models.BooleanField(default=False)),
            ],
        ),
    ]
