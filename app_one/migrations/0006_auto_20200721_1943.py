# Generated by Django 3.0.6 on 2020-07-21 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0005_auto_20200721_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='photo',
            field=models.ImageField(upload_to='static/uploads/'),
        ),
    ]
