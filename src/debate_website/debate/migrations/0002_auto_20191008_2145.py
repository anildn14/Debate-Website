# Generated by Django 2.2.6 on 2019-10-08 16:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('debate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
