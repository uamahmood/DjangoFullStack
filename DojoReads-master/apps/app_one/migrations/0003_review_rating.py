# Generated by Django 2.1.7 on 2019-02-23 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0002_auto_20190223_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
