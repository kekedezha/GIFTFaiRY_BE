# Generated by Django 4.2.7 on 2024-01-30 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bestow', '0025_user_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=300, null=True, unique=True),
        ),
    ]
