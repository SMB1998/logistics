# Generated by Django 3.2.15 on 2025-04-03 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion_board', '0004_discussionboard_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussionboard',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='discussionboard',
            name='referencia',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
