# Generated by Django 5.0.3 on 2024-05-17 14:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일시')),
                ('tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=20, verbose_name='해시태그')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일시')),
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('writer', models.CharField(max_length=10, verbose_name='작성자')),
                ('category', models.CharField(choices=[('DIARY', '일기'), ('STUDY', '공부'), ('ETC', '기타')], max_length=20)),
                ('imgfile', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HashtagPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일시')),
                ('hashtag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.hashtag')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='hashtag',
            name='post',
            field=models.ManyToManyField(through='posts.HashtagPosts', to='posts.post'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일시')),
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('writer', models.CharField(max_length=10, verbose_name='작성자')),
                ('content', models.TextField(verbose_name='내용')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post', verbose_name='게시글')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
