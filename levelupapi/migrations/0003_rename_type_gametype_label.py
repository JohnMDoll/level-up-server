# Generated by Django 4.1.5 on 2023-02-01 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0002_alter_event_attendees'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gametype',
            old_name='type',
            new_name='label',
        ),
    ]