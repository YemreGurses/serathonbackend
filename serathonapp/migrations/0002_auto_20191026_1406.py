# Generated by Django 2.2.6 on 2019-10-26 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serathonapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='married',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='salary',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
