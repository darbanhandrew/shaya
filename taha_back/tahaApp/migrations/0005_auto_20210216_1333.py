# Generated by Django 3.1.6 on 2021-02-16 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tahaApp', '0004_auto_20210211_0847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basemodel',
            name='images',
        ),
        migrations.AddField(
            model_name='basemodel',
            name='images',
            field=models.ForeignKey(default='123', on_delete=django.db.models.deletion.CASCADE, to='tahaApp.image'),
            preserve_default=False,
        ),
    ]
