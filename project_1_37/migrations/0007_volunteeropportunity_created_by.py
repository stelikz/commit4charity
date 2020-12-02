# Generated by Django 3.1.1 on 2020-11-03 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_1_37', '0006_auto_20201030_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteeropportunity',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to='auth.user'),
            preserve_default=False,
        ),
    ]
