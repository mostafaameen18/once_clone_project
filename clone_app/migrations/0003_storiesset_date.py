# Generated by Django 3.1.2 on 2020-11-04 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clone_app', '0002_auto_20201104_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='storiesset',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]