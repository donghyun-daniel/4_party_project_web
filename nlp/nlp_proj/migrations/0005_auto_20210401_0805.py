# Generated by Django 3.1.7 on 2021-04-01 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nlp_proj', '0004_auto_20210401_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
        ),
    ]
