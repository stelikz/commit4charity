# Generated by Django 3.1.1 on 2020-11-03 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_1_37', '0007_volunteeropportunity_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationopportunity',
            name='d_created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='d_created_by', to='auth.user'),
            preserve_default=False,
        ),
    ]