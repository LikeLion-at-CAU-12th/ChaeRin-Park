# Generated by Django 5.0.3 on 2024-06-06 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_thumnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumnails/', verbose_name='썸네일'),
        ),
    ]
