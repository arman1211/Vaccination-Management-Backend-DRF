# Generated by Django 5.0.7 on 2024-10-19 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine_campaign', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinecampaignmodel',
            name='image',
            field=models.CharField(default=None, max_length=100),
        ),
    ]