# Generated by Django 3.1.2 on 2020-11-05 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_1_37', '0008_donationopportunity_d_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationopportunity',
            name='d_amount',
            field=models.PositiveIntegerField(),
        ),
    ]