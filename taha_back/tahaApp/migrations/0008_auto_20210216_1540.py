# Generated by Django 3.1.6 on 2021-02-16 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tahaApp', '0007_auto_20210216_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('affiliate', 'affiliate'), ('manager', 'manager')], default='affiliate', max_length=120)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='receipt',
            name='related_affiliate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tahaApp.profile'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='related_affiliate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tahaApp.profile'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='related_affiliate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tahaApp.profile'),
        ),
        migrations.DeleteModel(
            name='Affiliate',
        ),
    ]
