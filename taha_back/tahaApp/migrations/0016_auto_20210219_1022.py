# Generated by Django 3.1.6 on 2021-02-19 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tahaApp', '0015_auto_20210218_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bank_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='sheba',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='transaction_status',
            field=models.CharField(choices=[('a', 'Active'), ('d', 'Deactive')], default='d', max_length=2),
        ),
        migrations.AlterField(
            model_name='otp',
            name='message',
            field=models.CharField(default='40072', max_length=7),
        ),
    ]
