# Generated by Django 4.2.6 on 2023-10-19 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routes',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
