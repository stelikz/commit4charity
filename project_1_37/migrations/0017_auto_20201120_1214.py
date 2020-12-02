# Generated by Django 3.1.1 on 2020-11-20 17:14

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project_1_37', '0016_auto_20201119_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationopportunity',
            name='d_causes',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Children', 'Children'), ('Elderly', 'Elderly'), ('Environmental', 'Environmental'), ('Animals', 'Animals'), ('Homelessness', 'Homelessness'), ('Poverty', 'Poverty'), ('Disabilities', 'Disabilities'), ('Medical Philanthropy', 'Medical Philanthropy')], max_length=93),
        ),
    ]
