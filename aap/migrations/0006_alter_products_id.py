# Generated by Django 4.1.7 on 2023-05-11 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aap', '0005_alter_products_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
