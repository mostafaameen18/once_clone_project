# Generated by Django 3.1.2 on 2020-11-01 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='shop_password',
            field=models.CharField(default=0, max_length=500, unique=True),
            preserve_default=False,
        ),
    ]