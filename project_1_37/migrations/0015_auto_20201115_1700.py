# Generated by Django 3.1.1 on 2020-11-15 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_1_37', '0014_auto_20201115_1559'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NameNumber',
        ),
        migrations.RemoveField(
            model_name='donationopportunity',
            name='d_amount',
        ),
        migrations.RemoveField(
            model_name='donationopportunity',
            name='d_donator',
        ),
        migrations.AddField(
            model_name='donationopportunity',
            name='d_total_received',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
