# Generated by Django 3.2.15 on 2022-09-22 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yogi6', '0002_user_like_user_review_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_like',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='user_review',
            options={'managed': False},
        ),
        migrations.AlterModelTable(
            name='user',
            table='yogi6_user',
        ),
    ]