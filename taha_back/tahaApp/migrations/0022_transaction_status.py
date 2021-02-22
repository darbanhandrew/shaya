# Generated by Django 3.1.6 on 2021-02-22 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tahaApp', '0021_auto_20210222_0306'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('paid', 'Paid'), ('requested', 'Requested'), ('cancelled', 'Cancelled')], default='requested', max_length=15),
        ),
    ]