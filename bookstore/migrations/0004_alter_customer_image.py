# Generated by Django 3.2.12 on 2022-06-13 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0003_customer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to=''),
        ),
    ]