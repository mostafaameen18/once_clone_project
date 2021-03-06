# Generated by Django 3.1.2 on 2020-11-04 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clone_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='views',
        ),
        migrations.CreateModel(
            name='storiesSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='My Once Story', max_length=500)),
                ('views', models.IntegerField(default=0)),
                ('storiesSet', models.ManyToManyField(to='clone_app.story')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
