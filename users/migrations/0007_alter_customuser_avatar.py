# Generated by Django 5.1 on 2024-09-17 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_user_agreement_customuser_acceptterms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='profile_images/default.png', upload_to='profile_images/'),
        ),
    ]
