# Generated by Django 3.1.2 on 2020-11-05 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clone_app', '0006_auto_20201105_1416'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storiesset',
            old_name='desciption',
            new_name='description',
        ),
    ]