# Generated by Django 3.1.2 on 2020-11-06 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clone_app', '0007_auto_20201105_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='storiesset',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
