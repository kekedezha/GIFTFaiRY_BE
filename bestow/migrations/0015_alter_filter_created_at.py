# Generated by Django 4.2.7 on 2024-01-12 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bestow', '0014_alter_filter_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
