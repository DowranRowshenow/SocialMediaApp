# Generated by Django 4.1 on 2022-09-11 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_dislikes_postcomment_dislikes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcomment',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comments', to='posts.postcomment'),
        ),
    ]
