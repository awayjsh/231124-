# Generated by Django 4.2.4 on 2023-11-23 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='like_count',
            field=models.IntegerField(null=True),
        ),
    ]