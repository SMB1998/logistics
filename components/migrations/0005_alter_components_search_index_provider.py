# Generated by Django 5.0.3 on 2024-07-09 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0004_alter_components_search_index_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='components',
            name='search_index_provider',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
