# Generated by Django 4.1.6 on 2023-09-09 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_otp_options_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='expration_date',
            field=models.DateTimeField(default=-12600),
        ),
    ]
