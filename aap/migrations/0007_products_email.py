# Generated by Django 4.0 on 2023-06-14 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aap', '0006_alter_products_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='email',
            field=models.EmailField(default='@gmail.com', max_length=100),
        ),
    ]
