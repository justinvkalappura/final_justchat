# Generated by Django 3.2.4 on 2023-03-29 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0004_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.IntegerField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.TextField(null=True),
        ),
    ]
