# Generated by Django 5.0.3 on 2024-06-29 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0004_alter_requests_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
