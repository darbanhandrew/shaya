# Generated by Django 3.1.6 on 2021-02-17 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tahaApp', '0011_auto_20210216_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='otp',
            name='message',
            field=models.CharField(default='13652', max_length=7),
        ),
    ]
