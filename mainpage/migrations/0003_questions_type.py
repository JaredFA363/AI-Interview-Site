# Generated by Django 5.0.2 on 2024-04-12 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0002_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='type',
            field=models.CharField(default=0, max_length=40),
            preserve_default=False,
        ),
    ]