# Generated by Django 4.1.5 on 2023-01-15 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blog/%Y/%m'),
        ),
    ]
