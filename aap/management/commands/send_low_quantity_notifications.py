from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from aap.models import Merchant, products

class Command(BaseCommand):
    def handle(self, *args, **options):
        merchants = Merchant.objects.all()
        for merchant in merchants:
            low_quantity_products = products.objects.filter(quantity__lt=merchant.threshold, merchant=merchant)
            if low_quantity_products.exists():
                self.send_notification(merchant, low_quantity_products)

    def send_notification(self, merchant, products):
        subject = 'Low quantity alert'
        message = f"Dear {merchant.name},\n\nThe following products are below the threshold:\n\n"
        for product in products:
            message += f"- {product.name}: {product.quantity}\n"
        message += "\nPlease take necessary action.\n\nBest regards,\nYour Application"

        send_mail(
            subject=subject,
            message=message,
            from_email='mchanti648@example.com',
            recipient_list=[merchant.email],
        )
