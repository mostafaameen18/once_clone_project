# Generated by Django 3.1.2 on 2020-11-05 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clone_app', '0005_storiesset_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='storiesset',
            name='desciption',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='storiesset',
            name='src',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='storiesset',
            name='title',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]