# Generated by Django 5.0.3 on 2024-07-09 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0003_components_datasheet_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='components',
            name='search_index_provider',
            field=models.CharField(default='', max_length=100),
        ),
    ]