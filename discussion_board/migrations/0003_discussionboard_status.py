# Generated by Django 3.2.15 on 2025-03-27 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion_board', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussionboard',
            name='status',
            field=models.CharField(choices=[('created', 'Creado'), ('filling_participants', 'Llenando Participantes'), ('closed', 'Cerrado')], default='created', max_length=20),
        ),
    ]
