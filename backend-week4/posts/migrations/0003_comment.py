# Generated by Django 5.0.3 on 2024-03-27 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_remove_post_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일시')),
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.IntegerField(verbose_name='게시글id')),
                ('writer', models.CharField(max_length=10, verbose_name='작성자')),
                ('content', models.TextField(verbose_name='내용')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]