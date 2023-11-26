# Generated by Django 4.2.7 on 2023-11-26 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='adm_no',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='grade',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
