# Generated by Django 4.0 on 2023-06-15 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aap', '0008_bill_customer_billproduct_bill_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='customer',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]