# Generated by Django 3.1.2 on 2020-11-02 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clone_app', '0004_components_rotation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='components',
            old_name='noCount',
            new_name='yesNoCount',
        ),
        migrations.RemoveField(
            model_name='components',
            name='yesCount',
        ),
        migrations.AlterField(
            model_name='components',
            name='noTimes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='components',
            name='yesTimes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]